# Author: Ronit Verma
# Created on: 8.21.26

# This file reads the knowledge base and vectorizes each .txt file

import glob, os
from backend.rag.embeddings import embed
from backend.rag.vector_store import add

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
KNOWLEDGE_DIR = os.path.join(ROOT, "knowledge")

def load_documents() -> list[str]:
    docs = []
    for p in glob.glob(os.path.join(KNOWLEDGE_DIR, "*.txt")):
        with open(p, encoding="utf-8") as f:
            docs.append(f.read().strip())
    return docs

def ingest():
    docs = load_documents()
    for doc in docs:
        add(doc, embed(doc))
    return len(docs)