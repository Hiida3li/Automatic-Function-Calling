import os
from dotenv import load_dotenv
from gemini_model import create_chat_client
from utils import print_chat_turns

def main():
    """Run a chat session with the Gemini API over the SQLite database."""
    load_dotenv()
    api_key = os.getenv("google_api_key")
    
    if not api_key:
        print("ERROR: API key not found! Make sure you have a .env file with google_api_key set.")
        return
    
    print("Initializing chat client...")
    chat = create_chat_client(api_key)
    
    print("\n=== SQLite Database Chat Interface ===")
    print("Ask questions about the database in natural language.")
    print("Type 'exit' to quit, 'history' to see the conversation history.\n")
    
    while True:
        user_input = input("\nYou: ")
        
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
            
        if user_input.lower() == 'history':
            print("\n=== Conversation History ===")
            print_chat_turns(chat)
            print("===========================\n")
            continue
        
        try:
            response = chat.send_message(user_input)
            print(f"Assistant: {response.text}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
