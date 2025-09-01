# AI-Powered Resume Analyzer

## Run (no virtual environment)
### 1) Install Python deps globally
pip install --upgrade pip
pip install -r backend/requirements.txt
python -m spacy download en_core_web_sm

### 2) Install JS deps
npm i

### 3) Start both servers on Windows
npm run dev:win

- API: http://127.0.0.1:8000
- UI : http://127.0.0.1:8501
