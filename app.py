import streamlit as st
import os
from dotenv import load_dotenv
from google import genai

# 1. Setup
load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

st.set_page_config(page_title="GITAM AI Assistant", page_icon="🎓")
st.title("🎓 GITAM University AI")
st.markdown("Ask me anything about admissions, fees, or campuses!")

# 2. Load Knowledge
@st.cache_data
def load_knowledge():
    with open("gitam_data.md", "r", encoding="utf-8") as f:
        return f.read()

knowledge = load_knowledge()

# 3. Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("How can I help you today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # RAG Logic
    rules = "Answer in 2-3 lines using ONLY the context. If unknown, give GITAM's contact email."
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"{rules}\n\nContext: {knowledge}\n\nQuestion: {prompt}"
    )
    
    with st.chat_message("assistant"):
        st.markdown(response.text)
    st.session_state.messages.append({"role": "assistant", "content": response.text})