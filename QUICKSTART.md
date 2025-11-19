# 🤖 Docubot - Quick Start Guide

## What You Have

A fully functional **Docubot** chatbot that answers questions about **Ceph distributed storage** using:
- ✅ **Gemini AI** for intelligent responses
- ✅ **FAISS** vector search with 5,129 Ceph documentation chunks
- ✅ **Flask** web server with REST API
- ✅ **Clean web UI** with chat interface

## Getting Started (3 Steps)

### Step 1: Set Your Gemini API Key

**Windows PowerShell:**
```powershell
$env:GEMINI_API_KEY = "your-api-key-here"
```

**Windows Command Prompt:**
```cmd
set GEMINI_API_KEY=your-api-key-here
```

**Permanent (all sessions):**
- Control Panel → System and Security → System → Advanced System Settings
- Click "Environment Variables"
- Add new System variable: `GEMINI_API_KEY` = `your-key`
- Restart terminal

### Step 2: Start the Flask Server

```bash
cd "c:\Users\pc1\Desktop\cloned repo\Docubot"
python app.py
```

Expected output:
```
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

### Step 3: Open in Browser

Visit: **http://localhost:5000**

That's it! 🎉

---

## How to Use

1. **Ask a Question** - Type in the chat box:
   - "What is Ceph?"
   - "Explain the CRUSH algorithm"
   - "What are OSDs?"

2. **Adjust Difficulty** - Select from sidebar:
   - **Beginner** - Simple, no jargon
   - **Intermediate** - Some technical terms
   - **Expert** - Full technical details

3. **Control Precision** - Use "Top K" slider:
   - Lower (1-3) - More focused answers
   - Higher (7-10) - More comprehensive

---

## Project Structure

```
Docubot/
├── app.py                      ← Flask server (run this!)
├── backend/
│   └── query_engine.py        ← AI processing
├── templates/
│   └── index.html             ← Web interface
├── static/
│   ├── style.css              ← Styling
│   └── script.js              ← Chat logic
├── data/
│   └── data_prepocessing/
│       ├── ceph_faiss.index   ← Vector search index (5,129 chunks)
│       └── ceph_metadata.json ← Document sources
└── FLASK_SETUP.md             ← Detailed documentation
```

---

## API Endpoints

### POST /api/chat
Send a chat query:
```json
{
  "query": "What is Ceph?",
  "level": "beginner",
  "top_k": 5
}
```

Response:
```json
{
  "status": "success",
  "response": "Ceph is a distributed storage system...",
  "timestamp": "2024-01-15T10:30:45"
}
```

### GET /api/health
Check server status:
```json
{
  "status": "ok",
  "gemini_api_key_set": true
}
```

### GET /api/config
Get available options:
```json
{
  "levels": ["beginner", "intermediate", "expert"],
  "top_k_options": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
}
```

---

## Troubleshooting

### ⚠️ "Docubot is thinking..." spins forever
- ❌ API key not set → Set `GEMINI_API_KEY` env var
- ❌ Network issue → Check internet connection
- ❌ API quota exceeded → Check Gemini API usage

### ⚠️ "Connection error" in chat
- ❌ Server not running → Run `python app.py`
- ❌ Wrong URL → Use http://localhost:5000 (not https)
- ❌ Port 5000 in use → Change port in app.py

### ⚠️ Button says "Status: Error"
- ❌ Check browser console (F12 → Console tab)
- ❌ Check terminal output for error messages
- ❌ Verify API key is valid

### ⚠️ "ModuleNotFoundError" when starting
```bash
pip install flask google-genai faiss-cpu sentence-transformers numpy
```

---

## Example Questions

Try asking about Ceph:

**Basic Level:**
- "What is Ceph?"
- "What is object storage?"
- "What is RADOS?"

**Intermediate:**
- "How does the CRUSH algorithm work?"
- "What are Ceph OSDs?"
- "Explain Ceph's replication strategy"

**Advanced:**
- "Describe the CRUSH algorithm's pseudorandom function"
- "How does Ceph handle data distribution with CRUSH?"
- "Explain OSD component architecture"

---

## Performance

| Operation | Time |
|-----------|------|
| Page load | 1-2s |
| FAISS search | <100ms |
| Embedding query | <100ms |
| Gemini API call | 5-10s |
| **Total response** | **~5-10s** |

---

## Architecture

```
Browser
  ↓
  ├→ UI (index.html + script.js)
  ├→ Chat Interface (style.css)
  ↓
Flask Server (app.py)
  ↓
  ├→ POST /api/chat
  ├→ Query: "What is Ceph?"
  ↓
Query Engine (backend/query_engine.py)
  ├→ Embed query (SentenceTransformer)
  ├→ Search FAISS index (top_k=5)
  ├→ Get metadata
  ├→ Build prompt with context
  ├→ Call Gemini API
  ↓
Response
  ├→ JSON: {status, response}
  ├→ Flask returns to browser
  ↓
Browser
  ├→ script.js displays response
  ├→ Updates chat history
  ├→ Hides spinner
```

---

## Want to Customize?

### Change Port
Edit `app.py` line ~105:
```python
app.run(host='localhost', port=8080)  # Use 8080 instead
```

### Adjust Responses
Edit `backend/query_engine.py` to modify:
- System prompts for each level
- Top-k default value
- Embedding model

### Add More Data
Add more chunks to FAISS index using scripts in `data/data_prepocessing/`

---

## Next Steps

1. ✅ Run `python app.py`
2. ✅ Visit http://localhost:5000
3. ✅ Ask a question!
4. ✅ Share feedback

---

## Support Files

- **FLASK_SETUP.md** - Complete technical documentation
- **test_backend.py** - Test query engine functionality
- **verify_setup.py** - Check all dependencies

---

**Ready? Run: `python app.py` and enjoy! 🚀**
