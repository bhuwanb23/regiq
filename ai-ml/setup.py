#!/usr/bin/env python3
"""
REGIQ AI/ML Complete Setup Script
Runs all setup tasks for Phase 1: Project Setup & Infrastructure
"""

import sys
import subprocess
import os
from pathlib import Path

def run_setup_step(script_name: str, description: str) -> bool:
    """Run a setup script and return success status."""
    print(f"\n{'='*60}")
    print(f"🚀 {description}")
    print(f"{'='*60}")
    
    try:
        # Run the script
        result = subprocess.run([sys.executable, f"scripts/{script_name}"], 
                              capture_output=False, 
                              text=True)
        
        if result.returncode == 0:
            print(f"✅ {description} - Completed successfully")
            return True
        else:
            print(f"❌ {description} - Failed with return code {result.returncode}")
            return False
            
    except Exception as e:
        print(f"❌ {description} - Error: {e}")
        return False

def check_python_version() -> bool:
    """Check if Python version is compatible."""
    version = sys.version_info
    print(f"🐍 Python Version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor >= 9:
        print("✅ Python version is compatible (3.9+)")
        return True
    else:
        print("❌ Python version must be 3.9 or higher")
        print("   Please install Python 3.9+ from https://python.org")
        return False

def check_virtual_environment() -> bool:
    """Check if running in virtual environment."""
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    
    if in_venv:
        print("✅ Running in virtual environment")
        return True
    else:
        print("⚠️  Not running in virtual environment")
        print("   Recommended: Create and activate virtual environment")
        print("   python -m venv venv")
        print("   venv\\Scripts\\activate  # Windows")
        return False

def main():
    """Main setup function."""
    print("🤖 REGIQ AI/ML Complete Setup")
    print("Phase 1: Project Setup & Infrastructure")
    print("="*60)
    
    # Check prerequisites
    print("🔍 Checking Prerequisites...")
    
    python_ok = check_python_version()
    if not python_ok:
        print("\n❌ Setup cannot continue without Python 3.9+")
        return False
    
    venv_ok = check_virtual_environment()
    if not venv_ok:
        response = input("\nContinue without virtual environment? (y/N): ")
        if response.lower() != 'y':
            print("Setup cancelled. Please create and activate virtual environment first.")
            return False
    
    # Setup steps
    setup_steps = [
        ("setup_directories.py", "Directory Structure Setup"),
        ("setup_database.py", "Database Setup"),
        ("verify_installation.py", "Installation Verification"),
    ]
    
    success_count = 0
    total_steps = len(setup_steps)
    
    print(f"\n🎯 Running {total_steps} setup steps...")
    
    for script, description in setup_steps:
        success = run_setup_step(script, description)
        if success:
            success_count += 1
        else:
            print(f"\n⚠️  Setup step failed: {description}")
            response = input("Continue with remaining steps? (y/N): ")
            if response.lower() != 'y':
                break
    
    # Final report
    print(f"\n{'='*60}")
    print(f"📊 SETUP SUMMARY")
    print(f"{'='*60}")
    print(f"Completed Steps: {success_count}/{total_steps}")
    print(f"Success Rate: {(success_count/total_steps)*100:.1f}%")
    
    if success_count == total_steps:
        print(f"\n🎉 Setup Complete! All steps successful.")
        print(f"\n✨ Your REGIQ AI/ML environment is ready!")
        print(f"\n🚀 Next Steps:")
        print(f"   1. Install dependencies: pip install -r requirements.txt")
        print(f"   2. Set up Google API key: export GOOGLE_API_KEY='your-key'")
        print(f"   3. Start development with Phase 2: Regulatory Intelligence")
        
    elif success_count >= total_steps * 0.8:
        print(f"\n👍 Setup Mostly Complete! Some steps may need attention.")
        print(f"\n⚠️  Please review any failed steps above.")
        
    else:
        print(f"\n❌ Setup Incomplete. Multiple steps failed.")
        print(f"\n🔧 Please resolve the issues and run setup again.")
    
    print(f"\n📋 Manual Steps Still Required:")
    print(f"   • Create virtual environment (if not done)")
    print(f"   • Install requirements: pip install -r requirements.txt")
    print(f"   • Configure Google API key")
    print(f"   • Review configuration files in config/")
    
    return success_count == total_steps

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
