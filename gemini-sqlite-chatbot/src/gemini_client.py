from google import genai
from google.genai import types
from db_tools import list_tables, describe_table, execute_query

def create_chat_client(api_key: str):
    """Create Gemini chat client with function calling."""
    client = genai.Client(api_key=api_key)
    
    db_tools = [list_tables, describe_table, execute_query]
    
    instruction = """You are a helpful chatbot that can interact with an SQL database.
    Use the tools to answer user questions about the database."""
    
    chat = client.chats.create(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(
            system_instruction=instruction,
            tools=db_tools,
        ),
    )
    return chat