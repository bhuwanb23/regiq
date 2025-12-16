/**
 * Test file for API Client Setup
 * This is a simple integration test to verify our API client is properly configured
 */

import apiClient from '../api';
import { login, isAuthenticated } from '../authService';
import { storeToken, getToken, removeToken } from '../../utils/storage';

// Mock localStorage for testing
global.localStorage = {
  store: {},
  getItem(key) {
    return this.store[key] || null;
  },
  setItem(key, value) {
    this.store[key] = value.toString();
  },
  removeItem(key) {
    delete this.store[key];
  },
  clear() {
    this.store = {};
  }
};

describe('API Client Setup', () => {
  beforeEach(() => {
    // Clear localStorage before each test
    global.localStorage.clear();
  });

  test('should create axios instance with correct baseURL', () => {
    expect(apiClient.defaults.baseURL).toBe('http://localhost:3000/api');
  });

  test('should have timeout set to 10 seconds', () => {
    expect(apiClient.defaults.timeout).toBe(10000);
  });

  test('should have JSON content type header', () => {
    expect(apiClient.defaults.headers['Content-Type']).toBe('application/json');
  });

  test('should store and retrieve token from storage', async () => {
    const testToken = 'test-jwt-token';
    
    // Store token
    await storeToken(testToken);
    
    // Retrieve token
    const retrievedToken = await getToken();
    
    expect(retrievedToken).toBe(testToken);
  });

  test('should remove token from storage', async () => {
    const testToken = 'test-jwt-token';
    
    // Store token
    await storeToken(testToken);
    
    // Verify token is stored
    let retrievedToken = await getToken();
    expect(retrievedToken).toBe(testToken);
    
    // Remove token
    await removeToken();
    
    // Verify token is removed
    retrievedToken = await getToken();
    expect(retrievedToken).toBeNull();
  });
});

console.log('API Client Setup Tests Completed');