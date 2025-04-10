import os

from langchain.docstore.document import Document
from langchain.vectorstores import FAISS
from langchain_upstage import UpstageEmbeddings  # UpstageEmbeddings 사용

from api.utils import get_project_path, load_config

CONFIG = load_config()

class FAISSVectorStore:
    def __init__(self, db_path=None, model_name="solar-embedding-1-large-passage",
                 api_key=None):
        """
        :param db_path: FAISS DB를 저장하거나 로드할 경로 (기본값: None)
        :param model_name: Upstage 임베딩 모델 이름 (기본값: "solar-embedding-1-large-query")
        :param api_key: Upstage API 키
        """
        if api_key is None:
            api_key = CONFIG['api']['upstage']
        self.embedding_model = UpstageEmbeddings(model=model_name, api_key=api_key)  # Upstage 임베딩 모델 및 API 키 설정
        self.db_path = db_path
        self.db = None

        if db_path and os.path.exists(db_path):
            self.load_db(db_path)

    def create_db(self, documents):
        """
        새로운 FAISS 벡터 데이터베이스를 생성합니다.

        :param documents: 리스트 형태의 문서 (List[str]) 또는 Document 객체 리스트 (List[Document])
        """
        docs = [Document(page_content=doc) for doc in documents]
        doc_embeddings = self.embedding_model.embed_documents([doc.page_content for doc in docs])
        text_embedding_pairs = list(zip(documents, doc_embeddings))  # 텍스트와 임베딩을 쌍으로 저장
        self.db = FAISS.from_embeddings(text_embedding_pairs, self.embedding_model)

    def add_documents(self, documents):
        """
        기존 데이터베이스에 문서를 추가합니다.

        :param documents: 리스트 형태의 문서 (List[str]) 또는 Document 객체 리스트 (List[Document])
        """
        if not self.db:
            raise ValueError("벡터 데이터베이스가 생성되지 않았습니다. 먼저 create_db 메서드를 사용하세요.")

        docs = [Document(page_content=doc) for doc in documents]
        doc_embeddings = self.embedding_model.embed_documents([doc.page_content for doc in docs])
        text_embedding_pairs = list(zip(documents, doc_embeddings))  # 텍스트와 임베딩을 쌍으로 저장
        self.db.add_embeddings(text_embedding_pairs)

    def search(self, query, k=5):
        """
        쿼리에 대한 상위 k개의 검색 결과를 반환합니다.

        :param query: 검색할 쿼리 문자열
        :param k: 검색 결과로 반환할 상위 문서 수 (기본값: 5)
        :return: 검색 결과 문서들 (List[str])
        """
        if not self.db:
            raise ValueError("벡터 데이터베이스가 생성되지 않았습니다.")

        query_embedding = self.embedding_model.embed_query(query)
        docs = self.db.similarity_search_by_vector(query_embedding, k=k)
        return [doc.page_content for doc in docs]

    def save_db(self, db_path):
        """
        벡터 데이터베이스를 지정된 경로에 저장합니다.

        :param db_path: 저장할 경로 (기본값: "/content/drive/faiss_index")
        """
        if not self.db:
            raise ValueError("저장할 벡터 데이터베이스가 없습니다.")

        self.db.save_local(db_path)

    def load_db(self, db_path):
        """
        지정된 경로에서 벡터 데이터베이스를 로드합니다.

        :param db_path: 로드할 DB 경로 (파일명 포함)
        """
        self.db = FAISS.load_local(db_path, self.embedding_model, allow_dangerous_deserialization=True)


class FactsRetriever:
    def __init__(self):
        self.embedding = FAISSVectorStore()
        db_path = get_project_path() / 'resource' / 'facts-embedding'
        self.embedding.load_db(db_path)

    def search(self, story):
        retrieved = self.embedding.search(story, k=3)
        ret = []
        for doc in retrieved:
            facts, ruling = doc.split("@@@@")
            ret.append({
                'facts': facts,
                'ruling': ruling,
            })

        return ret


if __name__ == '__main__':
    facts = FactsRetriever()
    print(facts.search('친구가 때렸어'))
