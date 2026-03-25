/**
 * API Client Service - Contains methods for all API endpoints
 */
import apiClient from './api';

// ---------- REGULATORY INTELLIGENCE ----------
/**
 * Get all regulations
 * @param {Object} params - Query parameters
 * @returns {Promise<Array>} List of regulations
 */
export const getRegulations = async (params = {}) => {
  try {
    const response = await apiClient.get('/regulatory/regulations', { params });
    return response;
  } catch (error) {
    console.error('Error fetching regulations:', error);
    throw error;
  }
};

/**
 * Get regulation by ID
 * @param {string} id - Regulation ID
 * @returns {Promise<Object>} Regulation data
 */
export const getRegulationById = async (id) => {
  try {
    const response = await apiClient.get(`/regulatory/regulations/${id}`);
    return response;
  } catch (error) {
    console.error(`Error fetching regulation ${id}:`, error);
    throw error;
  }
};

/**
 * Search regulations
 * @param {string} query - Search query
 * @param {Object} params - Additional parameters
 * @returns {Promise<Array>} Search results
 */
export const searchRegulations = async (query, params = {}) => {
  try {
    const response = await apiClient.get('/regulatory/regulations/search', { 
      params: { q: query, ...params } 
    });
    return response;
  } catch (error) {
    console.error('Error searching regulations:', error);
    throw error;
  }
};

/**
 * Get regulation categories
 * @returns {Promise<Array>} List of categories
 */
export const getRegulationCategories = async () => {
  try {
    const response = await apiClient.get('/regulatory/regulations/categories');
    return response;
  } catch (error) {
    console.error('Error fetching regulation categories:', error);
    throw error;
  }
};

/**
 * Get regulation deadlines
 * @param {Object} params - Query parameters
 * @returns {Promise<Array>} List of deadlines
 */
export const getRegulationDeadlines = async (params = {}) => {
  try {
    const response = await apiClient.get('/regulatory/regulations/deadlines', { params });
    return response;
  } catch (error) {
    console.error('Error fetching regulation deadlines:', error);
    throw error;
  }
};

// ---------- BIAS ANALYSIS ----------
/**
 * Get bias analysis reports
 * @param {Object} params - Query parameters
 * @returns {Promise<Array>} List of bias reports
 */
export const getBiasReports = async (params = {}) => {
  try {
    const response = await apiClient.get('/api/bias/reports', { params });
    return response;
  } catch (error) {
    console.error('Error fetching bias reports:', error);
    throw error;
  }
};

/**
 * Get bias report by ID
 * @param {string} id - Report ID
 * @returns {Promise<Object>} Bias report data
 */
export const getBiasReportById = async (id) => {
  try {
    const response = await apiClient.get(`/api/bias/reports/${id}`);
    return response;
  } catch (error) {
    console.error(`Error fetching bias report ${id}:`, error);
    throw error;
  }
};

/**
 * Create bias analysis
 * @param {Object} data - Analysis data
 * @returns {Promise<Object>} Analysis result
 */
export const createBiasAnalysis = async (data) => {
  try {
    const response = await apiClient.post('/api/bias/analysis', data);
    return response;
  } catch (error) {
    console.error('Error creating bias analysis:', error);
    throw error;
  }
};

/**
 * Get bias mitigation recommendations
 * @param {string} modelId - Model ID
 * @returns {Promise<Object>} Mitigation recommendations
 */
export const getBiasMitigation = async (modelId) => {
  try {
    const response = await apiClient.get(`/api/bias/mitigation/${modelId}`);
    return response;
  } catch (error) {
    console.error(`Error fetching bias mitigation for model ${modelId}:`, error);
    throw error;
  }
};

// ---------- RISK SIMULATION ----------
/**
 * Get risk simulations
 * @param {Object} params - Query parameters
 * @returns {Promise<Array>} List of simulations
 */
export const getRiskSimulations = async (params = {}) => {
  try {
    const response = await apiClient.get('/api/risk/simulations', { params });
    return response;
  } catch (error) {
    console.error('Error fetching risk simulations:', error);
    throw error;
  }
};

/**
 * Get risk simulation by ID
 * @param {string} id - Simulation ID
 * @returns {Promise<Object>} Simulation data
 */
export const getRiskSimulationById = async (id) => {
  try {
    const response = await apiClient.get(`/api/risk/simulations/${id}`);
    return response;
  } catch (error) {
    console.error(`Error fetching risk simulation ${id}:`, error);
    throw error;
  }
};

/**
 * Create risk simulation
 * @param {Object} data - Simulation data
 * @returns {Promise<Object>} Simulation result
 */
export const createRiskSimulation = async (data) => {
  try {
    const response = await apiClient.post('/api/risk/simulations', data);
    return response;
  } catch (error) {
    console.error('Error creating risk simulation:', error);
    throw error;
  }
};

