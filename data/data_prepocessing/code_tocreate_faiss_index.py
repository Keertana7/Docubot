import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer

# === 1️⃣ Load FAISS index and metadata ===
index = faiss.read_index("ceph_faiss.index")

with open("ceph_metadata.json", "r", encoding="utf-8") as f:
    metadata = json.load(f)

# === 2️⃣ Load the same embedding model used earlier ===
model = SentenceTransformer("all-MiniLM-L6-v2")  # or whichever model you used

# === 3️⃣ Take user query and generate embedding ===
query_text = input("Enter your query: ")
query_vector = model.encode(query_text)

# === 4️⃣ Search in FAISS index ===
query_embedding = np.array([query_vector]).astype("float32")
k = 3  # number of top results to retrieve
distances, indices = index.search(query_embedding, k)

# === 5️⃣ Display top results ===
for i, idx in enumerate(indices[0]):
    print(f"\nResult {i+1} (distance={distances[0][i]:.4f})")
    print("📄 File:", metadata[idx]["file"])
    print("📝 Content snippet:", metadata[idx]["content"][:300], "...")
    print("-" * 90)

