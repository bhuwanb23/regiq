#!/usr/bin/env python3
"""
REGIQ AI/ML - Sample Report Generator
Generate sample reports to demonstrate the system capabilities.
"""

import json
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from services.report_generator.templates.base.base_template import ReportData
from services.report_generator.templates.executive.executive_template import ExecutiveTemplate
from services.report_generator.templates.technical.technical_template import TechnicalTemplate
from services.report_generator.templates.regulatory.regulatory_template import RegulatoryTemplate
from services.report_generator.templates.utils.data_formatter import DataFormatter


def load_sample_data():
    """Load sample data from fixtures."""
    sample_data_path = Path(__file__).parent / "fixtures" / "sample_data"
    
    with open(sample_data_path / "regulatory_intelligence_output.json") as f:
        regulatory_data = json.load(f)
    
    with open(sample_data_path / "bias_analysis_output.json") as f:
        bias_data = json.load(f)
    
    with open(sample_data_path / "risk_simulation_output.json") as f:
        risk_data = json.load(f)
    
    return regulatory_data, bias_data, risk_data


def generate_executive_report():
    """Generate executive report sample."""
    print("🔵 Generating Executive Report...")
    
    regulatory_data, bias_data, risk_data = load_sample_data()
    
    # Create report data
    report_data = ReportData(
        regulatory_data=regulatory_data,
        bias_analysis_data=bias_data,
        risk_simulation_data=risk_data
    )
    
    # Generate report
    template = ExecutiveTemplate()
    
    # HTML Report
    html_report = template.generate_report(report_data, "html")
    html_output_path = Path(__file__).parent / "generated_outputs" / "executive_report.html"
    html_output_path.parent.mkdir(exist_ok=True)
    
    with open(html_output_path, 'w', encoding='utf-8') as f:
        f.write(html_report["content"])
    
    # JSON Report
    json_report = template.generate_report(report_data, "json")
    json_output_path = Path(__file__).parent / "generated_outputs" / "executive_report.json"
    
    with open(json_output_path, 'w', encoding='utf-8') as f:
        json.dump(json_report, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Executive Report generated:")
    print(f"   📄 HTML: {html_output_path}")
    print(f"   📊 JSON: {json_output_path}")
    
    return html_report, json_report


def generate_technical_report():
    """Generate technical report sample."""
    print("\n🔵 Generating Technical Report...")
    
    regulatory_data, bias_data, risk_data = load_sample_data()
    
    # Create report data
    report_data = ReportData(
        bias_analysis_data=bias_data,
        risk_simulation_data=risk_data
    )
    
    # Generate report
    template = TechnicalTemplate()
    
    # HTML Report
    html_report = template.generate_report(report_data, "html")
    html_output_path = Path(__file__).parent / "generated_outputs" / "technical_report.html"
    
    with open(html_output_path, 'w', encoding='utf-8') as f:
        f.write(html_report["content"])
    
    # JSON Report
    json_report = template.generate_report(report_data, "json")
    json_output_path = Path(__file__).parent / "generated_outputs" / "technical_report.json"
    
    with open(json_output_path, 'w', encoding='utf-8') as f:
        json.dump(json_report, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Technical Report generated:")
    print(f"   📄 HTML: {html_output_path}")
    print(f"   📊 JSON: {json_output_path}")
    
    return html_report, json_report


def generate_regulatory_report():
    """Generate regulatory report sample."""
    print("\n🔵 Generating Regulatory Report...")
    
    regulatory_data, bias_data, risk_data = load_sample_data()
    
    # Create report data
    report_data = ReportData(
        regulatory_data=regulatory_data,
        bias_analysis_data=bias_data
    )
    
    # Generate report
    template = RegulatoryTemplate()
    
    # HTML Report
    html_report = template.generate_report(report_data, "html")
    html_output_path = Path(__file__).parent / "generated_outputs" / "regulatory_report.html"
    
    with open(html_output_path, 'w', encoding='utf-8') as f:
        f.write(html_report["content"])
    
    # JSON Report
    json_report = template.generate_report(report_data, "json")
    json_output_path = Path(__file__).parent / "generated_outputs" / "regulatory_report.json"
    
    with open(json_output_path, 'w', encoding='utf-8') as f:
        json.dump(json_report, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Regulatory Report generated:")
    print(f"   📄 HTML: {html_output_path}")
    print(f"   📊 JSON: {json_output_path}")
    
    return html_report, json_report


def demonstrate_json_structure():
    """Demonstrate JSON structure for frontend integration."""
    print("\n🔵 Demonstrating JSON Structure for Frontend...")
    
    regulatory_data, bias_data, risk_data = load_sample_data()
    
    # Use data formatter to show structured data
    formatter = DataFormatter()
    report_data = formatter.create_report_data(
        regulatory_data=regulatory_data,
        bias_data=bias_data,
        risk_data=risk_data
    )
    
    # Generate executive report JSON
    template = ExecutiveTemplate()
    json_report = template.generate_report(report_data, "json")
    
    # Extract key data for frontend
    frontend_data = {
        "report_metadata": json_report["template_metadata"],
        "sections": [],
        "charts_data": {},
        "metrics": {}
    }
    
    # Process sections for frontend
    for section in json_report["content"]["sections"]:
        section_data = {
            "id": section["section_id"],
            "title": section["title"],
            "type": section["section_type"],
            "order": section["order"]
        }
        
        # Extract metrics for charts
        if section["section_type"] == "metrics":
            # This would contain data for charts/graphs
            frontend_data["charts_data"][section["section_id"]] = {
                "type": "metrics_dashboard",
                "data": "Parsed from section content"
            }
        
        frontend_data["sections"].append(section_data)
    
    # Save frontend-ready JSON
    frontend_output_path = Path(__file__).parent / "generated_outputs" / "frontend_data.json"
    with open(frontend_output_path, 'w', encoding='utf-8') as f:
        json.dump(frontend_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Frontend JSON structure saved to: {frontend_output_path}")
    
    return frontend_data


def main():
    """Generate all sample reports."""
    print("🚀 REGIQ AI/ML - Sample Report Generation")
    print("=" * 50)
    
    try:
        # Generate all report types
        exec_html, exec_json = generate_executive_report()
        tech_html, tech_json = generate_technical_report()
        reg_html, reg_json = generate_regulatory_report()
        
        # Demonstrate frontend integration
        frontend_data = demonstrate_json_structure()
        
        print("\n" + "=" * 50)
        print("🎉 ALL SAMPLE REPORTS GENERATED SUCCESSFULLY!")
        print("\n📁 Check the generated_outputs folder for:")
        print("   📄 HTML files (for preview/PDF generation)")
        print("   📊 JSON files (for frontend integration)")
        print("   🔧 Frontend-ready data structure")
        
        print("\n💡 Usage:")
        print("   • HTML files: Open in browser for preview")
        print("   • JSON files: Send to frontend for charts/graphs")
        print("   • Frontend data: Ready for React/Vue components")
        
    except Exception as e:
        print(f"❌ Error generating reports: {str(e)}")
        raise


if __name__ == "__main__":
    main()
