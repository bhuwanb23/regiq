/**
 * Centralized Axios instance for API calls
 */
import axios from 'axios';
import { getToken, removeToken } from '../utils/storage';

// Configuration from environment variables
const API_BASE_URL = process.env.REACT_NATIVE_API_BASE_URL || 'http://localhost:3000/api';
const API_TIMEOUT = parseInt(process.env.REACT_NATIVE_API_TIMEOUT, 10) || 10000;

// Create axios instance with default configuration
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: API_TIMEOUT,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Flag to prevent multiple token refresh attempts
let isRefreshing = false;
let failedQueue = [];

const processQueue = (error, token = null) => {
  failedQueue.forEach(prom => {
    if (error) {
      prom.reject(error);
    } else {
      prom.resolve(token);
    }
  });
  
  failedQueue = [];
};

// Request interceptor to add auth token to headers
apiClient.interceptors.request.use(
  async (config) => {
    const token = await getToken();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for handling responses and errors
apiClient.interceptors.response.use(
  (response) => {
    // Return only the data part of the response
    return response.data;
  },
  async (error) => {
    const originalRequest = error.config;

    // If token expired and we haven't tried to refresh it yet
    if (error.response?.status === 401 && !originalRequest._retry) {
      if (isRefreshing) {
        return new Promise(function(resolve, reject) {
          failedQueue.push({resolve, reject});
        }).then(token => {
          originalRequest.headers['Authorization'] = 'Bearer ' + token;
          return apiClient(originalRequest);
        }).catch(err => {
          return Promise.reject(err);
        });
      }

      originalRequest._retry = true;
      isRefreshing = true;

      try {
        // We'll handle token refresh in the calling code to avoid circular dependency
        // This is a placeholder - in a real implementation, we would call a refresh function
        console.warn('Token refresh needed but not implemented in interceptor to avoid circular dependency');
        await removeToken();
        return Promise.reject(new Error('Token expired'));
      } catch (err) {
        processQueue(err, null);
        // Clear auth data and redirect to login
        await removeToken();
        // In a real app, we would redirect to login screen
        // window.location.href = '/login';
        return Promise.reject(err);
      } finally {
        isRefreshing = false;
      }
    }

    // Handle other errors
    if (error.response) {
      // Server responded with error status
      console.error('API Error:', error.response.status, error.response.data);
    } else if (error.request) {
      // Request was made but no response received
      console.error('Network Error:', error.message);
    } else {
      // Something else happened
      console.error('Error:', error.message);
    }

    return Promise.reject(error);
  }
);

export default apiClient;