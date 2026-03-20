#!/usr/bin/env python3
"""Test model loading and validation"""

from services.regulatory_intelligence.utils.model_persistence import ModelPersistence

print("\n" + "="*60)
print("REGIQ Model Validation Test")
print("="*60)

# List all models
p = ModelPersistence('models/nlp')
models = p.list_models()

print(f"\n📦 Total Models Saved: {len(models)}\n")
for m in models:
    print(f"  ✅ {m['name']} ({m['type']}) v{m['version']} - {m['size_mb']} MB")

# Test loading NER model
print("\n🔍 Testing NER Model Loading...")
try:
    ner = p.load('regulatory_ner')
    print("  ✅ NER model loaded successfully")
except Exception as e:
    print(f"  ❌ NER model load failed: {e}")

# Test loading classifier
print("\n🔍 Testing Classifier Loading...")
try:
    clf = p.load('regulatory_regulation_type')
    print("  ✅ Classifier loaded successfully")
    
    # Test predictions
    test_texts = [
        'SEC files enforcement action',
        'Basel III banking rules', 
        'GDPR privacy compliance'
    ]
    preds = clf.predict(test_texts)
    print(f"  ✅ Predictions working: {list(preds)}")
except Exception as e:
    print(f"  ❌ Classifier load failed: {e}")

print("\n" + "="*60)
print("✅ Model Validation Complete!")
print("="*60 + "\n")
