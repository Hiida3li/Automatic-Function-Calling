import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

from db_tools import list_tables, describe_table, execute_query

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

if __name__ == "__main__":
    if not api_key:
        print("API key not found. Make sure you have set the google_api_key in your .env file.")
        exit(1)
        
    print(f"API key loaded: {'Yes' if api_key else 'No'}")
    
    try:
        tables = list_tables()
        print(f"Tables in database: {tables}")
    except Exception as e:
        print(f"Error listing tables: {e}")
        exit(1)
    
    chat = create_chat_client(api_key)
    resp = chat.send_message("What is the cheapest product?")
    print(f"\nResponse: {resp.text}")
