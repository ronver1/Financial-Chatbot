# Author: Ronit Verma
# Created on: 8.21.26

# This file turns a string into a vector

import requests, time

def embed(text: str, retries: int = 4, delay: float = 2.0) -> list[float]:
    url = "http://localhost:11434/api/embeddings"
    data = {
        "model": "nomic-embed-text",
        "prompt": text,
        "keep_alive": "10m",   
    }
    last = None
    for attempt in range(retries):
        response = requests.post(url, json=data)
        body = response.json()
        if "embedding" in body:
            return body["embedding"]
        last = body                    # remember what Ollama actually said
        time.sleep(delay)              # give the model a moment to finish loading
    raise RuntimeError(f"Embedding failed after {retries} tries: {last}")