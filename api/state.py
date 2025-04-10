import json
import re
from pathlib import Path
from typing import Optional, Type, Dict

from fastapi import FastAPI
from langchain.prompts import PromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_upstage import ChatUpstage
from predibase import Predibase

from embedding import FactsRetriever
from rag import StatuteRagOurs
from utils import load_config

app = FastAPI()

CONFIG = load_config()
CHAT = ChatUpstage(api_key=CONFIG['api']['upstage'], temperature=0.1)
FACTS_RETRIEVER = FactsRetriever()
RAG = StatuteRagOurs()

# In-memory store for session contexts
session_store: Dict[str, 'Context'] = {}


def extract_json_from_text(text, pattern):
    match = re.search(pattern, text)
    if match:
        json_str = match.group()
        return json.loads(json_str)
    return None


class Context:
    def __init__(self, session_id: str, state: 'State', story: str):
        self._state: Optional[State] = None
        self.context_data = {'session_id': session_id, 'story': story}
        self.transition_to(state)

    def transition_to(self, state: 'State'):
        self._state = state
        self._state.context = self
        self.context_data['state'] = state.__class__.__name__

    def handle(self):
        return self._state.handle()


class State:
    template_file_name = ''

    def __init__(self):
        self.context: Optional[Context] = None

    def handle(self):
        raise NotImplementedError("Must override handle method in ConcreteState")

    def get_next_state_class(self) -> Optional[Type['State']]:
        raise NotImplementedError("Must override get_next_state_class method in ConcreteState")

    def load_prompt_template(self):
        project_root = Path(__file__).parents[1]
        template_path = project_root / 'resource' / 'prompt' / self.template_file_name
        with template_path.open() as f:
            return f.read()

    def get_prompt(self, args: dict):
        template = self.load_prompt_template()
        prompt = PromptTemplate(
            input_variables=[args.keys()],
            template=template,
        )

        return prompt.format(**args)


class StatuteState(State):

    def __init__(self):
        super().__init__()

    def handle(self):
        story = self.context.context_data['story']
        statute = RAG.generate(story)

        try:
            statute_parsed = eval(statute)
            statute_parsed = statute_parsed[:3]
        except Exception as e:
            statute_parsed = statute

        self.context.context_data['statute'] = statute_parsed
        print('statute: ', statute)

        next_state_class = self.get_next_state_class()
        self.context.transition_to(next_state_class())
        return self.context.handle()

    def get_next_state_class(self) -> Optional[Type[State]]:
        return KeyIssuesState


class KeyIssuesState(State):
    template_file_name = 'key_issue.txt'

    def __init__(self):
        super().__init__()
        self.re_pattern = re.compile(r'## 추가적으로 알아야할 정보\n(.+)', re.DOTALL)
        self.clean_pattern = re.compile(r'^[\d\-\*\.\s]+')

    def handle(self):
        story = self.context.context_data['story']
        statute = self.context.context_data['statute']
        additional_info_prompt = self.get_prompt({
            'story': story,
            'statute': statute,
        })
        messages = [SystemMessage(content="You are a helpful legal assistant."),
                    HumanMessage(content=additional_info_prompt)]
        additional_info_response = CHAT.invoke(messages)
        print('additional_info_response: ', additional_info_response)
        self.context.context_data['additional_info'], self.context.context_data[
            'additional_info_list'] = self.extract_result(additional_info_response.content)

        # Transition to next state
        next_state_class = self.get_next_state_class()
        if next_state_class:
            self.context.transition_to(next_state_class())
        return self.context.handle()

    def extract_result(self, text: str):
        extracted = re.findall(self.re_pattern, text)
        extracted = "\n".join(extracted)
        extracted = extracted.splitlines()
        extracted_list = [self.clean_pattern.sub('', line) for line in extracted]
        extracted = "\n".join(extracted_list)
        return extracted, extracted_list

    def get_next_state_class(self) -> Optional[Type[State]]:
        return MemoryUpdateState


class MemoryUpdateState(State):
    template_file_name = 'memory_update.txt'

    def __init__(self):
        super().__init__()
        self.info_pattern = r'\{\s*"information"\s*:\s*\{[^}]*\}[^}]*\}'

    def handle(self):
        if 'memory' not in self.context.context_data:
            additional_info = self.context.context_data['additional_info']
            additional_info = self.create_info_form(additional_info)
            self.context.context_data['memory'] = additional_info

        questionnaire_prompt = self.get_prompt({
            'previous_question': self.context.context_data.get('message', ''),
            'utterance': self.context.context_data['utterance'],
            'memory': self.context.context_data['memory'],
        })
        messages = [SystemMessage(content="You are a helpful legal assistant."),
                    HumanMessage(content=questionnaire_prompt)]
        memory = CHAT.invoke(messages).content
        self.context.context_data['memory'] = memory

        memory = json.loads(memory)
        if str(memory['finished']).lower() != 'false':
            self.context.transition_to(RefinementState())
        else:
            self.context.transition_to(AdditionalInfoState())

        return self.context.handle()

    def create_info_form(self, additional_info):
        lines = additional_info.strip().split('\n')
        information = {line: "" for line in lines}
        return json.dumps({
            "information": information,
            "finished": "false"
        }, ensure_ascii=False)


