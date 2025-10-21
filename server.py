# server.py
from fastapi import FastAPI, Request
from pydantic import BaseModel
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

app = FastAPI()

# Load embeddings + vector store
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = Chroma(persist_directory="./vectorstore", embedding_function=embeddings)

class Question(BaseModel):
    question: str

@app.post("/ask")
async def ask(q: Question):
    query = q.question.strip()
    docs = db.similarity_search(query, k=3)

    if not docs:
        return {"answer": "❌ Sorry, I couldn't find anything in the Odisha KB."}

    # Join best docs
    context = "\n".join([d.page_content for d in docs])
    return {
        "answer": f"✅ Based on KB:\n{context[:800]}...",  # limit for readability
        "matches": [d.page_content for d in docs]
    }

@app.get("/")
async def home():
    return {"msg": "Odisha KB Bot is running 🚀. Use POST /ask"}