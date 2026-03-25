#!/usr/bin/env node

/**
 * CORS Configuration Test Script
 * Tests backend CORS setup with various origins
 */

const axios = require('axios');

// Configuration
const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:3000';
const TEST_DELAY_MS = 1000;

// Test origins (simulating different frontend apps)
const testOrigins = [
  {
    name: 'Expo Go',
    origin: 'http://localhost:19000',
    shouldPass: true
  },
  {
    name: 'Expo Web',
    origin: 'http://localhost:19002',
    shouldPass: true
  },
  {
    name: 'React Native Metro',
    origin: 'http://localhost:8081',
    shouldPass: true
  },
  {
    name: 'Web Build',
    origin: 'http://localhost:3000',
    shouldPass: true
  },
  {
    name: 'Unauthorized Origin',
    origin: 'http://evil.com',
    shouldPass: false
  }
];

// Results tracking
const results = {
  passed: 0,
  failed: 0,
  tests: []
};

/**
 * Test CORS with specific origin
 */
async function testCorsOrigin(testCase) {
  const { name, origin, shouldPass } = testCase;
  
  try {
    // Send OPTIONS request (CORS preflight)
    const response = await axios.options(`${BACKEND_URL}/health`, {
      headers: {
        'Origin': origin,
        'Access-Control-Request-Method': 'GET',
        'Access-Control-Request-Headers': 'Content-Type, Authorization'
      },
      timeout: 5000
    });
    
    // Check CORS headers in response
    const corsHeaders = {
      'access-control-allow-origin': response.headers['access-control-allow-origin'],
      'access-control-allow-methods': response.headers['access-control-allow-methods'],
      'access-control-allow-headers': response.headers['access-control-allow-headers'],
      'access-control-allow-credentials': response.headers['access-control-allow-credentials']
    };
    
    // Verify if origin is allowed
    const originAllowed = corsHeaders['access-control-allow-origin'] === origin;
    
    if (shouldPass && originAllowed) {
      console.log(`✅ ${name}: PASSED (allowed)`);
      results.passed++;
      results.tests.push({
        name,
        status: 'PASS',
        expected: 'allowed',
        actual: 'allowed',
        headers: corsHeaders
      });
      return true;
    } else if (!shouldPass && !originAllowed) {
      console.log(`✅ ${name}: PASSED (correctly blocked)`);
      results.passed++;
      results.tests.push({
        name,
        status: 'PASS',
        expected: 'blocked',
        actual: 'blocked',
        headers: corsHeaders
      });
      return true;
    } else {
      console.log(`❌ ${name}: FAILED`);
      console.log(`   Expected: ${shouldPass ? 'allowed' : 'blocked'}`);
      console.log(`   Actual: ${originAllowed ? 'allowed' : 'blocked'}`);
      results.failed++;
      results.tests.push({
        name,
        status: 'FAIL',
        expected: shouldPass ? 'allowed' : 'blocked',
        actual: originAllowed ? 'allowed' : 'blocked',
        headers: corsHeaders
      });
      return false;
    }
  } catch (error) {
    // Network error or CORS blocked
    if (!shouldPass) {
      console.log(`✅ ${name}: PASSED (correctly blocked - ${error.message})`);
      results.passed++;
      results.tests.push({
        name,
        status: 'PASS',
        expected: 'blocked',
        actual: 'blocked (network error)',
        error: error.message
      });
      return true;
    } else {
      console.log(`❌ ${name}: FAILED (${error.message})`);
      results.failed++;
      results.tests.push({
        name,
        status: 'FAIL',
        expected: 'allowed',
        actual: 'error',
        error: error.message
      });
      return false;
    }
  }
}

/**
 * Test basic health endpoint (no CORS headers needed)
 */
async function testHealthEndpoint() {
  console.log('\n📋 Testing basic connectivity...\n');
  
  try {
    const response = await axios.get(`${BACKEND_URL}/health`, {
      timeout: 5000
    });
    
    console.log('✅ Backend health check: PASSED');
    console.log(`   Status: ${response.data.status}`);
    console.log(`   Timestamp: ${response.data.timestamp}`);
    return true;
  } catch (error) {
    console.log('❌ Backend health check: FAILED');
    console.log(`   Error: ${error.message}`);
    console.log('\n   Make sure backend server is running on port 3000');
    console.log('   Run: cd backend && npm run dev\n');
    return false;
  }
}

/**
 * Main test runner
 */
async function runTests() {
  console.log('╔════════════════════════════════════════════╗');
  console.log('║   REGIQ CORS Configuration Test Suite     ║');
  console.log('╚════════════════════════════════════════════╝\n');
  console.log(`Backend URL: ${BACKEND_URL}`);
  console.log(`Test Delay: ${TEST_DELAY_MS}ms\n`);
  
  // First, check if backend is running
  const isRunning = await testHealthEndpoint();
  if (!isRunning) {
    console.log('\n❌ Tests aborted: Backend not available\n');
    return;
  }
  
  console.log('\n📋 Testing CORS configurations...\n');
  
  // Run CORS tests with delay between each
  for (const testCase of testOrigins) {
    await testCorsOrigin(testCase);
    await new Promise(resolve => setTimeout(resolve, TEST_DELAY_MS));
  }
  
  // Print summary
  console.log('\n╔════════════════════════════════════════════╗');
  console.log('║              TEST SUMMARY                  ║');
  console.log('╚════════════════════════════════════════════╝\n');
  console.log(`Total Tests: ${results.passed + results.failed}`);
  console.log(`Passed: ${results.passed} ✅`);
  console.log(`Failed: ${results.failed} ❌`);
  console.log(`Success Rate: ${((results.passed / (results.passed + results.failed)) * 100).toFixed(1)}%\n`);
  
  if (results.failed > 0) {
    console.log('📝 Failed Tests Details:\n');
    results.tests.filter(t => t.status === 'FAIL').forEach(test => {
      console.log(`  • ${test.name}: Expected ${test.expected}, got ${test.actual}`);
    });
    console.log('\n💡 Troubleshooting Tips:');
    console.log('  1. Check ALLOWED_ORIGINS in backend/.env');
    console.log('  2. Restart backend server after changing .env');
    console.log('  3. Verify origin URLs match exactly (including trailing slash)');
    console.log('  4. Check browser console for detailed CORS errors\n');
  } else {
    console.log('🎉 All CORS tests passed!\n');
  }
}

// Run the tests
runTests().catch(console.error);
