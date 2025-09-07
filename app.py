import streamlit as st
from backend import query_llm
import uuid

st.set_page_config(page_title="RAG PDF Chatbot", layout="wide")
st.title("Chat with your PDF")

# Session ID for user
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# Chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display previous messages
for role, content in st.session_state.chat_history:
    st.chat_message(role).markdown(content)

# Chat input
if prompt := st.chat_input("Ask me something about your PDF..."):
    # Save user message
    st.chat_message("user").markdown(prompt)
    st.session_state.chat_history.append(("user", prompt))

    # Get response from backend
    with st.spinner("Thinking..."):
        response = query_llm(prompt)

    # Save assistant message
    st.chat_message("assistant").markdown(response)
    st.session_state.chat_history.append(("assistant", response))
