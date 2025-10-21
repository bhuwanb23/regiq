#!/usr/bin/env python3
"""
REGIQ AI/ML - Regulatory API Connector
Connects to various regulatory APIs (SEC, FINRA, CFTC, etc.)
Integrates with Gemini 2.5-flash for data analysis.
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
from urllib.parse import urljoin
import json
import sqlite3

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from config.env_config import get_env_config
from config.gemini_config import GeminiAPIManager


@dataclass
class APIConfig:
    """API configuration for regulatory services."""
    name: str
    base_url: str
    api_key: Optional[str] = None
    rate_limit_per_minute: int = 60
    requires_auth: bool = False
    auth_header: str = "Authorization"
    auth_prefix: str = "Bearer"


@dataclass
class RegulatoryAPIData:
    """Regulatory API data structure."""
    source_api: str
    data_type: str
    timestamp: str
    raw_data: Dict[str, Any]
    processed_data: Optional[Dict[str, Any]] = None
    record_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class RegulatoryAPIConnector:
    """
    Connector for various regulatory APIs.
    Handles authentication, rate limiting, and data processing.
    """
    
    # Major regulatory APIs
    API_CONFIGS = {
        "SEC_EDGAR": APIConfig(
            name="SEC EDGAR API",
            base_url="https://data.sec.gov",
            rate_limit_per_minute=10,  # SEC has strict rate limits
            requires_auth=False
        ),
        "FINRA_API": APIConfig(
            name="FINRA API",
            base_url="https://api.finra.org",
            rate_limit_per_minute=60,
            requires_auth=True,
            api_key=None  # Would need to be configured
        ),
        "CFTC_API": APIConfig(
            name="CFTC API", 
            base_url="https://publicreporting.cftc.gov",
            rate_limit_per_minute=30,
            requires_auth=False
        ),
        "FDIC_API": APIConfig(
            name="FDIC API",
            base_url="https://banks.data.fdic.gov/api",
            rate_limit_per_minute=60,
            requires_auth=False
        ),
        "FED_API": APIConfig(
            name="Federal Reserve API",
            base_url="https://api.stlouisfed.org/fred",
            rate_limit_per_minute=120,
            requires_auth=True,
            api_key=None  # Would need FRED API key
        )
    }
    
    def __init__(self):
        """Initialize regulatory API connector."""
        self.env_config = get_env_config()
        self.gemini_manager = GeminiAPIManager()
        self.logger = self._setup_logging()
        
        # Rate limiting tracking
        self.request_times = {}
        
        # Load API keys from environment
        self._load_api_keys()
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for API connector."""
        logger = logging.getLogger('regulatory_api_connector')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def _load_api_keys(self):
        """Load API keys from environment variables."""
        # Load API keys if available
        self.API_CONFIGS["FINRA_API"].api_key = self.env_config.get("FINRA_API_KEY")
        self.API_CONFIGS["FED_API"].api_key = self.env_config.get("FRED_API_KEY")
        
        # Log which APIs are configured
        for api_name, config in self.API_CONFIGS.items():
            if config.requires_auth:
                status = "✅ Configured" if config.api_key else "❌ Missing API Key"
                self.logger.info(f"{config.name}: {status}")
    
    def _rate_limit_check(self, api_name: str):
        """Check and enforce rate limiting for specific API."""
        if api_name not in self.request_times:
            self.request_times[api_name] = []
        
        current_time = time.time()
        config = self.API_CONFIGS[api_name]
        
        # Remove requests older than 1 minute
        self.request_times[api_name] = [
            t for t in self.request_times[api_name] 
            if current_time - t < 60
        ]
        
        # Check if we're hitting rate limits
        if len(self.request_times[api_name]) >= config.rate_limit_per_minute:
            sleep_time = 60 - (current_time - self.request_times[api_name][0])
            if sleep_time > 0:
                self.logger.info(f"Rate limiting {api_name}: sleeping {sleep_time:.1f}s")
                time.sleep(sleep_time)
        
        # Record this request
        self.request_times[api_name].append(current_time)
    
    def _make_api_request(self, api_name: str, endpoint: str, params: Dict = None) -> Optional[Dict]:
        """Make authenticated API request with rate limiting."""
        config = self.API_CONFIGS.get(api_name)
        if not config:
            self.logger.error(f"Unknown API: {api_name}")
            return None
        
        # Check authentication
        if config.requires_auth and not config.api_key:
            self.logger.error(f"API key required for {api_name} but not configured")
            return None
        
        # Rate limiting
        self._rate_limit_check(api_name)
        
        # Prepare request
        url = urljoin(config.base_url, endpoint)
        headers = {
            'User-Agent': 'REGIQ AI/ML Research Tool (compliance@regiq.com)',
            'Accept': 'application/json'
        }
        
        # Add authentication if required
        if config.requires_auth and config.api_key:
            headers[config.auth_header] = f"{config.auth_prefix} {config.api_key}"
        
        # Add API key as parameter for some APIs
        if config.api_key and api_name in ["FED_API"]:
            params = params or {}
            params['api_key'] = config.api_key
        
        try:
            self.logger.debug(f"Making {api_name} request: {url}")
            response = requests.get(url, headers=headers, params=params, timeout=30)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:
                self.logger.warning(f"Rate limited by {api_name}")
                time.sleep(60)  # Wait and retry
                return self._make_api_request(api_name, endpoint, params)
            else:
                self.logger.error(f"{api_name} API error {response.status_code}: {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            self.logger.error(f"{api_name} request failed: {e}")
            return None
    
    def fetch_sec_company_data(self, cik: str) -> Optional[RegulatoryAPIData]:
        """Fetch company data from SEC EDGAR API."""
        self.logger.info(f"📊 Fetching SEC data for CIK: {cik}")
        
        # Pad CIK to 10 digits
        cik_padded = str(cik).zfill(10)
        endpoint = f"/submissions/CIK{cik_padded}.json"
        
        data = self._make_api_request("SEC_EDGAR", endpoint)
        
        if data:
            return RegulatoryAPIData(
                source_api="SEC_EDGAR",
                data_type="company_submissions",
                timestamp=datetime.now().isoformat(),
                raw_data=data,
                record_id=cik,
                metadata={"cik": cik, "company_name": data.get("name")}
            )
        
        return None
    
    def fetch_sec_company_facts(self, cik: str) -> Optional[RegulatoryAPIData]:
        """Fetch company facts from SEC EDGAR API."""
        self.logger.info(f"📈 Fetching SEC facts for CIK: {cik}")
        
        cik_padded = str(cik).zfill(10)
        endpoint = f"/api/xbrl/companyfacts/CIK{cik_padded}.json"
        
        data = self._make_api_request("SEC_EDGAR", endpoint)
        
        if data:
            return RegulatoryAPIData(
                source_api="SEC_EDGAR",
                data_type="company_facts",
                timestamp=datetime.now().isoformat(),
                raw_data=data,
                record_id=cik,
                metadata={"cik": cik, "entity_name": data.get("entityName")}
            )
        
        return None
    
    def fetch_fdic_bank_data(self, cert_id: str = None, bank_name: str = None) -> Optional[RegulatoryAPIData]:
        """Fetch bank data from FDIC API."""
        self.logger.info(f"🏦 Fetching FDIC data for: {cert_id or bank_name}")
        
        endpoint = "/institutions"
        params = {
            "format": "json",
            "limit": 100
        }
        
        if cert_id:
            params["filters"] = f"CERT:{cert_id}"
        elif bank_name:
            params["search"] = bank_name
        
        data = self._make_api_request("FDIC_API", endpoint, params)
        
        if data:
            return RegulatoryAPIData(
                source_api="FDIC_API",
                data_type="bank_institutions",
                timestamp=datetime.now().isoformat(),
                raw_data=data,
                record_id=cert_id or bank_name,
                metadata={"search_term": cert_id or bank_name}
            )
        
        return None
    
    def fetch_cftc_swap_data(self, start_date: str = None, end_date: str = None) -> Optional[RegulatoryAPIData]:
        """Fetch swap data from CFTC API."""
        self.logger.info("📊 Fetching CFTC swap data")
        
        # CFTC has various endpoints, using swap dealer data as example
        endpoint = "/api/records/1.json"
        params = {
            "limit": 1000
        }
        
        if start_date:
            params["filters"] = f"as_of_date_in_utc:[{start_date} TO {end_date or '*'}]"
        
        data = self._make_api_request("CFTC_API", endpoint, params)
        
        if data:
            return RegulatoryAPIData(
                source_api="CFTC_API",
                data_type="swap_dealer_data",
                timestamp=datetime.now().isoformat(),
                raw_data=data,
                metadata={"start_date": start_date, "end_date": end_date}
            )
        
        return None
    
    def fetch_fred_economic_data(self, series_id: str) -> Optional[RegulatoryAPIData]:
        """Fetch economic data from Federal Reserve FRED API."""
        if not self.API_CONFIGS["FED_API"].api_key:
            self.logger.warning("FRED API key not configured")
            return None
        
        self.logger.info(f"📈 Fetching FRED data for series: {series_id}")
        
        endpoint = f"/series/observations"
        params = {
            "series_id": series_id,
            "file_type": "json"
        }
        
        data = self._make_api_request("FED_API", endpoint, params)
        
        if data:
            return RegulatoryAPIData(
                source_api="FED_API",
                data_type="economic_series",
                timestamp=datetime.now().isoformat(),
                raw_data=data,
                record_id=series_id,
                metadata={"series_id": series_id}
            )
        
        return None
    
    def analyze_api_data_with_gemini(self, api_data: RegulatoryAPIData) -> Dict[str, Any]:
        """
        Analyze regulatory API data using Gemini 2.5-flash.
        
        Args:
            api_data: Regulatory API data to analyze
            
        Returns:
            Analysis results from Gemini
        """
        self.logger.info(f"🤖 Analyzing {api_data.source_api} data with Gemini")
        
        # Prepare analysis prompt based on data type
        if api_data.data_type == "company_submissions":
            analysis_prompt = self._create_sec_submissions_prompt(api_data)
        elif api_data.data_type == "company_facts":
            analysis_prompt = self._create_sec_facts_prompt(api_data)
        elif api_data.data_type == "bank_institutions":
            analysis_prompt = self._create_fdic_prompt(api_data)
        else:
            analysis_prompt = self._create_generic_prompt(api_data)
        
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
                    "data_source": api_data.source_api,
                    "data_type": api_data.data_type
                }
            else:
                return {"error": "Gemini analysis failed"}
                
        except Exception as e:
            self.logger.error(f"Gemini analysis error: {e}")
            return {"error": f"Analysis failed: {str(e)}"}
    
    def _create_sec_submissions_prompt(self, api_data: RegulatoryAPIData) -> str:
        """Create analysis prompt for SEC submissions data."""
        data_sample = json.dumps(api_data.raw_data, indent=2)[:3000]
        
        return f"""
Analyze this SEC company submissions data and provide regulatory insights:

DATA SOURCE: SEC EDGAR API - Company Submissions
COMPANY: {api_data.metadata.get('company_name', 'Unknown')}
CIK: {api_data.metadata.get('cik')}

DATA SAMPLE:
{data_sample}...

Please analyze and provide:

1. COMPANY_PROFILE: Basic company information and business description
2. FILING_PATTERNS: Analysis of filing frequency and types
3. RECENT_ACTIVITY: Recent filing activity and any notable changes
4. COMPLIANCE_STATUS: Assessment of regulatory compliance based on filings
5. RISK_INDICATORS: Any red flags or risk indicators in filing patterns
6. REGULATORY_FOCUS: Key regulatory areas the company is subject to
7. BUSINESS_CHANGES: Any significant business changes indicated by filings
8. SUMMARY: Executive summary of regulatory and compliance insights

Format as JSON with these keys: company_profile, filing_patterns, recent_activity, compliance_status, risk_indicators, regulatory_focus, business_changes, summary
"""
    
    def _create_sec_facts_prompt(self, api_data: RegulatoryAPIData) -> str:
        """Create analysis prompt for SEC company facts data."""
        data_sample = json.dumps(api_data.raw_data, indent=2)[:3000]
        
        return f"""
Analyze this SEC company facts data and provide financial regulatory insights:

DATA SOURCE: SEC EDGAR API - Company Facts
ENTITY: {api_data.metadata.get('entity_name', 'Unknown')}

FINANCIAL DATA SAMPLE:
{data_sample}...

Please analyze and provide:

1. FINANCIAL_HEALTH: Assessment of financial health based on reported facts
2. KEY_METRICS: Important financial metrics and trends
3. REGULATORY_RATIOS: Key regulatory ratios if applicable
4. COMPLIANCE_METRICS: Metrics related to regulatory compliance
5. TREND_ANALYSIS: Trends in key financial indicators
6. RISK_ASSESSMENT: Financial risk assessment based on the data
7. REGULATORY_IMPLICATIONS: Implications for regulatory compliance
8. SUMMARY: Executive summary of financial regulatory status

Format as JSON with these keys: financial_health, key_metrics, regulatory_ratios, compliance_metrics, trend_analysis, risk_assessment, regulatory_implications, summary
"""
    
    def _create_fdic_prompt(self, api_data: RegulatoryAPIData) -> str:
        """Create analysis prompt for FDIC bank data."""
        data_sample = json.dumps(api_data.raw_data, indent=2)[:3000]
        
        return f"""
Analyze this FDIC bank institution data and provide banking regulatory insights:

DATA SOURCE: FDIC API - Bank Institutions
SEARCH TERM: {api_data.metadata.get('search_term')}

BANK DATA SAMPLE:
{data_sample}...

Please analyze and provide:

1. INSTITUTION_PROFILE: Bank profile and basic information
2. REGULATORY_STATUS: Current regulatory status and classifications
3. CAPITAL_ADEQUACY: Capital adequacy and financial strength indicators
4. COMPLIANCE_HISTORY: Any compliance issues or regulatory actions
5. RISK_PROFILE: Risk assessment based on available data
6. SUPERVISORY_ACTIONS: Any supervisory actions or enforcement
7. MARKET_POSITION: Market position and competitive standing
8. SUMMARY: Executive summary of regulatory and supervisory status

Format as JSON with these keys: institution_profile, regulatory_status, capital_adequacy, compliance_history, risk_profile, supervisory_actions, market_position, summary
"""
    
    def _create_generic_prompt(self, api_data: RegulatoryAPIData) -> str:
        """Create generic analysis prompt for other data types."""
        data_sample = json.dumps(api_data.raw_data, indent=2)[:3000]
        
        return f"""
Analyze this regulatory API data and provide insights:

DATA SOURCE: {api_data.source_api}
DATA TYPE: {api_data.data_type}
TIMESTAMP: {api_data.timestamp}

DATA SAMPLE:
{data_sample}...

Please analyze and provide:

1. DATA_OVERVIEW: Overview of the data and its regulatory significance
2. KEY_INSIGHTS: Key insights from the data
3. REGULATORY_IMPLICATIONS: Regulatory implications and compliance aspects
4. TRENDS_PATTERNS: Any trends or patterns in the data
5. RISK_FACTORS: Risk factors identified in the data
6. COMPLIANCE_ASPECTS: Compliance-related aspects
7. RECOMMENDATIONS: Recommendations based on the analysis
8. SUMMARY: Executive summary of findings

Format as JSON with these keys: data_overview, key_insights, regulatory_implications, trends_patterns, risk_factors, compliance_aspects, recommendations, summary
"""
    
    def batch_fetch_regulatory_data(self, 
                                  data_requests: List[Dict[str, Any]],
                                  analyze_with_ai: bool = True) -> List[Dict[str, Any]]:
        """
        Batch fetch data from multiple regulatory APIs.
        
        Args:
            data_requests: List of data request specifications
            analyze_with_ai: Whether to analyze with Gemini
            
        Returns:
            List of results with analysis
        """
        self.logger.info(f"📊 Batch fetching {len(data_requests)} regulatory data requests")
        
        results = []
        
        for request in data_requests:
            try:
                api_name = request.get("api")
                request_type = request.get("type")
                params = request.get("params", {})
                
                # Route to appropriate fetch method
                api_data = None
                
                if api_name == "SEC_EDGAR":
                    if request_type == "company_data":
                        api_data = self.fetch_sec_company_data(params.get("cik"))
                    elif request_type == "company_facts":
                        api_data = self.fetch_sec_company_facts(params.get("cik"))
                
                elif api_name == "FDIC_API":
                    api_data = self.fetch_fdic_bank_data(
                        params.get("cert_id"), 
                        params.get("bank_name")
                    )
                
                elif api_name == "CFTC_API":
                    api_data = self.fetch_cftc_swap_data(
                        params.get("start_date"), 
                        params.get("end_date")
                    )
                
                elif api_name == "FED_API":
                    api_data = self.fetch_fred_economic_data(params.get("series_id"))
                
                if api_data:
                    result = {
                        "request": request,
                        "api_data": api_data.__dict__,
                        "fetch_timestamp": datetime.now().isoformat()
                    }
                    
                    # AI Analysis
                    if analyze_with_ai:
                        ai_analysis = self.analyze_api_data_with_gemini(api_data)
                        result["ai_analysis"] = ai_analysis
                    
                    results.append(result)
                
            except Exception as e:
                self.logger.error(f"Error processing request {request}: {e}")
        
        self.logger.info(f"✅ Batch fetch completed: {len(results)} successful")
        return results
    
    def save_api_results_to_database(self, results: List[Dict[str, Any]], db_path: str = "data/regulatory_api_data.db"):
        """Save API results to SQLite database."""
        self.logger.info(f"💾 Saving {len(results)} API results to database")
        
        # Ensure data directory exists
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create table if not exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS regulatory_api_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_api TEXT,
                data_type TEXT,
                record_id TEXT,
                raw_data TEXT,
                ai_analysis TEXT,
                fetch_timestamp TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Insert results
        for result in results:
            try:
                api_data = result.get('api_data', {})
                ai_analysis = result.get('ai_analysis', {})
                
                cursor.execute("""
                    INSERT INTO regulatory_api_data 
                    (source_api, data_type, record_id, raw_data, ai_analysis, fetch_timestamp)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    api_data.get('source_api'),
                    api_data.get('data_type'),
                    api_data.get('record_id'),
                    json.dumps(api_data.get('raw_data'), default=str),
                    json.dumps(ai_analysis, default=str),
                    result.get('fetch_timestamp')
                ))
                
            except Exception as e:
                self.logger.error(f"Error saving API result: {e}")
        
        conn.commit()
        conn.close()
        
        self.logger.info("✅ API results saved to database")


def main():
    """Test the regulatory API connector."""
    print("🧪 Testing Regulatory API Connector")
    print("="*50)
    
    connector = RegulatoryAPIConnector()
    
    # Test data requests
    test_requests = [
        {
            "api": "SEC_EDGAR",
            "type": "company_data",
            "params": {"cik": "320193"}  # Apple Inc
        },
        {
            "api": "FDIC_API", 
            "type": "bank_data",
            "params": {"bank_name": "JPMorgan Chase"}
        }
    ]
    
    print(f"📊 Testing with {len(test_requests)} API requests")
    
    try:
        results = connector.batch_fetch_regulatory_data(
            test_requests,
            analyze_with_ai=True
        )
        
        print(f"✅ API testing completed!")
        print(f"📊 Results: {len(results)} successful requests")
        
        if results:
            print(f"📄 Sample result:")
            sample = results[0]
            api_data = sample['api_data']
            print(f"   API: {api_data['source_api']}")
            print(f"   Type: {api_data['data_type']}")
            print(f"   Record ID: {api_data.get('record_id')}")
            
            if 'ai_analysis' in sample:
                print(f"   🤖 AI Analysis: Available")
        
        # Save to database
        connector.save_api_results_to_database(results)
        
    except Exception as e:
        print(f"❌ Test failed: {e}")


if __name__ == "__main__":
    main()
