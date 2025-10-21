#!/usr/bin/env python3
"""
Install Testing Dependencies for REGIQ AI/ML
Installs pytest and related testing packages.
"""

import subprocess
import sys

def install_testing_packages():
    """Install testing packages."""
    packages = [
        "pytest",
        "pytest-cov", 
        "pytest-asyncio",
        "pytest-mock",
        "psutil"
    ]
    
    print("📦 Installing Testing Dependencies")
    print("="*50)
    
    for package in packages:
        print(f"\n📥 Installing {package}...")
        try:
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", package
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ {package} installed successfully")
            else:
                print(f"❌ Failed to install {package}: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Error installing {package}: {e}")
            return False
    
    print(f"\n🎉 All testing dependencies installed!")
    print(f"\n🧪 You can now run:")
    print(f"   python run_tests.py --suite quick")
    print(f"   pytest tests/unit/ -v")
    
    return True

def main():
    """Main installation function."""
    print("🚀 REGIQ AI/ML Testing Dependencies Installer")
    print("="*60)
    
    success = install_testing_packages()
    
    if success:
        print("\n✅ Installation complete!")
    else:
        print("\n❌ Installation failed!")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
