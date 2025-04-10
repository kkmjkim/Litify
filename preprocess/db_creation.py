from itertools import chain
from pathlib import Path

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from api.embedding import Embedding

from utils import get_project_path, load_config

CONFIG = load_config()
SOLAR_API_KEY = CONFIG['api']['upstage']


class MultiTextLoaderAndSplitter:
    def __init__(self, base_folder):
        self.base_folder = Path(base_folder)
        if not self.base_folder.is_absolute():
            self.base_folder = get_project_path() / base_folder
        self.splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100, length_function=len)

    def load_and_split(self):
        loaders = []
        for txt_file in self.base_folder.glob('**/*.txt'):
            loaders.append(TextLoader(str(txt_file)))

        docs = [loader.load_and_split() for loader in loaders]
        docs = list(chain.from_iterable(docs))
        return self.splitter.split_documents(docs)


if __name__ == '__main__':
    base_folder = "resource/rag"  # 여러 txt 파일이 저장된 폴더 경로
    loader_and_splitter = MultiTextLoaderAndSplitter(base_folder)
    docs = loader_and_splitter.load_and_split()
    embedding = Embedding()
    embedding.save_embedding(docs)
    print('Saved')
