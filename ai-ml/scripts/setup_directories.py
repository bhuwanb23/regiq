#!/usr/bin/env python3
"""
REGIQ AI/ML Directory Structure Setup Script
Creates all required directories for the AI/ML project.
"""

import os
from pathlib import Path
from typing import List

def create_directory_structure():
    """Create the complete directory structure for REGIQ AI/ML project."""
    
    # Base directory
    base_dir = Path(".")
    
    # Directory structure
    directories = [
        # Data directories
        "data",
        "data/raw",
        "data/processed",
        "data/models",
        "data/storage",
        "data/storage/models",
        "data/storage/datasets",
        "data/storage/reports",
        "data/storage/backups",
        "data/storage/uploads",
        "data/chroma_db",
        "data/faiss_index",
        
        # Service directories
        "services",
        "services/regulatory_intelligence",
        "services/regulatory_intelligence/scrapers",
        "services/regulatory_intelligence/nlp",
        "services/regulatory_intelligence/llm",
        "services/regulatory_intelligence/rag",
        
        "services/bias_analysis",
        "services/bias_analysis/metrics",
        "services/bias_analysis/explainability",
        "services/bias_analysis/mitigation",
        "services/bias_analysis/visualization",
        
        "services/risk_simulator",
        "services/risk_simulator/models",
        "services/risk_simulator/regulations",
        "services/risk_simulator/simulation",
        "services/risk_simulator/visualization",
        
        "services/report_generator",
        "services/report_generator/explainers",
        "services/report_generator/narrative",
        "services/report_generator/visualization",
        "services/report_generator/output",
        
        # Model directories
        "models",
        "models/nlp",
        "models/fairness",
        "models/simulation",
        
        # Notebook directories
        "notebooks",
        "notebooks/exploratory",
        "notebooks/experiments",
        "notebooks/demos",
        
        # Test directories
        "tests",
        "tests/unit",
        "tests/integration",
        "tests/performance",
        
        # Script directories
        "scripts",
        "scripts/data_pipeline",
        "scripts/model_training",
        "scripts/deployment",
        
        # Documentation directories
        "docs",
        "docs/api",
        "docs/models",
        "docs/tutorials",
        
        # Logging directories
        "logs",
        "logs/application",
        "logs/errors",
        "logs/performance",
        "logs/audit",
        
        # Temporary directories
        "tmp",
        "tmp/uploads",
        "tmp/processing",
        "tmp/exports",
    ]
    
    print("🏗️  Creating REGIQ AI/ML Directory Structure")
    print("="*50)
    
    created_count = 0
    existing_count = 0
    
    for directory in directories:
        dir_path = base_dir / directory
        
        if dir_path.exists():
            print(f"📁 {directory:<40} - Already exists")
            existing_count += 1
        else:
            try:
                dir_path.mkdir(parents=True, exist_ok=True)
                print(f"✅ {directory:<40} - Created")
                created_count += 1
            except Exception as e:
                print(f"❌ {directory:<40} - Error: {e}")
    
    # Create .gitkeep files in empty directories
    gitkeep_dirs = [
        "data/raw",
        "data/processed", 
        "logs/application",
        "logs/errors",
        "logs/performance",
        "logs/audit",
        "tmp/uploads",
        "tmp/processing",
        "tmp/exports",
    ]
    
    print(f"\n📝 Creating .gitkeep files...")
    for directory in gitkeep_dirs:
        gitkeep_path = base_dir / directory / ".gitkeep"
        try:
            gitkeep_path.touch()
            print(f"✅ {directory}/.gitkeep - Created")
        except Exception as e:
            print(f"❌ {directory}/.gitkeep - Error: {e}")
    
    print(f"\n📊 Directory Creation Summary:")
    print(f"   Created: {created_count}")
    print(f"   Already existed: {existing_count}")
    print(f"   Total: {len(directories)}")
    
    return created_count, existing_count

def create_init_files():
    """Create __init__.py files for Python packages."""
    
    init_files = [
        "services/__init__.py",
        "services/regulatory_intelligence/__init__.py",
        "services/regulatory_intelligence/scrapers/__init__.py",
        "services/regulatory_intelligence/nlp/__init__.py",
        "services/regulatory_intelligence/llm/__init__.py",
        "services/regulatory_intelligence/rag/__init__.py",
        
        "services/bias_analysis/__init__.py",
        "services/bias_analysis/metrics/__init__.py",
        "services/bias_analysis/explainability/__init__.py",
        "services/bias_analysis/mitigation/__init__.py",
        "services/bias_analysis/visualization/__init__.py",
        
        "services/risk_simulator/__init__.py",
        "services/risk_simulator/models/__init__.py",
        "services/risk_simulator/regulations/__init__.py",
        "services/risk_simulator/simulation/__init__.py",
        "services/risk_simulator/visualization/__init__.py",
        
        "services/report_generator/__init__.py",
        "services/report_generator/explainers/__init__.py",
        "services/report_generator/narrative/__init__.py",
        "services/report_generator/visualization/__init__.py",
        "services/report_generator/output/__init__.py",
        
        "models/__init__.py",
        "models/nlp/__init__.py",
        "models/fairness/__init__.py",
        "models/simulation/__init__.py",
        
        "tests/__init__.py",
        "tests/unit/__init__.py",
        "tests/integration/__init__.py",
        "tests/performance/__init__.py",
        
        "scripts/__init__.py",
        "scripts/data_pipeline/__init__.py",
        "scripts/model_training/__init__.py",
        "scripts/deployment/__init__.py",
    ]
    
    print(f"\n🐍 Creating Python __init__.py files...")
    created_init = 0
    
    for init_file in init_files:
        init_path = Path(init_file)
        try:
            if not init_path.exists():
                init_path.touch()
                print(f"✅ {init_file} - Created")
                created_init += 1
            else:
                print(f"📁 {init_file} - Already exists")
        except Exception as e:
            print(f"❌ {init_file} - Error: {e}")
    
    print(f"   Created {created_init} __init__.py files")
    return created_init

def main():
    """Main setup function."""
    print("🚀 REGIQ AI/ML Project Setup")
    print("="*60)
    
    # Create directory structure
    created, existing = create_directory_structure()
    
    # Create __init__.py files
    init_count = create_init_files()
    
    print(f"\n🎉 Setup Complete!")
    print(f"   📁 Directories: {created} created, {existing} existing")
    print(f"   🐍 Python packages: {init_count} __init__.py files created")
    print(f"\n✨ Your REGIQ AI/ML project structure is ready!")
    print(f"   Next: Run 'python scripts/verify_installation.py' to check dependencies")

if __name__ == "__main__":
    main()
