import pandas as pd
from datasets import load_dataset

from api.embedding import FAISSVectorStore


def get_facts_list(csv_file_path):
    """
    CSV 파일에서 'facts' 열을 리스트 형태로 반환하는 함수.

    Args:
    csv_file_path (str): CSV 파일 경로

    Returns:
    list: 'facts' 열의 값이 담긴 리스트
    """
    # CSV 파일을 pandas DataFrame으로 읽어들임
    df = pd.read_csv(csv_file_path)

    # 'facts' 열을 리스트로 변환
    facts_list = df['facts'].tolist()

    return facts_list


def split_list_and_exclude(lst, chunk_size, max_length):
    result = []
    for item in lst:
        if len(item.split()) >= max_length:
            print(f"Excluded item (length {len(item.split())}): {item}")
        else:
            result.append(item)
    return [result[i:i + chunk_size] for i in range(0, len(result), chunk_size)]


if __name__ == '__main__':
    dataset = load_dataset('lbox/lbox_open', 'ljp_criminal', split='train')

    faiss_store = FAISSVectorStore()
    batch_size = 50
    batch_docs = []

    for i, sample in enumerate(dataset):
        doc = f'{sample["facts"]}@@@@{sample["ruling"]["text"]}'
        if i == 0:
            faiss_store.create_db(doc)
            continue

        batch_docs.append(doc)

        # If we have reached the batch size, add the documents to the FAISS store
        if len(batch_docs) == batch_size:
            try:
                print(i)
                faiss_store.add_documents(batch_docs)
                batch_docs = []  # Reset the batch list after adding
            except Exception as e:
                print(e)
                continue

    # Add any remaining documents in the batch that didn't reach 50
    if batch_docs:
        try:
            faiss_store.add_documents(batch_docs)
        except Exception as e:
            print(e)

    faiss_store.save_db('resource/facts-embedding')

