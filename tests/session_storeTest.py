# Author: Ronit Verma
# Created on: 6.21.26

# This file is a test to ensure the functions inside backend/session/session_store.py accurately
# function as expected

from backend.session.session_store import create_session, add_message, get_history, destroy_session, sessions

create_session("testID")
print(sessions)
add_message("testID", "user", "This is a test run")
print(sessions)
testHistory = get_history("testID")
print(testHistory)
destroy_session("testID")
print(sessions)



