"""
Flask web server for Docubot
Provides REST API endpoints and serves the web UI
"""

import os
from flask import Flask, render_template, request, jsonify
from backend.query_engine import answer_query

app = Flask(__name__)

# API key from environment
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")


@app.route("/")
def index():
    """Serve the main web UI."""
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    """Handle chat queries and return generated responses."""
    try:
        data = request.get_json()
        query = data.get("query", "").strip()
        level = data.get("level", "beginner").lower()
        top_k = data.get("top_k", 3)

        if not query:
            return jsonify({"error": "Empty query"}), 400

        # Validate level
        if level not in ("beginner", "intermediate", "expert"):
            level = "beginner"

        # Ensure top_k is reasonable
        top_k = max(1, min(int(top_k or 3), 10))

        # Generate answer using the query engine
        try:
            response = answer_query(query, level=level, top_k=top_k)
        except Exception as gen_error:
            # If generation fails (e.g., no API key, model not available), provide informative response
            error_str = str(gen_error)
            if "Modern genai client" in error_str or "Legacy genai client" in error_str:
                response = (
                    f"[⚠️ API Configuration Issue]\n\n"
                    f"The Gemini API client is not properly configured.\n\n"
                    f"To use Docubot:\n"
                    f"1. Get a free Gemini API key from https://makersuite.google.com/app/apikey\n"
                    f"2. Set it in your environment: export GEMINI_API_KEY='your-api-key'\n"
                    f"3. Restart the server\n\n"
                    f"Technical details: {error_str}"
                )
            else:
                response = f"Generation error: {error_str}"

        return jsonify({"response": response, "level": level, "top_k": top_k}), 200

    except Exception as e:
        error_msg = f"Error processing query: {str(e)}"
        return jsonify({"error": error_msg}), 500


@app.route("/api/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({"status": "ok", "service": "docubot-api"}), 200


@app.route("/api/config", methods=["GET"])
def config():
    """Return basic configuration info."""
    return jsonify({
        "api_key_set": bool(GEMINI_API_KEY),
        "service": "Docubot Query Engine"
    }), 200


if __name__ == "__main__":
    # Start Flask server on localhost:5000
    print("\n" + "="*60)
    print("🚀 Docubot Flask Server Starting")
    print("="*60)
    print("📍 Open your browser and go to: http://localhost:5000")
    print("="*60 + "\n")
    
    app.run(debug=True, host="127.0.0.1", port=5000)