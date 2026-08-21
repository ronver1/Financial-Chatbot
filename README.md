# Secure Financial Chatbot

A command-line financial planning assistant built on a locally-hosted LLM (via [Ollama](https://ollama.com/)) that helps users with budgeting, saving, investing, and retirement planning. The project's guiding principle is **privacy by design**: every user's sensitive financial information stays strictly isolated to their own in-memory session, with no cross-user leakage through the application layer or the underlying model.

The chatbot is being extended with a **Retrieval-Augmented Generation (RAG)** layer so that answers can be grounded in a curated financial-planning knowledge base — keeping responses accurate even where the base model's training data is stale (for example, current-year contribution limits).

---

## Security & Session Isolation

Because this chatbot handles sensitive financial information, session isolation is a core design goal, not an afterthought:

- **Per-user session isolation.** Every user is keyed by username in `session_store.py`, and each session maintains its own independent message history. One user's financial details, goals, and conversation history are never merged with, appended to, or readable from another user's session.
- **No cross-session leakage into the model.** Each call to the LLM (`get_response`) is scoped to a single user's history at a time — only the requesting user's own messages are ever sent as context. There is no shared or global conversation state passed to the model, so one user's data cannot surface in another user's responses.
- **No persistent model memory (cache control).** The Ollama chat client calls the API with `"keep_alive": 0`, so the chat model is unloaded after each response rather than retaining context or state between calls. The LLM does not "remember" prior users or sessions beyond the explicit history it is given for a single request. This behavior is the focus of the `cache-control` branch.
- **Explicit session teardown.** `destroy_session()` clears a user's message list and removes it from the in-memory store entirely, so financial data does not linger beyond the intended lifetime of a session. Typing `Quit` tears down **all** active sessions and forces garbage collection before exit.
- **Multi-user by design.** The session store is a dictionary keyed by username, allowing multiple users to hold concurrent, fully independent sessions without any risk of their financial data intermingling.

---

## Retrieval-Augmented Generation (RAG)

The RAG layer grounds the assistant's answers in a hand-curated knowledge base of financial-planning reference material stored as plain-text files under `knowledge/`.

### How the pipeline works

1. **Knowledge base.** Each file in `knowledge/*.txt` is a single, self-contained paragraph covering one concept (e.g. emergency funds, Roth vs. traditional accounts, current-year contribution limits). Because each file is already one coherent chunk, no additional text-splitting is required.
2. **Vectorization (ingestion).** At startup, every document is passed to a dedicated embedding model (`nomic-embed-text`, served locally by Ollama) which converts it into a 768-dimension vector. Each `(text, vector)` pair is held in an in-memory store.
3. **Retrieval.** At query time, the user's question is embedded with the same model and compared against the stored vectors using cosine similarity. The top-*k* most relevant documents are returned.
4. **Augmentation & generation.** The retrieved documents are injected into the prompt as transient context for that single request, and the chat model (`llama3.2:3b`) generates a grounded answer. The retrieved context is **not** written into the user's stored session history, preserving the session-isolation guarantee.

### Why RAG here

The base model's knowledge is frozen at its training cutoff and will confidently return outdated figures (e.g. prior-year IRA/401(k)/HSA limits). Grounding answers in a maintained knowledge base keeps time-sensitive facts correct. The numeric knowledge files are labeled by tax year and are intended to be refreshed annually against [IRS.gov](https://www.irs.gov/).

### Current status

The RAG modules (`embeddings.py`, `loader.py`, `vector_store.py`) are implemented and have been **verified in isolation** — ingestion embeds all knowledge files and stores their vectors correctly. **Wiring retrieval into the live chat loop in `backendEngine.py` is the next step and is not yet complete.** The running chatbot currently sends conversation history to the model *without* retrieval augmentation; see [Roadmap](#roadmap).

---

## How It Works

1. The user is prompted to enter a username.
2. If no session exists for that username, one is created, seeded with a system prompt that instructs the model to act as a professional financial planning assistant (ask clarifying questions, give actionable advice, avoid unnecessarily repeating sensitive figures, redirect off-topic requests, and always note that guidance is informational).
3. The user chats with the assistant in a loop — each message is added to the session history, sent to the local Ollama chat model, and the reply is appended back to the history and printed.
4. Typing `Done` ends the current user's chat loop (returns to the username prompt). Typing `Quit` destroys all active sessions and exits the program.

---

## Project Structure

```
Secure-Financial-Chatbot/
├── backend/
│   ├── backendEngine.py         # Main entry point — runs the chat loop
│   ├── auth/
│   │   └── userAuth.py          # Looks up or creates a session for a username
│   ├── llm/
│   │   └── ollama_client.py     # Sends conversation history to Ollama, returns the reply
│   ├── rag/
│   │   ├── embeddings.py        # Turns a string into a vector via nomic-embed-text
│   │   ├── loader.py            # Reads knowledge/*.txt and vectorizes each file (ingest)
│   │   └── vector_store.py      # In-memory vector store + cosine-similarity search
│   └── session/
│       └── session_store.py     # In-memory session store (create, add, get, destroy)
├── knowledge/                   # RAG knowledge base — one concept per .txt file
│   ├── emergency_fund.txt
│   ├── roth_vs_traditional.txt
│   ├── budgeting_50_30_20.txt
│   ├── debt_payoff_strategies.txt
│   ├── compound_interest.txt
│   ├── saving_order_of_operations.txt
│   ├── term_vs_whole_life_insurance.txt
│   ├── index_funds_expense_ratios.txt
│   ├── contribution_limits_2026.txt
│   └── roth_ira_income_limits_2026.txt
├── tests/
│   ├── ollama_test.py           # Standalone script for exploring the Ollama chat API
│   ├── ollama_clientTest.py     # Sanity check for get_response()
│   ├── session_storeTest.py     # Sanity check for session_store functions
│   └── userAuthTest.py          # Auth test
└── requirements.txt
```

---

## Prerequisites

- **Python 3.9+**
- **[Ollama](https://ollama.com/)** installed and running locally, reachable at `http://localhost:11434`, with **two** models pulled:

  ```bash
  ollama pull llama3.2:3b        # chat / generation model
  ollama pull nomic-embed-text   # embedding model for RAG
  ollama serve
  ```

  Confirm both are present with `ollama list`.

---

## Setup

```bash
# Clone the repository
git clone https://github.com/ronver1/Secure-Financial-Chatbot.git
cd Secure-Financial-Chatbot

# (optional but recommended) create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

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

---

## Verifying the RAG Ingestion

You can confirm the knowledge base vectorizes correctly, independent of the chat loop, by running the ingestion directly from the project root:

```bash
python -c "
from backend.rag.loader import ingest
from backend.rag.vector_store import store
n = ingest()
print('files ingested:', n)
print('vectors stored:', len(store))
print('vector dimension:', len(store[0]['vector']))
"
```

Expected output (10 knowledge files, 768-dimension embeddings):

```
files ingested: 10
vectors stored: 10
vector dimension: 768
```

> **Note:** `nomic-embed-text` may be unloaded by Ollama after an idle period, so the first embedding call in a fresh process can incur a brief cold-start delay. `embeddings.py` retries around this and requests `keep_alive: "10m"` to keep the model warm during ingestion.

---

## Session Behavior

Sessions are stored **in memory only** (`backend/session/session_store.py`), keyed by username:

- `create_session(username)` — initializes a session seeded with the system prompt, if one does not already exist.
- `add_message(username, role, content)` — appends a `{role, content}` message to the session.
- `get_history(username)` — returns the full message history for a session.
- `destroy_session(username)` — clears and removes a session.

Since sessions live only in process memory, all conversation history is lost when the program exits.

---

## Running Tests

The `tests/` scripts are standalone sanity checks (not pytest-based, despite `pytest` being in `requirements.txt`) and are run directly:

```bash
python -m tests.session_storeTest
python -m tests.ollama_clientTest
```

`ollama_clientTest.py` and `ollama_test.py` require a running Ollama instance with `llama3.2:3b` pulled.

---

## Roadmap

- **Wire RAG into the chat loop.** Call `ingest()` once at startup and inject retrieved context per query in `backendEngine.py`, so live responses are grounded in the knowledge base.
- **Contrast testing.** Compare answers with and without retrieval (e.g. asking for the current-year IRA contribution limit) to confirm retrieval is materially improving accuracy.
- **Vector-store persistence.** Swap the in-memory store for a persistent local vector database (e.g. ChromaDB) once the knowledge base grows large enough that re-embedding at every startup becomes costly.
- **Knowledge-base maintenance.** Refresh the year-specific numeric files (contribution limits, income phase-outs) annually against IRS publications.

---

## Additional Information

- **No persistent storage.** User accounts, chat history, and vectors do not survive a restart; the knowledge base is re-embedded each launch.
- **No CI configured yet.** Tests are plain scripts rather than pytest test cases, and no automated runner is set up.
- Several Supabase / cryptography packages appear in `requirements.txt` in anticipation of future persistence and auth work; they are not yet exercised by the current code path.

---

## Disclaimer

This chatbot provides general, informational financial guidance generated by an LLM. It is **not** a licensed financial advisor, and its responses should not be treated as a substitute for professional financial advice.

This project also serves as a proof of concept for a privacy-preserving, non-data-leaking conversational architecture: a system in which each user's sensitive financial information remains strictly isolated to their own session, with no cross-user data exposure through the application layer or the underlying language model. It is intended to demonstrate feasible design patterns for secure, multi-user LLM applications rather than to serve as a production-hardened financial platform.

---

## Author

**Ronit Verma**
The University of Texas at Austin
Electrical & Computer Engineering Honors + Business Honors

LinkedIn: [www.linkedin.com/in/ronver1](https://www.linkedin.com/in/ronver1)
