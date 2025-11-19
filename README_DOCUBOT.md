# 🤖 Docubot - Ceph Documentation Chatbot

## ✅ Status: Ready to Use!

Docubot is a fully functional AI-powered chatbot that answers questions about Ceph distributed storage system using Google's Gemini API and vector search technology.

---

## 🎯 What is Docubot?

Docubot combines:
- **Gemini AI** - State-of-the-art language model for intelligent responses
- **FAISS Vector Search** - Fast similarity search over 5,129 Ceph documentation chunks
- **Flask Web Server** - REST API and web interface
- **Beautiful UI** - Modern, responsive chat interface

Ask any question about Ceph, and Docubot will search relevant documentation and provide an intelligent answer tailored to your expertise level.

---

## 🚀 Quick Start

### 1️⃣ Install Dependencies (One Time)

```bash
pip install -r requirements.txt
```

Or manually:
```bash
pip install flask google-generativeai faiss-cpu sentence-transformers numpy
```

### 2️⃣ Get Gemini API Key

1. Go to: **https://ai.google.dev/**
2. Click "Get API Key"
3. Create or use existing project
4. Copy your API key

### 3️⃣ Set API Key & Run Server

**PowerShell:**
```powershell
$env:GEMINI_API_KEY = "your-api-key-here"
python app.py
```

**Command Prompt:**
```cmd
set GEMINI_API_KEY=your-api-key-here
python app.py
```

### 4️⃣ Open Browser

Visit: **http://localhost:5000**

---

## 💬 How It Works

1. **Ask a question** about Ceph
2. **Choose difficulty level** (Beginner/Intermediate/Expert)
3. **Adjust precision** with Top-K slider
4. **Get instant answer** powered by Gemini AI

Example questions:
- "What is Ceph?"
- "How does CRUSH algorithm work?"
- "Explain OSDs in Ceph"

---

## 📁 Project Structure

```
Docubot/
├── app.py                    # Flask web server (START HERE)
├── backend/
│   └── query_engine.py      # AI processing engine
├── templates/
│   └── index.html           # Web interface
├── static/
│   ├── style.css            # Styling
│   └── script.js            # Chat logic
├── data/
│   └── data_prepocessing/
│       ├── ceph_faiss.index       # Vector search index
│       └── ceph_metadata.json     # Document metadata
├── requirements.txt         # Dependencies
├── COMPLETE_GUIDE.md        # Detailed documentation
└── README.md                # This file
```

---

## 🔧 Key Features

### 🎓 Expertise Levels
- **Beginner** - Simple, jargon-free explanations
- **Intermediate** - Technical details with examples
- **Expert** - Deep technical analysis

### 🔍 Precision Control
- **Top-K Slider** - Adjust how many document chunks to use
  - Lower (1-3) = Focused answers
  - Higher (7-10) = Comprehensive answers

### ⚡ Performance
- FAISS search: <100ms
- Gemini response: 5-10 seconds
- Total: ~5-10 seconds per query

### 🎨 UI/UX
- Modern chat interface
- Real-time message updates
- Loading indicators
- Mobile-responsive design
- Keyboard shortcuts (Enter to send)

---

## 📚 Documentation

- **COMPLETE_GUIDE.md** - Full setup and troubleshooting guide
- **QUICKSTART.md** - 3-step quick start guide
- **IMPLEMENTATION_SUMMARY.md** - Technical architecture details

---

## 🐛 Troubleshooting

### "Docubot is thinking..." spins forever
- ✅ Verify you're using a **real** Gemini API key (not test key)
- ✅ Check internet connection
- ✅ Check API key is valid at https://ai.google.dev/

### Connection refused / Port 5000 error
- ✅ Ensure Flask server is running (`python app.py`)
- ✅ Use http://localhost:5000 (not https)
- ✅ Check if port 5000 is available

### Package not found errors
```bash
pip install flask google-generativeai faiss-cpu sentence-transformers numpy
```

### Still having issues?
See **COMPLETE_GUIDE.md** for detailed troubleshooting.

---

## 🔌 API Endpoints

### POST /api/chat
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query":"What is Ceph?","level":"beginner","top_k":5}'
```

### GET /api/health
```bash
curl http://localhost:5000/api/health
```

### GET /api/config
```bash
curl http://localhost:5000/api/config
```

---

## 📊 Architecture

```
Browser (http://localhost:5000)
         ↓
    Flask Web Server
         ↓
    Query Engine
    - Embed query
    - Search FAISS
    - Build context
         ↓
    Gemini API
    - Generate response
         ↓
    Response → Browser → Chat UI
```

---

## 🔐 Security

- API key stored in environment variable (not in code)
- Never commit API key to git
- Flask debug mode enabled for development
- Use production WSGI server in production (gunicorn, waitress)

---

## 📝 Example Questions

### Beginner
- What is Ceph?
- What is object storage?
- What does RADOS stand for?

### Intermediate
- How does the CRUSH algorithm work?
- What are Ceph OSDs?
- Explain Ceph's replication strategy

### Expert
- Describe CRUSH's pseudorandom function
- How does Ceph distribute data?
- Explain OSD component architecture

---

## 🎓 Learning Resources

- [Gemini API Documentation](https://ai.google.dev/docs)
- [FAISS GitHub](https://github.com/facebookresearch/faiss)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Ceph Official Docs](https://docs.ceph.com/)

---

## ✅ Installation Checklist

Before running Docubot:

- [ ] Python 3.11+ installed
- [ ] All packages installed (`pip install -r requirements.txt`)
- [ ] Gemini API key obtained (https://ai.google.dev/)
- [ ] API key set in environment variable
- [ ] Port 5000 available
- [ ] Internet connection active

Verify installation:
```bash
python check_install.py
```

---

## 🚀 Running Docubot

### Basic Usage
```powershell
$env:GEMINI_API_KEY = "your-api-key"
python app.py
# Open http://localhost:5000
```

### Custom Port
Edit `app.py` line ~105 and change port from 5000 to another value.

### Production Deployment
Use a production WSGI server:
```bash
pip install gunicorn
gunicorn app:app
```

---

## 💡 Tips

- **Faster answers**: Use Top-K 1-3
- **Better quality**: Use higher expertise levels
- **Specific answers**: Ask detailed questions with context
- **Multiple questions**: You can ask follow-up questions

---

## 📄 Files Overview

| File | Purpose |
|------|---------|
| `app.py` | Main Flask server |
| `backend/query_engine.py` | AI processing |
| `templates/index.html` | Web UI template |
| `static/script.js` | Frontend logic |
| `static/style.css` | UI styling |
| `COMPLETE_GUIDE.md` | Full documentation |
| `check_install.py` | Verify installation |

---

## 🎉 You're All Set!

Everything is installed and configured. Just:

1. Set your Gemini API key
2. Run `python app.py`
3. Visit http://localhost:5000
4. Start asking questions!

---

## 📞 Support

If you encounter issues:

1. Check **COMPLETE_GUIDE.md** for troubleshooting
2. Verify all packages are installed: `python check_install.py`
3. Check Flask terminal output for error messages
4. Verify API key is set: `Write-Host $env:GEMINI_API_KEY`

---

**Happy Chatting! 🤖💬**

For detailed information, see **COMPLETE_GUIDE.md**
