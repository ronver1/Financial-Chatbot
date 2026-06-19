# Author: Ronit Verma
# Created on: 6.10.26

# This file consists of a function that takes in a user message, sends it to Ollama, and returns 
# the chatbot's response

import requests

def get_response(message):
    url = "http://localhost:11434/api/chat"
    data = {
        "model": "llama3.2:3b",
        "messages": message,
        "stream": False
    }

    response = requests.post(url, json=data)
    result = response.json()
    return result["message"]["content"]

