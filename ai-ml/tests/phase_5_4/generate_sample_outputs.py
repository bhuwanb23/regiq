#!/usr/bin/env python3
"""
REGIQ AI/ML - Phase 5.4 Sample Output Generator
Generate sample outputs for all supported formats.
"""

import json
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from services.report_generator.templates.base.base_template import ReportData
from services.report_generator.templates.executive.executive_template import ExecutiveTemplate


def generate_sample_outputs():
    """Generate sample outputs in all supported formats."""
    print("Generating sample outputs...")
    
    # Initialize template
    template = ExecutiveTemplate()
    
    # Load sample data
    sample_data_path = Path(__file__).parent / "fixtures" / "sample_data"
    
    with open(sample_data_path / "regulatory_intelligence_output.json") as f:
        regulatory_data = json.load(f)
    
    with open(sample_data_path / "bias_analysis_output.json") as f:
        bias_data = json.load(f)
    
    with open(sample_data_path / "risk_simulation_output.json") as f:
        risk_data = json.load(f)
    
    sample_data = ReportData(
        regulatory_data=regulatory_data,
        bias_analysis_data=bias_data,
        risk_simulation_data=risk_data
    )
    
    # Output directory
    output_dir = Path(__file__).parent / "generated_outputs"
    output_dir.mkdir(exist_ok=True)
    
    # Generate outputs in all formats
    formats = ["html", "pdf", "json", "csv", "xlsx"]
    
    for fmt in formats:
        try:
            print(f"Generating {fmt.upper()} output...")
            output_path = output_dir / f"executive_report_sample.{fmt}"
            saved_path = template.save_report(sample_data, str(output_path), fmt)
            print(f"  ✓ Saved to: {saved_path}")
        except Exception as e:
            print(f"  ✗ Failed to generate {fmt.upper()}: {e}")
    
    print("\nSample outputs generated successfully!")


if __name__ == "__main__":
    generate_sample_outputs()