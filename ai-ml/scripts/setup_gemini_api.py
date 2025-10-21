#!/usr/bin/env python3
"""
REGIQ AI/ML Gemini API Complete Setup Script
Handles installation, configuration, and testing of Gemini API.
"""

import subprocess
import sys
import os
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are available."""
    print("📦 Checking required dependencies...")
    
    required_packages = ['requests', 'pyyaml']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} - Available")
        except ImportError:
            print(f"❌ {package} - Missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n📋 Install missing packages:")
        print(f"   pip install {' '.join(missing_packages)}")
        return False
    
    print("✅ All required dependencies are available")
    return True

def create_config_file():
    """Create api_keys.yaml from template."""
    print("\n📁 Setting up configuration file...")
    
    source_path = Path("config/api_keys.yaml.example")
    target_path = Path("config/api_keys.yaml")
    
    if target_path.exists():
        print(f"✅ {target_path} already exists")
        return True
    
    if not source_path.exists():
        print(f"❌ Template file {source_path} not found")
        return False
    
    try:
        with open(source_path, 'r') as src, open(target_path, 'w') as dst:
            content = src.read()
            dst.write(content)
        
        print(f"✅ Created {target_path} from template")
        return True
    except Exception as e:
        print(f"❌ Failed to create config file: {e}")
        return False

def setup_api_key():
    """Guide user through API key setup."""
    print("\n🔑 API Key Setup...")
    
    # Check if already configured
    if os.getenv('GEMINI_API_KEY'):
        print("✅ GEMINI_API_KEY environment variable already set")
        return True
    
    config_path = Path("config/api_keys.yaml")
    if config_path.exists():
        with open(config_path, 'r') as f:
            content = f.read()
            if 'YOUR_GOOGLE_GEMINI_API_KEY_HERE' not in content:
                print("✅ API key appears to be configured in config file")
                return True
    
    print("⚠️  API key not configured yet")
    print("\n📋 To get your Gemini API key:")
    print("   1. Go to: https://aistudio.google.com/app/apikey")
    print("   2. Click 'Create API Key'")
    print("   3. Copy the generated key")
    print("\n📋 To configure the API key, choose one option:")
    print("   Option A - Environment Variable (Recommended):")
    print("      set GEMINI_API_KEY=your-actual-api-key")
    print("   Option B - Config File:")
    print("      Edit config/api_keys.yaml and replace YOUR_GOOGLE_GEMINI_API_KEY_HERE")
    
    return False

def test_api_setup():
    """Test the API setup."""
    print("\n🧪 Testing API setup...")
    
    try:
        # Import and test
        sys.path.append(str(Path(__file__).parent.parent))
        from config.gemini_config import GeminiAPIManager
        
        api_manager = GeminiAPIManager()
        success = api_manager.test_connection()
        
        if success:
            print("✅ API test successful!")
            return True
        else:
            print("❌ API test failed")
            return False
            
    except Exception as e:
        print(f"❌ API test error: {e}")
        return False

def main():
    """Main setup function."""
    print("🚀 REGIQ AI/ML Gemini API Complete Setup")
    print("="*60)
    
    steps = [
        ("Check Dependencies", check_dependencies),
        ("Create Configuration File", create_config_file),
        ("Setup API Key", setup_api_key),
        ("Test API Setup", test_api_setup),
    ]
    
    success_count = 0
    
    for step_name, step_func in steps:
        print(f"\n{'='*60}")
        print(f"🎯 {step_name}")
        print(f"{'='*60}")
        
        try:
            success = step_func()
            if success:
                success_count += 1
                print(f"✅ {step_name} - Completed")
            else:
                print(f"⚠️  {step_name} - Needs attention")
                
                if step_name == "Setup API Key":
                    print("   This is expected if you haven't set up your API key yet.")
                    print("   Please follow the instructions above, then run:")
                    print("   python scripts/test_gemini_api.py")
                elif step_name == "Test API Setup":
                    print("   This is expected if API key is not configured yet.")
                    break
        except Exception as e:
            print(f"❌ {step_name} - Error: {e}")
    
    # Final summary
    print(f"\n{'='*60}")
    print(f"📊 SETUP SUMMARY")
    print(f"{'='*60}")
    print(f"Completed Steps: {success_count}/{len(steps)}")
    
    if success_count >= 3:
        print("\n🎉 Gemini API setup is complete!")
        print("\n🚀 Next Steps:")
        print("   1. Make sure your API key is configured")
        print("   2. Run: python scripts/test_gemini_api.py")
        print("   3. Start using Gemini API in your code!")
        
    elif success_count >= 2:
        print("\n👍 Setup mostly complete!")
        print("\n📋 Remaining tasks:")
        print("   1. Configure your API key (see instructions above)")
        print("   2. Test the setup: python scripts/test_gemini_api.py")
        
    else:
        print("\n❌ Setup incomplete. Please resolve the issues above.")
    
    print(f"\n📚 Documentation:")
    print(f"   • Gemini API Docs: https://ai.google.dev/gemini-api/docs")
    print(f"   • Get API Key: https://aistudio.google.com/app/apikey")
    print(f"   • Configuration: config/gemini_config.py")

if __name__ == "__main__":
    main()
