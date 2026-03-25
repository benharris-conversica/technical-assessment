"""
Technical assessment entry point.
Connect to the assessment database and run your solution from here.

The database contains unclean data (duplicates, formatting issues, missing or
invalid values, inconsistencies across tables). Your solution must support
asking an LLM questions about this data for reasoning and proposed fixes.
"""
import json
import os
import sqlite3
from pathlib import Path
from openai import OpenAI

# Optional: load environment variables (e.g. for API key)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Path to the pre-populated SQLite database
PROJECT_ROOT = Path(__file__).resolve().parent
DATA_DIR = PROJECT_ROOT / "data"
DB_PATH = DATA_DIR / "assessment.db"


def get_connection() -> sqlite3.Connection:
    """
    Return a ready-to-use connection to the assessment SQLite database.
    Row factory is set to sqlite3.Row (dict-like access by column name).
    You do not need to open or configure the DB yourself—use this connection.
    """
    if not DB_PATH.exists():
        raise FileNotFoundError(
            f"Database not found at {DB_PATH}. Ensure data/assessment.db is present."
        )
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# --- Example tools (placeholders) ---
# These demonstrate the tool-calling pattern below. Replace them with
# your own tools for querying and/or modifying the database.

def get_user_name() -> str:
    """Return the current user's name."""
    return "Alice"


def get_user_favorite_color(user_name: str) -> str:
    """Return the user's favorite color given their name."""
    favorites = {"Alice": "blue", "Bob": "green"}
    return favorites.get(user_name, "unknown")


def tool_call_example():
    client = OpenAI()

    tools = [
        {
            "type": "function",
            "name": "get_user_name",
            "description": "Get the current user's name. Takes no arguments.",
            "parameters": {
                "type": "object",
                "properties": {},
            },
        },
        {
            "type": "function",
            "name": "get_user_favorite_color",
            "description": "Get a user's favorite color given their name.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_name": {
                        "type": "string",
                        "description": "The name of the user to look up.",
                    },
                },
                "required": ["user_name"],
            },
        },
    ]

    tool_dispatch = {
        "get_user_name": lambda _args: get_user_name(),
        "get_user_favorite_color": lambda args: get_user_favorite_color(args["user_name"]),
    }

    input_list = [
        {
            "role": "user",
            "content": (
                "Find out the current user's name, then look up their "
                "favorite color, and greet them with both pieces of info."
            ),
        }
    ]

    response = client.responses.create(
        model="gpt-5.2",
        tools=tools,
        input=input_list,
    )

    while True:
        input_list += response.output

        fn_calls = [item for item in response.output if item.type == "function_call"]

        if not fn_calls:
            break

        for call in fn_calls:
            args = json.loads(call.arguments) if call.arguments else {}
            print(f"  -> Tool call: {call.name}({json.dumps(args)})")

            result = tool_dispatch[call.name](args)

            input_list.append({
                "type": "function_call_output",
                "call_id": call.call_id,
                "output": json.dumps(result),
            })

        response = client.responses.create(
            model="gpt-5.2",
            tools=tools,
            input=input_list,
        )

    return response.output_text

def main() -> None:
    # DB connection is plumbed: use conn directly; no need to create your own.
    conn = get_connection()
    try:
        # Example query: rows support dict-like access by column name (conn.row_factory = sqlite3.Row)
        cur = conn.execute(
            "SELECT id, full_name, email, region FROM customers LIMIT 3"
        )
        for row in cur:
            print(dict(row))  # e.g. {"id": 1, "full_name": "John Smith", "email": "...", "region": "US"}
        # Candidate implements: data analysis, LLM calls, and proposed fixes here.
    finally:
        conn.close()

    print(tool_call_example())


if __name__ == "__main__":
    main()
