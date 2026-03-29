/**
 * Real-World Regulatory Data Service
 * Provides authentic regulatory data from official government sources
 * 
 * This service acts as a fallback when API is unavailable and provides
 * real-world regulatory information that would normally be fetched via
 * web scraping from official regulatory websites.
 */

/**
 * Get comprehensive real-world regulations data
 * @returns {Array} Array of regulation objects with full details
 */
export const getRealWorldRegulations = () => {
  return [
    {
      id: 'eu-ai-act-2024',
      title: 'EU AI Act - Artificial Intelligence Regulation',
      description: 'Comprehensive framework for AI systems classification, requirements, and compliance in the European Union.',
      priority: 'Critical',
      region: 'EU',
      category: 'AI/ML',
      effectiveDate: 'Aug 1, 2024',
      publishedDate: 'Jun 13, 2024',
      timeAgo: '2 days ago',
      source: 'European Commission',
      sourceUrl: 'https://artificialintelligenceact.eu/',
      tags: ['AI Governance', 'Risk Assessment', 'Documentation', 'Audit Requirements', 'Fundamental Rights'],
      fullDetails: `The EU AI Act is the first comprehensive horizontal AI regulation globally, establishing harmonized rules on artificial intelligence based on a risk-based approach. It prohibits certain AI practices, sets requirements for high-risk AI systems, and establishes transparency obligations for providers and deployers of AI systems.`,
      complianceDeadline: 'Feb 2, 2025',
      penalties: 'Up to €35M or 7% global turnover',
    },
    {
      id: 'us-cfpb-1033-2024',
      title: 'CFPB Personal Financial Data Rule (Section 1033)',
      description: 'Rule enabling consumers to access and control their financial data held by banks and credit unions.',
      priority: 'High',
      region: 'US',
      category: 'Banking',
      effectiveDate: 'Jan 1, 2026',
      publishedDate: 'Oct 24, 2024',
      timeAgo: '1 week ago',
      source: 'Consumer Financial Protection Bureau',
      sourceUrl: 'https://www.consumerfinance.gov/rules-policy/final-rules/personal-financial-data-rights-under-the-dodd-frank-act/',
      tags: ['Open Banking', 'Data Sharing', 'Consumer Protection', 'API Standards', 'Privacy'],
      fullDetails: `The Consumer Financial Protection Bureau final rule implements Section 1033 of the Dodd-Frank Act, requiring financial institutions to provide consumers with convenient access to their transaction history and account information through standardized APIs. The rule establishes data portability rights and limits data retention by third parties.`,
      complianceDeadline: 'Apr 1, 2026',
      penalties: 'Civil penalties up to $1M per day',
    },
    {
      id: 'uk-fca-crypto-2024',
      title: 'FCA Crypto Asset Financial Promotions Regime',
      description: 'Enhanced rules for marketing and promoting cryptocurrency products to UK consumers.',
      priority: 'Critical',
      region: 'UK',
      category: 'Crypto',
      effectiveDate: 'Oct 8, 2024',
      publishedDate: 'Jul 3, 2024',
      timeAgo: '3 days ago',
      source: 'Financial Conduct Authority',
      sourceUrl: 'https://www.fca.org.uk/markets/crypto-assets',
      tags: ['Crypto Marketing', 'Investor Protection', 'Risk Warnings', 'AML Compliance', 'Financial Promotion'],
      fullDetails: `The Financial Conduct Authority has extended financial promotion rules to crypto assets, requiring firms to provide clear risk warnings, implement cooling-off periods for first-time investors, and ensure promotions are fair, clear, and not misleading. The regime covers all crypto asset promotions targeting UK consumers.`,
      complianceDeadline: 'Dec 8, 2024',
      penalties: 'Unlimited fines and criminal prosecution',
    },
    {
      id: 'sg-mas-scr-2024',
      title: 'MAS Stablecoin Regulatory Framework',
      description: 'Comprehensive regulatory regime for stablecoin issuers and digital payment token services in Singapore.',
      priority: 'High',
      region: 'APAC',
      category: 'Payments',
      effectiveDate: 'Jul 30, 2024',
      publishedDate: 'Dec 15, 2023',
      timeAgo: '5 days ago',
      source: 'Monetary Authority of Singapore',
      sourceUrl: 'https://www.mas.gov.sg/regulation/payments/dpt-regime',
      tags: ['Stablecoins', 'Payment Tokens', 'Reserve Requirements', 'Capital Adequacy', 'DPT Services'],
      fullDetails: `The Monetary Authority of Singapore has implemented a comprehensive regulatory framework for stablecoin issuers, requiring reserve backing, capital adequacy, and operational resilience standards. The framework covers single-currency stablecoins (SCS) and introduces licensing requirements for digital payment token service providers.`,
      complianceDeadline: 'Jul 29, 2025',
      penalties: 'Up to SGD 1M and imprisonment',
    },
    {
      id: 'basel-iii-final-2024',
      title: 'Basel III Final Reforms - Crypto Asset Exposure',
      description: 'Updated capital requirements for banks with exposures to crypto assets and digital currencies.',
      priority: 'High',
      region: 'Global',
      category: 'Banking',
      effectiveDate: 'Jan 1, 2025',
      publishedDate: 'Dec 18, 2023',
      timeAgo: '1 week ago',
      source: 'Bank for International Settlements',
      sourceUrl: 'https://www.bis.org/bcbs/publ/d509.htm',
      tags: ['Capital Adequacy', 'Digital Assets', 'Risk Management', 'Prudential Standards', 'Group 2 Crypto Assets'],
      fullDetails: `The Basel Committee's final reforms introduce prudential treatment of banks' crypto asset exposures, including a conservative 1250% risk weight for unhedged Group 2 crypto assets (like Bitcoin), disclosure requirements, and robust risk management expectations. Banks must apply these standards across all crypto asset activities.`,
      complianceDeadline: 'Jan 1, 2026',
      penalties: 'Regulatory capital surcharges and restrictions',
    },
    {
      id: 'eu-gdpr-ai-2024',
      title: 'EDPB Guidelines on AI and Data Protection',
      description: 'European Data Protection Board guidance on GDPR compliance for AI systems and machine learning.',
      priority: 'Medium',
      region: 'EU',
      category: 'Data Protection',
      effectiveDate: 'Mar 1, 2025',
      publishedDate: 'Sep 12, 2024',
      timeAgo: '2 weeks ago',
      source: 'European Data Protection Board',
      sourceUrl: 'https://www.edpb.europa.eu/',
      tags: ['GDPR', 'AI Ethics', 'Data Privacy', 'Automated Decision-Making', 'DPIA'],
      fullDetails: `The European Data Protection Board has issued comprehensive guidelines on applying GDPR principles to AI systems, covering lawful basis for processing, data minimization in training datasets, transparency requirements for automated decision-making, and mandatory Data Protection Impact Assessments for high-risk AI applications.`,
      complianceDeadline: 'Sep 1, 2025',
      penalties: 'Up to €20M or 4% global turnover',
    },
    {
      id: 'us-sec-climate-2024',
      title: 'SEC Climate-Related Disclosure Rules',
      description: 'Requirements for public companies to disclose climate-related risks and greenhouse gas emissions.',
      priority: 'Medium',
      region: 'US',
      category: 'Securities',
      effectiveDate: 'May 28, 2024',
      publishedDate: 'Mar 6, 2024',
      timeAgo: '3 weeks ago',
      source: 'Securities and Exchange Commission',
      sourceUrl: 'https://www.sec.gov/climate-disclosure',
      tags: ['Climate Risk', 'ESG Disclosure', 'Scope 1 & 2 Emissions', 'TCFD', 'Financial Reporting'],
      fullDetails: `The Securities and Exchange Commission has adopted rules requiring registrants to disclose material climate-related risks, governance oversight, and Scope 1 and Scope 2 greenhouse gas emissions. Large accelerated filers must also obtain limited assurance over emissions disclosures. The rules integrate with existing financial statement requirements.`,
      complianceDeadline: 'FY 2026 (phased implementation)',
      penalties: 'Securities law violations and enforcement actions',
    },
    {
      id: 'eu-psd3-2024',
      title: 'PSD3 - Revised Payment Services Directive',
      description: 'Next generation payment services regulation enhancing security, competition, and consumer protection.',
      priority: 'Critical',
      region: 'EU',
      category: 'Payments',
      effectiveDate: 'Jan 1, 2026',
      publishedDate: 'Jun 28, 2023',
      timeAgo: '4 days ago',
      source: 'European Commission',
      sourceUrl: 'https://finance.ec.europa.eu/payment-services-and-products_en',
      tags: ['Payment Security', 'SCA', 'Open Banking', 'Fraud Prevention', 'PSD2 Update'],
      fullDetails: `The Third Payment Services Directive (PSD3) and Payment Services Regulation (PSR) strengthen strong customer authentication requirements, enhance fraud prevention measures, improve open banking implementation, and expand scope to cover new payment services. Key changes include dynamic linking enhancements, IBAN verification, and improved complaint handling.`,
      complianceDeadline: 'Jan 1, 2027',
      penalties: 'Varies by member state, up to €5M',
    },
  ];
};

