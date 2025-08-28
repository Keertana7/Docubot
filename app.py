import streamlit as st
import datetime


# Page config
st.set_page_config(page_title="Docubot", page_icon="🤖", layout="centered")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    st.title("📘 Docubot")
    st.markdown("Your AI-powered assistant using **LangChain + FAISS + Phi-3**")
    
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

st.title("💬 Chat with Docubot")

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        

# User input box
if prompt := st.chat_input("Ask me anything about your documents..."):
    # Store user query
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Temporary bot reply (to be replaced with backend call)
    bot_reply = f"🔍 You asked: **{prompt}**\n\n(Backend integration pending...)"

    # Store bot reply
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant"):
        st.markdown(bot_reply)
