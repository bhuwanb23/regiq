#!/usr/bin/env python3
"""
REGIQ AI/ML - EU Regulatory Scraper
Web scraper for European regulatory sites (ESMA, EBA, ECB, etc.)
Integrates with Gemini 2.5-flash for document analysis.
"""

import os
import sys
import time
import logging
import requests
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
from datetime import datetime, timedelta
from urllib.parse import urljoin, urlparse
import json
import sqlite3
import re

# Web scraping libraries
try:
    from bs4 import BeautifulSoup
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    WEB_SCRAPING_AVAILABLE = True
except ImportError as e:
    WEB_SCRAPING_AVAILABLE = False
    print(f"⚠️  Web scraping libraries not installed: {e}")

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from config.env_config import get_env_config
from config.gemini_config import GeminiAPIManager


@dataclass
class EURegulatoryDocument:
    """EU regulatory document information."""
    title: str
    url: str
    document_type: str
    publication_date: str
    source_agency: str
    language: str = "EN"
    summary: Optional[str] = None
    document_id: Optional[str] = None
    pdf_url: Optional[str] = None
    html_url: Optional[str] = None
    topics: List[str] = None
    status: Optional[str] = None


class EURegulatoryScaper:
    """
    European regulatory sites scraper.
    Covers ESMA, EBA, ECB, European Commission, and other EU regulatory bodies.
    """
    
    # Major EU regulatory agencies
    REGULATORY_SITES = {
        "ESMA": {
            "name": "European Securities and Markets Authority",
            "base_url": "https://www.esma.europa.eu",
            "news_url": "https://www.esma.europa.eu/news-and-events",
            "publications_url": "https://www.esma.europa.eu/databases-library/esma-library"
        },
        "EBA": {
            "name": "European Banking Authority", 
            "base_url": "https://www.eba.europa.eu",
            "news_url": "https://www.eba.europa.eu/news-and-communications",
            "publications_url": "https://www.eba.europa.eu/publications-and-media"
        },
        "ECB": {
            "name": "European Central Bank",
            "base_url": "https://www.ecb.europa.eu",
            "news_url": "https://www.ecb.europa.eu/press/html/index.en.html",
            "publications_url": "https://www.ecb.europa.eu/pub/html/index.en.html"
        },
        "EC": {
            "name": "European Commission",
            "base_url": "https://ec.europa.eu",
            "news_url": "https://ec.europa.eu/commission/presscorner/home/en",
            "publications_url": "https://op.europa.eu/en/publications"
        },
        "EIOPA": {
            "name": "European Insurance and Occupational Pensions Authority",
            "base_url": "https://www.eiopa.europa.eu",
            "news_url": "https://www.eiopa.europa.eu/news-and-events_en",
            "publications_url": "https://www.eiopa.europa.eu/publications_en"
        }
    }
    
    def __init__(self, rate_limit_delay: float = 2.0):
        """Initialize EU regulatory scraper."""
        self.rate_limit_delay = rate_limit_delay
        self.env_config = get_env_config()
        self.gemini_manager = GeminiAPIManager()
        self.logger = self._setup_logging()
        self.session = self._setup_session()
        
        # Rate limiting
        self.last_request_time = 0
        
        if not WEB_SCRAPING_AVAILABLE:
            self.logger.warning("Web scraping libraries not available. Limited functionality.")
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for scraper."""
        logger = logging.getLogger('eu_regulatory_scraper')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def _setup_session(self) -> requests.Session:
        """Setup requests session with proper headers."""
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'REGIQ AI/ML Research Tool (compliance@regiq.com)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })
        return session
    
    def _rate_limit(self):
        """Implement rate limiting to be respectful to EU servers."""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        
        if time_since_last_request < self.rate_limit_delay:
            sleep_time = self.rate_limit_delay - time_since_last_request
            self.logger.debug(f"Rate limiting: sleeping for {sleep_time:.2f} seconds")
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def _make_request(self, url: str, params: Dict = None) -> Optional[requests.Response]:
        """Make HTTP request with rate limiting and error handling."""
        self._rate_limit()
        
        try:
            self.logger.debug(f"Making request to: {url}")
            response = self.session.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                return response
            else:
                self.logger.warning(f"HTTP {response.status_code}: {url}")
                return None
                
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request failed: {e}")
            return None
    
    def scrape_esma_publications(self, days_back: int = 30, max_results: int = 50) -> List[EURegulatoryDocument]:
        """Scrape ESMA publications and news."""
        self.logger.info("🇪🇺 Scraping ESMA publications")
        
        documents = []
        
        # Scrape ESMA news
        news_url = self.REGULATORY_SITES["ESMA"]["news_url"]
        response = self._make_request(news_url)
        
        if response:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find news articles (ESMA-specific selectors)
            news_items = soup.find_all(['article', 'div'], class_=re.compile(r'news|article|item'))
            
            for item in news_items[:max_results]:
                try:
                    # Extract title
                    title_elem = item.find(['h1', 'h2', 'h3', 'h4'], class_=re.compile(r'title|heading'))
                    if not title_elem:
                        title_elem = item.find(['a'])
                    
                    title = title_elem.get_text(strip=True) if title_elem else "No title"
                    
                    # Extract URL
                    link_elem = item.find('a', href=True)
                    url = urljoin(self.REGULATORY_SITES["ESMA"]["base_url"], link_elem['href']) if link_elem else ""
                    
                    # Extract date
                    date_elem = item.find(['time', 'span'], class_=re.compile(r'date|time'))
                    date_text = date_elem.get_text(strip=True) if date_elem else ""
                    
                    # Parse date
                    pub_date = self._parse_date(date_text)
                    
                    # Check if within date range
                    if self._is_within_date_range(pub_date, days_back):
                        doc = EURegulatoryDocument(
                            title=title,
                            url=url,
                            document_type="News/Press Release",
                            publication_date=pub_date,
                            source_agency="ESMA",
                            html_url=url
                        )
                        documents.append(doc)
                
                except Exception as e:
                    self.logger.warning(f"Error parsing ESMA item: {e}")
        
        self.logger.info(f"✅ Found {len(documents)} ESMA documents")
        return documents
    
    def scrape_eba_publications(self, days_back: int = 30, max_results: int = 50) -> List[EURegulatoryDocument]:
        """Scrape EBA publications and consultations."""
        self.logger.info("🏦 Scraping EBA publications")
        
        documents = []
        
        # Scrape EBA publications
        pub_url = self.REGULATORY_SITES["EBA"]["publications_url"]
        response = self._make_request(pub_url)
        
        if response:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find publication items
            pub_items = soup.find_all(['div', 'article'], class_=re.compile(r'publication|document|item'))
            
            for item in pub_items[:max_results]:
                try:
                    # Extract title
                    title_elem = item.find(['h1', 'h2', 'h3', 'h4'])
                    title = title_elem.get_text(strip=True) if title_elem else "No title"
                    
                    # Extract URL
                    link_elem = item.find('a', href=True)
                    url = urljoin(self.REGULATORY_SITES["EBA"]["base_url"], link_elem['href']) if link_elem else ""
                    
                    # Extract date
                    date_elem = item.find(['time', 'span'], class_=re.compile(r'date'))
                    date_text = date_elem.get_text(strip=True) if date_elem else ""
                    pub_date = self._parse_date(date_text)
                    
                    # Extract document type
                    type_elem = item.find(['span', 'div'], class_=re.compile(r'type|category'))
                    doc_type = type_elem.get_text(strip=True) if type_elem else "Publication"
                    
                    if self._is_within_date_range(pub_date, days_back):
                        doc = EURegulatoryDocument(
                            title=title,
                            url=url,
                            document_type=doc_type,
                            publication_date=pub_date,
                            source_agency="EBA",
                            html_url=url
                        )
                        documents.append(doc)
                
                except Exception as e:
                    self.logger.warning(f"Error parsing EBA item: {e}")
        
        self.logger.info(f"✅ Found {len(documents)} EBA documents")
        return documents
    
    def scrape_ecb_publications(self, days_back: int = 30, max_results: int = 50) -> List[EURegulatoryDocument]:
        """Scrape ECB press releases and publications."""
        self.logger.info("🏛️ Scraping ECB publications")
        
        documents = []
        
        # Scrape ECB press releases
        press_url = self.REGULATORY_SITES["ECB"]["news_url"]
        response = self._make_request(press_url)
        
        if response:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find press release items
            press_items = soup.find_all(['div', 'article'], class_=re.compile(r'press|news|item'))
            
            for item in press_items[:max_results]:
                try:
                    # Extract title
                    title_elem = item.find(['h1', 'h2', 'h3'])
                    title = title_elem.get_text(strip=True) if title_elem else "No title"
                    
                    # Extract URL
                    link_elem = item.find('a', href=True)
                    url = urljoin(self.REGULATORY_SITES["ECB"]["base_url"], link_elem['href']) if link_elem else ""
                    
                    # Extract date
                    date_elem = item.find(['time', 'span'], class_=re.compile(r'date'))
                    date_text = date_elem.get_text(strip=True) if date_elem else ""
                    pub_date = self._parse_date(date_text)
                    
                    if self._is_within_date_range(pub_date, days_back):
                        doc = EURegulatoryDocument(
                            title=title,
                            url=url,
                            document_type="Press Release",
                            publication_date=pub_date,
                            source_agency="ECB",
                            html_url=url
                        )
                        documents.append(doc)
                
                except Exception as e:
                    self.logger.warning(f"Error parsing ECB item: {e}")
        
        self.logger.info(f"✅ Found {len(documents)} ECB documents")
        return documents
    
    def _parse_date(self, date_text: str) -> str:
        """Parse various date formats from EU sites."""
        if not date_text:
            return datetime.now().strftime('%Y-%m-%d')
        
        # Common EU date patterns
        date_patterns = [
            r'(\d{1,2})[/\-.](\d{1,2})[/\-.](\d{4})',  # DD/MM/YYYY or DD-MM-YYYY
            r'(\d{4})[/\-.](\d{1,2})[/\-.](\d{1,2})',  # YYYY/MM/DD or YYYY-MM-DD
            r'(\d{1,2})\s+([A-Za-z]+)\s+(\d{4})',      # DD Month YYYY
            r'([A-Za-z]+)\s+(\d{1,2}),?\s+(\d{4})',    # Month DD, YYYY
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, date_text)
            if match:
                try:
                    groups = match.groups()
                    if len(groups) == 3:
                        # Try to parse and format as YYYY-MM-DD
                        if groups[0].isdigit() and len(groups[0]) == 4:  # YYYY first
                            return f"{groups[0]}-{groups[1].zfill(2)}-{groups[2].zfill(2)}"
                        elif groups[2].isdigit() and len(groups[2]) == 4:  # YYYY last
                            return f"{groups[2]}-{groups[1].zfill(2) if groups[1].isdigit() else '01'}-{groups[0].zfill(2)}"
                except:
                    continue
        
        # Default to current date if parsing fails
        return datetime.now().strftime('%Y-%m-%d')
    
    def _is_within_date_range(self, date_str: str, days_back: int) -> bool:
        """Check if date is within the specified range."""
        try:
            doc_date = datetime.strptime(date_str, '%Y-%m-%d')
            cutoff_date = datetime.now() - timedelta(days=days_back)
            return doc_date >= cutoff_date
        except:
            return True  # Include if date parsing fails
    
    def download_document_content(self, document: EURegulatoryDocument) -> Optional[str]:
        """Download the content of a EU regulatory document."""
        self.logger.info(f"📥 Downloading: {document.title[:50]}...")
        
        response = self._make_request(document.url)
        
        if response:
            # Parse HTML content
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "header", "footer"]):
                script.decompose()
            
            # Extract main content
            content_selectors = [
                'main', 'article', '.content', '.main-content', 
                '.document-content', '.press-release', '.news-content'
            ]
            
            content = ""
            for selector in content_selectors:
                content_elem = soup.select_one(selector)
                if content_elem:
                    content = content_elem.get_text(separator='\n', strip=True)
                    break
            
            # Fallback to body if no specific content found
            if not content:
                body = soup.find('body')
                if body:
                    content = body.get_text(separator='\n', strip=True)
            
            return content
        
        return None
    
    def analyze_document_with_gemini(self, document: EURegulatoryDocument, content: str) -> Dict[str, Any]:
        """
        Analyze EU regulatory document using Gemini 2.5-flash.
        
        Args:
            document: EU regulatory document metadata
            content: Document text content
            
        Returns:
            Analysis results from Gemini
        """
        self.logger.info(f"🤖 Analyzing EU document with Gemini: {document.source_agency}")
        
        # Prepare analysis prompt
        analysis_prompt = f"""
