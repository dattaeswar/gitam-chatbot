import os
from dotenv import load_dotenv
from google import genai

# Load secrets from .env file
load_dotenv()
GOOGLE_KEY = os.getenv("AIzaSyBJy8RjBw6FLs92-A5uAb5e2KxRZ2sqFEU")

# Initialize Gemini 2.5 Client
client = genai.Client(api_key=GOOGLE_KEY)
MODEL_ID = "gemini-2.5-flash"

# Load the knowledge file created by the crawler
try:
    with open("gitam_data.md", "r", encoding="utf-8") as f:
        gitam_knowledge = f.read()
except FileNotFoundError:
    print("Error: gitam_data.md not found! Run crawl_gitam.py first.")
    exit()

def ask_ai(question):
    # These rules keep the AI fast, short, and honest
    system_rules = """
    Rules:
    1. Answer in MAX 2-3 lines.
    2. Use ONLY the provided context. No hallucinations.
    3. If the answer is missing, say: 'Information not found. Please contact GITAM admissions at admissions@gitam.edu for human help.'
    """
    
    response = client.models.generate_content(
        model=MODEL_ID,
        contents=f"{system_rules}\n\nContext: {gitam_knowledge}\n\nQuestion: {question}"
    )
    return response.text

print(f"--- GITAM AI (Powered by {MODEL_ID}) is Online! ---")

while True:
    user_input = input("\nYou: ")
    if user_input.lower() in ['exit', 'quit', 'bye']:
        break
        
    print("Thinking...")
    try:
        answer = ask_ai(user_input)
        print(f"AI: {answer}")
    except Exception as e:
        # If you hit the 429 Quota error, this will tell you
        print(f"Error: {e}")