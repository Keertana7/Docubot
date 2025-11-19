# Docubot Startup Script for Windows PowerShell
# Run with: .\start_docubot.ps1

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "   DOCUBOT - Ceph Documentation Chatbot" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found. Please install Python 3.11+" -ForegroundColor Red
    Write-Host "   Visit: https://www.python.org/downloads/" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check/Set API Key
if (-not $env:GEMINI_API_KEY) {
    Write-Host ""
    Write-Host "⚠️  GEMINI_API_KEY is not set" -ForegroundColor Yellow
    Write-Host "Get your API key at: https://ai.google.dev/" -ForegroundColor Yellow
    Write-Host ""
    $apiKey = Read-Host "Enter your GEMINI_API_KEY"
    
    if (-not $apiKey) {
        Write-Host "❌ API key is required" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
    
    $env:GEMINI_API_KEY = $apiKey
    Write-Host "✅ API key set" -ForegroundColor Green
} else {
    Write-Host "✅ Using GEMINI_API_KEY from environment" -ForegroundColor Green
}

# Check Flask
Write-Host ""
Write-Host "Checking Flask installation..." -ForegroundColor Cyan
try {
    python -c "import flask" 2>&1
    Write-Host "✅ Flask is installed" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Installing Flask and dependencies..." -ForegroundColor Yellow
    pip install flask google-genai faiss-cpu sentence-transformers numpy
}

# Check data files
Write-Host ""
Write-Host "Checking data files..." -ForegroundColor Cyan
$faissPath = "data/data_prepocessing/ceph_faiss.index"
$metadataPath = "data/data_prepocessing/ceph_metadata.json"

if ((Test-Path $faissPath) -and (Test-Path $metadataPath)) {
    Write-Host "✅ FAISS index found" -ForegroundColor Green
    Write-Host "✅ Metadata found" -ForegroundColor Green
} else {
    Write-Host "❌ Data files not found" -ForegroundColor Red
    if (-not (Test-Path $faissPath)) {
        Write-Host "   Missing: $faissPath" -ForegroundColor Red
    }
    if (-not (Test-Path $metadataPath)) {
        Write-Host "   Missing: $metadataPath" -ForegroundColor Red
    }
    Read-Host "Press Enter to exit"
    exit 1
}

# All checks passed
Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "   Starting Docubot Flask Server" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "🚀 Server starting on http://localhost:5000" -ForegroundColor Green
Write-Host ""
Write-Host "Press CTRL+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Start Flask app
python app.py

# If we get here, server was stopped
Write-Host ""
Write-Host "Docubot has been stopped." -ForegroundColor Cyan
Read-Host "Press Enter to exit"
