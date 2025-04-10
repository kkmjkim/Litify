import os
import re
import xml.etree.ElementTree as ET

from api.embedding import FAISSVectorStore


def save_xml_to_file(xml_content, keyword):
    output_folder = 'resource/rag'
    filename = f"{output_folder}/{keyword}.txt"
    with open(filename, "wb") as file:
        file.write(xml_content)


def check_clauses(clause_content):
    # "제(숫자)편", "제(숫자)장", "제(숫자)절" 패턴을 찾기 위한 정규 표현식
    pattern = r'제\d+편|제\d+장|제\d+절'
    result = re.findall(pattern, clause_content)
    return bool(result)


def load_txt_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"Error: 파일을 찾을 수 없습니다: {file_path}")
        return None


def get_txt_files(directory):
    txt_files = []
    # os.walk를 사용하여 디렉토리 내 모든 파일을 탐색
    for root, dirs, files in os.walk(directory):
        for file in files:
            # 확장자가 .txt인 파일을 필터링
            if file.endswith('.txt'):
                txt_files.append(os.path.join(root, file))
    return txt_files


def parse_law_xml(xml_data, file_name):
    """
    XML 데이터를 파싱하여 조문, 항, 호, 목 내용을 파싱하는 함수
    Args:
    xml_data (str): XML 데이터 문자열
    Returns:
    list: 파싱된 결과를 리스트로 반환
    """
    # XML 파싱
    root = ET.fromstring(xml_data)

    def parse_clause(element):
        """조문, 항, 호, 목 내용을 하나의 str로 묶는 함수"""
        result = [f'{file_name} ']
        clause_content = element.findtext('조문내용')
        if clause_content:
            result.append(clause_content.strip())
        for paragraph in element.findall('항'):
            para_content = paragraph.findtext('항내용')
            if para_content:
                result.append(f"{para_content.strip()}")
            # 호번호와 호내용
            for sub_item in paragraph.findall('호'):
                sub_item_content = sub_item.findtext('호내용')
                if sub_item_content:
                    result.append(f"{sub_item_content.strip()}")
                # 목번호와 목내용
                for sub_sub_item in sub_item.findall('목'):
                    sub_sub_item_content = sub_sub_item.findtext('목내용')
                    if sub_sub_item_content:
                        result.append(f"{sub_sub_item_content.strip()}")
        # 최종적으로 하나의 문자열로 반환
        return "\n".join(result)

    # 모든 조문단위 처리
    all_clauses = []
    for clause in root.findall('.//조문단위'):
        parsed_clause = parse_clause(clause)
        if not check_clauses(parsed_clause):
            all_clauses.append(parsed_clause)
    return all_clauses


def save_parsed_clauses_to_file(parsed_clauses, filename="parsed_clauses.txt"):
    """
    파싱된 결과를 파일로 저장하는 함수
    Args:
    parsed_clauses (list): 파싱된 조문 내용을 담은 리스트
    filename (str): 저장할 파일명 (기본값은 "parsed_clauses.txt")
    """
    with open(filename, "w", encoding="utf-8") as f:
        for idx, clause_text in enumerate(parsed_clauses, 1):
            f.write(f"조문 {idx}:\n{clause_text}\n\n")
    print(f"{filename} 파일로 저장되었습니다.")


if __name__ == '__main__':
    file_list = get_txt_files('resource/rag')
    faiss_store = FAISSVectorStore()

    for i, file_path in enumerate(file_list):
        file_name = os.path.basename(file_path)
        file_name = file_name[:-4]
        print(f'Start: {file_name}')
        xml_data = load_txt_file(file_path)
        parsed_xml = parse_law_xml(xml_data, file_name)
        print(f'Parsed xml len: {len(parsed_xml)}')

        if i == 0:
            faiss_store.create_db(parsed_xml)
            continue

        faiss_store.add_documents(parsed_xml)

    faiss_store.save_db('resource/embedding')