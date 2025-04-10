import requests
import xml.etree.ElementTree as ET
import time
import os

def fetch_all_terms_for_gana(gana, start_page, file_handle, progress_handle):
    base_url = "http://www.law.go.kr/DRF/lawSearch.do"
    params = {
        "OC": "docworlds",
        "target": "lstrm",
        "gana": gana,
        "type": "XML",
        "display": 100,
        "page": start_page
    }

    # 첫 페이지 호출하여 totalCnt 획득
    response = requests.get(base_url, params=params)
    response.encoding = 'utf-8'  # 인코딩 설정
    root = ET.fromstring(response.text)

    total_cnt = int(root.findtext('totalCnt'))
    display_cnt = int(root.findtext('numOfRows'))
    total_pages = (total_cnt - 1) // display_cnt + 1

    for page in range(start_page, total_pages + 1):
        params['page'] = page
        response = requests.get(base_url, params=params)
        response.encoding = 'utf-8'
        root = ET.fromstring(response.text)

        terms_string = extract_terms_from_root(root)
        file_handle.write(terms_string)

        print(f"Gana: {gana}, Page: {page}")

        progress_handle.seek(0)
        progress_handle.write(f"{gana},{page}\n")
        progress_handle.flush()

        time.sleep(1)

def extract_terms_from_root(root):
    terms_string = []
    for lstrm in root.findall('.//lstrm'):
        term_name_element = lstrm.find('법령용어명')
        if term_name_element is not None and term_name_element.text:
            term_name = term_name_element.text.strip()
            terms_string.append(term_name)
    return '\n'.join(terms_string)

def load_progress():
    if os.path.exists("progress.txt"):
        with open("progress.txt", "r") as f:
            line = f.readline().strip()
            if line:
                gana, page = line.split(",")
                return gana, int(page) + 1  # 다음 페이지부터 시작
    return None, 1  # 시작 지점이 없을 경우 첫 gana부터 시작

def save_progress(gana, page):
    with open("progress.txt", "w") as f:
        f.write(f"{gana},{page}\n")

if __name__ == "__main__":
    gana_list = ['ga', 'na', 'da', 'ra', 'ma', 'ba', 'sa', 'ah', 'ja', 'cha', 'ka', 'ta', 'pa', 'ha']

    # 진행 상황 로드
    last_gana, last_page = load_progress()

    with open("../resource/evaluation/terms.txt", "a", encoding="utf-8") as f, open("progress.txt", "w", encoding="utf-8") as progress_file:
        start = False
        for gana in gana_list:
            if last_gana:
                if gana == last_gana:
                    start = True  # 중단된 gana에서부터 시작
                if not start:
                    continue  # 아직 중단된 gana에 도달하지 않은 경우
            else:
                start = True  # 처음 시작하는 경우

            print(f"Fetching terms for gana: {gana}")
            fetch_all_terms_for_gana(gana, last_page if gana == last_gana else 1, f, progress_file)
            last_page = 1  # 첫 페이지로 리셋
