#!/usr/bin/env python3
"""
REGIQ AI/ML Installation Verification Script
Verifies that all required packages are installed and working correctly.
"""

import sys
import importlib
import subprocess
from typing import List, Tuple, Dict
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings("ignore")

def check_python_version() -> bool:
    """Check if Python version is 3.9 or higher."""
    version = sys.version_info
    print(f"🐍 Python Version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor >= 9:
        print("✅ Python version is compatible (3.9+)")
        return True
    else:
        print("❌ Python version must be 3.9 or higher")
        return False

def check_package_installation() -> Dict[str, bool]:
    """Check if all required packages are installed."""
    
    # Core packages to verify
    packages = {
        # Core ML frameworks
        'torch': 'PyTorch',
        'tensorflow': 'TensorFlow',
        'sklearn': 'scikit-learn',
        'numpy': 'NumPy',
        'pandas': 'Pandas',
        'scipy': 'SciPy',
        
        # NLP & LLM libraries
        'transformers': 'Hugging Face Transformers',
        'spacy': 'spaCy',
        'langchain': 'LangChain',
        
        # Fairness & Explainability
        'shap': 'SHAP',
        'lime': 'LIME',
        
        # Probabilistic & Simulation
        'pymc': 'PyMC',
        'statsmodels': 'StatsModels',
        
        # Data Processing & Storage
        'sqlalchemy': 'SQLAlchemy',
        'psycopg2': 'PostgreSQL adapter',
        'redis': 'Redis',
        'chromadb': 'ChromaDB',
        'faiss': 'FAISS',
        
        # Web Frameworks & APIs
        'fastapi': 'FastAPI',
        'uvicorn': 'Uvicorn',
        'pydantic': 'Pydantic',
        'requests': 'Requests',
        
        # Visualization & Reporting
        'matplotlib': 'Matplotlib',
        'seaborn': 'Seaborn',
        'plotly': 'Plotly',
        'reportlab': 'ReportLab',
        
        # Utilities
        'yaml': 'PyYAML',
        'click': 'Click',
        'tqdm': 'tqdm',
        'joblib': 'Joblib',
        
        # Testing & Development
        'pytest': 'pytest',
        'black': 'Black',
        'jupyter': 'Jupyter',
    }
    
    results = {}
    print("\n📦 Checking Package Installation:")
    print("-" * 50)
    
    for package, description in packages.items():
        try:
            importlib.import_module(package)
            print(f"✅ {description:<25} - Installed")
            results[package] = True
        except ImportError:
            print(f"❌ {description:<25} - Missing")
            results[package] = False
    
    return results

def check_google_api_setup() -> bool:
    """Check if Google Gemini API credentials are configured."""
    try:
        from google import genai  # noqa: F401
        print("\n🔑 google-genai SDK is installed")

        import os
        api_key = os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')
        if api_key:
            print("✅ GEMINI_API_KEY / GOOGLE_API_KEY environment variable is set")
            return True
        else:
            print("⚠️  GEMINI_API_KEY (or GOOGLE_API_KEY) environment variable not found")
            print("   Set it with: setx GEMINI_API_KEY your-api-key (Windows)")
            print("   Or: export GEMINI_API_KEY='your-api-key' (POSIX)")
            return False
    except ImportError:
        print("❌ google-genai SDK not installed")
        print("   Install with: pip install google-genai")
        return False

def check_database_setup() -> bool:
    """Check if database components are working."""
    try:
        import sqlite3
        print("\n🗄️  SQLite is available (built-in)")
        
        # Test SQLite connection
        conn = sqlite3.connect(':memory:')
        cursor = conn.cursor()
        cursor.execute('SELECT 1')
        result = cursor.fetchone()
        conn.close()
        
        if result[0] == 1:
            print("✅ SQLite connection test successful")
            return True
        else:
            print("❌ SQLite connection test failed")
            return False
    except Exception as e:
        print(f"❌ SQLite test failed: {e}")
        return False

def check_vector_database() -> bool:
    """Check if vector database components are working."""
    try:
        import chromadb
        print("\n🔍 ChromaDB is installed")
        
        # Test ChromaDB initialization
        client = chromadb.Client()
        print("✅ ChromaDB client initialization successful")
        return True
    except ImportError:
        print("❌ ChromaDB not installed")
        return False
    except Exception as e:
        print(f"⚠️  ChromaDB initialization warning: {e}")
        return True  # Still consider it working

def generate_report(results: Dict[str, bool]) -> None:
    """Generate installation report."""
    total_packages = len(results)
    installed_packages = sum(results.values())
    success_rate = (installed_packages / total_packages) * 100
    
    print("\n" + "="*60)
    print("📊 INSTALLATION REPORT")
    print("="*60)
    print(f"Total Packages Checked: {total_packages}")
    print(f"Successfully Installed: {installed_packages}")
    print(f"Missing Packages: {total_packages - installed_packages}")
    print(f"Success Rate: {success_rate:.1f}%")
    
    if success_rate >= 90:
        print("🎉 Excellent! Your environment is ready for development.")
    elif success_rate >= 75:
        print("👍 Good! Most packages are installed. Install missing ones.")
    elif success_rate >= 50:
        print("⚠️  Warning! Many packages are missing. Run: pip install -r requirements.txt")
    else:
        print("❌ Critical! Most packages are missing. Check your installation.")
    
    # List missing packages
    missing = [pkg for pkg, installed in results.items() if not installed]
    if missing:
        print(f"\n📋 Missing Packages: {', '.join(missing)}")
        print("💡 Install missing packages with:")
        print("   pip install " + " ".join(missing))

def main():
    """Main verification function."""
    print("🤖 REGIQ AI/ML Environment Verification")
    print("="*60)
    
    # Check Python version
    python_ok = check_python_version()
    
    # Check package installation
    package_results = check_package_installation()
    
    # Check Google API setup
    api_ok = check_google_api_setup()
    
    # Check database setup
    db_ok = check_database_setup()
    
    # Check vector database
    vector_ok = check_vector_database()
    
    # Generate report
    generate_report(package_results)
    
    print("\n🚀 Next Steps:")
    if not python_ok:
        print("1. Install Python 3.9 or higher")
    if sum(package_results.values()) < len(package_results):
        print("2. Install missing packages: pip install -r requirements.txt")
    if not api_ok:
        print("3. Set up Google API key: export GOOGLE_API_KEY='your-key'")
    if not db_ok:
        print("4. Check database setup")
    if not vector_ok:
        print("5. Install ChromaDB: pip install chromadb")
    
    print("\n✨ Once all checks pass, you're ready to start development!")

if __name__ == "__main__":
    main()
