const winston = require('winston');

/**
 * Error Handler Utilities for AI/ML Service
 * Handles error management, logging, and retry logic
 */

class ErrorHandler {
  constructor() {
    // Initialize logger
    this.logger = winston.createLogger({
      level: 'info',
      format: winston.format.json(),
      transports: [
        new winston.transports.Console(),
      ],
    });
  }

  /**
   * Handle AI/ML service errors
   * @param {Error} error - Error object
   * @param {string} context - Context where error occurred
   * @param {Object} data - Additional data related to error
   */
  handleAiMlError(error, context, data = {}) {
    const errorInfo = {
      context,
      message: error.message,
      stack: error.stack,
      data,
      timestamp: new Date().toISOString(),
    };

    // Log error
    this.logger.error('AI/ML Service Error', errorInfo);

    // Classify error type
    const errorType = this.classifyError(error);
    
    // Handle based on error type
    switch (errorType) {
      case 'NETWORK_ERROR':
        return this.handleNetworkError(error, context, data);
      case 'TIMEOUT_ERROR':
        return this.handleTimeoutError(error, context, data);
      case 'AUTH_ERROR':
        return this.handleAuthError(error, context, data);
      case 'RATE_LIMIT_ERROR':
        return this.handleRateLimitError(error, context, data);
      case 'VALIDATION_ERROR':
        return this.handleValidationError(error, context, data);
      case 'SERVER_ERROR':
        return this.handleServerError(error, context, data);
      default:
        return this.handleGenericError(error, context, data);
    }
  }

  /**
   * Classify error type based on error message or code
   * @param {Error} error - Error object
   * @returns {string} Error type
   */
  classifyError(error) {
    const message = error.message.toLowerCase();
    
    if (message.includes('network') || message.includes('connect') || message.includes('econnrefused')) {
      return 'NETWORK_ERROR';
    }
    
    if (message.includes('timeout') || message.includes('etimedout')) {
      return 'TIMEOUT_ERROR';
    }
    
    if (message.includes('unauthorized') || message.includes('forbidden') || message.includes('401') || message.includes('403')) {
      return 'AUTH_ERROR';
    }
    
    if (message.includes('rate limit') || message.includes('too many requests') || message.includes('429')) {
      return 'RATE_LIMIT_ERROR';
    }
    
    if (message.includes('validation') || message.includes('invalid') || message.includes('bad request') || message.includes('400')) {
      return 'VALIDATION_ERROR';
    }
    
    if (message.includes('server error') || message.includes('internal server error') || message.includes('500')) {
      return 'SERVER_ERROR';
    }
    
    return 'GENERIC_ERROR';
  }

  /**
   * Handle network errors
   * @param {Error} error - Error object
   * @param {string} context - Context where error occurred
   * @param {Object} data - Additional data related to error
   */
  handleNetworkError(error, context, data) {
    this.logger.warn('Network error occurred, may require retry', { context, error: error.message });
    return {
      shouldRetry: true,
      retryDelay: 5000, // 5 seconds
      maxRetries: 3,
      errorType: 'NETWORK_ERROR',
      message: 'Network connectivity issue, retrying...',
    };
  }

  /**
   * Handle timeout errors
   * @param {Error} error - Error object
   * @param {string} context - Context where error occurred
   * @param {Object} data - Additional data related to error
   */
  handleTimeoutError(error, context, data) {
    this.logger.warn('Timeout error occurred, may require retry with longer timeout', { context, error: error.message });
    return {
      shouldRetry: true,
      retryDelay: 10000, // 10 seconds
      maxRetries: 2,
      errorType: 'TIMEOUT_ERROR',
      message: 'Request timeout, retrying with longer timeout...',
    };
  }

  /**
   * Handle authentication errors
   * @param {Error} error - Error object
   * @param {string} context - Context where error occurred
   * @param {Object} data - Additional data related to error
   */
  handleAuthError(error, context, data) {
    this.logger.error('Authentication error occurred, check API credentials', { context, error: error.message });
    return {
      shouldRetry: false,
      errorType: 'AUTH_ERROR',
      message: 'Authentication failed, please check API credentials',
    };
  }

