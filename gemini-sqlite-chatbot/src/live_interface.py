import os
from dotenv import load_dotenv
from live_api import live_api_query

def main():
    """Run a chat session with the Gemini Live API over the SQLite database."""
    
    load_dotenv()
    api_key = os.getenv("google_api_key")
    
    if not api_key:
        print("ERROR: API key not found! Make sure you have a .env file with google_api_key set.")
        return
    
    print("\n=== Gemini Live API Database Interface ===")
    print("This interface uses the v1alpha Live API with code execution.")
    print("Ask questions or request visualizations from your database.")
    print("Try asking to create visualizations or insert data!")
    print("Type 'exit' to quit.\n")
    
    while True:
        user_input = input("\nYou: ")
        
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        
        try:
            
            live_api_query(user_input)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
    