class AdditionalInfoState(State):
    template_file_name = 'additional_info_esc.txt'

    def __init__(self):
        super().__init__()
        self.re_pattern = re.compile(r'## 추가적으로 알아야할 정보\n(.+)', re.DOTALL)
        self.response_pattern = r"### 공감 전략\n(.*?)\n\n### AI 메시지\n(.*?)\n"

    def handle(self):
        pre_question = self.context.context_data.get('previous_question', '')
        memory = self.context.context_data['memory']
        if pre_question:
            memory['information'][pre_question] = self.context.context_data['utterance']
        else:
            memory = json.loads(memory)

        self.context.context_data['memory'] = memory
        next_query = self.find_first_empty_key(
            self.context.context_data['additional_info_list'],
            self.context.context_data['memory'])

        self.context.context_data['previous_question'] = next_query

        if not next_query:
            self.context.transition_to(RefinementState())
            return self.context.handle()

        questionnaire_prompt = self.get_prompt({
            'utterance': self.context.context_data['utterance'],
            'additional_info': next_query,
            'previous_question': self.context.context_data.get('message', ''),
        })

        messages = [SystemMessage(content="You are a helpful legal assistant."),
                    HumanMessage(content=questionnaire_prompt)]
        questionnaire_response = CHAT.invoke(messages)
        print('questionnaire_response: ', questionnaire_response)

        content = questionnaire_response.content
        self.context.context_data['message'] = self.extract_message(content)
        self.context.transition_to(AdditionalInfoState())
        return self.context

    def find_first_empty_key(self, additional_info_list, memory):
        # additional_info_list 순서에 맞춰 빈 문자열을 가진 첫 번째 key 찾기
        for key in additional_info_list:
            if memory['information'].get(key, "") == "":
                return key
        return ""

    def extract_message(self, text):
        out1 = text.split("### 공감 전략")[-1]
        strategy = out1.split("### AI 메시지")[0].strip()
        response = text.split("### AI 메시지")[-1].strip()
        return response

    def get_next_state_class(self) -> Optional[Type[State]]:
        return AdditionalInfoState


class RefinementState(State):
    template_file_name = 'refinement.txt'

    def handle(self):
        story = self.context.context_data['story']
        questionnaire = self.context.context_data['memory']
        answers_prompt = self.get_prompt({
            'story': story,
            'questionnaire': questionnaire,
        })
        messages = [SystemMessage(content="You are a helpful legal assistant."), HumanMessage(content=answers_prompt)]
        answers_response = CHAT.invoke(messages)
        print('answers_response: ', answers_response)
        self.context.context_data['refined_story'] = answers_response.content

        next_state_class = self.get_next_state_class()
        self.context.transition_to(next_state_class())
        return self.context.handle()

    def get_next_state_class(self) -> Optional[Type[State]]:
        return StatuteVerificationState


class StatuteVerificationState(State):
    def __init__(self):
        super().__init__()
        pb = Predibase(api_token=CONFIG['api']['predibase'])
        self.lorax_client = pb.deployments.client("solar-1-mini-chat-240612")

        self.template = """<|im_start|>system:\n사건에 해당하는 형사법조를 찾아줘.<|im_end|>
        <|im_start|>[사건]\n {story}
        <|im_start|>[형사 법조]\n"""

    def handle(self):
        refined_story = self.context.context_data['refined_story']

        input_prompt = self.template.format(story=refined_story)
        generated_text = self.lorax_client.generate(
            input_prompt, adapter_id="litify-model/3",
            max_new_tokens=300).generated_text

        self.context.context_data['statute_verification'] = generated_text

        next_state_class = self.get_next_state_class()
        self.context.transition_to(next_state_class())
        return self.context.handle()

    def get_next_state_class(self) -> Optional[Type[State]]:
        return ComplaintDraftState


class ComplaintDraftState(State):
    template_file_name = 'complaint_draft.txt'

    def postprocess_draft(self, draft):
        draft = draft.replace("\n", "<br/>")
        draft = draft.replace("<고소취지>", "<h3>고소취지</h3>")
        draft = draft.replace("<고소이유>", "<h3>고소이유</h3>")
        return draft

    def handle(self):
        refined_story = self.context.context_data['refined_story']
        statute = self.context.context_data['statute_verification']
        draft_prompt = self.get_prompt({
            'refined_story': refined_story,
            'statute': statute,
        })
        messages = [SystemMessage(content="You are a helpful legal assistant."), HumanMessage(content=draft_prompt)]
        draft_response = CHAT.invoke(messages)

        self.context.context_data['message'] = self.postprocess_draft(draft_response.content)
        try:
            parsed_complaint = self.extract_sections(draft_response.content)
            if 'purpose' in parsed_complaint and 'reason' in parsed_complaint:
                self.context.context_data['complaint'] = self.extract_sections(draft_response.content)
        except Exception as e:
            print('Error: extract_sections in ComplaintDraftState', e)

        self.context.context_data['facts'] = FACTS_RETRIEVER.search(refined_story)
        print('draft_response: ', self.context.context_data['message'])
        return self.context

    def get_next_state_class(self) -> Optional[Type[State]]:
        return None  # No more states

    def extract_sections(self, text):
        # 고소취지와 고소이유 각각의 시작 패턴을 정의 (다중 줄 대응)
        patterns = {
            "purpose": r"<고소취지>\s*(.*?)\s*(?=<|$)",
            "reason": r"<고소이유>\s*(.*?)\s*(?=<|$)"
        }

        result = {}

        # 각각의 패턴에 대해 매칭되는 부분을 찾아 저장
        for section, pattern in patterns.items():
            match = re.search(pattern, text, re.DOTALL)
            if match:
                result[section] = match.group(1).strip()

        return result


# Mapping of state names to their respective classes
state_mapping: Dict[str, Type[State]] = {
    "StatuteState": StatuteState,
    "KeyIssuesState": KeyIssuesState,
    "MemoryUpdateState": MemoryUpdateState,
    "AdditionalInfoState": AdditionalInfoState,
    "RefinementState": RefinementState,
    "StatuteVerificationState": StatuteVerificationState,
    "ComplaintDraftState": ComplaintDraftState,
}
