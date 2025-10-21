#!/usr/bin/env python3
"""
REGIQ AI/ML - SEC EDGAR Scraper
Web scraper for SEC EDGAR database with rate limiting and respectful crawling.
Integrates with Gemini 2.5-flash for document analysis.
"""

import os
import sys
import time
import logging
import requests
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
from urllib.parse import urljoin, urlparse
import json
import sqlite3

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
    print("   Install with: pip install beautifulsoup4 selenium requests")

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from config.env_config import get_env_config
from config.gemini_config import GeminiAPIManager


@dataclass
class SECFiling:
    """SEC filing information."""
    cik: str
    company_name: str
    form_type: str
    filing_date: str
    accession_number: str
    document_url: str
    html_url: Optional[str] = None
    txt_url: Optional[str] = None
    size: Optional[int] = None
    description: Optional[str] = None


@dataclass
class ScrapingConfig:
    """Configuration for web scraping."""
    rate_limit_delay: float = 1.0  # Seconds between requests
    max_retries: int = 3
    timeout: int = 30
    user_agent: str = "REGIQ AI/ML Research Tool (compliance@regiq.com)"
    respect_robots_txt: bool = True


class SECEdgarScraper:
    """
    SEC EDGAR database scraper with rate limiting and respectful crawling.
    Follows SEC guidelines for automated access.
    """
    
    BASE_URL = "https://www.sec.gov"
    EDGAR_SEARCH_URL = "https://www.sec.gov/edgar/search/"
    EDGAR_API_URL = "https://data.sec.gov"
    
    def __init__(self, config: ScrapingConfig = None):
        """Initialize SEC EDGAR scraper."""
        self.config = config or ScrapingConfig()
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
        logger = logging.getLogger('sec_edgar_scraper')
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
            'User-Agent': self.config.user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })
        return session
    
    def _rate_limit(self):
        """Implement rate limiting to be respectful to SEC servers."""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        
        if time_since_last_request < self.config.rate_limit_delay:
            sleep_time = self.config.rate_limit_delay - time_since_last_request
            self.logger.debug(f"Rate limiting: sleeping for {sleep_time:.2f} seconds")
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def _make_request(self, url: str, params: Dict = None) -> Optional[requests.Response]:
        """Make HTTP request with rate limiting and error handling."""
        self._rate_limit()
        
        for attempt in range(self.config.max_retries):
            try:
                self.logger.debug(f"Making request to: {url}")
                response = self.session.get(
                    url, 
                    params=params, 
                    timeout=self.config.timeout
                )
                
                if response.status_code == 200:
                    return response
                elif response.status_code == 429:  # Rate limited
                    wait_time = (attempt + 1) * 2
                    self.logger.warning(f"Rate limited. Waiting {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    self.logger.warning(f"HTTP {response.status_code}: {url}")
                    
            except requests.exceptions.RequestException as e:
                self.logger.warning(f"Request failed (attempt {attempt + 1}): {e}")
                if attempt < self.config.max_retries - 1:
                    time.sleep((attempt + 1) * 2)
        
        return None
    
    def search_company_filings(self, 
                             company_name: str = None, 
                             cik: str = None, 
                             form_types: List[str] = None,
                             date_from: str = None,
                             date_to: str = None,
                             max_results: int = 100) -> List[SECFiling]:
        """
        Search for company filings using SEC EDGAR search.
        
        Args:
            company_name: Company name to search for
            cik: Central Index Key (CIK) number
            form_types: List of form types (e.g., ['10-K', '10-Q', '8-K'])
            date_from: Start date (YYYY-MM-DD)
            date_to: End date (YYYY-MM-DD)
            max_results: Maximum number of results to return
            
        Returns:
            List of SEC filings
        """
        self.logger.info(f"🔍 Searching SEC filings for: {company_name or cik}")
        
        # Use SEC EDGAR API for structured data
        api_url = f"{self.EDGAR_API_URL}/submissions/"
        
        if cik:
            # Direct CIK lookup
            cik_padded = str(cik).zfill(10)  # SEC requires 10-digit CIK
            url = f"{api_url}CIK{cik_padded}.json"
        else:
            # Need to search by company name first
            return self._search_by_company_name(company_name, form_types, date_from, date_to, max_results)
        
        response = self._make_request(url)
        if not response:
            self.logger.error(f"Failed to fetch data for CIK: {cik}")
            return []
        
        try:
            data = response.json()
            return self._parse_sec_api_response(data, form_types, date_from, date_to, max_results)
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse SEC API response: {e}")
            return []
    
    def _search_by_company_name(self, company_name: str, form_types: List[str], 
                               date_from: str, date_to: str, max_results: int) -> List[SECFiling]:
        """Search by company name using company tickers endpoint."""
        # Get company tickers to find CIK
        tickers_url = f"{self.EDGAR_API_URL}/company_tickers.json"
        response = self._make_request(tickers_url)
        
        if not response:
            return []
        
        try:
            tickers_data = response.json()
            
            # Find matching company
            matching_cik = None
            for entry in tickers_data.values():
                if company_name.lower() in entry.get('title', '').lower():
                    matching_cik = entry.get('cik_str')
                    break
            
            if matching_cik:
                return self.search_company_filings(
                    cik=matching_cik,
                    form_types=form_types,
                    date_from=date_from,
                    date_to=date_to,
                    max_results=max_results
                )
            else:
                self.logger.warning(f"Company not found: {company_name}")
                return []
                
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse company tickers: {e}")
            return []
    
    def _parse_sec_api_response(self, data: Dict, form_types: List[str], 
                               date_from: str, date_to: str, max_results: int) -> List[SECFiling]:
        """Parse SEC API response into SECFiling objects."""
        filings = []
        
        try:
            recent_filings = data.get('filings', {}).get('recent', {})
            
            if not recent_filings:
                return filings
            
            # Get arrays of filing data
            accession_numbers = recent_filings.get('accessionNumber', [])
            filing_dates = recent_filings.get('filingDate', [])
            form_types_list = recent_filings.get('form', [])
            
            company_name = data.get('name', 'Unknown')
            cik = data.get('cik', '')
            
            for i in range(min(len(accession_numbers), max_results)):
                form_type = form_types_list[i] if i < len(form_types_list) else ''
                filing_date = filing_dates[i] if i < len(filing_dates) else ''
                accession_number = accession_numbers[i]
                
                # Filter by form type
                if form_types and form_type not in form_types:
                    continue
                
                # Filter by date range
                if date_from and filing_date < date_from:
                    continue
                if date_to and filing_date > date_to:
                    continue
                
                # Construct document URLs
                accession_clean = accession_number.replace('-', '')
                document_url = f"{self.BASE_URL}/Archives/edgar/data/{cik}/{accession_clean}/{accession_number}.txt"
                html_url = f"{self.BASE_URL}/Archives/edgar/data/{cik}/{accession_clean}/{accession_number}-index.html"
                
                filing = SECFiling(
                    cik=str(cik),
                    company_name=company_name,
                    form_type=form_type,
                    filing_date=filing_date,
                    accession_number=accession_number,
                    document_url=document_url,
                    html_url=html_url,
                    txt_url=document_url
                )
                
                filings.append(filing)
        
        except Exception as e:
            self.logger.error(f"Error parsing SEC API response: {e}")
        
        self.logger.info(f"✅ Found {len(filings)} matching filings")
        return filings
    
    def download_filing_content(self, filing: SECFiling) -> Optional[str]:
        """Download the content of a SEC filing."""
        self.logger.info(f"📥 Downloading filing: {filing.accession_number}")
        
        # Try text version first
        response = self._make_request(filing.txt_url or filing.document_url)
        
        if response:
            return response.text
        else:
            self.logger.error(f"Failed to download filing: {filing.accession_number}")
            return None
    
    def analyze_filing_with_gemini(self, filing: SECFiling, content: str) -> Dict[str, Any]:
        """
        Analyze SEC filing content using Gemini 2.5-flash.
        
        Args:
            filing: SEC filing metadata
            content: Filing text content
            
        Returns:
            Analysis results from Gemini
        """
        self.logger.info(f"🤖 Analyzing filing with Gemini: {filing.form_type}")
        
        # Prepare analysis prompt
        analysis_prompt = f"""
Analyze this SEC filing and provide structured insights:

FILING METADATA:
- Company: {filing.company_name}
- Form Type: {filing.form_type}
- Filing Date: {filing.filing_date}
- CIK: {filing.cik}

FILING CONTENT (first 4000 characters):
{content[:4000]}...

Please provide a comprehensive analysis including:

1. DOCUMENT_TYPE: What type of SEC filing is this and what does it typically contain?
2. KEY_BUSINESS_INFO: Main business information, revenue, key metrics mentioned
3. RISK_FACTORS: Any risk factors or regulatory concerns mentioned
4. REGULATORY_COMPLIANCE: Compliance matters, regulatory changes, or legal issues
5. FINANCIAL_HIGHLIGHTS: Key financial information or changes
6. MANAGEMENT_DISCUSSION: Important management commentary or outlook
7. REGULATORY_IMPACT: How regulatory changes might impact the business
8. COMPLIANCE_REQUIREMENTS: Any new compliance requirements mentioned
9. SUMMARY: Executive summary of the most important points

Format your response as JSON with these keys: document_type, key_business_info, risk_factors, regulatory_compliance, financial_highlights, management_discussion, regulatory_impact, compliance_requirements, summary
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
                    "filing_metadata": filing.__dict__
                }
            else:
                return {"error": "Gemini analysis failed"}
                
        except Exception as e:
            self.logger.error(f"Gemini analysis error: {e}")
            return {"error": f"Analysis failed: {str(e)}"}
    
    def scrape_recent_filings(self, 
                            companies: List[str], 
                            form_types: List[str] = None,
                            days_back: int = 30,
                            analyze_with_ai: bool = True) -> List[Dict[str, Any]]:
        """
        Scrape recent filings for multiple companies.
        
        Args:
            companies: List of company names or CIKs
            form_types: List of form types to search for
            days_back: Number of days to look back
            analyze_with_ai: Whether to analyze with Gemini
            
        Returns:
            List of filing results with analysis
        """
        self.logger.info(f"🔍 Scraping recent filings for {len(companies)} companies")
        
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)
        
        date_from = start_date.strftime('%Y-%m-%d')
        date_to = end_date.strftime('%Y-%m-%d')
        
        all_results = []
        
        for company in companies:
            try:
                self.logger.info(f"📊 Processing company: {company}")
                
                # Search for filings
                filings = self.search_company_filings(
                    company_name=company if not company.isdigit() else None,
                    cik=company if company.isdigit() else None,
                    form_types=form_types,
                    date_from=date_from,
                    date_to=date_to,
                    max_results=50
                )
                
                # Process each filing
                for filing in filings:
                    try:
                        # Download content
                        content = self.download_filing_content(filing)
                        
                        if content:
                            result = {
                                "company": company,
                                "filing": filing.__dict__,
                                "content_length": len(content),
                                "download_timestamp": datetime.now().isoformat(),
                                "content": content[:10000]  # Store first 10k chars
                            }
                            
                            # AI Analysis
                            if analyze_with_ai and content:
                                ai_analysis = self.analyze_filing_with_gemini(filing, content)
                                result["ai_analysis"] = ai_analysis
                            
                            all_results.append(result)
                            
                        else:
                            self.logger.warning(f"Failed to download: {filing.accession_number}")
                    
                    except Exception as e:
                        self.logger.error(f"Error processing filing {filing.accession_number}: {e}")
            
            except Exception as e:
                self.logger.error(f"Error processing company {company}: {e}")
        
        self.logger.info(f"✅ Scraping completed: {len(all_results)} filings processed")
        return all_results
    
    def save_results_to_database(self, results: List[Dict[str, Any]], db_path: str = "data/sec_filings.db"):
        """Save scraping results to SQLite database."""
        self.logger.info(f"💾 Saving {len(results)} results to database")
        
        # Ensure data directory exists
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create table if not exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sec_filings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company TEXT,
                cik TEXT,
                form_type TEXT,
                filing_date TEXT,
                accession_number TEXT UNIQUE,
                content TEXT,
                ai_analysis TEXT,
                download_timestamp TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Insert results
        for result in results:
            try:
                filing = result.get('filing', {})
                ai_analysis = result.get('ai_analysis', {})
                
                cursor.execute("""
                    INSERT OR REPLACE INTO sec_filings 
                    (company, cik, form_type, filing_date, accession_number, 
                     content, ai_analysis, download_timestamp)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    result.get('company'),
                    filing.get('cik'),
                    filing.get('form_type'),
                    filing.get('filing_date'),
                    filing.get('accession_number'),
                    result.get('content'),
                    json.dumps(ai_analysis, default=str),
                    result.get('download_timestamp')
                ))
                
            except sqlite3.IntegrityError:
                # Filing already exists
                pass
            except Exception as e:
                self.logger.error(f"Error saving result: {e}")
        
        conn.commit()
        conn.close()
        
        self.logger.info("✅ Results saved to database")


