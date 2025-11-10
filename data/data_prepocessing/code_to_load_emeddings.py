import json
import numpy as np

with open("D:\ceph\ceph\ceph_embeddings_free.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Each entry might look like:
# { "file": "doc/architecture.rst", "chunk_id": 1, "content": "....", "embedding": [0.123, 0.456, ...] }

embeddings = [item["embedding"] for item in data]
metadata = [ {"file": item["file"], "chunk_id": item["chunk_id"], "content": item["content"]} for item in data ]

# Convert to NumPy array for FAISS
embeddings = np.array(embeddings).astype("float32")
