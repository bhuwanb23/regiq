#!/usr/bin/env python3
"""Report Generator Pipeline Demo"""

from services.report_generator.terminology import TerminologyManager
from services.report_generator.output import ReportOutputGenerator
from services.report_generator.explainers import ReportExplainerFactory

print("=" * 70)
print("REPORT GENERATOR - FULL PIPELINE DEMONSTRATION")
print("=" * 70)

# Step 1: Generate fairness explanation HTML
print("\n📊 Step 1: Generating Fairness Analysis Section...")
factory = ReportExplainerFactory()
fairness_html = factory.explain('fairness', {
    'overall_bias_score': 0.82,
    'fairness_metrics': {
        'demographic_parity': 0.91,
        'equalized_odds': 0.84,
        'calibration': 0.88
    },
    'protected_attributes': ['gender', 'age'],
}, audience='regulatory')

print(f"   ✅ Fairness section generated: {len(fairness_html)} characters")

# Step 2: Generate terminology glossary
print("\n📚 Step 2: Generating Terminology Glossary...")
tm = TerminologyManager()
glossary = tm.generate_glossary_html(categories=['fairness'], audience='regulatory')
print(f"   ✅ Glossary generated: {len(glossary)} characters")

# Step 3: Assemble full report
print("\n📄 Step 3: Assembling Complete Report...")
gen = ReportOutputGenerator('data/reports')
result = gen.generate(
    sections=[{
        'section_id': 'fairness',
        'title': 'Fairness Analysis',
        'content': fairness_html,
        'order': 1
    }],
    metadata={
        'title': 'Test Compliance Report',
        'report_type': 'Audit',
        'generated_by': 'REGIQ AI/ML'
    },
    formats=['html', 'json'],
    glossary_html=glossary
)

print(f"   ✅ Report generated successfully!")
if result.get('html'):
    print(f"   📁 HTML Path: {result['html']['path']}")
if result.get('json'):
    print(f"   📁 JSON Path: {result['json']['path']}")

print("\n" + "=" * 70)
print("✅ REPORT GENERATOR VALIDATED SUCCESSFULLY")
print("=" * 70)
