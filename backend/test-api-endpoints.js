#!/usr/bin/env node

/**
 * API Endpoint Alignment Test
 * Verifies all frontend ↔ backend endpoints are working
 */

const axios = require('axios');

// Configuration
const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:3000';
const TEST_TIMEOUT = 5000;

// Test cases organized by category
const testCases = [
  {
    category: 'Health Check',
    tests: [
      {
        name: 'Backend Health',
        method: 'GET',
        endpoint: '/health',
        expectedStatus: 200
      }
    ]
  },
  
  {
    category: 'Regulatory Intelligence',
    tests: [
      {
        name: 'Get Regulations',
        method: 'GET',
        endpoint: '/regulatory/regulations',
        expectedStatus: 200
      },
      {
        name: 'Get Regulation Categories',
        method: 'GET',
        endpoint: '/regulatory/regulations/categories',
        expectedStatus: 200
      },
      {
        name: 'Get Regulation Deadlines',
        method: 'GET',
        endpoint: '/regulatory/regulations/deadlines',
        expectedStatus: 200
      }
    ]
  },
  
  {
    category: 'Bias Analysis',
    tests: [
      {
        name: 'Get Bias Reports',
        method: 'GET',
        endpoint: '/api/bias/reports',
        expectedStatus: 200
      },
      {
        name: 'Get Bias Scoring',
        method: 'GET',
        endpoint: '/api/bias/scoring',
        expectedStatus: 200
      },
      {
        name: 'Get Bias Visualization',
        method: 'GET',
        endpoint: '/api/bias/visualization',
        expectedStatus: 200
      }
    ]
  },
  
  {
    category: 'Risk Simulation',
    tests: [
      {
        name: 'Get Risk Simulations',
        method: 'GET',
        endpoint: '/api/risk/simulations',
        expectedStatus: 200
      },
      {
        name: 'Get Risk Scenarios',
        method: 'GET',
        endpoint: '/api/risk/scenarios',
        expectedStatus: 200
      },
      {
        name: 'Get Regulatory Frameworks',
        method: 'GET',
        endpoint: '/api/risk/frameworks',
        expectedStatus: 200
      }
    ]
  },
  
  {
    category: 'Report Generation',
    tests: [
      {
        name: 'Get Reports',
        method: 'GET',
        endpoint: '/api/reports',
        expectedStatus: 200
      },
      {
        name: 'Get Report Glossary',
        method: 'GET',
        endpoint: '/api/reports/glossary',
        expectedStatus: 200
      },
      {
        name: 'Get Report Templates',
        method: 'GET',
        endpoint: '/api/reports/templates',
        expectedStatus: 200
      }
    ]
  },
  
  {
    category: 'User Management',
    tests: [
      {
        name: 'Get Users (requires auth)',
        method: 'GET',
        endpoint: '/api/users',
        expectedStatus: 401, // Requires authentication
        note: 'This is expected - needs valid JWT token'
      },
      {
        name: 'Get User Preferences (requires auth)',
        method: 'GET',
        endpoint: '/api/users/preferences',
        expectedStatus: 401, // Requires authentication
        note: 'This is expected - needs valid JWT token'
      }
    ]
  },
  
  {
    category: 'Notifications',
    tests: [
      {
        name: 'Get Notifications (requires auth)',
        method: 'GET',
        endpoint: '/api/notifications',
        expectedStatus: 401, // Requires authentication
        note: 'This is expected - needs valid JWT token'
      },
      {
        name: 'Get Notification Preferences (requires auth)',
        method: 'GET',
        endpoint: '/api/notifications/preferences',
        expectedStatus: 401, // Requires authentication
        note: 'This is expected - needs valid JWT token'
      }
    ]
  }
];

// Results tracking
const results = {
  total: 0,
  passed: 0,
  failed: 0,
  errors: []
};

/**
 * Test single endpoint
 */
async function testEndpoint(category, test) {
  const { name, method, endpoint, expectedStatus, note } = test;
  const url = `${BACKEND_URL}${endpoint}`;
  
  try {
    const response = await axios({
      method,
      url,
      timeout: TEST_TIMEOUT,
      validateStatus: () => true // Don't throw on error status
    });
    
    results.total++;
    
    if (response.status === expectedStatus) {
      console.log(`✅ ${category}: ${name}`);
      if (note) {
        console.log(`   ℹ️  Note: ${note}`);
      }
      results.passed++;
      return true;
    } else {
      console.log(`⚠️  ${category}: ${name} - Status: ${response.status} (expected ${expectedStatus})`);
      results.failed++;
      results.errors.push({
        category,
        name,
        type: 'status_mismatch',
        expected: expectedStatus,
        actual: response.status
      });
      return false;
    }
  } catch (error) {
    results.total++;
    results.failed++;
    console.log(`❌ ${category}: ${name} - ${error.message}`);
    results.errors.push({
      category,
      name,
      type: 'error',
      message: error.message
    });
    return false;
  }
}

/**
 * Run all tests
 */
async function runTests() {
  console.log('╔════════════════════════════════════════════╗');
  console.log('║     REGIQ API Endpoint Alignment Test     ║');
  console.log('╚════════════════════════════════════════════╝\n');
  console.log(`Backend URL: ${BACKEND_URL}`);
  console.log(`Timeout: ${TEST_TIMEOUT}ms\n`);
  
  // First check if backend is running
  console.log('📋 Checking backend availability...\n');
  try {
    await axios.get(`${BACKEND_URL}/health`, { timeout: 5000 });
    console.log('✅ Backend is running\n');
  } catch (error) {
    console.log('❌ Backend not available!');
    console.log(`   Error: ${error.message}`);
    console.log('\n   Please start the backend server:');
    console.log('   cd backend && npm run dev\n');
    return;
  }
  
  // Run tests by category
  console.log('📋 Testing API endpoints...\n');
  
  for (const category of testCases) {
    console.log(`\n${category.category}:`);
    console.log('─'.repeat(40));
    
    for (const test of category.tests) {
      await testEndpoint(category.category, test);
      await new Promise(resolve => setTimeout(resolve, 200)); // Small delay between tests
    }
  }
  
  // Print summary
  console.log('\n╔════════════════════════════════════════════╗');
  console.log('║              TEST SUMMARY                  ║');
  console.log('╚════════════════════════════════════════════╝\n');
  console.log(`Total Tests: ${results.total}`);
  console.log(`Passed: ${results.passed} ✅`);
  console.log(`Failed: ${results.failed} ❌`);
  console.log(`Success Rate: ${((results.passed / results.total) * 100).toFixed(1)}%\n`);
  
  if (results.failed > 0) {
    console.log('📝 Issues Found:\n');
    results.errors.forEach((error, index) => {
      console.log(`${index + 1}. ${error.category} - ${error.name}`);
      if (error.type === 'status_mismatch') {
        console.log(`   Expected status ${error.expected}, got ${error.actual}`);
      } else {
        console.log(`   Error: ${error.message}`);
      }
    });
    
    console.log('\n💡 Recommendations:');
    console.log('  • Check if backend routes are properly configured');
    console.log('  • Verify database connection if getting 500 errors');
    console.log('  • Check CORS configuration for cross-origin requests');
    console.log('  • Review API_ENDPOINT_MAPPING_COMPLETE.md for details\n');
  } else {
    console.log('🎉 All endpoints are working correctly!\n');
    console.log('✅ Priority 2: API Endpoint Alignment - COMPLETE\n');
  }
}

// Run the tests
runTests().catch(console.error);