/**
 * Get risk scenarios
 * @param {Object} params - Query parameters
 * @returns {Promise<Array>} List of scenarios
 */
export const getRiskScenarios = async (params = {}) => {
  try {
    const response = await apiClient.get('/api/risk/scenarios', { params });
    return response;
  } catch (error) {
    console.error('Error fetching risk scenarios:', error);
    throw error;
  }
};

// ---------- REPORT GENERATION ----------
/**
 * Get reports
 * @param {Object} params - Query parameters
 * @returns {Promise<Array>} List of reports
 */
export const getReports = async (params = {}) => {
  try {
    const response = await apiClient.get('/api/reports', { params });
    return response;
  } catch (error) {
    console.error('Error fetching reports:', error);
    throw error;
  }
};

/**
 * Get report by ID
 * @param {string} id - Report ID
 * @returns {Promise<Object>} Report data
 */
export const getReportById = async (id) => {
  try {
    const response = await apiClient.get(`/api/reports/${id}`);
    return response;
  } catch (error) {
    console.error(`Error fetching report ${id}:`, error);
    throw error;
  }
};

/**
 * Generate report
 * @param {Object} data - Report generation data
 * @returns {Promise<Object>} Generated report
 */
export const generateReport = async (data) => {
  try {
    const response = await apiClient.post('/api/reports/generate', data);
    return response;
  } catch (error) {
    console.error('Error generating report:', error);
    throw error;
  }
};

/**
 * Schedule report generation
 * @param {Object} data - Schedule data
 * @returns {Promise<Object>} Schedule confirmation
 */
export const scheduleReport = async (data) => {
  try {
    const response = await apiClient.post('/api/reports/schedules', data);
    return response;
  } catch (error) {
    console.error('Error scheduling report:', error);
    throw error;
  }
};

/**
 * Export report as PDF
 * @param {string} id - Report ID
 * @returns {Promise<Blob>} PDF blob
 */
export const exportReportPdf = async (id) => {
  try {
    const response = await apiClient.get(`/api/reports/${id}/export/pdf`, {
      responseType: 'blob'
    });
    return response.data;
  } catch (error) {
    console.error(`Error exporting report ${id} as PDF:`, error);
    throw error;
  }
};

/**
 * Export report as CSV
 * @param {string} id - Report ID
 * @returns {Promise<Blob>} CSV blob
 */
export const exportReportCsv = async (id) => {
  try {
    const response = await apiClient.get(`/api/reports/${id}/export/csv`, {
      responseType: 'blob'
    });
    return response.data;
  } catch (error) {
    console.error(`Error exporting report ${id} as CSV:`, error);
    throw error;
  }
};

/**
 * Export report as JSON
 * @param {string} id - Report ID
 * @returns {Promise<Object>} JSON data
 */
export const exportReportJson = async (id) => {
  try {
    const response = await apiClient.get(`/api/reports/${id}/export/json`);
    return response.data;
  } catch (error) {
    console.error(`Error exporting report ${id} as JSON:`, error);
    throw error;
  }
};
// ---------- USER MANAGEMENT ----------
/**
 * Get users
 * @param {Object} params - Query parameters
 * @returns {Promise<Array>} List of users
 */
export const getUsers = async (params = {}) => {
  try {
    const response = await apiClient.get('/api/users', { params });
    return response;
  } catch (error) {
    console.error('Error fetching users:', error);
    throw error;
  }
};

/**
 * Get user by ID
 * @param {string} id - User ID
 * @returns {Promise<Object>} User data
 */
export const getUserById = async (id) => {
  try {
    const response = await apiClient.get(`/api/users/${id}`);
    return response;
  } catch (error) {
    console.error(`Error fetching user ${id}:`, error);
    throw error;
  }
};

/**
 * Get authenticated user's profile
 * @returns {Promise<Object>} User profile data
 */
export const getUserProfile = async () => {
  try {
    const response = await apiClient.get('/api/users/profile');
    return response;
  } catch (error) {
    console.error('Error fetching user profile:', error);
    throw error;
  }
};

/**
 * Update authenticated user's profile
 * @param {Object} userData - User data to update
 * @returns {Promise<Object>} Updated user profile
 */
export const updateUserProfile = async (userData) => {
  try {
    const response = await apiClient.put('/api/users/profile', userData);
    return response;
  } catch (error) {
    console.error('Error updating user profile:', error);
    throw error;
  }
};

/**
 * Get authenticated user's preferences
 * @returns {Promise<Object>} User preferences
 */
export const getUserPreferences = async () => {
  try {
    const response = await apiClient.get('/api/users/preferences');
    return response;
  } catch (error) {
    console.error('Error fetching user preferences:', error);
    throw error;
  }
};

/**
 * Update authenticated user's preferences
 * @param {Object} preferences - Preferences to update
 * @returns {Promise<Object>} Updated preferences
 */
