#!/usr/bin/env python3
"""
Install Google Gemini API SDK
"""

import subprocess
import sys

def install_google_genai():
    """Install the official Google GenAI SDK."""
    print("📦 Installing Google GenAI SDK...")
    
    try:
        # Install the official Google GenAI package
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-q", "-U", "google-genai"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Google GenAI SDK installed successfully")
            return True
        else:
            print(f"❌ Installation failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Installation error: {e}")
        return False

if __name__ == "__main__":
    success = install_google_genai()
    if success:
        print("\n🚀 Ready to configure Gemini API!")
        print("   Next: Get your API key from https://aistudio.google.com/app/apikey")
    else:
        print("\n❌ Installation failed. Please try manually:")
        print("   pip install -q -U google-genai")
