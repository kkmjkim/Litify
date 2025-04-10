from langchain.prompts import PromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_upstage import ChatUpstage

import re
from embedding import Embedding
from utils import load_config, load_prompt

CONFIG = load_config()


class Conversation:

    def __init__(self):
        self.llm = ChatUpstage(api_key=CONFIG['api']['upstage'], temperature=0.1)
        self.prompt_template = PromptTemplate(
            input_variables=['additional_info', 'previous_question', 'utterance'],
            template=load_prompt('additional_info_esc.txt'),
        )
        self.response_pattern = r"### 공감 전략\n(.*?)\n\n### AI 메시지\n(.*?)\n"

    def generate(self, additional_info, previous_question, utterance):
        prompt = self.prompt_template.format(additional_info=additional_info, previous_question=previous_question, utterance=utterance)
        messages = [SystemMessage(content="You are a helpful legal assistant."), HumanMessage(content=prompt)]
        response = self.llm.invoke(messages)
        return response.content

    def extract_message(self, text):
        out1 = text.split("### 공감 전략")[-1]
        strategy = out1.split("### AI 메시지")[0].strip()
        response = text.split("### AI 메시지")[-1].strip()
        return strategy, response



if __name__ == '__main__':
    conversation = Conversation()
    additional_info = """{
    "information": {
        "고소인과 상대방의 관계": "친구",
        "폭행이 발생한 구체적인 상황": "돌맹이로 맞았어",
        "폭행의 정도와 피해 정도": "전치2주",
        "상대방의 고의성 여부": "아니요",
        "목격자나 증거의 유무": ""
    }
}"""
    previous_question = "뭘로 맞으셨나요?"
    utterance = "돌맹이로 맞았어"

    res = conversation.generate(additional_info=additional_info, previous_question=previous_question, utterance=utterance)
    print(res)
    print()
    final_output = conversation.extract_message(res)
    print(final_output)
