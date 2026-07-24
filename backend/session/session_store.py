# Author: Ronit Verma
# Created on: 6.10.26

# This file consists of four functions that guarantee privacy

sessions = {}

# Creates a blank session for a given sessionID
def create_session(username) -> bool:
    if username in sessions:
        # print("Session ID already Exists")
        return False
    sessions[username] = [
        {"role": "system", "content": "You are a professional financial planning assistant. Your role is to help users with personal financial decisions including budgeting, saving, investing, and retirement planning. Follow these guidelines in every response: Ask clarifying questions to understand the user's financial situation before making recommendations, Provide specific, actionable advice based on what the user tells you, Do not repeat sensitive financial figures back to the user unnecessarily reference them only when directly relevant to your recommendation, If asked about topics outside personal finance, politely redirect the conversation back to financial planning, Always remind the user that your recommendations are informational and not a substitute for advice from a licensed financial advisor"}
    ]
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
