#!/usr/bin/env python3
import os, json, re
from pathlib import Path
from sentence_transformers import SentenceTransformer
import chromadb
#from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

DATA_DIR = Path("data")
PERSIST_DIR = "vectorstore"
COLLECTION = "odisha_kb"

def load_texts():
    docs = []
    # txt files
    for p in DATA_DIR.rglob("*.txt"):
        txt = p.read_text(encoding="utf-8", errors="ignore")
        docs.append({"path": str(p), "text": txt})
    # rss -> synth doc
    rss = DATA_DIR / "rss" / "odisha_news.json"
    if rss.exists():
        arr = json.loads(rss.read_text(encoding="utf-8"))
        lines = []
        for it in arr[:50]:
            lines.append(f"- {it.get('title')} ({it.get('published')}) {it.get('link')}")
        docs.append({"path": str(rss), "text": "\n".join(lines)})
    return docs

def split_docs(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200, chunk_overlap=150,
        separators=["\n\n","\n","."," ",""]
    )
    chunks = []
    for d in docs:
        for i, c in enumerate(splitter.split_text(d["text"])):
            chunks.append({"id": f'{d["path"]}__{i}', "text": c, "source": d["path"]})
    return chunks

def main():
    docs = load_texts()
    if not docs:
        print("No data found under ./data")
        return
    chunks = split_docs(docs)
    print(f"Prepared {len(chunks)} chunks")

    model = SentenceTransformer("all-MiniLM-L6-v2")
    client = chromadb.PersistentClient(path=PERSIST_DIR)
    try:
        client.delete_collection(COLLECTION)
    except Exception:
        pass
    col = client.get_or_create_collection(COLLECTION)

    ids = [c["id"] for c in chunks]
    texts = [c["text"] for c in chunks]
    metas = [{"source": c["source"]} for c in chunks]
    embs = model.encode(texts, normalize_embeddings=True).tolist()
    col.add(ids=ids, documents=texts, embeddings=embs, metadatas=metas)
    print("✅ Ingestion complete → ./vectorstore")

if __name__ == "__main__":
    main()
