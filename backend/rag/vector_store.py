# Author: Ronit Verma
# Created on: 8.21.26

# This file stores the knowledge base as vectors

import numpy as np

store = []

def add(text: str, vector: list[float]):
    store.append({"text": text, "vector": np.array(vector)})

def search(query_vector: list[float], k: int = 4) -> list[str]:
    q = np.array(query_vector)
    def cosine(v):
        return np.dot(q, v) / (np.linalg.norm(q) * np.linalg.norm(v))
    ranked = sorted(store, key=lambda e: cosine(e["vector"]), reverse=True)
    return [e["text"] for e in ranked[:k]]
