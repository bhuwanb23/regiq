#!/usr/bin/env python3
"""
REGIQ AI/ML - Document Processing Pipeline
Main orchestrator for all document processing activities.
Coordinates PDF processing, web scraping, and API data collection.
"""

import os
import sys
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import json
import sqlite3

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from config.env_config import get_env_config
from config.gemini_config import GeminiAPIManager

# Import our processing modules
try:
    from .pdf_processor import PDFProcessor
    from .sec_edgar_scraper import SECEdgarScraper
    from .eu_regulatory_scraper import EURegulatoryScaper
    from .regulatory_api_connector import RegulatoryAPIConnector
    PROCESSORS_AVAILABLE = True
except ImportError as e:
    PROCESSORS_AVAILABLE = False
    print(f"⚠️  Some processors not available: {e}")


class DocumentProcessingPipeline:
    """
    Main document processing pipeline orchestrator.
    Coordinates all document processing activities and provides unified interface.
    """
    
    def __init__(self):
        """Initialize document processing pipeline."""
        self.env_config = get_env_config()
        self.gemini_manager = GeminiAPIManager()
        self.logger = self._setup_logging()
        
        # Initialize processors
        self.pdf_processor = None
        self.sec_scraper = None
        self.eu_scraper = None
        self.api_connector = None
        
        self._initialize_processors()
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for pipeline."""
        logger = logging.getLogger('document_pipeline')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def _initialize_processors(self):
        """Initialize all document processors."""
        try:
            if PROCESSORS_AVAILABLE:
                self.pdf_processor = PDFProcessor()
                self.sec_scraper = SECEdgarScraper()
                self.eu_scraper = EURegulatoryScaper()
                self.api_connector = RegulatoryAPIConnector()
                self.logger.info("✅ All processors initialized successfully")
            else:
                self.logger.warning("⚠️  Some processors not available")
        except Exception as e:
            self.logger.error(f"Error initializing processors: {e}")
    
    def process_pdf_documents(self, 
                            pdf_paths: List[str], 
                            analyze_with_ai: bool = True) -> List[Dict[str, Any]]:
        """
        Process multiple PDF documents.
        
        Args:
            pdf_paths: List of PDF file paths
            analyze_with_ai: Whether to analyze with Gemini
            
        Returns:
            List of processing results
        """
        self.logger.info(f"📄 Processing {len(pdf_paths)} PDF documents")
        
        if not self.pdf_processor:
            self.logger.error("PDF processor not available")
            return []
        
        results = []
        
        for pdf_path in pdf_paths:
            try:
                self.logger.info(f"Processing: {pdf_path}")
                result = self.pdf_processor.process_regulatory_pdf(pdf_path, analyze_with_ai)
                results.append(result)
                
            except Exception as e:
                self.logger.error(f"Error processing {pdf_path}: {e}")
                results.append({
                    "error": str(e),
                    "pdf_path": pdf_path,
                    "processing_timestamp": datetime.now().isoformat()
                })
        
        self.logger.info(f"✅ PDF processing completed: {len(results)} documents")
        return results
    
    def scrape_regulatory_websites(self, 
                                 sources: List[str] = None,
                                 days_back: int = 30,
                                 analyze_with_ai: bool = True) -> Dict[str, List[Dict]]:
        """
        Scrape regulatory websites.
        
        Args:
            sources: List of sources ('SEC', 'EU', or both)
            days_back: Number of days to look back
            analyze_with_ai: Whether to analyze with Gemini
            
        Returns:
            Dictionary with results by source
        """
        if sources is None:
            sources = ['SEC', 'EU']
        
        self.logger.info(f"🌐 Scraping regulatory websites: {sources}")
        
        results = {}
        
        # SEC EDGAR scraping
        if 'SEC' in sources and self.sec_scraper:
            try:
                self.logger.info("📊 Scraping SEC EDGAR...")
                
                # Major companies for testing
                companies = ["Apple Inc", "Microsoft Corporation", "JPMorgan Chase & Co"]
                form_types = ["10-K", "10-Q", "8-K"]
                
                sec_results = self.sec_scraper.scrape_recent_filings(
                    companies=companies,
                    form_types=form_types,
                    days_back=days_back,
                    analyze_with_ai=analyze_with_ai
                )
                
                results['SEC'] = sec_results
                self.logger.info(f"✅ SEC scraping completed: {len(sec_results)} documents")
                
            except Exception as e:
                self.logger.error(f"SEC scraping error: {e}")
                results['SEC'] = []
        
        # EU regulatory scraping
        if 'EU' in sources and self.eu_scraper:
            try:
                self.logger.info("🇪🇺 Scraping EU regulatory sites...")
                
                agencies = ["ESMA", "EBA", "ECB"]
                
                eu_results = self.eu_scraper.scrape_all_agencies(
                    agencies=agencies,
                    days_back=days_back,
                    max_results_per_agency=20,
                    analyze_with_ai=analyze_with_ai
                )
                
                results['EU'] = eu_results
                self.logger.info(f"✅ EU scraping completed: {len(eu_results)} documents")
                
            except Exception as e:
                self.logger.error(f"EU scraping error: {e}")
                results['EU'] = []
        
        return results
    
    def fetch_regulatory_api_data(self, 
                                api_requests: List[Dict[str, Any]] = None,
                                analyze_with_ai: bool = True) -> List[Dict[str, Any]]:
        """
        Fetch data from regulatory APIs.
        
        Args:
            api_requests: List of API request specifications
            analyze_with_ai: Whether to analyze with Gemini
            
        Returns:
            List of API results
        """
        if api_requests is None:
            # Default API requests for testing
            api_requests = [
                {
                    "api": "SEC_EDGAR",
                    "type": "company_data",
                    "params": {"cik": "320193"}  # Apple
                },
                {
                    "api": "SEC_EDGAR", 
                    "type": "company_data",
                    "params": {"cik": "789019"}  # Microsoft
                },
                {
                    "api": "FDIC_API",
                    "type": "bank_data", 
                    "params": {"bank_name": "JPMorgan Chase"}
                }
            ]
        
        self.logger.info(f"📊 Fetching regulatory API data: {len(api_requests)} requests")
        
        if not self.api_connector:
            self.logger.error("API connector not available")
            return []
        
        try:
            results = self.api_connector.batch_fetch_regulatory_data(
                api_requests,
                analyze_with_ai=analyze_with_ai
            )
            
            self.logger.info(f"✅ API data fetch completed: {len(results)} successful")
            return results
            
        except Exception as e:
            self.logger.error(f"API data fetch error: {e}")
            return []
    
    def run_full_pipeline(self, 
                        pdf_paths: List[str] = None,
                        scraping_sources: List[str] = None,
                        api_requests: List[Dict] = None,
                        days_back: int = 30,
                        analyze_with_ai: bool = True) -> Dict[str, Any]:
        """
        Run the complete document processing pipeline.
        
        Args:
            pdf_paths: PDF files to process
            scraping_sources: Web scraping sources
            api_requests: API data requests
            days_back: Days to look back for scraping
            analyze_with_ai: Whether to analyze with Gemini
            
        Returns:
            Complete pipeline results
        """
        self.logger.info("🚀 Starting full document processing pipeline")
        
        pipeline_start = datetime.now()
        results = {
            "pipeline_start": pipeline_start.isoformat(),
            "configuration": {
                "days_back": days_back,
                "analyze_with_ai": analyze_with_ai,
                "pdf_count": len(pdf_paths) if pdf_paths else 0,
                "scraping_sources": scraping_sources or [],
                "api_requests": len(api_requests) if api_requests else 0
            },
            "results": {}
        }
        
        # 1. Process PDF documents
        if pdf_paths:
            self.logger.info("📄 Phase 1: PDF Processing")
            pdf_results = self.process_pdf_documents(pdf_paths, analyze_with_ai)
            results["results"]["pdf_processing"] = pdf_results
        
        # 2. Web scraping
        if scraping_sources:
            self.logger.info("🌐 Phase 2: Web Scraping")
            scraping_results = self.scrape_regulatory_websites(
                scraping_sources, days_back, analyze_with_ai
            )
            results["results"]["web_scraping"] = scraping_results
        
        # 3. API data collection
        if api_requests or not pdf_paths and not scraping_sources:  # Default if nothing specified
            self.logger.info("📊 Phase 3: API Data Collection")
            api_results = self.fetch_regulatory_api_data(api_requests, analyze_with_ai)
            results["results"]["api_data"] = api_results
        
        # Pipeline completion
        pipeline_end = datetime.now()
        results["pipeline_end"] = pipeline_end.isoformat()
        results["pipeline_duration"] = str(pipeline_end - pipeline_start)
        
        # Summary statistics
        results["summary"] = self._generate_pipeline_summary(results)
        
        self.logger.info(f"✅ Full pipeline completed in {results['pipeline_duration']}")
        return results
    
    def _generate_pipeline_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate summary statistics for pipeline results."""
        summary = {
            "total_documents_processed": 0,
            "successful_operations": 0,
            "failed_operations": 0,
            "ai_analyses_completed": 0,
            "data_sources_used": [],
            "processing_phases": []
        }
        
        pipeline_results = results.get("results", {})
        
        # PDF processing summary
        if "pdf_processing" in pipeline_results:
            pdf_results = pipeline_results["pdf_processing"]
            summary["total_documents_processed"] += len(pdf_results)
            summary["processing_phases"].append("PDF Processing")
            
            for result in pdf_results:
                if "error" not in result:
                    summary["successful_operations"] += 1
                    if "ai_analysis" in result:
                        summary["ai_analyses_completed"] += 1
                else:
                    summary["failed_operations"] += 1
        
        # Web scraping summary
        if "web_scraping" in pipeline_results:
            scraping_results = pipeline_results["web_scraping"]
            summary["processing_phases"].append("Web Scraping")
            
            for source, documents in scraping_results.items():
                summary["data_sources_used"].append(source)
                summary["total_documents_processed"] += len(documents)
                
                for doc in documents:
                    if "error" not in doc:
                        summary["successful_operations"] += 1
                        if "ai_analysis" in doc:
                            summary["ai_analyses_completed"] += 1
                    else:
                        summary["failed_operations"] += 1
        
        # API data summary
        if "api_data" in pipeline_results:
            api_results = pipeline_results["api_data"]
            summary["processing_phases"].append("API Data Collection")
            summary["total_documents_processed"] += len(api_results)
            
            for result in api_results:
                api_data = result.get("api_data", {})
                source_api = api_data.get("source_api")
                if source_api and source_api not in summary["data_sources_used"]:
                    summary["data_sources_used"].append(source_api)
                
                if "error" not in result:
                    summary["successful_operations"] += 1
                    if "ai_analysis" in result:
                        summary["ai_analyses_completed"] += 1
                else:
                    summary["failed_operations"] += 1
        
        return summary
    
    def save_pipeline_results(self, results: Dict[str, Any], output_path: str = None):
        """Save pipeline results to file and database."""
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"data/pipeline_results_{timestamp}.json"
        
        # Ensure output directory exists
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Save to JSON file
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, default=str)
            self.logger.info(f"💾 Pipeline results saved to: {output_path}")
        except Exception as e:
            self.logger.error(f"Error saving results to file: {e}")
        
        # Save to databases
        try:
            self._save_to_databases(results)
        except Exception as e:
            self.logger.error(f"Error saving to databases: {e}")
    
    def _save_to_databases(self, results: Dict[str, Any]):
        """Save results to appropriate databases."""
        pipeline_results = results.get("results", {})
        
        # Save PDF results
        if "pdf_processing" in pipeline_results and self.pdf_processor:
            # PDF processor has its own database saving logic
            pass
        
        # Save SEC results
        if "web_scraping" in pipeline_results and "SEC" in pipeline_results["web_scraping"]:
            if self.sec_scraper:
                sec_results = pipeline_results["web_scraping"]["SEC"]
                self.sec_scraper.save_results_to_database(sec_results)
        
        # Save EU results
        if "web_scraping" in pipeline_results and "EU" in pipeline_results["web_scraping"]:
            if self.eu_scraper:
                eu_results = pipeline_results["web_scraping"]["EU"]
                self.eu_scraper.save_results_to_database(eu_results)
        
        # Save API results
        if "api_data" in pipeline_results and self.api_connector:
            api_results = pipeline_results["api_data"]
            self.api_connector.save_api_results_to_database(api_results)