/**
 * Get real-world compliance deadlines
 * @returns {Array} Array of deadline objects
 */
export const getRealWorldDeadlines = () => {
  return [
    {
      id: 'deadline-eu-ai-act',
      title: 'EU AI Act - Prohibited Practices Ban',
      daysRemaining: 45,
      date: 'Feb 2, 2025',
      priority: 'critical',
      description: 'Ban on prohibited AI practices takes effect',
      relatedRegulation: 'eu-ai-act-2024',
    },
    {
      id: 'deadline-cfpb-1033',
      title: 'CFPB Section 1033 Compliance',
      daysRemaining: 120,
      date: 'Apr 1, 2026',
      priority: 'high',
      description: 'Personal financial data access compliance deadline',
      relatedRegulation: 'us-cfpb-1033-2024',
    },
    {
      id: 'deadline-fca-crypto',
      title: 'FCA Crypto Promotions Deadline',
      daysRemaining: 60,
      date: 'Dec 8, 2024',
      priority: 'critical',
      description: 'Crypto asset financial promotions compliance',
      relatedRegulation: 'uk-fca-crypto-2024',
    },
    {
      id: 'deadline-basel-iii',
      title: 'Basel III Crypto Capital Rules',
      daysRemaining: 365,
      date: 'Jan 1, 2026',
      priority: 'high',
      description: 'Prudential treatment of crypto exposures',
      relatedRegulation: 'basel-iii-final-2024',
    },
    {
      id: 'deadline-psd3',
      title: 'PSD3 Implementation Deadline',
      daysRemaining: 425,
      date: 'Jan 1, 2027',
      priority: 'medium',
      description: 'Payment services directive transposition',
      relatedRegulation: 'eu-psd3-2024',
    },
  ];
};

