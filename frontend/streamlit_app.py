# frontend/streamlit_app.py
import streamlit as st
from backend.query_engine import answer_query

st.title("📚 DocuBot Lite")
st.write("If you see this, Streamlit is running correctly!")
query = st.text_input("Ask a question about the docs:")
level = st.selectbox("Choose your level:", ["Beginner", "Intermediate", "Expert"])

if st.button("Get Answer"):
    if query:
        with st.spinner("Fetching answer..."):
            ans = answer_query(query, level)
        st.subheader("Answer:")
        st.write(ans)
