import streamlit as st
from google import genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Works both locally (.env) and on Streamlit Cloud (secrets)
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except:
    api_key = os.getenv("GEMINI_API_KEY")

# Page configuration
st.set_page_config(
    page_title="Foxxy AI 🔥",
    page_icon="🔥",
    layout="centered"
)

st.title("Foxxy AI 🔥")
st.caption("Simple chatbot powered by SYED ABRAR Inc")

# Check API key
if not api_key:
    st.error("❌ GEMINI_API_KEY not found")
    st.stop()

# Keep the client alive (important for Streamlit)
@st.cache_resource
def get_gemini_client():
    return genai.Client(api_key=api_key)

client = get_gemini_client()

# Sidebar
with st.sidebar:
    st.header("Settings")
    model_name = st.selectbox(
        "Choose model",
        [
            "gemini-3.8-flash",
            "gemini-3.5-flash",
            "gemini-3.5-flash-lite"
        ],
        index=0
    )

    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm Foxxy AI 🔥. How can I help you today?"}
    ]

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Type your message..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get response from Gemini
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Rebuild history
                history = []
                for m in st.session_state.messages[:-1]:
                    role = "user" if m["role"] == "user" else "model"
                    history.append({"role": role, "parts": [{"text": m["content"]}]})

                chat = client.chats.create(model=model_name, history=history)
                response = chat.send_message(prompt)
                reply = response.text
            except Exception as e:
                reply = f"⚠️ Error: {str(e)}"

        st.markdown(reply)

    # Save assistant reply
    st.session_state.messages.append({"role": "assistant", "content": reply})