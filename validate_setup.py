#!/usr/bin/env python
"""Validation script to check if the setup is correct."""
import sys
import os
from pathlib import Path

def check_python_version():
    """Check Python version."""
    version = sys.version_info
    if version >= (3, 13):
        print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"❌ Python version {version.major}.{version.minor}.{version.micro} is too old")
        print("   Required: Python 3.13+")
        return False

def check_env_file():
    """Check if .env file exists."""
    if Path(".env").exists():
        print("✅ .env file exists")
        
        # Check for OpenAI key
        with open(".env", "r") as f:
            content = f.read()
            if "OPENAI_API_KEY" in content and "your_openai_api_key_here" not in content:
                print("✅ OpenAI API key is configured")
            else:
                print("⚠️  OpenAI API key not configured in .env")
        return True
    else:
        print("❌ .env file not found")
        print("   Run: cp .env.example .env")
        return False

def check_directories():
    """Check if required directories exist."""
    dirs = ["backend", "frontend", "uploads"]
    all_exist = True
    for dir_name in dirs:
        if Path(dir_name).exists():
            print(f"✅ Directory exists: {dir_name}/")
        else:
            print(f"❌ Directory missing: {dir_name}/")
            all_exist = False
    return all_exist

def check_dependencies():
    """Check if key dependencies are installed."""
    dependencies = [
        ("fastapi", "FastAPI"),
        ("streamlit", "Streamlit"),
        ("qdrant_client", "Qdrant Client"),
        ("openai", "OpenAI"),
        ("inngest", "Inngest"),
    ]
    
    all_installed = True
    for module, name in dependencies:
        try:
            __import__(module)
            print(f"✅ {name} installed")
        except ImportError:
            print(f"❌ {name} not installed")
            all_installed = False
    
    return all_installed

def check_docker():
    """Check if Docker is running."""
    import subprocess
    try:
        result = subprocess.run(
            ["docker", "ps"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print("✅ Docker is running")
            
            # Check for Qdrant
            if "qdrant" in result.stdout:
                print("✅ Qdrant container is running")
            else:
                print("⚠️  Qdrant container not found")
                print("   Run: docker-compose up -d")
            return True
        else:
            print("❌ Docker is not running")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("⚠️  Could not check Docker status")
        return False

def main():
    """Run all validation checks."""
    print("=" * 50)
    print("Event-Driven RAG Document Assistant - Setup Validation")
    print("=" * 50)
    print()
    
    checks = [
        ("Python Version", check_python_version()),
        ("Environment File", check_env_file()),
        ("Directories", check_directories()),
        ("Dependencies", check_dependencies()),
        ("Docker", check_docker()),
    ]
    
    print()
    print("=" * 50)
    print("Summary")
    print("=" * 50)
    
    passed = sum(1 for _, status in checks if status)
    total = len(checks)
    
    for name, status in checks:
        status_str = "✅ PASS" if status else "❌ FAIL"
        print(f"{status_str} - {name}")
    
    print()
    print(f"Result: {passed}/{total} checks passed")
    
    if passed == total:
        print()
        print("🎉 Setup is complete! You're ready to start.")
        print()
        print("Next steps:")
        print("1. Start backend: ./start_backend.sh")
        print("2. Start frontend: ./start_frontend.sh")
        print("3. Open: http://localhost:8501")
        return 0
    else:
        print()
        print("⚠️  Some checks failed. Please fix the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
