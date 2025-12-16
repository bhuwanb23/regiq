/**
 * Authentication service for handling user login, logout, and token management
 */
import apiClient from './api';
import { storeToken, storeRefreshToken, getToken, getRefreshToken, clearAuthData } from '../utils/storage';

/**
 * Login user with email and password
 * @param {string} email - User's email
 * @param {string} password - User's password
 * @returns {Promise<Object>} User data and tokens
 */
export const login = async (email, password) => {
  try {
    const response = await apiClient.post('/auth/login', { email, password });
    
    // Store tokens
    if (response.token) {
      await storeToken(response.token);
    }
    
    if (response.refreshToken) {
      await storeRefreshToken(response.refreshToken);
    }
    
    return response;
  } catch (error) {
    console.error('Login error:', error);
    throw error;
  }
};

/**
 * Register new user
 * @param {Object} userData - User registration data
 * @returns {Promise<Object>} Registered user data
 */
export const register = async (userData) => {
  try {
    const response = await apiClient.post('/auth/register', userData);
    return response;
  } catch (error) {
    console.error('Registration error:', error);
    throw error;
  }
};

/**
 * Refresh authentication token
 * @returns {Promise<string>} New access token
 */
export const refreshToken = async () => {
  try {
    const refreshTokenValue = await getRefreshToken();
    if (!refreshTokenValue) {
      throw new Error('No refresh token available');
    }
    
    const response = await apiClient.post('/auth/refresh', { refreshToken: refreshTokenValue });
    
    // Store new token
    if (response.token) {
      await storeToken(response.token);
      return response.token;
    }
    
    throw new Error('Failed to refresh token');
  } catch (error) {
    console.error('Token refresh error:', error);
    await logout(); // Clear auth data on refresh failure
    throw error;
  }
};

/**
 * Logout user and clear authentication data
 */
export const logout = async () => {
  try {
    // Attempt to call logout endpoint
    await apiClient.post('/auth/logout');
  } catch (error) {
    console.warn('Logout endpoint error (continuing with local logout):', error);
  } finally {
    // Clear local auth data regardless of server response
    await clearAuthData();
  }
};

/**
 * Get current user profile
 * @returns {Promise<Object>} User profile data
 */
export const getCurrentUser = async () => {
  try {
    const response = await apiClient.get('/users/profile');
    return response;
  } catch (error) {
    console.error('Get user profile error:', error);
    throw error;
  }
};

/**
 * Update user profile
 * @param {Object} userData - Updated user data
 * @returns {Promise<Object>} Updated user data
 */
export const updateUserProfile = async (userData) => {
  try {
    const response = await apiClient.put('/users/profile', userData);
    return response;
  } catch (error) {
    console.error('Update user profile error:', error);
    throw error;
  }
};

/**
 * Change user password
 * @param {Object} passwordData - Current and new passwords
 * @returns {Promise<Object>} Success message
 */
export const changePassword = async (passwordData) => {
  try {
    const response = await apiClient.put('/users/password', passwordData);
    return response;
  } catch (error) {
    console.error('Change password error:', error);
    throw error;
  }
};

/**
 * Check if user is authenticated
 * @returns {Promise<boolean>} Authentication status
 */
export const isAuthenticated = async () => {
  try {
    const token = await getToken();
    return !!token;
  } catch (error) {
    console.error('Authentication check error:', error);
    return false;
  }
};