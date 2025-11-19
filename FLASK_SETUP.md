# Docubot - Ceph Documentation Chatbot

A Flask-based web application that answers questions about Ceph distributed storage using Gemini AI and FAISS vector search.

## Features

- 🤖 **AI-Powered Responses** - Uses Google Gemini API for intelligent answers
- 📚 **Vector Search** - FAISS index with 5,129 Ceph documentation chunks
- 🎯 **Expertise Levels** - Adjust responses for Beginner/Intermediate/Expert
- 🔍 **Top-K Retrieval** - Customize number of relevant chunks (1-10)
- 💬 **Chat Interface** - Clean web UI with message history
- ⚡ **Real-time Processing** - Instant responses with loading feedback

## Setup

### Prerequisites
- Python 3.11+
- Anaconda/Conda environment
- Google Gemini API key

### Installation

1. **Install dependencies**:
   ```bash
   pip install flask google-genai faiss-cpu sentence-transformers numpy
   ```

2. **Set Gemini API key**:
   ```bash
   # Windows PowerShell
   $env:GEMINI_API_KEY = "your-api-key-here"
   
   # Or permanently set system environment variable:
   # Control Panel → System → Environment Variables
   ```

3. **Verify data files**:
   - `data/data_prepocessing/ceph_faiss.index` (FAISS index with 5,129 chunks)
   - `data/data_prepocessing/ceph_metadata.json` (chunk metadata)

## Usage

### Start the Flask Server

```bash
# Option 1: Direct Python
python app.py

# Option 2: With Flask CLI
flask run

# Server will start at http://localhost:5000
```

### Access the UI

Open your browser to: **http://localhost:5000**

### API Endpoints

- `GET /` - Main chatbot interface
- `POST /api/chat` - Submit a query
  ```json
  {
    "query": "What is Ceph?",
    "level": "beginner",
    "top_k": 5
  }
  ```
- `GET /api/health` - Health check
- `GET /api/config` - Get frontend configuration

## Project Structure

```
Docubot/
├── app.py                          # Flask application
├── backend/
│   ├── query_engine.py            # Core query processing
│   └── build_index.py             # Index building utilities
├── frontend/
│   └── streamlit_app.py           # Alternative Streamlit UI
├── data/
│   ├── chunks_embeddings.npy      # Pre-computed embeddings
│   ├── chunks.json                # Original chunks
│   └── data_prepocessing/
│       ├── ceph_faiss.index       # FAISS vector index (5,129 chunks)
│       └── ceph_metadata.json     # Chunk metadata
├── templates/
│   └── index.html                 # HTML template
├── static/
│   ├── style.css                  # Styling
│   └── script.js                  # Frontend logic
└── test_backend.py                # Backend tests
```

## How It Works

1. **User Query** → Frontend sends question, level, top_k to `/api/chat`
2. **Embedding** → Query is embedded using SentenceTransformer
3. **FAISS Search** → Top-k similar chunks retrieved from index
4. **Metadata Lookup** → Source documents identified from metadata
5. **Prompt Building** → Context chunks + level instructions + question
6. **Gemini Call** → API generates response using retrieved context
7. **Response** → Formatted answer returned to frontend and displayed

## Troubleshooting

### "GEMINI_API_KEY not set"
Set your API key before running:
```bash
$env:GEMINI_API_KEY = "your-key"
```

### "ModuleNotFoundError: No module named 'flask'"
Install Flask:
```bash
pip install flask
```

### "FileNotFoundError: ceph_faiss.index"
Ensure FAISS index exists at `data/data_prepocessing/ceph_faiss.index`

### Chat returns empty responses
Check that:
- GEMINI_API_KEY is set correctly
- FAISS index and metadata files exist and are aligned
- Network connection is working

## Development

### Test Backend
```bash
python test_backend.py
```

### Run with Debug Mode
Edit `app.py` line to:
```python
app.run(debug=True, host='localhost', port=5000)
```

## Configuration

Edit `backend/query_engine.py` to customize:
- Embedding model (`all-MiniLM-L6-v2`)
- FAISS index path
- Metadata path
- Default top_k value
- Prompt templates for each expertise level

## Performance Notes

- **First load**: ~2-3 seconds (loads FAISS index)
- **Typical query**: ~5-10 seconds (Gemini API latency)
- **FAISS search**: <100ms
- **Embedding**: <100ms
- **Index size**: ~50MB (FAISS)
- **Metadata size**: ~2MB (JSON)

## License

This project is for educational purposes. Ensure compliance with:
- Ceph Documentation License
- Google Gemini API Terms of Service
- FAISS Library License

## References

- [Ceph Documentation](https://docs.ceph.com/)
- [Google Generative AI](https://ai.google.dev/)
- [FAISS Documentation](https://github.com/facebookresearch/faiss)
- [Sentence Transformers](https://www.sbert.net/)

---

**Created**: 2024 | **Last Updated**: January 2025
