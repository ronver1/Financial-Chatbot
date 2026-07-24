# Financial Chatbot

A command-line financial planning assistant that uses a locally-hosted LLM (via [Ollama](https://ollama.com/)) to help users with budgeting, saving, investing, and retirement planning. The chatbot maintains per-user conversation sessions in memory and is guided by a system prompt that keeps it focused on personal finance topics.

## Security & Session Isolation

Because this chatbot handles sensitive financial information, session isolation is a core design goal, not an afterthought:

- **Per-user session isolation.** Every user is keyed by username in `session_store.py`, and each session maintains its own independent message history. One user's financial details, goals, and conversation history are never merged with, appended to, or readable from another user's session.
- **No cross-session leakage into the model.** Each call to the LLM (`get_response`) is scoped to a single user's history at a time — only the requesting user's own messages are ever sent as context. There is no shared or global conversation state passed to the model, so one user's data cannot surface in another user's responses.
- **No persistent model memory.** The Ollama client calls the API with `"keep_alive": 0`, meaning the model is unloaded after each response rather than retaining context or state between calls. The LLM itself does not "remember" prior users or sessions outside of the explicit history it's given for that single request.
- **Explicit session teardown.** `destroy_session()` clears a user's message list and removes it from the in-memory store entirely, so financial data does not linger beyond the intended lifetime of a session.
- **Multi-user by design.** The session store is a dictionary keyed by username, allowing multiple users to hold concurrent, fully independent sessions without any risk of their financial data intermingling.

## How It Works

1. The user is prompted to enter a username.
2. If no session exists for that username, one is created with a system prompt that instructs the model to act as a professional financial planning assistant.
3. The user chats with the assistant in a loop — each message is added to the session history, sent to a local Ollama model (`llama3.2:3b`), and the model's reply is appended back to the history and printed.
4. Typing `Done` ends the current user's chat loop (returns to the username prompt). Typing `Quit` destroys all active sessions and exits the program.

## Project Structure

```
Financial-Chatbot-main/
├── backend/
│   ├── backendEngine.py        # Main entry point — runs the chat loop
│   ├── auth/
│   │   └── userAuth.py         # Looks up or creates a session for a username
│   ├── llm/
│   │   └── ollama_client.py    # Sends conversation history to Ollama and returns the reply
│   └── session/
│       └── session_store.py    # In-memory session store (create, add, get, destroy)
├── tests/
│   ├── ollama_test.py          # Standalone script for exploring the Ollama chat API
│   ├── ollama_clientTest.py    # Sanity check for get_response()
│   ├── session_storeTest.py    # Sanity check for session_store functions
│   └── userAuthTest.py         # Auth test (currently out of sync — see Known Issues)
└── requirements.txt
```

## Prerequisites

- Python 3.9+
- [Ollama](https://ollama.com/) installed and running locally, with the `llama3.2:3b` model pulled:
  ```bash
  ollama pull llama3.2:3b
  ollama serve
  ```
  The client expects Ollama's API to be reachable at `http://localhost:11434`.

## Setup

```bash
# Clone the repository
git clone <repo-url>
cd Financial-Chatbot-main

# Create and activate a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Running the Chatbot

From the project root (so the `backend` package resolves correctly):

```bash
python -m backend.backendEngine
```

Then:
- Enter a username to start (or resume) a session.
- Type messages at the `Chat:` prompt to talk with the assistant.
- Type `Done` to stop chatting as the current user and return to the username prompt.
- Type `Quit` to destroy all sessions and exit the program entirely.

## Session Behavior

Sessions are stored **in memory only** (`backend/session/session_store.py`), keyed by username:
- `create_session(username)` — initializes a session with the system prompt, if one doesn't already exist.
- `add_message(username, role, content)` — appends a `{role, content}` message to the session.
- `get_history(username)` — returns the full message history for a session.
- `destroy_session(username)` — clears and removes a session.

Since sessions live only in process memory, all conversation history is lost when the program exits.

## Running Tests

The `tests/` scripts are standalone sanity checks (not pytest-based, despite `pytest` being in `requirements.txt`) and are run directly:

```bash
python -m tests.session_storeTest
python -m tests.ollama_clientTest
```

`ollama_clientTest.py` and `ollama_test.py` require a running Ollama instance with `llama3.2:3b` pulled.

## Additional Information

- No persistent storage: user accounts and chat history do not survive a restart.
- No automated test runner/CI is configured yet (tests are plain scripts, not pytest test cases).

## Disclaimer

This chatbot provides general, informational financial guidance generated by an LLM. It is not a licensed financial advisor, and its responses should not be treated as a substitute for professional financial advice.

This project also serves as a proof of concept for a privacy-preserving, non-data-leaking conversational architecture: a system in which each user's sensitive financial information remains strictly isolated to their own session, with no cross-user data exposure through the application layer or the underlying language model. It is intended to demonstrate feasible design patterns for secure, multi-user LLM applications rather than to serve as a production-hardened financial platform.

## Author

**Ronit Verma**
The University of Texas at Austin
Electrical & Computer Engineering Honors + Business Honors

LinkedIn: [www.linkedin.com/in/ronver1](https://www.linkedin.com/in/ronver1)
