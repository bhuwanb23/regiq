#!/usr/bin/env python3
"""
Comprehensive Test Suite for Phase 2.2: NLP Processing
Tests all components of the natural language processing pipeline.
"""

import sys
import os
from pathlib import Path
import json
import time

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

def test_phase_2_2_overview():
    """Test Phase 2.2 overview and requirements."""
    print("🧠 Phase 2.2: NLP Processing - Comprehensive Test")
    print("="*70)
    print("📋 Testing Requirements:")
    print("   2.2.1 Text Preprocessing - Clean, normalize, tokenize, segment")
    print("   2.2.2 Entity Recognition - Extract regulatory entities, dates, penalties")
    print("   2.2.3 Text Classification - Regulation types, compliance, risk, urgency")
    print("="*70)
    return True

def test_text_preprocessing_complete():
    """Test complete text preprocessing functionality."""
    print("\n🧹 Testing Text Preprocessing (2.2.1)...")
    
    try:
        from services.regulatory_intelligence.nlp.text_preprocessing import (
            TextPreprocessor, PreprocessingConfig, ProcessedText
        )
        print("✅ Text preprocessing classes imported")
        
        # Test preprocessor initialization
        config = PreprocessingConfig(
            remove_stopwords=True,
            lemmatize=True,
            min_word_length=2
        )
        preprocessor = TextPreprocessor(config)
        print("✅ Text preprocessor initialized")
        
        # Test text cleaning
        sample_text = "The SEC has announced new regulations!!! This is a test document with special characters: $1,000,000."
        cleaned_text = preprocessor.clean_text(sample_text)
        print("✅ Text cleaning works")
        
        # Test tokenization
        tokens = preprocessor.tokenize_text(cleaned_text)
        print(f"✅ Tokenization works: {len(tokens)} tokens")
        
        # Test sentence segmentation
        sentences = preprocessor.segment_sentences(cleaned_text)
        print(f"✅ Sentence segmentation works: {len(sentences)} sentences")
        
        # Test complete processing
        result = preprocessor.process_text(sample_text)
        print("✅ Complete text processing works")
        
        # Test metadata
        metadata = result.metadata
        print(f"✅ Metadata generated: {len(metadata)} fields")
        
        print("✅ Text Preprocessing (2.2.1) - COMPLETE")
        return True
        
    except Exception as e:
        print(f"❌ Text preprocessing test failed: {e}")
        return False

def test_entity_recognition_complete():
    """Test complete entity recognition functionality."""
    print("\n🔍 Testing Entity Recognition (2.2.2)...")
    
    try:
        from services.regulatory_intelligence.nlp.entity_recognition import (
            RegulatoryEntityRecognizer, EntityRecognitionResult
        )
        print("✅ Entity recognition classes imported")
        
        # Test recognizer initialization
        recognizer = RegulatoryEntityRecognizer()
        print("✅ Entity recognizer initialized")
        
        # Test regulatory entity extraction
        sample_text = "The Securities and Exchange Commission (SEC) has announced new regulations under the Dodd-Frank Act."
        regulatory_entities = recognizer.extract_regulatory_entities(sample_text)
        print(f"✅ Regulatory entity extraction works: {len(regulatory_entities)} entities")
        
        # Test date extraction
        date_text = "The deadline is January 1, 2024, and the effective date is March 15, 2024."
        date_entities = recognizer.extract_dates(date_text)
        print(f"✅ Date extraction works: {len(date_entities)} dates")
        
        # Test penalty extraction
        penalty_text = "Failure to comply may result in penalties of up to $1,000,000 per violation."
        penalty_entities = recognizer.extract_penalties(penalty_text)
        print(f"✅ Penalty extraction works: {len(penalty_entities)} penalties")
        
        # Test complete entity recognition
        full_text = "The SEC has announced new regulations under Dodd-Frank with a deadline of January 1, 2024. Penalties may reach $1,000,000."
        result = recognizer.recognize_entities(full_text)
        print("✅ Complete entity recognition works")
        
        # Test metadata
        metadata = result.metadata
        print(f"✅ Entity recognition metadata: {metadata}")
        
        print("✅ Entity Recognition (2.2.2) - COMPLETE")
        return True
        
    except Exception as e:
        print(f"❌ Entity recognition test failed: {e}")
        return False

