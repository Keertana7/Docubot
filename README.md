# Docubot: AI Chatbot using Retrieval-Augmented Generation (RAG)

**Docubot** is a modular AI chatbot system that answers questions from documentation using semantic search and embeddings (RAG).

---

## Features

- **Semantic Search** using FAISS vector index  
- **Document Chunking** for efficient retrieval  
- **Pre-generated Embeddings** with Sentence Transformers  
- **Single-Question Query Support** (multi-turn chat planned)  
- **Streamlit Frontend** for interactive queries  

---

## How It Works

The system processes a user query in the following steps:

1. Convert the query into an embedding using `all-MiniLM-L6-v2`.  
2. Perform a similarity search in the FAISS index.  
3. Retrieve the most relevant document chunks.  
4. Generate an answer using the retrieved context.  
5. Return the answer via the backend or Streamlit frontend.

---

## Usage

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/Docubot.git
cd Docubot
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Backend
```bash
python backend/app.py
```

### 4. Run the Frontend
```bash
streamlit run frontend/streamlit_app.py
```

---

## Notes

- `knowledge_base/` contains pre-generated chunks, embeddings, and the FAISS index.  
- `build_index.py` is used to generate chunks and embeddings from a given text.  
- This version supports **single-question queries**. Multi-turn conversation support is planned for future updates.

---

## Future Features (Planned)

- Multi-turn conversation support (chat memory)  
- Level-based answers: Beginner, Intermediate, Expert  
- Improved explanations and context handling  
- Frontend UI enhancements (chat bubbles, better interface)
