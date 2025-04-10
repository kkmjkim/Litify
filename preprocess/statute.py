import requests

# 키워드 리스트
keywords = [
    '도로교통법'
]

# 파일로 저장할 폴더 경로 (없으면 현재 경로에 저장)
output_folder = 'resource/rag'

# 기본 URL 설정
base_url = "https://www.law.go.kr/DRF/lawService.do?OC=docworlds&target=law&type=XML&LM="


def save_xml_to_file(xml_content, keyword):
    filename = f"{output_folder}/{keyword}.txt"
    with open(filename, "wb") as file:
        file.write(xml_content)


def process_keywords(keywords):
    for keyword in keywords:
        # 각 키워드에 대해 URL을 생성
        url = base_url + keyword
        print(f"Processing URL: {url}")

        # URL에서 XML 데이터 가져오기
        response = requests.get(url)
        if response.status_code == 200:
            xml_content = response.content
            # XML 전체 내용을 파일로 저장
            save_xml_to_file(xml_content, keyword)
            print(f"Saved XML content for keyword '{keyword}' to file '{keyword}.txt'.")
        else:
            print(f"Failed to retrieve data for keyword '{keyword}'.")


# 키워드 리스트를 처리
process_keywords(keywords)
