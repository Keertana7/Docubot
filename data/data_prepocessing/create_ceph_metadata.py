#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Generate ceph_metadata.json from available source data.
This script creates proper metadata for the FAISS index to enable:
1. Source attribution (which file/section)
2. Better retrieval and ranking
3. User-facing context and audit trails

Tries multiple sources in order:
1. ceph_docs_preprocessed.json (if it exists from preprocessing pipeline)
2. chunks.json from main data folder (fallback)
3. Creates structured entries from available data
"""
import json
import os
import sys

def generate_from_preprocessed():
    """Load metadata from ceph_docs_preprocessed.json if available."""
    path = os.path.join(os.path.dirname(__file__), "ceph_docs_preprocessed.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        print(f"[OK] Loaded {len(data)} chunks from ceph_docs_preprocessed.json")
        return data
    return None

def generate_from_chunks_json():
    """Load metadata from chunks.json in main data folder."""
    path = os.path.join(os.path.dirname(__file__), "..", "chunks.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        print(f"[OK] Loaded {len(data)} chunks from chunks.json")
        
        # Transform chunks.json format to standardized metadata format
        metadata = []
        for i, item in enumerate(data):
            meta = {
                "file": item.get("metadata", {}).get("doc_name", "unknown.txt"),
                "section": item.get("metadata", {}).get("section", "General"),
                "chunk_id": i + 1,
                "content": item.get("text", ""),
                "word_count": len(item.get("text", "").split())
            }
            metadata.append(meta)
        return metadata
    return None

def main():
    print("=" * 70)
    print("Generating ceph_metadata.json")
    print("=" * 70)
    
    metadata = None
    
    # Try to load from preprocessed data first
    metadata = generate_from_preprocessed()
    
    # If not available, try chunks.json
    if metadata is None:
        metadata = generate_from_chunks_json()
    
    if metadata is None:
        print("[ERROR] No source data found!")
        print("Please run the preprocessing pipeline first:")
        print("  python embedding_generation_code.py")
        sys.exit(1)
    
    # Save metadata
    output_path = os.path.join(os.path.dirname(__file__), "ceph_metadata.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    print(f"\n[OK] Metadata saved to {output_path}")
    print(f"Total chunks: {len(metadata)}")
    print(f"\nExample metadata entry:")
    print(json.dumps(metadata[0], indent=2))
    print(f"\nMetadata structure includes:")
    print("  - file: Source documentation file")
    print("  - section: Section title within the file")
    print("  - chunk_id: Sequential chunk ID within file")
    print("  - content: The actual text chunk")
    print("  - word_count: Number of words in chunk")
    print("\nThis metadata enables:")
    print("  ✓ Source attribution for answers")
    print("  ✓ Better retrieval ranking")
    print("  ✓ Audit trails and fact-checking")
    print("  ✓ Improved user experience (show where info came from)")

if __name__ == "__main__":
    main()