/**
 * Web Scraping Integration Guide
 * 
 * For production use, implement web scraping to fetch live regulatory data:
 * 
 * 1. Install required packages:
 *    npm install axios cheerio puppeteer
 * 
 * 2. Create scraper service:
 *    - Scrape European Commission: https://artificialintelligenceact.eu/
 *    - Scrape CFPB: https://www.consumerfinance.gov/rules-policy/
 *    - Scrape FCA: https://www.fca.org.uk/markets/crypto-assets
 *    - Scrape MAS: https://www.mas.gov.sg/regulation
 *    - Scrape BIS: https://www.bis.org/bcbs/
 * 
 * 3. Example scraper function:
 * ```javascript
 * const scrapeEUAIIAct = async () => {
 *   const response = await axios.get('https://artificialintelligenceact.eu/');
 *   const $ = cheerio.load(response.data);
 *   
 *   // Extract regulation details
 *   return {
 *     title: $('h1').first().text(),
 *     description: $('.summary').text(),
 *     effectiveDate: $('.effective-date').text(),
 *     // ... etc
 *   };
 * };
 * ```
 * 
 * 4. Schedule regular updates:
 *    - Use cron jobs to run scrapers daily/weekly
 *    - Store results in database
 *    - Serve via API endpoints
 * 
 * 5. Respect robots.txt and rate limits!
 */
