import os
import asyncio
from pprint import pformat
from dotenv import load_dotenv
from google import genai
from google.genai import types
from db_tools import execute_query

# For Jupyter notebooks
try:
    import nest_asyncio
    nest_asyncio.apply()
except ImportError:
    pass

async def handle_response(stream, tool_impl=None):
    """Stream output and handle any tool calls during the session."""
    all_responses = []

    async for msg in stream.receive():
        all_responses.append(msg)

        if text := msg.text:
            # Output any text chunks that are streamed back.
            if len(all_responses) < 2 or not all_responses[-2].text:
                # Print a header if this is the first text chunk.
                print("\n=== Text ===")
            print(text, end='')

        elif tool_call := msg.tool_call:
            # Handle tool-call requests.
            for fc in tool_call.function_calls:
                print(f"\n=== Tool Call: {fc.name} ===")

                # Execute the tool and collect the result to return to the model.
                if callable(tool_impl):
                    try:
                        result = tool_impl(**fc.args)
                    except Exception as e:
                        result = str(e)
                else:
                    result = 'ok'

                tool_response = types.LiveClientToolResponse(
                    function_responses=[types.FunctionResponse(
                        name=fc.name,
                        id=fc.id,
                        response={'result': result},
                    )]
                )
                await stream.send(input=tool_response)

        elif msg.server_content and msg.server_content.model_turn:
            # Print any messages showing code the model generated and ran.
            for part in msg.server_content.model_turn.parts:
                if code := part.executable_code:
                    print(f"\n=== Code ===\n{code.code}")

                elif result := part.code_execution_result:
                    print(f"\n=== Result: {result.outcome} ===\n{pformat(result.output)}")

    print()
    return all_responses

async def run_live_query(api_key, user_message):
    """Run a query using the Gemini Live API with code execution."""
    
    # Use the exact same model as in the tutorial
    model = 'gemini-2.0-flash-exp'
    
    live_client = genai.Client(
        api_key=api_key,
        http_options=types.HttpOptions(api_version='v1alpha')
    )

    # Wrap the execute_query tool
    execute_query_tool_def = types.FunctionDeclaration.from_callable(
        client=live_client, 
        callable=execute_query
    )

    sys_int = """You are a database interface. Use the `execute_query` function
    to answer questions about a computer store database with tables:
    - products (product_id, name, price, category, stock)
    - staff (staff_id, name, position, hire_date) 
    - orders (order_id, product_id, staff_id, quantity, order_date)

    First inspect table structure with PRAGMA table_info() before querying.
    """

    config = {
        "response_modalities": ["TEXT"],
        "system_instruction": {"parts": [{"text": sys_int}]},
        "tools": [
            {"code_execution": {}},
            {"function_declarations": [execute_query_tool_def.to_json_dict()]},
        ],
    }

    try:
        print(f"Connecting to Live API with model: {model}")
        
        async with live_client.aio.live.connect(model=model, config=config) as session:
            print(f"> {user_message}\n")
            await session.send(input=user_message, end_of_turn=True)
            responses = await handle_response(session, tool_impl=execute_query)
            
        return responses
    except Exception as e:
        print(f"Error connecting to Live API: {e}")
        print("\nIf you encounter model not found errors, you may not have access to the experimental Live API.")
        print("Try using the regular function calling interface instead.")
        
        
        try:
            print("\nAvailable models for your API key:")
            models = live_client.list_models()
            for m in models:
                if "flash" in m.name or "exp" in m.name:
                    print(f"- {m.name}")
        except:
            pass
            
        return None

def live_api_query(query):
    """Run a Live API query (blocking wrapper for async function)."""
    load_dotenv()
    api_key = os.getenv("google_api_key")
    
    if not api_key:
        print("ERROR: API key not found! Make sure you have a .env file with google_api_key set.")
        return
        
    loop = asyncio.get_event_loop()
    responses = loop.run_until_complete(run_live_query(api_key, query))
    return responses

if __name__ == "__main__":
    
    query = input("Enter your database query/request: ")
    live_api_query(query)
