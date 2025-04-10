# <img src="https://github.com/user-attachments/assets/73dbccf5-09e4-49a2-b96b-ce39ac9ef967" alt="litify_bot_icon" style="width:30px;"> Litify
Criminal complaint drafting system that aims to save time for lawyers and make legal assistance easy for clients.

## Setup
### 1. Create the virtual environment.
```
git clone https://github.com/kkmjkim/Litify.git
conda create -n litify python=3.10
```
### 2. Install the required packages.
```
cd Litify
pip install -r api/requirements.txt
npm install
pip install nodeenv
nodeenv env
```
### 3. Fill in your solar API key.
Fill in your API key by replacing `<<Your solar API key>>` in the `upstage_api_key` variable within the `/api/state.py` file.

## Run
### Running Frontend
Follow the below steps.
```
conda activate litify
. env/bin/activate
cd frontend
npm start
```
If you want to access with Public IP,
```
npm start -- --host
```

### Running Backend
#### 1. Open the new terminal
#### 2. Follow the below steps
```
conda activate litify
export PYTHONPATH=$PWD
cd api
fastapi run main.py --port 8000
```
