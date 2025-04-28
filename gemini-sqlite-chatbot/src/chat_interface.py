import os
from dotenv import load_dotenv
from gemini_model import create_chat_client

def main():
    load_dotenv()
    
    api_key = os.getenv("google_api_key")
    
    print(f"API key loaded: {'Yes' if api_key else 'No'}")
    
    chat = create_chat_client(api_key)
    
    print("Chat with SQLite database. Type 'exit' to quit.")
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'exit':
            break
            
        response = chat.send_message(user_input)
        print(f"Gemini-AI: {response.text}")

if __name__ == "__main__":
    main()
