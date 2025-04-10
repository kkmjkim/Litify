import asyncio
from abc import abstractmethod
from pathlib import Path

import pandas as pd
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_upstage import ChatUpstage
from predibase import Predibase
from tqdm import tqdm
from openai import OpenAI
from api.embedding import FAISSVectorStore
from api.utils import get_project_path, load_config
from api.rag import StatuteRAG

CONFIG = load_config()

class LLM:
    template_file_name = ''

    @abstractmethod
    def generate(self, prompt: str):
        pass

    def load_prompt_template(self):
        project_root = Path(__file__).parents[1]
        template_path = project_root / 'resource' / 'prompt' / self.template_file_name
        with template_path.open() as f:
            return f.read()


class Llama(LLM):
    template_file_name = 'statute2.txt'

    def __init__(self):
        self.host = 'http://localhost:9000/v1'
        self.client = OpenAI(
            base_url=self.host,
            api_key="EMPTY",
        )

        self.prompt_template = self.load_prompt_template()

    def generate(self, story: str) -> str:
        prompt = self.prompt_template.format(story=story)
        completion = self.client.chat.completions.create(
            model="meta-llama/Meta-Llama-3.1-8B-Instruct",
            max_tokens=1500,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        print(completion.choices[0].message.content)
        return completion.choices[0].message.content


class Qwen(LLM):
    template_file_name = 'statute2.txt'

    def __init__(self):
        self.host = 'http://localhost:9000/v1'
        self.client = OpenAI(
            base_url=self.host,
            api_key="EMPTY",
        )

        self.prompt_template = self.load_prompt_template()

    def generate(self, story: str) -> str:
        prompt = self.prompt_template.format(story=story)
        completion = self.client.chat.completions.create(
            model="Qwen/Qwen2-7B-Instruct",
            max_tokens=1500,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        print(completion.choices[0].message.content)
        return completion.choices[0].message.content


class Solar(LLM):
    template_file_name = 'statute2.txt'

    def __init__(self):
        upstage_api_key = CONFIG["api"]["upstage"]
        self.chat = ChatUpstage(
            api_key=upstage_api_key,
            temperature=0.1,
            max_tokens=300,
        )
        self.prompt_template = self.load_prompt_template()

    def generate(self, story: str):
        prompt = self.prompt_template.format(story=story)
        messages = [SystemMessage(content="You are a helpful legal assistant."), HumanMessage(content=prompt)]
        statute_response = self.chat.invoke(messages).content
        return statute_response


class Ours(LLM):
    def __init__(self):
        self.api_token = CONFIG["api"]["predibase"]
        pb = Predibase(self.api_token)
        self.lorax_client = pb.deployments.client("solar-1-mini-chat-240612")

        self.template = """<|im_start|>system:\n사건에 해당하는 형사법조를 찾아줘.<|im_end|>
    <|im_start|>[사건]\n {story}
    <|im_start|>[형사 법조]\n"""

    def generate(self, story: str):
        input_prompt = self.template.format(story=story)
        generated_text = self.lorax_client.generate(
            input_prompt, adapter_id="litify-model/3",
            max_new_tokens=300).generated_text

        return generated_text


class RagOurs(LLM):
    def __init__(self, ):
        self.api_token = CONFIG["api"]["predibase"]
        pb = Predibase(self.api_token)
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
        # documents = [document.page_content for document in documents]
        return '\n\n'.join(documents)


class Rag(LLM):
    def __init__(self):
        self.rag = StatuteRAG()

    def generate(self, story: str):
        try:
            generated_text = self.rag.generate(story)
        except Exception as e:
            print(e)
            return ""
        return generated_text


def get_strategy(strategy_name: str) -> LLM:
    strategies = {
        "Ours": Ours,
        "RagOurs": RagOurs,
        "Rag": Rag,
        "Solar": Solar,
        "Llama": Llama,
        "Qwen": Qwen,
    }
    if strategy_name in strategies:
        return strategies[strategy_name]()
    else:
        raise ValueError(f"Unknown strategy name: {strategy_name}")


# Context 클래스 - 전략을 사용하는 부분
class Context:
    def __init__(self, strategy_name: str):
        self.strategy = get_strategy(strategy_name)

    def set_strategy(self, strategy_name: str):
        self.strategy = get_strategy(strategy_name)

    def execute_strategy(self, story: str) -> str:
        return self.strategy.generate(story)


# 평가 클래스 정의
class Evaluator:
    def __init__(self, context: Context, dataframe: pd.DataFrame):
        self.context = context
        self.dataframe = dataframe

    async def evaluate_row(self, row) -> tuple:
        statutes_list = eval(row['statutes'])
        story = row['story']

        generated_text = self.context.execute_strategy(story)
        print(generated_text)

        em_score = 1
        accuracy_score = 0

        for statute in statutes_list:
            if statute in generated_text:
                accuracy_score += 1
            else:
                em_score = 0

        total_items = len(statutes_list)
        return em_score, accuracy_score, total_items

    async def evaluate(self) -> tuple:
        tasks = []
        total_items_count = 0
        total_accuracy_score = 0
        total_em_score = 0

        for _, row in tqdm(self.dataframe.iterrows(), total=self.dataframe.shape[0], desc="Evaluating"):
            tasks.append(self.evaluate_row(row))

        results = await asyncio.gather(*tasks)

        for em_score, accuracy_score, total_items in results:
            total_em_score += em_score
            total_accuracy_score += accuracy_score
            total_items_count += total_items

        average_em = total_em_score / len(self.dataframe) if len(self.dataframe) > 0 else 0
        average_accuracy = total_accuracy_score / total_items_count if total_items_count > 0 else 0

        print('total_em_score:', total_em_score)
        print('total_accuracy_score:', total_accuracy_score)
        print('total_items_count:', total_items_count)

        return average_em, average_accuracy


def main():
    file_path = get_project_path() / 'resource' / 'train' / 'test_data_sample100.csv'
    df = pd.read_csv(str(file_path))
    context = Context("Rag")
    evaluator = Evaluator(context, df)

    loop = asyncio.get_event_loop()
    average_score = loop.run_until_complete(evaluator.evaluate())

    print(f'Average Score: {average_score}')


if __name__ == '__main__':
    main()
    # rag = Rag()
    # a = rag.generate('친구가 때렸어')
    # print(a)
