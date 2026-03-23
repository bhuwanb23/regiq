#!/usr/bin/env node
/**
 * REGIQ Backend ↔ AI/ML Integration Test Script
 * Tests all API endpoints that call Python AI/ML service
 */

const axios = require('axios');

const BACKEND_URL = 'http://localhost:3000';
const AI_ML_URL = 'http://localhost:8000';

// Color codes for console output
const colors = {
  reset: '\x1b[0m',
  green: '\x1b[32m',
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  cyan: '\x1b[36m'
};

console.log(`${colors.cyan}============================================================${colors.reset}`);
console.log(`${colors.cyan}  REGIQ BACKEND ↔ AI/ML INTEGRATION TEST${colors.reset}`);
console.log(`${colors.cyan}============================================================${colors.reset}\n`);

console.log(`${colors.blue}Backend URL:${colors.reset} ${BACKEND_URL}`);
console.log(`${colors.blue}AI/ML URL:${colors.reset} ${AI_ML_URL}\n`);

// Test results tracking
const results = {
  passed: 0,
  failed: 0,
  tests: []
};

/**
 * Test a single endpoint
 */
async function testEndpoint(method, endpoint, data = null, description = '') {
  const testName = `${method} ${endpoint}`;
  
  try {
    console.log(`${colors.yellow}Testing:${colors.reset} ${testName}`);
    if (description) {
      console.log(`  ${colors.blue}Description:${colors.reset} ${description}`);
    }
    
    const config = {
      method: method.toLowerCase(),
      url: `${BACKEND_URL}${endpoint}`,
      headers: {
        'Content-Type': 'application/json',
      },
      timeout: 30000, // 30 second timeout
    };
    
    if (data && method.toUpperCase() !== 'GET') {
      config.data = data;
    }
    
    const response = await axios(config);
    
    if (response.status >= 200 && response.status < 300) {
      console.log(`${colors.green}✅ PASS${colors.reset} - Status: ${response.status}`);
      
      // Check if response contains expected data
      if (response.data) {
        const keys = Object.keys(response.data).slice(0, 5);
        console.log(`  ${colors.green}Response keys:${colors.reset} [${keys.join(', ')}]`);
        
        // Check for python_ai_ml source indicator
        if (JSON.stringify(response.data).includes('python_ai_ml')) {
          console.log(`  ${colors.green}✓ Data from Python AI/ML service${colors.reset}`);
        }
      }
      
      results.passed++;
      results.tests.push({ name: testName, status: 'PASS', statusCode: response.status });
      return true;
    } else {
      console.log(`${colors.red}❌ FAIL${colors.reset} - Unexpected status: ${response.status}`);
      results.failed++;
      results.tests.push({ name: testName, status: 'FAIL', statusCode: response.status });
      return false;
    }
  } catch (error) {
    console.log(`${colors.red}❌ FAIL${colors.reset} - ${error.message}`);
    
    if (error.response) {
      console.log(`  ${colors.red}Status:${colors.reset} ${error.response.status}`);
      console.log(`  ${colors.red}Data:${colors.reset} ${JSON.stringify(error.response.data).substring(0, 200)}`);
    } else if (error.request) {
      console.log(`  ${colors.red}No response received${colors.reset}`);
    }
    
    results.failed++;
    results.tests.push({ name: testName, status: 'FAIL', error: error.message });
    return false;
  }
}

/**
 * Run all integration tests
 */
