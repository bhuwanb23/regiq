#!/usr/bin/env python3
"""
REGIQ AI/ML - Enhanced Report Generator with Narratives
Generate sample reports with intelligent narratives to demonstrate Phase 5.2 capabilities.
"""

import json
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from services.report_generator.templates.base.base_template import ReportData
from services.report_generator.templates.executive.executive_template import ExecutiveTemplate
from services.report_generator.narrative.narrative_generator import NarrativeGenerator


def load_sample_data():
    """Load sample data from Phase 5.1 fixtures."""
    sample_data_path = Path(__file__).parent.parent / "phase_5_1" / "fixtures" / "sample_data"
    
    with open(sample_data_path / "regulatory_intelligence_output.json") as f:
        regulatory_data = json.load(f)
    
    with open(sample_data_path / "bias_analysis_output.json") as f:
        bias_data = json.load(f)
    
    with open(sample_data_path / "risk_simulation_output.json") as f:
        risk_data = json.load(f)
    
    return regulatory_data, bias_data, risk_data


def generate_enhanced_executive_report():
    """Generate enhanced executive report with narratives."""
    print("🔵 Generating Enhanced Executive Report with Narratives...")
    
    regulatory_data, bias_data, risk_data = load_sample_data()
    
    # Create report data
    report_data = ReportData(
        regulatory_data=regulatory_data,
        bias_analysis_data=bias_data,
        risk_simulation_data=risk_data
    )
    
    # Generate enhanced report
    template = ExecutiveTemplate()
    
    try:
        # Generate enhanced report with narratives
        enhanced_report = template.generate_enhanced_report(report_data, "json")
        
        # Save enhanced report
        output_path = Path(__file__).parent / "generated_outputs" / "enhanced_executive_report.json"
        output_path.parent.mkdir(exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(enhanced_report, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Enhanced Executive Report generated: {output_path}")
        
        # Generate narrative-only version for easy reading
        if enhanced_report.get("enhanced") and "enhanced_sections" in enhanced_report:
            narrative_report = {
                "report_title": "Executive Report - Narrative Version",
                "generation_timestamp": enhanced_report.get("generation_timestamp"),
                "narrative_stats": enhanced_report.get("narrative_stats", {}),
                "sections": []
            }
            
            for section in enhanced_report["enhanced_sections"]:
                if section.get("narrative"):
                    narrative_report["sections"].append({
                        "section_id": section["section_id"],
                        "title": section["title"],
                        "narrative": section["narrative"],
                        "confidence_score": section["confidence_score"]
                    })
            
            # Save narrative-only version
            narrative_path = Path(__file__).parent / "generated_outputs" / "executive_narratives.json"
            with open(narrative_path, 'w', encoding='utf-8') as f:
                json.dump(narrative_report, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Executive Narratives extracted: {narrative_path}")
        
        return enhanced_report
        
    except Exception as e:
        print(f"❌ Enhanced report generation failed: {str(e)}")
        # Fallback to regular report
        regular_report = template.generate_report(report_data, "json")
        regular_report["enhancement_error"] = str(e)
        return regular_report


def demonstrate_narrative_generation():
    """Demonstrate standalone narrative generation."""
    print("\n🔵 Demonstrating Standalone Narrative Generation...")
    
    regulatory_data, bias_data, risk_data = load_sample_data()
    
    # Initialize narrative generator
    generator = NarrativeGenerator()
    
    # Test different audience types
    audiences = ["executive", "technical", "regulatory"]
    section_types = ["summary", "metrics", "recommendations"]
    
    narrative_examples = {}
    
    for audience in audiences:
        narrative_examples[audience] = {}
        
        for section_type in section_types:
            try:
                # Prepare section data
                section_data = {
                    "regulatory_data": regulatory_data,
                    "bias_analysis_data": bias_data,
                    "risk_simulation_data": risk_data
                }
                
                # Generate narrative
                narrative_section = generator.generate_narrative_for_section(
                    section_data=section_data,
                    section_id=f"{audience}_{section_type}",
                    section_title=f"{section_type.title()} for {audience.title()}",
                    audience_type=audience,
                    section_type=section_type
                )
                
                narrative_examples[audience][section_type] = {
                    "narrative": narrative_section.narrative,
                    "confidence_score": narrative_section.confidence_score,
                    "processing_time": narrative_section.processing_time,
                    "metadata": narrative_section.metadata
                }
                
                print(f"✅ Generated {audience} {section_type} narrative "
                      f"(confidence: {narrative_section.confidence_score:.3f})")
                
            except Exception as e:
                print(f"❌ Failed to generate {audience} {section_type}: {str(e)}")
                narrative_examples[audience][section_type] = {
                    "error": str(e),
                    "narrative": None
                }
    
    # Save narrative examples
    examples_path = Path(__file__).parent / "generated_outputs" / "narrative_examples.json"
    with open(examples_path, 'w', encoding='utf-8') as f:
        json.dump(narrative_examples, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Narrative examples saved: {examples_path}")
    
    return narrative_examples


def test_narrative_quality():
    """Test narrative quality and validation."""
    print("\n🔵 Testing Narrative Quality and Validation...")
    
    generator = NarrativeGenerator()
    
    # Test service validation
    is_valid, errors = generator.validate_service()
    
    print(f"📊 Service Validation: {'✅ PASSED' if is_valid else '❌ FAILED'}")
    if errors:
        for error in errors:
            print(f"   ⚠️ {error}")
    
    # Test generation statistics
    stats = generator.get_generation_stats()
    
    print(f"📊 Generation Statistics:")
    print(f"   🤖 LLM Available: {stats['llm_service'].get('model_available', False)}")
    print(f"   📝 Templates: {stats['prompt_engine'].get('total_templates', 0)}")
    print(f"   🎯 Audience Types: {len(stats['prompt_engine'].get('audience_types', []))}")
    print(f"   📋 Section Types: {len(stats['prompt_engine'].get('section_types', []))}")
    
    # Save validation results
    validation_results = {
        "service_validation": {
            "is_valid": is_valid,
            "errors": errors
        },
        "generation_stats": stats,
        "test_timestamp": "2024-01-01T00:00:00"  # Would be actual timestamp
    }
    
    validation_path = Path(__file__).parent / "generated_outputs" / "validation_results.json"
    with open(validation_path, 'w', encoding='utf-8') as f:
        json.dump(validation_results, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Validation results saved: {validation_path}")
    
    return validation_results


def create_narrative_comparison():
    """Create comparison between structured data and narratives."""
    print("\n🔵 Creating Narrative Comparison...")
    
    regulatory_data, bias_data, risk_data = load_sample_data()
    generator = NarrativeGenerator()
    
    # Sample structured data
    structured_data = {
        "compliance_score": 0.78,
        "bias_score": 0.734,
        "risk_probability": 0.287,
        "flagged_attributes": ["gender", "age_group"],
        "high_priority_deadlines": 1
    }
    
    # Generate narratives for different audiences
    comparison = {
        "structured_data": structured_data,
        "narratives": {}
    }
    
    for audience in ["executive", "technical", "regulatory"]:
        try:
            narrative_section = generator.generate_narrative_for_section(
                section_data={
                    "regulatory_data": regulatory_data,
                    "bias_analysis_data": bias_data,
                    "risk_simulation_data": risk_data
                },
                section_id="comparison_section",
                section_title="Data Analysis Summary",
                audience_type=audience,
                section_type="summary"
            )
            
            comparison["narratives"][audience] = {
                "narrative": narrative_section.narrative,
                "confidence": narrative_section.confidence_score,
                "word_count": len(narrative_section.narrative.split()),
                "reading_level": "appropriate"  # Would be calculated
            }
            
        except Exception as e:
            comparison["narratives"][audience] = {
                "error": str(e),
                "narrative": None
            }
    
    # Save comparison
    comparison_path = Path(__file__).parent / "generated_outputs" / "narrative_comparison.json"
    with open(comparison_path, 'w', encoding='utf-8') as f:
        json.dump(comparison, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Narrative comparison saved: {comparison_path}")
    
    return comparison


def main():
    """Generate all enhanced reports and demonstrations."""
    print("🚀 REGIQ AI/ML - Phase 5.2 Enhanced Report Generation")
    print("=" * 60)
    
    try:
        # Generate enhanced executive report
        enhanced_report = generate_enhanced_executive_report()
        
        # Demonstrate narrative generation
        narrative_examples = demonstrate_narrative_generation()
        
        # Test narrative quality
        validation_results = test_narrative_quality()
        
        # Create narrative comparison
        comparison = create_narrative_comparison()
        
        print("\n" + "=" * 60)
        print("🎉 ALL PHASE 5.2 DEMONSTRATIONS COMPLETED!")
        print("\n📁 Check the generated_outputs folder for:")
        print("   📊 Enhanced executive report with narratives")
        print("   📝 Extracted narrative examples")
        print("   🔍 Narrative quality validation results")
        print("   📋 Structured data vs narrative comparison")
        
        print("\n💡 Phase 5.2 Features Demonstrated:")
        print("   🤖 LLM-powered narrative generation")
        print("   🎯 Audience-specific language adaptation")
        print("   📈 Context-aware insight generation")
        print("   ✅ Quality validation and optimization")
        print("   🔗 Seamless integration with Phase 5.1 templates")
        
        # Summary statistics
        if enhanced_report.get("enhanced"):
            narrative_stats = enhanced_report.get("narrative_stats", {})
            print(f"\n📊 Generation Statistics:")
            print(f"   📝 Sections Enhanced: {narrative_stats.get('sections_with_narratives', 0)}")
            print(f"   🎯 Average Confidence: {narrative_stats.get('average_confidence', 0.0):.3f}")
        
    except Exception as e:
        print(f"❌ Error in demonstration: {str(e)}")
        raise


if __name__ == "__main__":
    main()
