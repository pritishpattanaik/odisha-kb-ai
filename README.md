# Odisha KB RAG (Minimal)

## Folders
- `data/` ← your merged knowledge
- `ingest.py` ← build vector DB
- `server.py` ← FastAPI Q&A

## Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python ingest.py
uvicorn server:app --reload --port 8890
```

## Ask
```bash
curl -s -X POST http://127.0.0.1:8890/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"Tell me about Chilika Lake"}'
```