def main():
    """Test the SEC EDGAR scraper."""
    print("🧪 Testing SEC EDGAR Scraper")
    print("="*50)
    
    scraper = SECEdgarScraper()
    
    # Test with major companies
    test_companies = ["Apple Inc", "Microsoft Corporation", "Amazon.com Inc"]
    test_form_types = ["10-K", "10-Q", "8-K"]
    
    print(f"🔍 Testing with companies: {test_companies}")
    print(f"📋 Form types: {test_form_types}")
    
    try:
        results = scraper.scrape_recent_filings(
            companies=test_companies[:1],  # Test with just one company
            form_types=test_form_types,
            days_back=90,
            analyze_with_ai=True
        )
        
        print(f"✅ Scraping completed!")
        print(f"📊 Results: {len(results)} filings found")
        
        if results:
            print(f"📄 Sample result:")
            sample = results[0]
            print(f"   Company: {sample.get('company')}")
            print(f"   Form: {sample['filing']['form_type']}")
            print(f"   Date: {sample['filing']['filing_date']}")
            print(f"   Content length: {sample.get('content_length')} chars")
            
            if 'ai_analysis' in sample:
                print(f"   🤖 AI Analysis: Available")
        
        # Save to database
        scraper.save_results_to_database(results)
        
    except Exception as e:
        print(f"❌ Test failed: {e}")


if __name__ == "__main__":
    main()