def main():
    """Test the document processing pipeline."""
    print("🧪 Testing Document Processing Pipeline")
    print("="*60)
    
    pipeline = DocumentProcessingPipeline()
    
    # Test configuration
    test_config = {
        "scraping_sources": ["SEC", "EU"],
        "days_back": 60,
        "analyze_with_ai": True
    }
    
    print(f"🔧 Test configuration:")
    print(f"   Sources: {test_config['scraping_sources']}")
    print(f"   Days back: {test_config['days_back']}")
    print(f"   AI Analysis: {test_config['analyze_with_ai']}")
    
    try:
        # Run pipeline
        results = pipeline.run_full_pipeline(**test_config)
        
        # Display results
        print(f"\n✅ Pipeline completed!")
        print(f"📊 Summary:")
        summary = results.get("summary", {})
        print(f"   Total documents: {summary.get('total_documents_processed', 0)}")
        print(f"   Successful operations: {summary.get('successful_operations', 0)}")
        print(f"   Failed operations: {summary.get('failed_operations', 0)}")
        print(f"   AI analyses: {summary.get('ai_analyses_completed', 0)}")
        print(f"   Data sources: {', '.join(summary.get('data_sources_used', []))}")
        print(f"   Duration: {results.get('pipeline_duration', 'Unknown')}")
        
        # Save results
        pipeline.save_pipeline_results(results)
        
    except Exception as e:
        print(f"❌ Pipeline test failed: {e}")


if __name__ == "__main__":
    main()