export const updateUserPreferences = async (preferences) => {
  try {
    const response = await apiClient.put('/api/users/preferences', preferences);
    return response;
  } catch (error) {
    console.error('Error updating user preferences:', error);
    throw error;
  }
};// ---------- NOTIFICATIONS ----------
/**
 * Get notifications
 * @param {Object} params - Query parameters
 * @returns {Promise<Array>} List of notifications
 */
export const getNotifications = async (params = {}) => {
  try {
    const response = await apiClient.get('/api/notifications', { params });
    return response;
  } catch (error) {
    console.error('Error fetching notifications:', error);
    throw error;
  }
};

/**
 * Get notification by ID
 * @param {string} id - Notification ID
 * @returns {Promise<Object>} Notification data
 */
export const getNotificationById = async (id) => {
  try {
    const response = await apiClient.get(`/api/notifications/${id}`);
    return response;
  } catch (error) {
    console.error(`Error fetching notification ${id}:`, error);
    throw error;
  }
};

/**
 * Get user notification preferences
 * @returns {Promise<Object>} User notification preferences
 */
export const getNotificationPreferences = async () => {
  try {
    const response = await apiClient.get('/api/notifications/preferences');
    return response;
  } catch (error) {
    console.error('Error fetching notification preferences:', error);
    throw error;
  }
};

/**
 * Update user notification preferences
 * @param {Object} preferences - Notification preferences to update
 * @returns {Promise<Object>} Updated preferences
 */
export const updateNotificationPreferences = async (preferences) => {
  try {
    const response = await apiClient.put('/api/notifications/preferences', { preferences });
    return response;
  } catch (error) {
    console.error('Error updating notification preferences:', error);
    throw error;
  }
};
// ---------- HELPER FUNCTIONS ----------
/**
 * Handle API errors with user-friendly messages
 * @param {Error} error - The error object
 * @returns {string} User-friendly error message
 */
export const handleApiError = (error) => {
  if (error.response) {
    // Server responded with error status
    switch (error.response.status) {
      case 400:
        return 'Bad request. Please check your input.';
      case 401:
        return 'Unauthorized. Please log in again.';
      case 403:
        return 'Forbidden. You do not have permission to perform this action.';
      case 404:
        return 'Resource not found.';
      case 500:
        return 'Server error. Please try again later.';
      default:
        return error.response.data?.message || 'An error occurred.';
    }
  } else if (error.request) {
    // Request was made but no response received
    return 'Network error. Please check your connection.';
  } else {
    // Something else happened
    return error.message || 'An unexpected error occurred.';
  }
};

/**
 * Add loading state management
 * @param {Function} setLoading - setState function for loading state
 * @returns {Function} Wrapped API call function
 */
export const withLoading = (setLoading) => (apiCall) => async (...args) => {
  try {
    setLoading(true);
    const result = await apiCall(...args);
    return result;
  } finally {
    setLoading(false);
  }
};

/**
 * Add retry mechanism to API calls
 * @param {Function} apiCall - The API call function
 * @param {number} maxRetries - Maximum number of retries
 * @param {number} delay - Delay between retries in milliseconds
 * @returns {Function} API call function with retry mechanism
 */
export const withRetry = (apiCall, maxRetries = 3, delay = 1000) => {
  return async (...args) => {
    let lastError;
    
    for (let i = 0; i <= maxRetries; i++) {
      try {
        const result = await apiCall(...args);
        return result;
      } catch (error) {
        lastError = error;
        
        // Don't retry on client errors (4xx) except 401
        if (error.response && error.response.status >= 400 && error.response.status < 500 && error.response.status !== 401) {
          throw error;
        }
        
        // If we've exhausted retries, throw the last error
        if (i === maxRetries) {
          throw error;
        }
        
        // Wait before retrying
        await new Promise(resolve => setTimeout(resolve, delay * Math.pow(2, i)));
      }
    }
    
    throw lastError;
  };
};

export default {
  // Regulatory Intelligence
  getRegulations,
  getRegulationById,
  searchRegulations,
  getRegulationCategories,
  getRegulationDeadlines,
  
  // Bias Analysis
  getBiasReports,
  getBiasReportById,
  createBiasAnalysis,
  getBiasMitigation,
  
  // Risk Simulation
  getRiskSimulations,
  getRiskSimulationById,
  createRiskSimulation,
  getRiskScenarios,
  
  // Report Generation
  getReports,
  getReportById,
  generateReport,
  scheduleReport,
  exportReportPdf,
  exportReportCsv,
  exportReportJson,  
  // User Management
  getUsers,
  getUserById,
  getUserProfile,
  updateUserProfile,
  getUserPreferences,
  updateUserPreferences,
  
  // Notifications
  getNotifications,
  getNotificationById,
  getNotificationPreferences,
  updateNotificationPreferences,
  // Helpers
  handleApiError,
  withLoading,
  withRetry
};