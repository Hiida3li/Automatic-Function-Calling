from gemini_client import create_chat_client

def main():
    API_KEY = "google_api_key"  # Replace or use environment variable
    chat = create_chat_client(API_KEY)
    
    print("Chat with SQLite database. Type 'exit' to quit.")
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'exit':
            break
            
        response = chat.send_message(user_input)
        print(f"Assistant: {response.text}")

if __name__ == "__main__":
    main()