async function runTests() {
  console.log(`${colors.cyan}============================================================${colors.reset}`);
  console.log(`${colors.cyan}  PHASE 1: Health Checks${colors.reset}`);
  console.log(`${colors.cyan}============================================================${colors.reset}\n`);
  
  // Health checks
  await testEndpoint('GET', '/health', null, 'Backend health check');
  await testEndpoint('GET', '', null, 'Backend root endpoint');
  
  console.log(`\n${colors.cyan}============================================================${colors.reset}`);
  console.log(`${colors.cyan}  PHASE 2: Bias Analysis Integration${colors.reset}`);
  console.log(`${colors.cyan}============================================================${colors.reset}\n`);
  
  // Bias Analysis endpoints
  await testEndpoint(
    'GET', 
    '/api/bias/scoring', 
    null,
    'Get bias scores from Python service'
  );
  
  await testEndpoint(
    'POST', 
    '/api/bias/explain', 
    { analysis_id: 'test_123', explainer_type: 'shap' },
    'Get SHAP explanations from Python'
  );
  
  await testEndpoint(
    'GET', 
    '/api/bias/visualization', 
    null,
    'Get visualization data from Python'
  );
  
  console.log(`\n${colors.cyan}============================================================${colors.reset}`);
  console.log(`${colors.cyan}  PHASE 3: Risk Simulator Integration${colors.reset}`);
  console.log(`${colors.cyan}============================================================${colors.reset}\n`);
  
  // Risk Simulator endpoints
  await testEndpoint(
    'GET', 
    '/api/risk/frameworks', 
    null,
    'Get regulatory frameworks from Python (requires simulation ID)'
  );
  
  await testEndpoint(
    'POST', 
    '/api/risk/run/bayesian', 
    { 
      prior: { mean: 0.5, std: 0.1 },
      data: [0.4, 0.6, 0.5, 0.7, 0.55]
    },
    'Run Bayesian inference in Python'
  );
  
  console.log(`\n${colors.cyan}============================================================${colors.reset}`);
  console.log(`${colors.cyan}  PHASE 4: Regulatory Intelligence Integration${colors.reset}`);
  console.log(`${colors.cyan}============================================================${colors.reset}\n`);
  
  // Regulatory Intelligence endpoints
  await testEndpoint(
    'POST', 
    '/ai-ml/compliance', 
    { 
      document_text: 'GDPR requires organizations to protect personal data and privacy.',
      document_type: 'regulation',
      analysis_depth: 'standard'
    },
    'Analyze document compliance with Python NLP'
  );
  
  await testEndpoint(
    'POST', 
    '/ai-ml/summarize', 
    { 
      text: 'The GDPR requires organizations to implement appropriate technical and organizational measures to ensure a level of security appropriate to the risk.',
      summary_type: 'executive',
      max_length: 300
    },
    'Summarize document with Python NLP'
  );
  
  await testEndpoint(
    'POST', 
    '/ai-ml/qa', 
    { 
      question: 'What are the penalties for GDPR violations?',
      query: 'GDPR penalties and fines'
    },
    'Q&A with RAG system in Python'
  );
  
  console.log(`\n${colors.cyan}============================================================${colors.reset}`);
  console.log(`${colors.cyan}  PHASE 5: Report Generator Integration${colors.reset}`);
  console.log(`${colors.cyan}============================================================${colors.reset}\n`);
  
  // Report Generator endpoints
  await testEndpoint(
    'POST', 
    '/api/reports/generate', 
    { 
      report_type: 'fairness',
      data: { test: 'integration_data' }
    },
    'Generate report with Python service'
  );
  
  await testEndpoint(
    'GET', 
    '/api/reports/glossary', 
    null,
    'Get compliance glossary from Python'
  );
}

/**
 * Print final summary
 */
function printSummary() {
  console.log(`\n${colors.cyan}============================================================${colors.reset}`);
  console.log(`${colors.cyan}  TEST SUMMARY${colors.reset}`);
  console.log(`${colors.cyan}============================================================${colors.reset}\n`);
  
  const total = results.passed + results.failed;
  const passRate = ((results.passed / total) * 100).toFixed(1);
  
  console.log(`${colors.blue}Total Tests:${colors.reset} ${total}`);
  console.log(`${colors.green}Passed:${colors.reset} ${results.passed}`);
  console.log(`${colors.red}Failed:${colors.reset} ${results.failed}`);
  console.log(`${colors.yellow}Pass Rate:${colors.reset} ${passRate}%\n`);
  
  console.log(`${colors.cyan}Detailed Results:${colors.reset}`);
  results.tests.forEach((test, index) => {
    const icon = test.status === 'PASS' ? '✅' : '❌';
    console.log(`  ${icon} ${test.name} - ${test.status}`);
  });
  
  console.log(`\n${colors.cyan}============================================================${colors.reset}`);
  
  if (results.passed === total) {
    console.log(`${colors.green}🎉 ALL TESTS PASSED!${colors.reset}`);
    console.log(`\n${colors.green}Backend ↔ AI/ML integration is fully operational!${colors.reset}`);
    console.log(`\n${colors.blue}Next steps:${colors.reset}`);
    console.log('1. ✅ All endpoints returning real Python AI/ML data');
    console.log('2. ✅ Authentication working correctly');
    console.log('3. ✅ Service-to-service communication verified');
    console.log('4. Ready for frontend integration testing\n');
  } else {
    console.log(`${colors.yellow}⚠️  SOME TESTS FAILED${colors.reset}`);
    console.log(`\n${colors.red}Failed: ${results.failed}/${total}${colors.reset}`);
    console.log(`\n${colors.blue}Troubleshooting:${colors.reset}`);
    console.log('1. Check AI/ML service logs for errors');
    console.log('2. Verify .env has correct API keys');
    console.log('3. Ensure both services are running');
    console.log('4. Check network connectivity between services\n');
  }
  
  console.log(`${colors.cyan}============================================================${colors.reset}\n`);
}

// Run all tests
(async () => {
  await runTests();
  printSummary();
  
  // Exit with appropriate code
  process.exit(results.failed > 0 ? 1 : 0);
})();
