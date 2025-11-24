# 🤖 DocuBot: Adaptive AI Assistant for Documentation-Centered Question Answering
**Docubot** is an adaptive AI assistant designed to answer queries directly from technical documentation using a Retrieval-Augmented Generation (RAG) pipeline.
It combines:

- **FAISS-based semantic search**
- **SentenceTransformer embeddings**
- **Google Gemini API for final answer generation**
This architecture enables DocuBot to provide **accurate, context-aware, and level-adaptive explanations** tailored to the user’s understanding.

---

## 🌟 Features

- 🔍 **Semantic Search** using FAISS  
- 📘 **Document Chunking** for precise context  
- 🧠 **Pre-computed Embeddings** (`all-MiniLM-L6-v2`)  
- 🎚️ **Level-Based Answers:** Beginner, Intermediate, and Expert modes  
- ⚡ **Gemini-powered Explanation & Summarization**
- 💻 **Flask Frontend** with HTML + CSS + JS  
- 📡 REST API for integration into other apps

---

## ⚙️ How It Works

1. User enters a question in the UI.  
2. Query is embedded using `all-MiniLM-L6-v2`
3. FAISS index retrieves most relevant document chunks
4. Retrieved context + query are passed to Google Gemini
5. Gemini generates a clean, level-specific explanation
6. Flask frontend displays the response

---

## 🚀 Usage

### 1. Clone the Repository
```bash
git clone https://github.com/Keertana7/Docubot.git
cd Docubot
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Your Gemini API Key
Linux / Mac:
```bash
export GEMINI_API_KEY="your-key-here"
```
Windows (PowerShell):
```bash
setx GEMINI_API_KEY "your-key-here"
```

### 4. Run the Flask Server
```bash
python app.py
```

### 5. Open in Browser
```bash
http://localhost:5000
```

---

## 🔧 Regenerating the FAISS Index
If you update or add new documentation, you can implement logic inside:
```bash
backend/build_index.py
```
This script should:
- read raw text files
- chunk the text
- embed each chunk
- build the FAISS index
- save chunks + embeddings + index
(Currently, the file is empty and optional.)

---

## Future Features

- Support for user-uploaded documents (PDF/TXT/Docs → On-the-fly indexing)
- Conversation history and session memory
- Multilingual query & response support
- Improved document chunking and indexing pipeline
- Enhanced UI with chat bubbles and better layout
- Cleaner integration with the latest Gemini API client

---

## Project Structure
```
Docubot/
│
├── backend/
│   ├── build_index.py          # (optional) script to rebuild FAISS index
│   └── query_engine.py         # RAG pipeline + Gemini integration
│
├── data/
│   └── data_prepocessing/
│       ├── chunks.json          # text chunks of documentation
│       ├── chunks_embeddings.npy
│       └── index.faiss          # FAISS vector index
│
├── frontend/
│   ├── static/
│   │   ├── script.css           # styling
│   │   └── script.js            # AJAX + UI logic
│   └── templates/
│       └── index.html           # main webpage
│
├── app.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🧠 Tech Stack

- Python
- Flask
- Sentence Transformers
- FAISS
- Google Gemini API
- HTML, CSS, JavaScript

