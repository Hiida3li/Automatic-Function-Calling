# Automatic-Function-Calling


# Gemini API + Function Calling with SQLite Example

This is a simple but powerful example showing how to build a chatbot using Google's Gemini API with automatic function calling — allowing the model to query a live SQLite database.

 Project Overview:

- Use Google Gemini to chat and take actions via Python functions.
- Connect Gemini to a local SQLite database.
- Automatically list tables, describe schemas, execute SQL queries, and even plot graphs.
- Explore both automatic function calling and live streaming API capabilities.

 How It Works:

1. Setup Gemini API and authenticate.
2. Create a sample database (products, staff, orders) with synthetic data.
3. Define Python functions to interact with the database:
- list_tables()
- describe_table()
- execute_query(sql)
4. Connect these functions to Gemini API as callable tools.
5. Start chatting with Gemini to explore and modify the database.
6. Use Live API for real-time streaming, code generation, and dynamic execution.

 Tech Stack:


Tool	Purpose:
Google Gemini API	LLM for conversation and reasoning
SQLite	Local lightweight database
Python 3	Backend logic and SDK integration
Pandas + Seaborn, matplotlib	Plotting and data visualization

 Setup Instructions:

1. Install Dependencies
pip install -U google-genai
pip install pandas seaborn matplotlib ipython
(Optional if running in Kaggle: uninstall conflicting jupyterlab packages.)

2. API Key
Get your Google Gemini API key from Google AI Studio.
If you're using Kaggle, store it under Add-ons ➔ Secrets ➔ GOOGLE_API_KEY.
3. Create Sample Database
The notebook automatically creates a sample.db SQLite file with:

Products
Staff
Orders
You can modify or expand this database easily!

4. Run the Notebook
The notebook will:

Connect Gemini API
Define callable functions
Chat naturally with the model while it interacts with the database!

 Features Demo:

Ask: "What is the cheapest product?"
➔ Gemini generates SQL, runs it, and replies.
Ask: "What products has Alice sold?"
➔ Gemini joins tables and gives a clean answer.
Ask: "Plot number of orders per staff."
➔ Gemini writes Python code to generate a Seaborn bar chart!

 Advanced Features:

Live Streaming API:
See Gemini generate code live.
Watch tool calls and outputs in real-time.
Compositional Function Calling:
Gemini can chain multiple tool calls together automatically.
 Notes & Limitations:

Security: This is a toy example. In real apps:
Sanitize user input.
Secure database connections.
Validate SQL queries.
Rate Limits: API retries are handled but high load may still fail.
Cost: Gemini API usage might incur billing depending on your Google account.
