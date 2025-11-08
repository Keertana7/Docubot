# frontend/streamlit_app.py
import sys
import os
import streamlit as st
from threading import Thread
from queue import Queue

# Add parent folder to path so backend can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.query_engine import answer_query

# --- Page configuration ---
st.set_page_config(page_title="Docubot Chat", page_icon="🤖")

st.title("🤖 Docubot Chat")
st.markdown("Ask me anything from your documents!")

# --- Sidebar for level selection ---
level = st.sidebar.selectbox(
    "Choose your level",
    ["Beginner", "Intermediate", "Advanced"]
)

# --- Initialize chat history ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Function to run backend in separate thread ---
def run_query(query, level, queue):
    try:
        response = answer_query(query, level=level.lower())
    except Exception as e:
        response = f"Error: {str(e)}"
    queue.put(response)

# --- Chat input ---
query = st.text_input("You:", "")

if st.button("Send") and query:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": query})

    # Queue for thread result
    q = Queue()
    thread = Thread(target=run_query, args=(query, level, q))
    thread.start()

    # Display spinner while waiting
    with st.spinner("Docubot is thinking..."):
        thread.join()  # Wait for thread to finish
        response = q.get()

    # Add bot response
    st.session_state.messages.append({"role": "bot", "content": response})

# --- Display chat history ---
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"*You:* {msg['content']}")
    else:
        st.markdown(f"*Docubot:* {msg['content']}")