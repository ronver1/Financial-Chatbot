# Author: Ronit Verma
# Created on: 6.10.26

# This file consists of four functions that guarantee privacy

sessions = {}

# Creates a blank session for a given sessionID
def create_session(session_id) -> bool:
    if session_id in sessions:
        # print("Session ID already Exists")
        return False
    sessions[session_id] = []
    # print("Successfully Created Session")
    return True

# Appends a message to given sessionID's session 
def add_message(session_id, role, content) -> bool:
    if session_id not in sessions:
        # print("Session ID does not exist. Please create a Session first")
        return False
    sessions[session_id].append({"role": role, "content": content})
    return True

# Returns the session history of a given sessionID
def get_history(session_id) -> list[dict]:
    if session_id not in sessions:
        # print("Session ID does not exist. Please create a Session first")
        return []
    return sessions[session_id]

# Deletes session for a given sessionID from memory
def destroy_session(session_id) -> bool:
    if session_id not in sessions:
        # print("Session ID does not exist. Please create a Session first")
        return False
    sessions[session_id].clear()
    del sessions[session_id]
    return True
