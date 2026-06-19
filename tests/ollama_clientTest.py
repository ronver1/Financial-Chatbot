# Author: Ronit Verma
# Created on: 6.18.26

# This file is a test to ensure the get_response function inside /backend/llm properly works

from backend.llm.ollama_client import get_response

history = [{"role": "user", "content": "Tell me about Basketball"}]
reply = get_response(history)
print(reply)