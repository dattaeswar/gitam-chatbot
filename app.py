import streamlit as st
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# 1. Setup
load_dotenv()
api_key = st.secrets.get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("API Key not found. Please add GOOGLE_API_KEY to Streamlit Secrets.")
    st.stop()

# Force the API to use version 'v1' instead of the broken 'v1beta'
client = genai.Client(
    api_key=api_key,
    http_options=types.HttpOptions(api_version="v1")
)

# Use the 2026 stable workhorse model
MODEL_ID = "gemini-2.5-flash"

st.set_page_config(page_title="GITAM AI Assistant", page_icon="🎓")
st.title("🎓 GITAM University AI")

# 2. Load Knowledge
@st.cache_data
def load_knowledge():
    try:
        with open("gitam_data.md", "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return "Knowledge base file not found."

knowledge = load_knowledge()

# 3. Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("How can I help you?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        msg_box = st.empty()
        msg_box.markdown("Thinking...")
        
        try:
            rules = "Answer in 2-3 lines using ONLY the context. If unknown, give admissions@gitam.edu."
            response = client.models.generate_content(
                model=MODEL_ID,
                contents=f"{rules}\n\nContext: {knowledge}\n\nQuestion: {prompt}"
            )
            ans = response.text
            msg_box.markdown(ans)
            st.session_state.messages.append({"role": "assistant", "content": ans})
        except Exception as e:
            error_msg = f"API Error: {str(e)}"
            msg_box.markdown("⚠️ I'm busy right now. Please try again in 10 seconds.")
            st.sidebar.error(error_msg)