from langchain.prompts import PromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_upstage import ChatUpstage

from embedding import FAISSVectorStore
from utils import load_config, load_prompt, get_project_path

from predibase import Predibase

CONFIG = load_config()


class StatuteRAG:

    def __init__(self):
        self.embedding = FAISSVectorStore()
        db_path = get_project_path() / 'resource' / 'embedding'
        self.embedding.load_db(db_path)
        self.llm = ChatUpstage(api_key=CONFIG['api']['upstage'], temperature=0.1)
        self.prompt_template = PromptTemplate(
            input_variables=['query', 'documents'],
            template=load_prompt('statute_classification.txt'),
        )

    def generate(self, query):
        documents = self.retrieve_docs(query)
        prompt = self.prompt_template.format(query=query, documents=documents)
        messages = [SystemMessage(content="You are a helpful legal assistant."), HumanMessage(content=prompt)]
        response = self.llm.invoke(messages)
        return response.content

    def retrieve_docs(self, query):
        documents = self.embedding.search(query)
        return '\n\n'.join(documents)


class StatuteRagOurs:
    def __init__(self):
        pb = Predibase(api_token=CONFIG['api']['predibase'])
        self.lorax_client = pb.deployments.client("solar-1-mini-chat-240612")
        self.embedding = FAISSVectorStore(model_name="solar-embedding-1-large-query")
        db_path = get_project_path() / 'resource' / 'embedding'
        self.embedding.load_db(db_path)
        self.template = """<|im_start|>system:\n# 지시
너가 할 일은 사건에 해당하는 법률을 찾아내는 것이야. 주어진 사건에 해당하는 법률을 “검색된 법률 문서” 범위 내에 찾아줘. 이때, 주어진 “한국 법 체계”를 참고해서 가장 하위 조문을 찾아줘. 조문만 출력해줘.

# 한국 법 체계
한국의 법은 기본적으로는 조로써 구분하고, 조금 더 세분할 필요가 있을 때에는 항으로써 구분한다. 한 '조'나 '항' 내에서 어떤 사항들을 나열할 필요가 있을 때에는 호를 사용하고, 한 '호' 내에서 다시 나열이 필요할 때에는 ‘목’을 사용한다. 즉, 조>항>호>목의 순으로 구성되어 있다.
<|im_end|>
    <|im_start|>[사건]\n {story}\n

# 검색된 법률 문서
{documents}
    <|im_start|>[형사 법조]\n"""

    def generate(self, story: str):
        try:
            documents = self.retrieve_docs(story)
            input_prompt = self.template.format(story=story, documents=documents)
            generated_text = self.lorax_client.generate(
                input_prompt, adapter_id="litify-model/3",
                max_new_tokens=1500).generated_text
        except Exception as e:
            print(e)
            return ''
        return generated_text

    def retrieve_docs(self, query):
        documents = self.embedding.search(query)
        return '\n\n'.join(documents)


if __name__ == '__main__':
    rag = StatuteRagOurs()
    res = rag.generate("친구가 나를 때렸어")
    print(res)