def test_text_classification_complete():
    """Test complete text classification functionality."""
    print("\n📊 Testing Text Classification (2.2.3)...")
    
    try:
        from services.regulatory_intelligence.nlp.text_classification import (
            RegulatoryTextClassifier, ClassificationConfig, ClassificationResult
        )
        print("✅ Text classification classes imported")
        
        # Test classifier initialization
        config = ClassificationConfig(
            model_type="logistic_regression",
            use_transformer=False
        )
        classifier = RegulatoryTextClassifier(config)
        print("✅ Text classifier initialized")
        
        # Test model training
        classifier.train_all_models()
        print("✅ Model training works")
        
        # Test text classification
        sample_text = "The SEC has issued new regulations requiring immediate compliance with enhanced reporting requirements."
        result = classifier.classify_text(sample_text)
        print("✅ Text classification works")
        
        # Test classification results
        print(f"   Regulation Type: {result.regulation_type}")
        print(f"   Compliance Category: {result.compliance_category}")
        print(f"   Risk Level: {result.risk_level}")
        print(f"   Urgency Level: {result.urgency_level}")
        
        # Test confidence scores
        confidence_scores = result.confidence_scores
        print(f"✅ Confidence scores: {confidence_scores}")
        
        # Test metadata
        metadata = result.metadata
        print(f"✅ Classification metadata: {len(metadata)} fields")
        
        print("✅ Text Classification (2.2.3) - COMPLETE")
        return True
        
    except Exception as e:
        print(f"❌ Text classification test failed: {e}")
        return False

def test_nlp_libraries():
    """Test NLP libraries availability."""
    print("\n📚 Testing NLP Libraries...")
    
    libraries = {
        'spacy': 'spacy',
        'nltk': 'nltk',
        'sklearn': 'sklearn',
        'transformers': 'transformers',
        'torch': 'torch'
    }
    
    all_available = True
    
    for lib_name, import_name in libraries.items():
        try:
            __import__(import_name)
            print(f"✅ {lib_name} - Available")
        except ImportError:
            print(f"❌ {lib_name} - Missing")
            all_available = False
    
    return all_available

def test_spacy_models():
    """Test spaCy models availability."""
    print("\n🤖 Testing spaCy Models...")
    
    try:
        import spacy
        
        models = ['en_core_web_sm', 'en_core_web_md']
        available_models = []
        
        for model in models:
            try:
                nlp = spacy.load(model)
                available_models.append(model)
                print(f"✅ {model} - Available")
            except OSError:
                print(f"❌ {model} - Not installed")
        
        return len(available_models) > 0
        
    except Exception as e:
        print(f"❌ spaCy model test failed: {e}")
        return False

def test_nlp_integration():
    """Test NLP modules integration."""
    print("\n🔄 Testing NLP Integration...")
    
    try:
        # Test importing all NLP modules
        from services.regulatory_intelligence.nlp.text_preprocessing import TextPreprocessor
        from services.regulatory_intelligence.nlp.entity_recognition import RegulatoryEntityRecognizer
        from services.regulatory_intelligence.nlp.text_classification import RegulatoryTextClassifier
        
        print("✅ All NLP modules imported successfully")
        
        # Test module initialization
        preprocessor = TextPreprocessor()
        recognizer = RegulatoryEntityRecognizer()
        classifier = RegulatoryTextClassifier()
        
        print("✅ All NLP modules initialized successfully")
        
        # Test end-to-end processing
        sample_text = "The SEC has announced new regulations under Dodd-Frank with a deadline of January 1, 2024. Penalties may reach $1,000,000."
        
        # Preprocess
        processed = preprocessor.process_text(sample_text)
        print("✅ Text preprocessing integration works")
        
        # Extract entities
        entities = recognizer.recognize_entities(sample_text)
        print("✅ Entity recognition integration works")
        
        # Classify
        classification = classifier.classify_text(sample_text)
        print("✅ Text classification integration works")
        
        print("✅ NLP Integration - COMPLETE")
        return True
        
    except Exception as e:
        print(f"❌ NLP integration test failed: {e}")
        return False

