# Technical Assessment

## Goal

Build a **data analysis agent** that a non-technical user could interact with to understand and ask questions about their customer data.

The provided SQLite database (`data/assessment.db`) is pre-populated with data. The data has **intentional quality issues** that may affect the accuracy of the agent's answers. Discovering and dealing with these issues is part of the challenge — how you choose to address them is up to you.

See **[EXAMPLE_QUESTIONS.md](EXAMPLE_QUESTIONS.md)** for the types of questions a user might ask the agent you build.

---

## Getting started

We recommend starting by running `main.py`:

```bash
python main.py
```

`main.py` contains template code for your convenience. It demonstrates:

1. **Connecting to the SQLite database** — `get_connection()` returns a ready-to-use connection to `data/assessment.db` (with `row_factory` set for dict-like row access).
2. **Using the OpenAI Responses API with tool calling** — `tool_call_example()` shows the request/response pattern for defining tools, dispatching calls, and looping until the model is done. The example tools (`get_user_name`, `get_user_favorite_color`) are placeholders to illustrate the API pattern — replace them with your own tools.

---

## Setup (local only — skip if using Coderpad)

If you are running this on your own machine (not in Coderpad), you will need to install dependencies and configure your API key:

1. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **API key**

   Copy `.env.example` to `.env` and fill in the key provided by the interviewer. Ensure your solution loads the key from the environment (e.g. via `python-dotenv`). Do not commit real keys.

---

## Repository structure

```
.
├── README.md                # This file
├── EXAMPLE_QUESTIONS.md     # Example questions your agent should handle
├── requirements.txt         # Python dependencies
├── .env.example             # Placeholder for API key
├── main.py                  # Entry point — build your agent here
└── data/
    └── assessment.db        # SQLite DB (pre-populated; explore via queries)
```
