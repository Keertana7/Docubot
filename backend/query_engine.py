# backend/query_engine.py
import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Load FAISS index & data
# backend/query_engine.py
import os

# Correct path
DATA_FOLDER = os.path.join(os.path.dirname(__file__), "../data/")  # points to Docubot/data/



index = faiss.read_index(os.path.join(DATA_FOLDER, "index.faiss"))
embeddings = np.load(DATA_FOLDER + "chunks_embeddings.npy")
with open(DATA_FOLDER + "chunks.json", "r") as f:
    chunks_list = json.load(f)

# Map index → text
id2chunk = {str(i): chunk["text"] for i, chunk in enumerate(chunks_list)}


# Embedding model for queries
embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Summarizer model (FLAN-T5)
tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")

def answer_query(query, level="beginner", top_k=3):
    # Embed the query
    query_embedding = embedder.encode([query])
    # Search FAISS
    D, I = index.search(query_embedding.astype("float32"), top_k)

    # Collect top chunks from FAISS search
    top_chunks = [id2chunk[str(i)] for i in I[0]]

    # Format chunks nicely
    chunk_text = ""
    for i, chunk in enumerate(top_chunks, start=1):
        cleaned = chunk.replace(":term:", "")  # remove glossary artifacts
        chunk_text += f"{i}. {cleaned}\n"

    # Level-specific instruction
    if level.lower().startswith("b"):
        instruction = "Explain this like a human teacher to a beginner, in simple language, with examples if possible."
    elif level.lower().startswith("i"):
        instruction = "Explain this clearly to an intermediate user with relevant details."
    else:
        instruction = "Explain this to an expert user in technical detail."

    # Full prompt
    prompt = f"{instruction}\n\nInformation:\n{chunk_text}\nQuestion: {query}"

    # Generate answer
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True)
    
    outputs = model.generate(
    **inputs,
    max_new_tokens=400,
    num_beams=3,
    do_sample=True,
    temperature=0.7,
    top_p=0.9
    )

    return tokenizer.decode(outputs[0], skip_special_tokens=True)