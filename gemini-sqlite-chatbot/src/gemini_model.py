import os
import sqlite3
from dotenv import load_dotenv
from google import genai
from google.genai import types
from db_tools import list_tables, describe_table, execute_query

# Get the absolute path to the database file
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_file = os.path.join(base_dir, 'database', 'sample.db')
db_conn = sqlite3.connect(db_file)

load_dotenv()
api_key = os.getenv("google_api_key")

def create_chat_client(api_key: str):
    """Create Gemini chat client with function calling."""
    client = genai.Client(api_key=api_key)
    
    db_tools = [list_tables, describe_table, execute_query]
    
    instruction = """You are a helpful chatbot that can interact with an SQL database
    for a computer store. You will take the users questions and turn them into SQL
    queries using the tools available. Once you have the information you need, you will
    answer the user's question using the data returned.
    
    Use list_tables to see what tables are present, describe_table to understand the
    schema, and execute_query to issue an SQL SELECT query."""
    
    chat = client.chats.create(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(
            system_instruction=instruction,
            tools=db_tools,
        ),
    )
    return chat

# Test code at the bottom of the file
if __name__ == "__main__":
    chat = create_chat_client(api_key)
    resp = chat.send_message("What is the cheapest product?")
    print(f"\n{resp.text}") 