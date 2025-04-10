from konlpy.tag import Okt
from tqdm import tqdm


def txt_to_list(file_path):
    """
    주어진 텍스트 파일을 읽어서 줄 단위로 리스트로 반환하는 함수.

    :param file_path: 텍스트 파일 경로 (string)
    :return: 각 줄이 리스트 항목으로 저장된 리스트 (list)
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 각 줄의 끝에 있는 개행 문자를 제거합니다.
    lines = [line.strip() for line in lines]

    return lines


def count_word_occurrences(text_file_path, word_list_file_path):
    """
    텍스트 파일에서 단어 목록의 발생 빈도를 계산하고, 전체 단어 중 몇 개가 단어 목록에 있는지 확인하는 함수.

    :param text_file_path: 분석할 텍스트 파일 경로 (string)
    :param word_list_file_path: 단어 목록이 포함된 파일 경로 (string)
    :return: 단어별 빈도수와 포함된 단어의 총 개수를 저장한 딕셔너리 (dict)
    """
    # 단어 목록 파일을 읽어 리스트로 변환
    word_list = txt_to_list(word_list_file_path)

    # 형태소 분석기 초기화
    okt = Okt()

    # 빈도 사전 초기화
    word_count = {word: 0 for word in word_list}
    total_word_found = 0
    total_words_in_text = 0

    with open(text_file_path, 'r', encoding='utf-8') as file:
        # 전체 파일의 라인 수를 미리 계산
        total_lines = sum(1 for _ in open(text_file_path, 'r', encoding='utf-8'))

        # tqdm을 사용하여 진행 상황을 표시
        with tqdm(total=total_lines, desc="Processing lines") as pbar:
            for line in file:
                # 형태소 분석 및 명사 추출
                tokens = okt.nouns(line)
                for token in tokens:
                    total_words_in_text += 1
                    if token in word_count:
                        word_count[token] += 1
                        total_word_found += 1
                # 진행 상황 업데이트
                pbar.update(1)

    return word_count, total_word_found, total_words_in_text
