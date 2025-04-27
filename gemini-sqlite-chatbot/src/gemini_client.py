from google import genai
from google.genai import types
from db_tools import list_tables, describe_table, execute_query

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
    
    client = genai.Client(api_key=GOOGLE_API_KEY)

    # Start a chat with automatic function calling enabled.
    chat = client.chats.create(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(
            system_instruction=instruction,
            tools=db_tools,
        ),
    )
resp = chat.send_message("What is the cheapest product?")
print(f"\n{resp.text}")    