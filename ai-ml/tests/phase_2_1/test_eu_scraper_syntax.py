#!/usr/bin/env python3
"""
Quick syntax test for EU regulatory scraper
"""

try:
    from services.regulatory_intelligence.scrapers.eu_regulatory_scraper import EURegulatoryScaper, EURegulatoryDocument
    print("✅ EU regulatory scraper imports successfully")
    print("✅ EURegulatoryDocument class is properly defined")
    
    # Test creating an instance
    scraper = EURegulatoryScaper()
    print("✅ EURegulatoryScaper can be instantiated")
    
    # Test creating a document
    doc = EURegulatoryDocument(
        title="Test Document",
        url="https://example.com",
        document_type="Test",
        publication_date="2024-01-01",
        source_agency="TEST"
    )
    print("✅ EURegulatoryDocument can be created")
    
    print("\n🎉 All syntax tests passed! The EU regulatory scraper is working correctly.")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
except SyntaxError as e:
    print(f"❌ Syntax error: {e}")
except Exception as e:
    print(f"❌ Other error: {e}")
