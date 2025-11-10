from sentence_transformers import SentenceTransformer
from tqdm import tqdm
import json

# 1️⃣ Load preprocessed dataset
with open("ceph_docs_preprocessed.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"Loaded {len(data)} chunks.")

# 2️⃣ Load free open-source embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# 3️⃣ Generate embeddings
embedded_data = []
for item in tqdm(data, desc="Generating embeddings"):
    embedding = model.encode(item["content"]).tolist()
    embedded_data.append({
        "file": item["file"],
        "chunk_id": item["chunk_id"],
        "embedding": embedding,
        "word_count": item["word_count"],
        "content": item["content"]
    })

# 4️⃣ Save embeddings
with open("ceph_embeddings_free.json", "w", encoding="utf-8") as f:
    json.dump(embedded_data, f, indent=2, ensure_ascii=False)

print("✅ Free embeddings saved as ceph_embeddings_free.json")
