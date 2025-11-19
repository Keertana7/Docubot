#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Simple test script to call answer_query() with Gemini API
"""
import os
import sys
from backend.query_engine import answer_query

def main():
    print("=" * 60)
    print("Testing answer_query() with Gemini API")
    print("=" * 60)
    
    # Check if API key is set
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key:
        print(f"[OK] GEMINI_API_KEY is set (length: {len(api_key)} chars)")
    else:
        print("[FAIL] GEMINI_API_KEY is NOT set")
        return
    
    print("\n" + "-" * 60)
    
    # Test queries
    test_queries = [
        ("What is ceph?", "beginner"),
        ("Explain about ceph cluster", "intermediate"),
        ("How does rgw work?", "expert"),
    ]
    
    for query, level in test_queries:
        print(f"\nQuery: {query}")
        print(f"Level: {level}")
        print("-" * 60)
        try:
            answer = answer_query(query, level=level, top_k=3)
            print(f"[OK] Answer:\n{answer}\n")
        except Exception as e:
            print(f"[ERROR] {e}\n")

if __name__ == "__main__":
    main()

