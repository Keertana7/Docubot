#!/usr/bin/env python
"""
Generate ceph_metadata.json from ceph_docs_preprocessed.json for use with ceph_faiss.index
This metadata maps FAISS index positions to document chunks.
"""
import json
import os

# Load the preprocessed documents
preprocessed_file = os.path.join(os.path.dirname(__file__), "ceph_docs_preprocessed.json")

if not os.path.exists(preprocessed_file):
    print(f"ERROR: {preprocessed_file} not found.")
    print("Please run embedding_generation_code.py or preprocess_ceph_docs.py first.")
    exit(1)

with open(preprocessed_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# The metadata list should match the order of embeddings in ceph_faiss.index
# Extract relevant fields for each chunk
metadata = []
for item in data:
    metadata.append({
        "file": item.get("file", ""),
        "section": item.get("section", ""),
        "chunk_id": item.get("chunk_id", 0),
        "content": item.get("content", ""),
        "word_count": item.get("word_count", 0)
    })

# Save metadata
output_file = os.path.join(os.path.dirname(__file__), "ceph_metadata.json")
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(metadata, f, indent=2, ensure_ascii=False)

print(f"✅ Metadata file created: {output_file}")
print(f"Total chunks: {len(metadata)}")
print(f"Example metadata entry:\n{json.dumps(metadata[0], indent=2)}")
