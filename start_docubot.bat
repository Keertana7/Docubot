@echo off
REM Docubot Startup Script for Windows
REM This script sets up the environment and starts the Flask server

echo.
echo ==========================================
echo    DOCUBOT - Ceph Documentation Chatbot
echo ==========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.11+ or add it to your PATH
    pause
    exit /b 1
)

REM Get the API key from user if not set
if not defined GEMINI_API_KEY (
    echo.
    echo IMPORTANT: You need a Gemini API key to run Docubot
    echo Get one at: https://ai.google.dev/
    echo.
    set /p API_KEY="Enter your GEMINI_API_KEY: "
    if not defined API_KEY (
        echo ERROR: API key is required
        pause
        exit /b 1
    )
    set GEMINI_API_KEY=%API_KEY%
) else (
    echo Using GEMINI_API_KEY from environment
)

REM Check if Flask is installed
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo.
    echo Installing required packages...
    pip install flask google-genai faiss-cpu sentence-transformers numpy
    if errorlevel 1 (
        echo ERROR: Failed to install packages
        pause
        exit /b 1
    )
)

REM Check if data files exist
if not exist "data\data_prepocessing\ceph_faiss.index" (
    echo ERROR: FAISS index not found at data\data_prepocessing\ceph_faiss.index
    echo Please ensure all data files are present
    pause
    exit /b 1
)

echo.
echo ==========================================
echo    Starting Docubot Flask Server...
echo ==========================================
echo.
echo Opening http://localhost:5000 in your browser...
echo.
echo Press CTRL+C to stop the server
echo.

REM Start Flask server
python app.py

pause
