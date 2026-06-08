import requests
url = "http://localhost:11434/api/chat"

message = []

while True: 
    user_input = input("Message: ")
    if user_input.lower() == "quit":
        break
    message.append({"role": "user", "content": user_input})

    data = {
        "model": "llama3.2:3b",
        "messages": message,
        "stream": False
    }

    response = requests.post(url, json=data)
    result = response.json()
    print(result["message"]["content"])
    message.append({"role": "assistant", "content":result["message"]["content"]})
