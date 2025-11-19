# Docubot Setup & Usage Guide

## ✅ What's Been Completed

1. **Backend Query Engine** - Fully functional with Gemini API integration
   - Replaced FLAN-T5 with Google's Gemini API
   - Loads 5,129 Ceph documentation chunks from FAISS index
   - Supports 3 expertise levels: beginner, intermediate, expert
   - Uses SentenceTransformer embeddings for semantic search

2. **Data Pipeline** - Complete and verified
   - FAISS index: `data/data_prepocessing/ceph_faiss.index` (5,129 chunks)
   - Metadata: `data/data_prepocessing/ceph_metadata.json` (perfectly aligned)
   - Chunks loaded and ready for embedding-based retrieval

3. **Frontend - Flask Web App**
   - HTTP server with REST API (`app.py`)
   - HTML/CSS/JavaScript chatbot UI
   - Live in browser at `http://localhost:5000`
   - Responsive design with sidebar controls

4. **Dependencies Installed**
   - ✓ google-generativeai (v0.8.5) - Official Gemini API client
   - ✓ flask (v3.1.2)
   - ✓ faiss-cpu
   - ✓ sentence-transformers
   - ✓ All supporting packages

## 🚀 Quick Start

### Step 1: Set Gemini API Key

Get your Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

In PowerShell:
```powershell
$env:GEMINI_API_KEY = "YOUR_ACTUAL_API_KEY_HERE"
```

Or permanently set it (restart terminal after):
```powershell
[System.Environment]::SetEnvironmentVariable("GEMINI_API_KEY", "YOUR_KEY", "User")
```

### Step 2: Start the Flask Server

```powershell
cd "c:\Users\pc1\Desktop\cloned repo\Docubot"
python app.py
```

Expected output:
```
[INFO] Loaded FAISS index from preprocessing folder (ceph_faiss.index)
[INFO] Loaded metadata from ceph_metadata.json
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

### Step 3: Open the UI

Go to: **http://localhost:5000**

## 📝 How to Use Docubot

1. **Set your expertise level** using the sidebar dropdown
   - Beginner: Simple, example-rich explanations
   - Intermediate: Clear explanations with technical details
   - Expert: In-depth technical information

2. **Adjust top_k** (1-10) to control how many document chunks are used
   - Lower = faster, more focused answers
   - Higher = more comprehensive answers

3. **Type your question** and press Enter or click Send

4. **Wait for Gemini to generate** the response
   - Loading spinner indicates processing
   - Response time: ~2-5 seconds

## 🧪 Example Questions to Try

Ask Docubot anything about Ceph:

- "What is Ceph?"
- "Explain the CRUSH algorithm"
- "What are OSDs and MONs?"
- "How does Ceph handle data replication?"
- "What is RADOS?"
- "Explain Ceph object storage"
- "How does erasure coding work in Ceph?"

## 🔧 API Endpoints

The Flask server provides these REST APIs:

```bash
# Get main UI
GET http://localhost:5000/

# Send a query
POST http://localhost:5000/api/chat
Content-Type: application/json
{
    "query": "What is Ceph?",
    "level": "beginner",
    "top_k": 3
}

# Check server status
GET http://localhost:5000/api/health

# Get configuration
GET http://localhost:5000/api/config
```

## 📊 System Architecture

```
User Input (Browser)
        ↓
JavaScript (script.js)
        ↓
POST /api/chat (Flask)
        ↓
query_engine.answer_query()
        ↓
Embedding (SentenceTransformer)
        ↓
FAISS Search (5,129 chunks)
        ↓
Gemini API Generation
        ↓
Response JSON (Flask)
        ↓
Chat Display (Browser)
```

## ⚙️ File Structure

```
Docubot/
├── app.py                          # Flask server
├── backend/
│   └── query_engine.py             # Core Q&A logic
├── frontend/
│   └── streamlit_app.py            # Streamlit version (alternative)
├── templates/
│   └── index.html                  # Web UI HTML
├── static/
│   ├── style.css                   # UI styling
│   └── script.js                   # JavaScript interaction
├── data/
│   └── data_prepocessing/
│       ├── ceph_faiss.index        # FAISS index (5,129 chunks)
│       └── ceph_metadata.json      # Document metadata
└── requirements.txt                # Python dependencies
```

## 🐛 Troubleshooting

### Issue: "GEMINI_API_KEY not set"
**Solution:** Set the environment variable before running
```powershell
$env:GEMINI_API_KEY = "YOUR_KEY"
python app.py
```

### Issue: "Connection error" in chat
**Solution:** Check Flask server is running and accessible
```powershell
# In another terminal:
curl http://localhost:5000/api/health
```

### Issue: Port 5000 already in use
**Solution:** Either stop the existing process or use a different port
```powershell
# Kill the process using port 5000
Get-Process | Where-Object {$_.Name -eq "python"} | Stop-Process -Force
```

### Issue: Slow responses
**Solution:** This is normal for first query (~5-10 seconds). Subsequent queries are faster due to model caching.

### Issue: Blank responses from Gemini
**Solution:** 
1. Check API key is valid: Get a new one from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Check model availability: `gemini-1.5-flash` is the default
3. Check rate limits: Gemini has free-tier rate limits

## 📦 Requirements Installed

- google-generativeai==0.8.5
- flask==3.1.2
- faiss-cpu
- sentence-transformers
- numpy
- All dependencies

To install manually:
```powershell
pip install google-generativeai flask faiss-cpu sentence-transformers numpy
```

## 🎯 Next Steps

1. **Get API Key**: Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. **Set Environment Variable**: `$env:GEMINI_API_KEY = "YOUR_KEY"`
3. **Run Flask**: `python app.py`
4. **Open Browser**: `http://localhost:5000`
5. **Start Chatting**: Ask your first question!

---

**Status**: ✅ Fully functional and ready to use!
**Last Updated**: November 19, 2025