  /**
   * Handle rate limit errors
   * @param {Error} error - Error object
   * @param {string} context - Context where error occurred
   * @param {Object} data - Additional data related to error
   */
  handleRateLimitError(error, context, data) {
    this.logger.warn('Rate limit exceeded, implementing backoff strategy', { context, error: error.message });
    return {
      shouldRetry: true,
      retryDelay: 30000, // 30 seconds
      maxRetries: 1,
      errorType: 'RATE_LIMIT_ERROR',
      message: 'Rate limit exceeded, backing off before retry...',
    };
  }

  /**
   * Handle validation errors
   * @param {Error} error - Error object
   * @param {string} context - Context where error occurred
   * @param {Object} data - Additional data related to error
   */
  handleValidationError(error, context, data) {
    this.logger.error('Validation error occurred, check input data', { context, error: error.message, data });
    return {
      shouldRetry: false,
      errorType: 'VALIDATION_ERROR',
      message: 'Invalid input data, please check and correct',
    };
  }

  /**
   * Handle server errors
   * @param {Error} error - Error object
   * @param {string} context - Context where error occurred
   * @param {Object} data - Additional data related to error
   */
  handleServerError(error, context, data) {
    this.logger.error('Server error occurred, may require retry', { context, error: error.message });
    return {
      shouldRetry: true,
      retryDelay: 15000, // 15 seconds
      maxRetries: 2,
      errorType: 'SERVER_ERROR',
      message: 'Server error occurred, retrying...',
    };
  }

  /**
   * Handle generic errors
   * @param {Error} error - Error object
   * @param {string} context - Context where error occurred
   * @param {Object} data - Additional data related to error
   */
  handleGenericError(error, context, data) {
    this.logger.error('Unexpected error occurred', { context, error: error.message });
    return {
      shouldRetry: false,
      errorType: 'GENERIC_ERROR',
      message: 'An unexpected error occurred',
    };
  }

  /**
   * Implement exponential backoff retry logic
   * @param {Function} operation - Function to retry
   * @param {Object} retryConfig - Retry configuration
   * @returns {Promise<any>} Result of operation
   */
  async retryWithBackoff(operation, retryConfig = {}) {
    const {
      maxRetries = 3,
      baseDelay = 1000,
      maxDelay = 30000,
      exponentialFactor = 2,
    } = retryConfig;

    let lastError;
    
    for (let attempt = 1; attempt <= maxRetries; attempt++) {
      try {
        return await operation();
      } catch (error) {
        lastError = error;
        
        // If this is the last attempt, don't retry
        if (attempt === maxRetries) {
          break;
        }
        
        // Calculate delay with exponential backoff
        const delay = Math.min(baseDelay * Math.pow(exponentialFactor, attempt - 1), maxDelay);
        
        this.logger.warn(`Operation failed, retrying in ${delay}ms (attempt ${attempt}/${maxRetries})`, {
          error: error.message,
        });
        
        // Wait before retrying
        await this.delay(delay);
      }
    }
    
    // If we get here, all retries failed
    throw lastError;
  }

  /**
   * Delay execution for specified milliseconds
   * @param {number} ms - Milliseconds to delay
   * @returns {Promise<void>}
   */
  delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  /**
   * Create a standardized error response
   * @param {string} message - Error message
   * @param {string} code - Error code
   * @param {number} statusCode - HTTP status code
   * @param {Object} details - Additional error details
   * @returns {Object} Standardized error response
   */
  createErrorResponse(message, code, statusCode, details = {}) {
    return {
      success: false,
      error: {
        message,
        code,
        statusCode,
        timestamp: new Date().toISOString(),
        ...details,
      },
    };
  }

  /**
   * Log error with context
   * @param {Error} error - Error object
   * @param {string} context - Context where error occurred
   * @param {Object} metadata - Additional metadata
   */
  logError(error, context, metadata = {}) {
    this.logger.error(context, {
      error: error.message,
      stack: error.stack,
      ...metadata,
    });
  }
}

// Export singleton instance
module.exports = new ErrorHandler();