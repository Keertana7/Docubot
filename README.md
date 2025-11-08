# 🤖 Docubot: AI Chatbot using Retrieval-Augmented Generation (RAG)

**Docubot** is a modular AI chatbot that answers questions from documentation using a Retrieval-Augmented Generation (RAG) pipeline.  
It combines semantic search (via FAISS) with generative summarization (via FLAN-T5) to deliver clear, level-adaptive explanations.

---

## 🌟 Features

- **Semantic Search** powered by FAISS vector index  
- **Document Chunking** for efficient information retrieval  
- **Pre-generated Embeddings** using Sentence Transformers (`all-MiniLM-L6-v2`)  
- **Level-Based Answers:** Beginner, Intermediate, and Expert modes  
- **Streamlit Frontend** for interactive Q&A  
- **Single-Question Query Support** *(multi-turn chat planned)*  

---

## ⚙️ How It Works

1. The user query is converted into an embedding using `all-MiniLM-L6-v2`.  
2. The FAISS index searches for semantically similar document chunks.  
3. The top chunks are retrieved and passed as context.  
4. The `flan-t5-base` model generates a summarized and level-adapted answer.  
5. The Streamlit interface displays the final response.  

---

## 🚀 Usage

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/Docubot.git
cd Docubot
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Frontend
```bash
streamlit run frontend/streamlit_app.py
```

---


## Notes

- `data/` contains pre-generated chunks, embeddings, and the FAISS index.  
- `backend/build_index.py` can be used to regenerate the FAISS index and embeddings from raw text.
- The current version supports **single-turn queries**; multi-turn conversational memory will be added in a future release.

---

## Future Features (Planned)

- Multi-turn conversation support (chat memory)  
- Improved summarization and contextual awareness  
- Enhanced frontend UI with chat bubbles and history
- Model performance optimization for faster responses

## Project Structure
```
Docubot/
│
├── backend/
│   ├── build_index.py          # Script to build FAISS index
│   └── query_engine.py         # Core retrieval and answer generation logic
│
├── data/                       # FAISS index and pre-computed embeddings
│   ├── chunks.json
│   ├── chunks_embeddings.npy
│   └── index.faiss
│
├── frontend/
│   └── streamlit_app.py        # Streamlit-based chat interface
│
├── .gitignore
├── README.md
└── requirements.txt
```

## 🧠 Tech Stack

- Python
- Streamlit
- Sentence Transformers
- FAISS
- Hugging Face Transformers (FLAN-T5)

