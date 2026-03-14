import streamlit as st
import os
from google import genai
from google.genai import types

# 1. Setup - Safe Key Loading
api_key = st.secrets.get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("🔑 API Key Missing! Please add GOOGLE_API_KEY to Streamlit Secrets.")
    st.stop()

# Initialize with stable API version v1 to avoid 'Not Found' errors
client = genai.Client(
    api_key=api_key,
    http_options=types.HttpOptions(api_version="v1")
)

# 2. Load Knowledge base
@st.cache_data
def load_knowledge():
    try:
        with open("gitam_data.md", "r", encoding="utf-8") as f:
            return f.read()
    except:
        return "Knowledge base empty."

knowledge = load_knowledge()

st.title("🎓 GITAM University AI")

if prompt := st.chat_input("Ask me something..."):
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Using the stable 2.5 Flash model
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=f"Context: {knowledge}\n\nQuestion: {prompt}\n\nAnswer in 2 lines."
            )
            st.markdown(response.text)
        except Exception as e:
            # Handle the specific "Leaked Key" error if it happens again
            if "403" in str(e):
                st.error("❌ This API Key has been disabled by Google. Please generate a NEW one in AI Studio.")
            else:
                st.error(f"Error: {e}")