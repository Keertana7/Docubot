"""
Query engine for Docubot
 - Loads FAISS index and metadata
 - Embeds queries with SentenceTransformer
 - Retrieves top-k chunks from FAISS
 - Calls Google Gemini via either:
     - modern client: from google import genai (preferred)
     - legacy client: import google.generativeai as genai (fallback)

This file uses a robust approach to support both client libraries and multiple model names.
"""

import os
import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Try to import both possible Gemini clients. We prefer from google import genai (google-genai),
# but keep a fallback to the older google.generativeai package if available.
try:
    from google import genai as genai_client  # type: ignore
except Exception:
    genai_client = None

try:
    import google.generativeai as genai_legacy  # type: ignore
except Exception:
    genai_legacy = None

# Data paths
ROOT = os.path.dirname(__file__)
DATA_FOLDER = os.path.join(ROOT, "..", "data")
DATA_PREPROCESS_FOLDER = os.path.join(ROOT, "..", "data", "data_prepocessing")

# Attempt to load FAISS index and metadata
index = None
metadata_list = []

ceph_index_path = os.path.join(DATA_PREPROCESS_FOLDER, "ceph_faiss.index")
ceph_metadata_path = os.path.join(DATA_PREPROCESS_FOLDER, "ceph_metadata.json")
main_index_path = os.path.join(DATA_FOLDER, "index.faiss")
main_chunks_path = os.path.join(DATA_FOLDER, "chunks.json")

# Try preprocessed folder first
if os.path.exists(ceph_index_path):
    try:
        index = faiss.read_index(ceph_index_path)
        if os.path.exists(ceph_metadata_path):
            with open(ceph_metadata_path, "r", encoding="utf-8") as f:
                metadata_list = json.load(f)
            print("[INFO] Loaded metadata from ceph_metadata.json")
        else:
            # create simple metadata placeholders if missing
            metadata_list = [{"content": f"Chunk {i}", "chunk_id": i} for i in range(index.ntotal)]
            print("[WARNING] ceph_metadata.json not found; created placeholders")
        print("[INFO] Loaded FAISS index from preprocessing folder (ceph_faiss.index)")
    except Exception as e:
        print(f"[WARNING] Failed to load preprocessed index: {e}")

# Fallback to main data folder
if index is None:
    try:
        index = faiss.read_index(main_index_path)
        with open(main_chunks_path, "r", encoding="utf-8") as f:
            metadata_list = json.load(f)
        print("[INFO] Loaded FAISS index from main data folder (index.faiss)")
    except Exception as e:
        raise RuntimeError(f"Failed to load FAISS index and metadata: {e}")

# Build id -> chunk text mapping
id2chunk = {}
for i, item in enumerate(metadata_list):
    if isinstance(item, dict):
        text = item.get("text") or item.get("content") or ""
        id2chunk[str(i)] = text
    else:
        id2chunk[str(i)] = str(item)

# Embedding model
embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Configure legacy client (if present) with API key if provided (best-effort)

if genai_legacy is not None and GEMINI_API_KEY:
    try:
        genai_legacy.configure(api_key=GEMINI_API_KEY)
    except Exception:
        pass
if genai_client is not None and GEMINI_API_KEY:
    try:
        genai_client.configure(api_key=GEMINI_API_KEY)
    except Exception:
        pass


def _generate_with_modern_client(prompt: str):
    """Use from google import genai client if available."""
    if genai_client is None:
        raise RuntimeError("Modern genai client not available")

    client = genai_client.Client()

    # Candidate models to try in order
    candidates = ["gemini-2.5-flash", "gemini-1.5-flash", "gemini-pro"]
    last_exc = None
    for candidate in candidates:
        try:
            resp = client.models.generate_content(model=candidate, contents=prompt)
            # response may expose .text or .content
            return getattr(resp, "text", None) or getattr(resp, "content", None) or str(resp)
        except Exception as e:
            last_exc = e
            continue

    # Try listing models and use first available
    try:
        model_list = client.models.list()
        names = []
        for m in model_list:
            name = getattr(m, "name", None) or (m if isinstance(m, str) else None)
            if name:
                names.append(name)
        if names:
            resp = client.models.generate_content(model=names[0], contents=prompt)
            return getattr(resp, "text", None) or getattr(resp, "content", None) or str(resp)
    except Exception as e:
        last_exc = e

    raise RuntimeError(f"Modern genai client failed to generate response. Last error: {last_exc}")


def _generate_with_legacy_client(prompt: str):
    """Use older google.generativeai style client if available."""
    if genai_legacy is None:
        raise RuntimeError("Legacy genai client not available")

    # Try some common model names
    for candidate in ("gemini-pro", "gemini-1.5-flash", "gemini-2.5-flash"):
        try:
            model = genai_legacy.GenerativeModel(candidate)
            resp = model.generate_content(prompt)
            return getattr(resp, "text", None) or str(resp)
        except Exception:
            continue

    # As fallback, try listing models if available
    try:
        models = genai_legacy.list_models()
        available = [getattr(m, "name", None) for m in models]
        available = [n for n in available if n]
        if available:
            model = genai_legacy.GenerativeModel(available[0].split("/")[-1])
            resp = model.generate_content(prompt)
            return getattr(resp, "text", None) or str(resp)
    except Exception as e:
        raise RuntimeError(f"Legacy client failed to generate response: {e}")

    raise RuntimeError("No compatible generative model available via legacy client")


def answer_query(query: str, level: str = "beginner", top_k: int = 3) -> str:
    """Answer a user query using FAISS retrieval + Gemini generation.

    Args:
        query: user question
        level: beginner|intermediate|expert
        top_k: number of retrieved chunks to include
    Returns:
        Generated text (string)
    """
    # Embed & search
    query_embedding = embedder.encode([query])
    D, I = index.search(np.array(query_embedding).astype("float32"), top_k)

    # Get top chunks
    top_chunks = [id2chunk.get(str(idx), "") for idx in I[0]]

    # Format context
    chunk_text = ""
    for i, chunk in enumerate(top_chunks, start=1):
        cleaned = chunk.replace(":term:", "")
        chunk_text += f"{i}. {cleaned}\n"

    # Level instruction
    lvl = (level or "").lower()
    if lvl.startswith("b"):
        instruction = "Explain this like a human teacher to a beginner, in simple language, with examples if possible."
    elif lvl.startswith("i"):
        instruction = "Explain this clearly to an intermediate user with relevant details."
    else:
        instruction = "Explain this to an expert user in technical detail."

    prompt = f"{instruction}\n\nInformation:\n{chunk_text}\nQuestion: {query}"

    # Try modern client first, then legacy client
    last_error = None
    try:
        return _generate_with_modern_client(prompt)
    except Exception as e:
        last_error = e
        try:
            return _generate_with_legacy_client(prompt)
        except Exception as e2:
            # Surface combined error for debugging
            raise RuntimeError(f"Generation failed. Modern client error: {last_error}; Legacy client error: {e2}")

    raise RuntimeError("No compatible generative model available")