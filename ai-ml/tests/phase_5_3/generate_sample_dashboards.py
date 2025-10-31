#!/usr/bin/env python3
"""
REGIQ AI/ML - Sample Dashboard Generator
Generate sample dashboards and visualizations to demonstrate Phase 5.3 capabilities.
"""

import json
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from services.report_generator.visualization.visualization_generator import (
    VisualizationGenerator, VisualizationRequest
)
from services.report_generator.visualization.chart_engine import ChartEngine, ChartConfig, ChartType
from services.report_generator.visualization.data_binder import DataBinder
from services.report_generator.visualization.export_engine import ExportEngine, ExportConfig


def load_sample_data():
    """Load sample data from Phase 5.1 fixtures."""
    sample_data_path = Path(__file__).parent.parent / "phase_5_1" / "fixtures" / "sample_data"
    
    with open(sample_data_path / "regulatory_intelligence_output.json") as f:
        regulatory_data = json.load(f)
    
    with open(sample_data_path / "bias_analysis_output.json") as f:
        bias_data = json.load(f)
    
    with open(sample_data_path / "risk_simulation_output.json") as f:
        risk_data = json.load(f)
    
    return {
        "regulatory_data": regulatory_data,
        "bias_analysis_data": bias_data,
        "risk_simulation_data": risk_data
    }


