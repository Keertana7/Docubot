#!/usr/bin/env python
"""
Docubot Installation Verification Script
Ensures all required packages are properly installed
"""
import sys
import subprocess

def check_package(package_name, import_name=None):
    """Check if a package is installed"""
    if import_name is None:
        import_name = package_name
    
    try:
        __import__(import_name)
        return True, None
    except ImportError as e:
        return False, str(e)

def main():
    print("\n" + "="*60)
    print("DOCUBOT - INSTALLATION VERIFICATION")
    print("="*60 + "\n")
    
    packages = [
        ("flask", "flask"),
        ("google-generativeai", "google.generativeai"),
        ("faiss-cpu", "faiss"),
        ("sentence-transformers", "sentence_transformers"),
        ("numpy", "numpy"),
    ]
    
    all_ok = True
    missing = []
    
    print("Checking required packages:\n")
    
    for package, import_name in packages:
        ok, error = check_package(package, import_name)
        status = "✅" if ok else "❌"
        print(f"{status} {package:30} ", end="")
        
        if ok:
            print("installed")
        else:
            print("NOT installed")
            all_ok = False
            missing.append(package)
    
    print("\n" + "="*60)
    
    if all_ok:
        print("✅ ALL PACKAGES INSTALLED!")
        print("\nYou can now run: python app.py")
        print("\nThen open: http://localhost:5000")
        return 0
    else:
        print("❌ MISSING PACKAGES")
        print(f"\nRun this to install missing packages:")
        print(f"  pip install {' '.join(missing)}")
        print("\nOr install all at once:")
        print("  pip install -r requirements.txt")
        return 1

if __name__ == "__main__":
    sys.exit(main())