Analyze this European regulatory document and provide structured insights:

DOCUMENT METADATA:
- Source Agency: {document.source_agency}
- Document Type: {document.document_type}
- Publication Date: {document.publication_date}
- Title: {document.title}

DOCUMENT CONTENT (first 4000 characters):
{content[:4000]}...

Please provide a comprehensive analysis including:

1. REGULATORY_FOCUS: What specific regulatory area does this document address?
2. KEY_REQUIREMENTS: Main regulatory requirements or changes introduced
3. COMPLIANCE_DEADLINES: Any implementation deadlines or effective dates
4. AFFECTED_ENTITIES: Who is affected (banks, insurers, investment firms, etc.)
5. REGULATORY_CHANGES: What changes from previous regulations
6. IMPLEMENTATION_GUIDANCE: Any guidance on how to implement requirements
7. PENALTIES_ENFORCEMENT: Enforcement mechanisms or penalties mentioned
8. CROSS_BORDER_IMPACT: Impact on cross-border activities or non-EU entities
9. INDUSTRY_IMPACT: Expected impact on the financial services industry
10. SUMMARY: Executive summary of the most important regulatory points

Format your response as JSON with these keys: regulatory_focus, key_requirements, compliance_deadlines, affected_entities, regulatory_changes, implementation_guidance, penalties_enforcement, cross_border_impact, industry_impact, summary
"""
        
        try:
            response = self.gemini_manager.generate_content(
                analysis_prompt,
                model="gemini-2.5-flash"
            )
            
            if response:
                return {
                    "gemini_analysis": response,
                    "analysis_timestamp": datetime.now().isoformat(),
                    "model_used": "gemini-2.5-flash",
                    "document_metadata": document.__dict__
                }
            else:
                return {"error": "Gemini analysis failed"}
                
        except Exception as e:
            self.logger.error(f"Gemini analysis error: {e}")
            return {"error": f"Analysis failed: {str(e)}"}
    
    def scrape_all_agencies(self, 
                          agencies: List[str] = None,
                          days_back: int = 30,
                          max_results_per_agency: int = 20,
                          analyze_with_ai: bool = True) -> List[Dict[str, Any]]:
        """
        Scrape documents from multiple EU regulatory agencies.
        
        Args:
            agencies: List of agency codes (ESMA, EBA, ECB, etc.)
            days_back: Number of days to look back
            max_results_per_agency: Max results per agency
            analyze_with_ai: Whether to analyze with Gemini
            
        Returns:
            List of document results with analysis
        """
        if agencies is None:
            agencies = ["ESMA", "EBA", "ECB"]
        
        self.logger.info(f"🇪🇺 Scraping {len(agencies)} EU regulatory agencies")
        
        all_results = []
        
        # Agency-specific scraping methods
        scraping_methods = {
            "ESMA": self.scrape_esma_publications,
            "EBA": self.scrape_eba_publications,
            "ECB": self.scrape_ecb_publications,
        }
        
        for agency in agencies:
            if agency in scraping_methods:
                try:
                    self.logger.info(f"📊 Processing agency: {agency}")
                    
                    # Get documents
                    documents = scraping_methods[agency](days_back, max_results_per_agency)
                    
                    # Process each document
                    for document in documents:
                        try:
                            # Download content
                            content = self.download_document_content(document)
                            
                            if content:
                                result = {
                                    "agency": agency,
                                    "document": document.__dict__,
                                    "content_length": len(content),
                                    "download_timestamp": datetime.now().isoformat(),
                                    "content": content[:10000]  # Store first 10k chars
                                }
                                
                                # AI Analysis
                                if analyze_with_ai and content:
                                    ai_analysis = self.analyze_document_with_gemini(document, content)
                                    result["ai_analysis"] = ai_analysis
                                
                                all_results.append(result)
                            
                        except Exception as e:
                            self.logger.error(f"Error processing document {document.title}: {e}")
                
                except Exception as e:
                    self.logger.error(f"Error processing agency {agency}: {e}")
            else:
                self.logger.warning(f"No scraping method for agency: {agency}")
        
        self.logger.info(f"✅ EU scraping completed: {len(all_results)} documents processed")
        return all_results
    
    def save_results_to_database(self, results: List[Dict[str, Any]], db_path: str = "data/eu_regulatory.db"):
        """Save scraping results to SQLite database."""
        self.logger.info(f"💾 Saving {len(results)} EU regulatory results to database")
        
        # Ensure data directory exists
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create table if not exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS eu_regulatory_documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agency TEXT,
                title TEXT,
                document_type TEXT,
                publication_date TEXT,
                url TEXT UNIQUE,
                content TEXT,
                ai_analysis TEXT,
                download_timestamp TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Insert results
        for result in results:
            try:
                document = result.get('document', {})
                ai_analysis = result.get('ai_analysis', {})
                
                cursor.execute("""
                    INSERT OR REPLACE INTO eu_regulatory_documents 
                    (agency, title, document_type, publication_date, url,
                     content, ai_analysis, download_timestamp)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    result.get('agency'),
                    document.get('title'),
                    document.get('document_type'),
                    document.get('publication_date'),
                    document.get('url'),
                    result.get('content'),
                    json.dumps(ai_analysis, default=str),
                    result.get('download_timestamp')
                ))
                
            except sqlite3.IntegrityError:
                # Document already exists
                pass
            except Exception as e:
                self.logger.error(f"Error saving result: {e}")
        
        conn.commit()
        conn.close()
        
        self.logger.info("✅ EU regulatory results saved to database")


