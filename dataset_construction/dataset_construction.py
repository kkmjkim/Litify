from datasets import load_dataset
import pandas as pd
import json
from langchain.prompts.prompt import PromptTemplate
from langchain_upstage import ChatUpstage
from langchain_core.messages import HumanMessage, SystemMessage
from utils import load_config

def load_prompt(args):
    prompt_path = 'facts2story.txt'
    with open(prompt_path, 'r',encoding='utf-8') as f:
        template = f.read()
    prompt = PromptTemplate(
            input_variables=[args.keys()],
            template=template,
        )
    return prompt.format(**args)

def generate_story(fact):
    config = load_config()
    upstage_api_key = config["api"]["upstage"]
    chat = ChatUpstage(api_key=upstage_api_key,temperature=0.1)
    messages = [
    SystemMessage(content="You are a helpful legal assistant."),
    HumanMessage(content=load_prompt({'fact':fact}))
    ]
    response = chat.invoke(messages)
    story = response.content
    return story

def main():
    dataset = load_dataset('lbox/lbox_open','statute_classification_plus')
    data_split = ['train','test','validation']

    for data_type in data_split:
        data = pd.DataFrame([i for i in dataset[data_type] if '피해자' in i['facts']])
        data = data[~data['facts'].str.contains('사망')]
        data = data.drop(['id','casetype'],axis=1)
        data = data.reset_index()
        # train: 8558
        # test: 1413
        # valid: 1512

        stories = []
        for i in range(len(data)):
            story = generate_story(data['facts'][i])
            stories.append(story)
        data['story'] = stories
        data.to_csv(f'{data_type}_data.csv',encoding='utf-8')

if __name__ == '__main__':
    main()