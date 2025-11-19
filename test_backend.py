#!/usr/bin/env python
"""
Test script to verify Docubot functionality
"""
import os
import sys
import json

# Add repo to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from backend.query_engine import answer_query

# Set test API key if not already set
if not os.environ.get("GEMINI_API_KEY"):
    print("⚠️  GEMINI_API_KEY not set. Tests will fail without it.")
    print("Set it: $env:GEMINI_API_KEY = 'YOUR_KEY'")
    sys.exit(1)

def test_query_engine():
    """Test the query engine with different expertise levels"""
    
    test_questions = [
        "What is Ceph?",
        "Explain CRUSH algorithm",
        "What are OSDs?",
    ]
    
    levels = ["beginner", "intermediate", "expert"]
    
    print("=" * 60)
    print("DOCUBOT QUERY ENGINE TEST")
    print("=" * 60)
    
    for question in test_questions:
        print(f"\n📌 Question: {question}")
        print("-" * 60)
        
        for level in levels:
            try:
                response = answer_query(question, level=level, top_k=3)
                print(f"\n  [{level.upper()}]")
                print(f"  Response length: {len(response)} chars")
                print(f"  First 100 chars: {response[:100]}...")
            except Exception as e:
                print(f"  ❌ Error at {level}: {str(e)}")
    
    print("\n" + "=" * 60)
    print("✅ Tests completed!")
    print("=" * 60)

if __name__ == "__main__":
    test_query_engine()