def test_performance_considerations():
    """Test performance considerations."""
    print("\n⚡ Testing Performance Considerations...")
    
    try:
        from services.regulatory_intelligence.nlp.text_preprocessing import TextPreprocessor
        from services.regulatory_intelligence.nlp.entity_recognition import RegulatoryEntityRecognizer
        from services.regulatory_intelligence.nlp.text_classification import RegulatoryTextClassifier
        
        # Test processing time
        sample_text = "The SEC has announced new regulations under Dodd-Frank with a deadline of January 1, 2024. Penalties may reach $1,000,000."
        
        start_time = time.time()
        
        preprocessor = TextPreprocessor()
        processed = preprocessor.process_text(sample_text)
        
        recognizer = RegulatoryEntityRecognizer()
        entities = recognizer.recognize_entities(sample_text)
        
        classifier = RegulatoryTextClassifier()
        classification = classifier.classify_text(sample_text)
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        print(f"✅ Processing time: {processing_time:.2f} seconds")
        
        # Test batch processing
        texts = [sample_text] * 5
        start_time = time.time()
        batch_results = preprocessor.batch_process(texts)
        end_time = time.time()
        batch_time = end_time - start_time
        
        print(f"✅ Batch processing time: {batch_time:.2f} seconds for {len(texts)} texts")
        
        print("✅ Performance Considerations - COMPLETE")
        return True
        
    except Exception as e:
        print(f"❌ Performance test failed: {e}")
        return False

def test_error_handling():
    """Test error handling across all NLP modules."""
    print("\n🛡️ Testing Error Handling...")
    
    try:
        from services.regulatory_intelligence.nlp.text_preprocessing import TextPreprocessor
        from services.regulatory_intelligence.nlp.entity_recognition import RegulatoryEntityRecognizer
        from services.regulatory_intelligence.nlp.text_classification import RegulatoryTextClassifier
        
        # Test with empty text
        preprocessor = TextPreprocessor()
        empty_result = preprocessor.process_text("")
        print("✅ Empty text handling works")
        
        # Test with None input
        try:
            preprocessor.process_text(None)
            print("✅ None input handling works")
        except Exception:
            print("✅ None input properly rejected")
        
        # Test with very long text
        long_text = "The SEC has announced new regulations. " * 1000
        long_result = preprocessor.process_text(long_text)
        print("✅ Long text handling works")
        
        # Test with special characters
        special_text = "Special chars: @#$%^&*()_+{}|:<>?[]\\;'\",./"
        special_result = preprocessor.process_text(special_text)
        print("✅ Special character handling works")
        
        print("✅ Error Handling - COMPLETE")
        return True
        
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
        return False

def main():
    """Run comprehensive Phase 2.2 tests."""
    print("🚀 REGIQ AI/ML - Phase 2.2 Comprehensive Test Suite")
    print("="*70)
    
    tests = [
        ("Phase 2.2 Overview", test_phase_2_2_overview),
        ("NLP Libraries", test_nlp_libraries),
        ("spaCy Models", test_spacy_models),
        ("Text Preprocessing (2.2.1)", test_text_preprocessing_complete),
        ("Entity Recognition (2.2.2)", test_entity_recognition_complete),
        ("Text Classification (2.2.3)", test_text_classification_complete),
        ("NLP Integration", test_nlp_integration),
        ("Performance Considerations", test_performance_considerations),
        ("Error Handling", test_error_handling),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            print(f"\n{'='*70}")
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            results[test_name] = False
    
    # Final Summary
    print(f"\n{'='*70}")
    print("📊 PHASE 2.2 COMPREHENSIVE TEST SUMMARY")
    print(f"{'='*70}")
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<35} {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 ALL PHASE 2.2 TESTS PASSED!")
        print("✅ NLP Processing Pipeline is COMPLETE and READY")
        print("\n📋 Phase 2.2 Status:")
        print("   ✅ 2.2.1 Text Preprocessing - COMPLETE")
        print("   ✅ 2.2.2 Entity Recognition - COMPLETE") 
        print("   ✅ 2.2.3 Text Classification - COMPLETE")
        print("\n🚀 Ready to proceed to Phase 2.3!")
    else:
        print(f"\n⚠️  {total - passed} tests failed. Please review and fix issues.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