def generate_executive_dashboard():
    """Generate executive dashboard."""
    print("🔵 Generating Executive Dashboard...")
    
    source_data = load_sample_data()
    generator = VisualizationGenerator()
    
    request = VisualizationRequest(
        request_id="exec_dashboard_demo",
        visualization_type="dashboard",
        source_data=source_data,
        config={"dashboard_type": "executive_dashboard"}
    )
    
    dashboard = generator.generate_visualization(request)
    
    # Save dashboard
    output_path = Path(__file__).parent / "generated_outputs" / "executive_dashboard.json"
    output_path.parent.mkdir(exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(dashboard, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Executive Dashboard generated: {output_path}")
    print(f"   📊 Charts: {len(dashboard.get('charts', []))}")
    print(f"   📐 Layout: {dashboard['layout']['grid']['columns']}x{dashboard['layout']['grid']['rows']}")
    
    return dashboard


def generate_technical_dashboard():
    """Generate technical dashboard."""
    print("\n🔵 Generating Technical Dashboard...")
    
    source_data = load_sample_data()
    generator = VisualizationGenerator()
    
    request = VisualizationRequest(
        request_id="tech_dashboard_demo",
        visualization_type="dashboard",
        source_data=source_data,
        config={"dashboard_type": "technical_dashboard"}
    )
    
    dashboard = generator.generate_visualization(request)
    
    # Save dashboard
    output_path = Path(__file__).parent / "generated_outputs" / "technical_dashboard.json"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(dashboard, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Technical Dashboard generated: {output_path}")
    print(f"   📊 Charts: {len(dashboard.get('charts', []))}")
    
    return dashboard


def generate_regulatory_dashboard():
    """Generate regulatory dashboard."""
    print("\n🔵 Generating Regulatory Dashboard...")
    
    source_data = load_sample_data()
    generator = VisualizationGenerator()
    
    request = VisualizationRequest(
        request_id="reg_dashboard_demo",
        visualization_type="dashboard",
        source_data=source_data,
        config={"dashboard_type": "regulatory_dashboard"}
    )
    
    dashboard = generator.generate_visualization(request)
    
    # Save dashboard
    output_path = Path(__file__).parent / "generated_outputs" / "regulatory_dashboard.json"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(dashboard, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Regulatory Dashboard generated: {output_path}")
    print(f"   📊 Charts: {len(dashboard.get('charts', []))}")
    
    return dashboard


def generate_individual_charts():
    """Generate individual chart examples."""
    print("\n🔵 Generating Individual Chart Examples...")
    
    source_data = load_sample_data()
    generator = VisualizationGenerator()
    charts = {}
    
    # Compliance Gauge
    gauge_request = VisualizationRequest(
        request_id="compliance_gauge_demo",
        visualization_type="single_chart",
        source_data=source_data,
        config={
            "chart_type": "gauge",
            "chart_id": "compliance_gauge",
            "title": "Compliance Score",
            "data": {"value": 0.78, "max_value": 1.0, "target": 0.9}
        }
    )
    
    charts["compliance_gauge"] = generator.generate_visualization(gauge_request)
    
    # Risk Matrix
    matrix_request = VisualizationRequest(
        request_id="risk_matrix_demo",
        visualization_type="single_chart",
        source_data=source_data,
        config={
            "chart_type": "heatmap",
            "chart_id": "risk_matrix",
            "title": "Risk Assessment Matrix",
            "data": {
                "x_values": ["Low", "Medium", "High"],
                "y_values": ["Low Impact", "Medium Impact", "High Impact"],
                "z_values": [[0.1, 0.2, 0.3], [0.2, 0.4, 0.6], [0.3, 0.6, 0.9]]
            }
        }
    )
    
    charts["risk_matrix"] = generator.generate_visualization(matrix_request)
    
    # Model Performance Radar
    radar_request = VisualizationRequest(
        request_id="model_performance_demo",
        visualization_type="single_chart",
        source_data=source_data,
        config={
            "chart_type": "radar",
            "chart_id": "model_performance",
            "title": "Model Performance Metrics",
            "data": {
                "metrics": ["Accuracy", "Precision", "Recall", "F1-Score", "Fairness"],
                "values": [0.85, 0.82, 0.79, 0.81, 0.73]
            }
        }
    )
    
    charts["model_performance"] = generator.generate_visualization(radar_request)
    
    # Compliance Distribution Pie
    pie_request = VisualizationRequest(
        request_id="compliance_distribution_demo",
        visualization_type="single_chart",
        source_data=source_data,
        config={
            "chart_type": "pie",
            "chart_id": "compliance_distribution",
            "title": "Compliance Status Distribution",
            "data": {
                "categories": ["Compliant", "Non-Compliant", "Pending Review"],
                "values": [19, 6, 2]
            }
        }
    )
    
    charts["compliance_distribution"] = generator.generate_visualization(pie_request)
    
    # Save individual charts
    charts_output_path = Path(__file__).parent / "generated_outputs" / "individual_charts.json"
    
    with open(charts_output_path, 'w', encoding='utf-8') as f:
        json.dump(charts, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Individual Charts generated: {charts_output_path}")
    print(f"   📊 Chart Types: {len(charts)}")
    
    return charts


def generate_report_integration_charts():
    """Generate charts for report integration."""
    print("\n🔵 Generating Report Integration Charts...")
    
    source_data = load_sample_data()
    generator = VisualizationGenerator()
    
    request = VisualizationRequest(
        request_id="report_charts_demo",
        visualization_type="report_charts",
        source_data=source_data,
        config={}
    )
    
    report_charts = generator.generate_visualization(request)
    
    # Save report charts
    output_path = Path(__file__).parent / "generated_outputs" / "report_integration_charts.json"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report_charts, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Report Integration Charts generated: {output_path}")
    print(f"   📊 Charts: {len(report_charts.get('charts', []))}")
    
    return report_charts


def demonstrate_data_binding():
    """Demonstrate data binding capabilities."""
    print("\n🔵 Demonstrating Data Binding...")
    
    source_data = load_sample_data()
    binder = DataBinder()
    
    # Test different binding types
    binding_results = {}
    
    # Compliance bindings
    compliance_bindings = binder.create_compliance_bindings()
    compliance_data = binder.bind_data(source_data, compliance_bindings)
    binding_results["compliance"] = compliance_data
    
    # Bias analysis bindings
    bias_bindings = binder.create_bias_analysis_bindings()
    bias_data = binder.bind_data(source_data, bias_bindings)
    binding_results["bias_analysis"] = bias_data
    
    # Risk simulation bindings
    risk_bindings = binder.create_risk_simulation_bindings()
    risk_data = binder.bind_data(source_data, risk_bindings)
    binding_results["risk_simulation"] = risk_data
    
    # Complete dashboard binding
    dashboard_data = binder.bind_compliance_dashboard_data(source_data)
    binding_results["dashboard"] = dashboard_data
    
    # Save binding results
    output_path = Path(__file__).parent / "generated_outputs" / "data_binding_demo.json"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(binding_results, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Data Binding Demo generated: {output_path}")
    print(f"   🔗 Binding Types: {len(binding_results)}")
    
    return binding_results


def demonstrate_chart_engine():
    """Demonstrate chart engine capabilities."""
    print("\n🔵 Demonstrating Chart Engine...")
    
    engine = ChartEngine()
    
    # Get engine information
    engine_info = {
        "chart_types": engine.list_chart_types(),
        "templates": engine.list_templates(),
        "themes": engine.list_themes(),
        "sample_charts": {}
    }
    
    # Create sample charts of different types
    chart_configs = [
        {
            "chart_id": "sample_gauge",
            "chart_type": ChartType.GAUGE,
            "title": "Sample Gauge",
            "data": {"value": 0.75, "max_value": 1.0}
        },
        {
            "chart_id": "sample_bar",
            "chart_type": ChartType.BAR,
            "title": "Sample Bar Chart",
            "data": {"categories": ["Q1", "Q2", "Q3", "Q4"], "values": [85, 92, 78, 88]}
        },
        {
            "chart_id": "sample_line",
            "chart_type": ChartType.LINE,
            "title": "Sample Line Chart",
            "data": {"x_values": ["Jan", "Feb", "Mar", "Apr"], "y_values": [0.7, 0.75, 0.73, 0.78]}
        }
    ]
    
    for config_dict in chart_configs:
        config = ChartConfig(**config_dict)
        chart = engine.create_chart(config)
        engine_info["sample_charts"][config.chart_id] = chart
    
    # Save engine demo
    output_path = Path(__file__).parent / "generated_outputs" / "chart_engine_demo.json"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(engine_info, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Chart Engine Demo generated: {output_path}")
    print(f"   📊 Chart Types: {len(engine_info['chart_types'])}")
    print(f"   📋 Templates: {len(engine_info['templates'])}")
    print(f"   🎨 Themes: {len(engine_info['themes'])}")
    
    return engine_info


def demonstrate_export_capabilities():
    """Demonstrate export capabilities."""
    print("\n🔵 Demonstrating Export Capabilities...")
    
    engine = ChartEngine()
    exporter = ExportEngine()
    
    # Create a sample chart
    config = ChartConfig(
        chart_id="export_demo",
        chart_type=ChartType.BAR,
        title="Export Demo Chart",
        data={"categories": ["A", "B", "C"], "values": [10, 20, 15]}
    )
    
    chart = engine.create_chart(config)
    
    # Export in different formats
    export_results = {}
    
    for format_type in exporter.get_supported_formats():
        export_config = ExportConfig(
            export_id=f"demo_{format_type}",
            format=format_type,
            width=800,
            height=600
        )
        
        result = exporter.export_chart(chart, export_config)
        export_results[format_type] = result
    
    # Save export demo
    output_path = Path(__file__).parent / "generated_outputs" / "export_demo.json"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(export_results, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Export Demo generated: {output_path}")
    print(f"   📤 Export Formats: {len(export_results)}")
    
    return export_results


def create_frontend_integration_examples():
    """Create frontend integration examples."""
    print("\n🔵 Creating Frontend Integration Examples...")
    
    # Create React component configuration examples
    frontend_examples = {
        "react_dashboard": {
            "component": "ComplianceDashboard",
            "props": {
                "dashboardId": "executive_dashboard",
                "dataSource": "/api/compliance/data",
                "refreshInterval": 30000,
                "responsive": True
            },
            "charts": [
                {
                    "component": "GaugeChart",
                    "props": {
                        "chartId": "compliance_gauge",
                        "dataBinding": "$.compliance_score",
                        "thresholds": [0.6, 0.8, 0.9],
                        "colors": ["#DC3545", "#FFC107", "#28A745"]
                    }
                },
                {
                    "component": "HeatmapChart", 
                    "props": {
                        "chartId": "risk_matrix",
                        "dataBinding": "$.risk_matrix_data",
                        "interactive": True,
                        "tooltips": True
                    }
                }
            ]
        },
        "vue_dashboard": {
            "component": "compliance-dashboard",
            "data": {
                "dashboardConfig": {
                    "layout": "executive",
                    "responsive": True,
                    "charts": ["compliance_gauge", "risk_matrix", "trends"]
                }
            },
            "methods": {
                "refreshData": "async function() { ... }",
                "exportDashboard": "function(format) { ... }"
            }
        },
        "api_endpoints": {
            "/api/dashboards/executive": {
                "method": "GET",
                "response": "Executive dashboard configuration and data"
            },
            "/api/charts/{chart_id}": {
                "method": "GET", 
                "response": "Individual chart configuration and data"
            },
            "/api/export/{chart_id}/{format}": {
                "method": "POST",
                "response": "Exported chart in specified format"
            }
        }
    }
    
    # Save frontend examples
    output_path = Path(__file__).parent / "generated_outputs" / "frontend_integration.json"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(frontend_examples, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Frontend Integration Examples generated: {output_path}")
    
    return frontend_examples


def main():
    """Generate all Phase 5.3 demonstrations."""
    print("🚀 REGIQ AI/ML - Phase 5.3 Data Visualization Demonstrations")
    print("=" * 70)
    
    try:
        # Generate dashboards
        exec_dashboard = generate_executive_dashboard()
        tech_dashboard = generate_technical_dashboard()
        reg_dashboard = generate_regulatory_dashboard()
        
        # Generate individual charts
        individual_charts = generate_individual_charts()
        
        # Generate report integration charts
        report_charts = generate_report_integration_charts()
        
        # Demonstrate core capabilities
        binding_demo = demonstrate_data_binding()
        engine_demo = demonstrate_chart_engine()
        export_demo = demonstrate_export_capabilities()
        
        # Create frontend integration examples
        frontend_examples = create_frontend_integration_examples()
        
        print("\n" + "=" * 70)
        print("🎉 ALL PHASE 5.3 DEMONSTRATIONS COMPLETED!")
        print("\n📁 Check the generated_outputs folder for:")
        print("   📊 Executive, Technical, and Regulatory Dashboards")
        print("   📈 Individual Chart Examples (Gauge, Bar, Pie, Radar, Heatmap)")
        print("   🔗 Report Integration Charts")
        print("   🔧 Data Binding Demonstrations")
        print("   🎨 Chart Engine Capabilities")
        print("   📤 Export Format Examples")
        print("   💻 Frontend Integration Examples")
        
        print("\n💡 Phase 5.3 Features Demonstrated:")
        print("   📊 15+ Chart Types with Templates")
        print("   🎯 Smart Data Binding from Phase 5.1/5.2")
        print("   📐 Responsive Dashboard Layouts")
        print("   🎨 Multiple Themes (REGIQ, Dark, High Contrast)")
        print("   📤 Export Capabilities (PNG, SVG, PDF, JSON)")
        print("   💻 Frontend-Ready JSON Configurations")
        print("   🔧 Compliance-Specific Visualizations")
        
        # Summary statistics
        total_charts = (
            len(exec_dashboard.get("charts", [])) +
            len(tech_dashboard.get("charts", [])) +
            len(reg_dashboard.get("charts", [])) +
            len(individual_charts) +
            len(report_charts.get("charts", []))
        )
        
        print(f"\n📊 Generation Statistics:")
        print(f"   📈 Total Charts Generated: {total_charts}")
        print(f"   📋 Dashboard Templates: 3")
        print(f"   🎨 Chart Templates: {len(engine_demo.get('templates', []))}")
        print(f"   🔗 Data Bindings: {len(binding_demo)}")
        print(f"   📤 Export Formats: {len(export_demo)}")
        
    except Exception as e:
        print(f"❌ Error in demonstration: {str(e)}")
        raise


if __name__ == "__main__":
    main()
