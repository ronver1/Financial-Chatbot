# Author: Ronit Verma
# Created on: 6.10.26

# This file consists of four functions that guarantee privacy

sessions = {}

# Creates a blank session for a given sessionID
def create_session(username) -> bool:
    if username in sessions:
        # print("Session ID already Exists")
        return False
    sessions[username] = []
    # print("Successfully Created Session")
    return True

# Appends a message to given sessionID's session 
def add_message(username, role, content) -> bool:
    if username not in sessions:
        # print("Session ID does not exist. Please create a Session first")
        return False
    sessions[username].append({"role": role, "content": content})
    return True

# Returns the session history of a given sessionID
def get_history(username) -> list[dict]:
    if username not in sessions:
        # print("Session ID does not exist. Please create a Session first")
        return []
    return sessions[username]

# Deletes session for a given sessionID from memory
def destroy_session(username) -> bool:
    if username not in sessions:
        # print("Session ID does not exist. Please create a Session first")
        return False
    sessions[username].clear()
    del sessions[username]
    return True
