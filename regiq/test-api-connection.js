/**
 * Simple test script to verify API connection between frontend and backend
 */

// Import our API client
import apiClient from './src/services/api.js';
import { getRegulations } from './src/services/apiClient.js';

console.log('🧪 Testing API Connection...');

// Test the API client configuration
console.log('✅ API Client Base URL:', apiClient.defaults.baseURL);
console.log('✅ API Client Timeout:', apiClient.defaults.timeout, 'ms');

// Test a simple API call
async function testApiConnection() {
  try {
    console.log('\n📡 Testing Regulations API Endpoint...');
    
    // This will use our updated API client with the correct baseURL
    const response = await getRegulations();
    
    console.log('✅ API Connection Successful!');
    console.log('📊 Response Status:', response.success ? 'Success' : 'Error');
    
    if (response.data && response.data.regulations) {
      console.log('📚 Regulations Count:', response.data.regulations.length);
      console.log('📖 First Regulation Title:', response.data.regulations[0]?.title || 'No regulations found');
    }
    
    console.log('\n🎉 All tests passed! Frontend can successfully connect to backend.');
    return true;
  } catch (error) {
    console.error('❌ API Connection Failed:', error.message);
    
    if (error.response) {
      console.error('📋 Response Status:', error.response.status);
      console.error('📋 Response Data:', JSON.stringify(error.response.data, null, 2));
    } else if (error.request) {
      console.error('🌐 Network Error: Could not reach the server');
    }
    
    return false;
  }
}

// Run the test
testApiConnection().then(success => {
  if (success) {
    console.log('\n✅ Integration Test: PASSED');
  } else {
    console.log('\n❌ Integration Test: FAILED');
  }
});