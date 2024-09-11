# chatbot.py
import streamlit as st

def chatbot():
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    st.sidebar.header("Chatbot")
    user_input = st.sidebar.text_input("You:", "")

    if user_input:
        st.session_state.chat_history.append(f"You: {user_input}")
        st.session_state.chat_history.append(f"Bot: {user_input}")

    if st.session_state.chat_history:
        st.sidebar.text_area("Chat History:", value="\n".join(st.session_state.chat_history), height=300, max_chars=None, key="chat_history")
