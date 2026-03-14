import streamlit as st
import os
from google import genai

# 1. Setup - This line is the "Bridge"
api_key = st.secrets.get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("🔑 API Key Missing! Please add GOOGLE_API_KEY to Streamlit Secrets.")
    st.stop()

client = genai.Client(api_key=api_key)

# 2. Load Knowledge (The small version you made)
@st.cache_data
def load_knowledge():
    with open("gitam_data.md", "r", encoding="utf-8") as f:
        return f.read()

knowledge = load_knowledge()

# 3. Chat Logic
st.title("🎓 GITAM University AI")

if prompt := st.chat_input("Ask me about GITAM..."):
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # We use gemini-1.5-flash for the best stability on Free Tier
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=f"Context: {knowledge}\n\nQuestion: {prompt}\n\nAnswer in 2 lines."
            )
            st.markdown(response.text)
        except Exception as e:
            # This catches the ClientError and tells you WHY
            if "429" in str(e):
                st.warning("⏱️ Quota reached! Please wait 1 minute.")
            elif "403" in str(e):
                st.error("🚫 API Key is invalid or restricted.")
            else:
                st.error(f"Error: {e}")