def main():
    """Test the EU regulatory scraper."""
    print("🧪 Testing EU Regulatory Scraper")
    print("="*50)
    
    scraper = EURegulatoryScaper()
    
    # Test with major EU agencies
    test_agencies = ["ESMA", "EBA", "ECB"]
    
    print(f"🇪🇺 Testing with agencies: {test_agencies}")
    
    try:
        results = scraper.scrape_all_agencies(
            agencies=test_agencies[:1],  # Test with just one agency
            days_back=60,
            max_results_per_agency=5,
            analyze_with_ai=True
        )
        
        print(f"✅ EU scraping completed!")
        print(f"📊 Results: {len(results)} documents found")
        
        if results:
            print(f"📄 Sample result:")
            sample = results[0]
            print(f"   Agency: {sample.get('agency')}")
            print(f"   Title: {sample['document']['title'][:80]}...")
            print(f"   Type: {sample['document']['document_type']}")
            print(f"   Date: {sample['document']['publication_date']}")
            print(f"   Content length: {sample.get('content_length')} chars")
            
            if 'ai_analysis' in sample:
                print(f"   🤖 AI Analysis: Available")
        
        # Save to database
        scraper.save_results_to_database(results)
        
    except Exception as e:
        print(f"❌ Test failed: {e}")


if __name__ == "__main__":
    main()
