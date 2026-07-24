# Author: Ronit Verma
# Created on: 6.26.26

# This file is the engine that drives the LPA

from backend.auth.userAuth import userAccess
from backend.session.session_store import add_message, get_history, destroy_session, create_session
from backend.session.session_store import sessions 
from backend.llm.ollama_client import get_response
import sys, requests, gc

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
        result = get_response(get_history(userName))
        add_message(userName, "assistant", result)
        print(result)

    
