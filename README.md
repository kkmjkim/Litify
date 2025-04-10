### <업스테이지 글로벌 AI 해커톤 전체 3위 (Legal 트랙 1위) 수상작>

# <img src="https://github.com/user-attachments/assets/73dbccf5-09e4-49a2-b96b-ce39ac9ef967" alt="litify_bot_icon" style="width:30px;"> Litify
변호사의 업무 효율을 높이고, 의뢰인이 쉽게 법률 서비스를 이용할 수 있도록 하는 형사 고소장 자동 작성 시스템.

## Setup
### 1. 가상환경 생성
```
git clone https://github.com/kkmjkim/Litify.git
conda create -n litify python=3.10
```
### 2. 패키지 설치
```
cd Litify
pip install -r api/requirements.txt
npm install
pip install nodeenv
nodeenv env
```
### 3. API키 설정
`conf.d/config.yaml` 설정

## Run
### Server 실행
#### 1. 새로운 터미널 열기
#### 2. 아래 명령어 실행
```
conda activate litify
export PYTHONPATH=$PWD
cd api
fastapi run main.py --port 8000
```

### Client 실행
```
conda activate litify
. env/bin/activate
cd frontend
npm start
```
Public IP로 접근 시,
```
npm start -- --host
```

## 팀원
이수연(팀장), 김민진, 양동일, 심현정
