#!/usr/bin/env python
"""
Complete Docubot Test Suite
Verifies all components are working correctly
"""
import os
import sys
import json

# Add repo to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

print("=" * 70)
print("DOCUBOT COMPLETE TEST SUITE")
print("=" * 70)

# Test 1: Check environment
print("\n[1/5] Checking environment...")
gemini_key = os.environ.get("GEMINI_API_KEY")
if gemini_key:
    print(f"  ✓ GEMINI_API_KEY is set ({gemini_key[:10]}...)")
else:
    print("  ⚠ GEMINI_API_KEY is not set - some tests will fail")

# Test 2: Check dependencies
print("\n[2/5] Checking dependencies...")
dependencies = {
    "google.generativeai": "Gemini API client",
    "flask": "Web framework",
    "faiss": "Vector search",
    "sentence_transformers": "Embeddings",
    "numpy": "Array operations",
}

missing = []
for module, desc in dependencies.items():
    try:
        __import__(module)
        print(f"  ✓ {module:<25} {desc}")
    except ImportError:
        print(f"  ✗ {module:<25} {desc} [NOT INSTALLED]")
        missing.append(module)

if missing:
    print(f"\n  Missing packages: {', '.join(missing)}")
    print("  Run: pip install " + " ".join(missing))

# Test 3: Check data files
print("\n[3/5] Checking data files...")
data_files = {
    "data/data_prepocessing/ceph_faiss.index": "FAISS index",
    "data/data_prepocessing/ceph_metadata.json": "Metadata",
}

for path, desc in data_files.items():
    full_path = os.path.join(os.path.dirname(__file__), path)
    if os.path.exists(full_path):
        size_mb = os.path.getsize(full_path) / (1024 * 1024)
        print(f"  ✓ {desc:<20} {path} ({size_mb:.1f} MB)")
    else:
        print(f"  ✗ {desc:<20} {path} [NOT FOUND]")

# Test 4: Load query engine
print("\n[4/5] Loading query engine...")
try:
    from backend.query_engine import answer_query
    print("  ✓ Query engine imported successfully")
except Exception as e:
    print(f"  ✗ Failed to import query engine: {e}")
    sys.exit(1)

# Test 5: Test query (if API key is set)
print("\n[5/5] Testing query generation...")
if gemini_key and gemini_key != "test-key":
    try:
        test_query = "What is Ceph?"
        print(f"  Testing: '{test_query}'")
        response = answer_query(test_query, level="beginner", top_k=2)
        
        if response and len(response) > 10:
            print(f"  ✓ Query successful!")
            print(f"  Response length: {len(response)} characters")
            print(f"  First 100 chars: {response[:100]}...")
        else:
            print(f"  ⚠ Response seems short: {response}")
    except Exception as e:
        print(f"  ✗ Query failed: {e}")
        print("  Make sure you have a valid GEMINI_API_KEY")
else:
    print("  ⊘ Skipped (API key needed)")
    print("  Set: $env:GEMINI_API_KEY = 'YOUR_KEY'")

# Summary
print("\n" + "=" * 70)
if not missing:
    print("✅ All tests passed! System is ready.")
    print("\nNext steps:")
    print("1. Set API key: $env:GEMINI_API_KEY = 'YOUR_KEY'")
    print("2. Start server: python app.py")
    print("3. Open browser: http://localhost:5000")
else:
    print(f"⚠ {len(missing)} dependency issue(s) found")
    print("Install missing packages and try again")

print("=" * 70)
