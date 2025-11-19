#!/usr/bin/env python
"""
Docubot Setup Verification Script
Checks all components are properly configured before running
"""
import os
import sys
import json

def check_python_version():
    """Verify Python version"""
    version = sys.version_info
    required = (3, 11)
    
    if version >= required:
        print("✅ Python version OK:", f"{version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print("❌ Python version too old. Required: 3.11+, Found:", f"{version.major}.{version.minor}")
        return False

def check_packages():
    """Verify required packages are installed"""
    packages = [
        ('flask', 'Flask'),
        ('google', 'google-genai'),
        ('faiss', 'FAISS'),
        ('sentence_transformers', 'sentence-transformers'),
        ('numpy', 'NumPy'),
    ]
    
    all_ok = True
    for module, name in packages:
        try:
            __import__(module)
            print(f"✅ {name:30} installed")
        except ImportError:
            print(f"❌ {name:30} NOT installed - run: pip install {name}")
            all_ok = False
    
    return all_ok

def check_files():
    """Verify required files exist"""
    files = [
        ('app.py', 'Flask application'),
        ('backend/query_engine.py', 'Query engine'),
        ('templates/index.html', 'HTML template'),
        ('static/style.css', 'CSS styles'),
        ('static/script.js', 'JavaScript'),
        ('data/data_prepocessing/ceph_faiss.index', 'FAISS index'),
        ('data/data_prepocessing/ceph_metadata.json', 'Metadata'),
    ]
    
    all_ok = True
    for filepath, description in files:
        full_path = os.path.join(os.path.dirname(__file__), filepath)
        if os.path.exists(full_path):
            size = os.path.getsize(full_path)
            if size > 1024*1024:  # > 1MB
                size_str = f"{size / (1024*1024):.1f}MB"
            elif size > 1024:  # > 1KB
                size_str = f"{size / 1024:.1f}KB"
            else:
                size_str = f"{size}B"
            print(f"✅ {description:30} ({size_str})")
        else:
            print(f"❌ {description:30} NOT FOUND - {filepath}")
            all_ok = False
    
    return all_ok

def check_api_key():
    """Verify Gemini API key is set"""
    if os.environ.get('GEMINI_API_KEY'):
        key = os.environ.get('GEMINI_API_KEY')
        masked = key[:5] + '*' * (len(key) - 10) + key[-5:] if len(key) > 10 else '***'
        print(f"✅ GEMINI_API_KEY is set ({masked})")
        return True
    else:
        print("❌ GEMINI_API_KEY NOT SET")
        print("   Set with: $env:GEMINI_API_KEY = 'your-key'")
        print("   Or: set GEMINI_API_KEY=your-key (cmd.exe)")
        return False

def test_imports():
    """Test importing main modules"""
    try:
        from backend.query_engine import answer_query
        print("✅ backend.query_engine imported successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to import backend.query_engine: {e}")
        return False

def main():
    """Run all checks"""
    print("\n" + "="*60)
    print("DOCUBOT SETUP VERIFICATION")
    print("="*60 + "\n")
    
    checks = [
        ("Python Version", check_python_version),
        ("Required Packages", check_packages),
        ("Project Files", check_files),
        ("API Key", check_api_key),
        ("Module Imports", test_imports),
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n[{name}]")
        print("-" * 40)
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ Error during check: {e}")
            results.append((name, False))
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    all_passed = True
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status:10} {name}")
        if not result:
            all_passed = False
    
    print("="*60)
    
    if all_passed:
        print("\n✅ All checks passed! You can start the server:")
        print("   python app.py")
        print("\nThen open: http://localhost:5000")
        return 0
    else:
        print("\n❌ Some checks failed. Fix the issues above first.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
