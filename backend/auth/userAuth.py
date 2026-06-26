# Author: Ronit Verma
# Created on: 6.26.26

# This file handles authentication and registration within the database

from backend.session.session_store import sessions, create_session, get_history


def userAccess(username) -> list[dict]:
    if username not in sessions:
        create_session(username)
    return get_history(username)
