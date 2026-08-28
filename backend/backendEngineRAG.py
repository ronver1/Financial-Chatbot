# Author: Ronit Verma
# Created on: 8.26.26

# Engine that runs the Financial Chatbot with RAG implementation

from backend.auth.userAuth import userAccess
from backend.session.session_store import add_message, get_history, destroy_session, create_session
from backend.session.session_store import sessions
from backend.llm.ollama_client import get_response
from backend.rag.loader import ingest
from backend.rag.embeddings import embed
from backend.rag.vector_store import search
import sys, requests, gc

# Load Knowledge Base
print("Loading knowledge base...")
count = ingest()
print(f"Loaded {count} documents into the vector store.")

print("Hello! I am a Financial Chatbot designed for user and data security. Please proceed below")
while True:
    userName = input("Enter Username: ")
    userAccess(userName)

    while True:
        userInput = input("Chat: ")
        if userInput == "Done":
            break
        if userInput == "Quit":
            for username in list(sessions.keys()):
                destroy_session(username)
            gc.collect()
            sys.exit()

        add_message(userName, "user", userInput)

        # Retrieve Knowledge Base
        chunks = search(embed(userInput), k=4)
        context = "\n\n---\n\n".join(chunks)

        history = get_history(userName)
        augmented = history[:-1] + [{
            "role": "user",
            "content": (
                "Use the reference material below if relevant; ignore it otherwise.\n\n"
                f"Reference material:\n{context}\n\n"
                f"User question: {userInput}"
            ),
        }]

        result = get_response(augmented)
        add_message(userName, "assistant", result)
        print(result)