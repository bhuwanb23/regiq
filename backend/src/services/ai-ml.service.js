const axios = require('axios');
const winston = require('winston');
const { aiMlService, models } = require('../config/ai-ml.config');
const { performance } = require('perf_hooks');

/**
 * AI/ML Service Client
 * Handles communication with external AI/ML services
 */
class AIClient {
  constructor() {
    this.baseUrl = aiMlService.baseUrl;
    this.apiKey = aiMlService.apiKey;
    this.timeout = aiMlService.timeout;
    this.maxRetries = aiMlService.maxRetries;
    
    // Initialize axios instance with default configuration
    this.client = axios.create({
      baseURL: this.baseUrl,
      timeout: this.timeout,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.apiKey}`,
      },
    });

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
   * Make an API request with retry logic
   * @param {string} method - HTTP method (GET, POST, PUT, DELETE)
   * @param {string} endpoint - API endpoint
   * @param {Object} data - Request data
   * @param {Object} config - Additional axios config
   * @returns {Promise<Object>} Response data
   */
  async makeRequest(method, endpoint, data = null, config = {}) {
    let lastError;
    
    for (let attempt = 1; attempt <= this.maxRetries; attempt++) {
      try {
        const startTime = performance.now();
        
        const response = await this.client({
          method,
          url: endpoint,
          data,
          ...config,
        });
        
        const endTime = performance.now();
        const duration = endTime - startTime;
        
        this.logger.info(`AI/ML API request successful`, {
          method,
          endpoint,
          duration: `${duration.toFixed(2)}ms`,
          attempt,
        });
        
        return response.data;
      } catch (error) {
        lastError = error;
        this.logger.warn(`AI/ML API request failed (attempt ${attempt}/${this.maxRetries})`, {
          method,
          endpoint,
          error: error.message,
        });
        
        // If this is not the last attempt, wait before retrying
        if (attempt < this.maxRetries) {
          await this.delay(Math.pow(2, attempt) * 1000); // Exponential backoff
        }
      }
    }
    
    this.logger.error(`AI/ML API request failed after ${this.maxRetries} attempts`, {
      method,
      endpoint,
      error: lastError.message,
    });
    
    throw new Error(`AI/ML service request failed: ${lastError.message}`);
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
   * Analyze regulatory compliance using AI/ML model
   * @param {Object} data - Regulatory data to analyze
   * @returns {Promise<Object>} Analysis results
   */
  async analyzeCompliance(data) {
    try {
      const endpoint = models.complianceAnalysis.endpoint;
      const response = await this.makeRequest('POST', endpoint, data);
      return response;
    } catch (error) {
      this.logger.error('Compliance analysis failed', { error: error.message });
      throw new Error(`Compliance analysis failed: ${error.message}`);
    }
  }

  /**
   * Assess financial risk using AI/ML model
   * @param {Object} data - Financial data to analyze
   * @returns {Promise<Object>} Risk assessment results
   */
  async assessRisk(data) {
    try {
      const endpoint = models.riskAssessment.endpoint;
      const response = await this.makeRequest('POST', endpoint, data);
      return response;
    } catch (error) {
      this.logger.error('Risk assessment failed', { error: error.message });
      throw new Error(`Risk assessment failed: ${error.message}`);
    }
  }

  /**
   * Analyze market sentiment using AI/ML model
   * @param {Object} data - Market data to analyze
   * @returns {Promise<Object>} Sentiment analysis results
   */
  async analyzeSentiment(data) {
    try {
      const endpoint = models.sentimentAnalysis.endpoint;
      const response = await this.makeRequest('POST', endpoint, data);
      return response;
    } catch (error) {
      this.logger.error('Sentiment analysis failed', { error: error.message });
      throw new Error(`Sentiment analysis failed: ${error.message}`);
    }
  }

  /**
   * Detect anomalies in data using AI/ML model
   * @param {Object} data - Data to analyze for anomalies
   * @returns {Promise<Object>} Anomaly detection results
   */
  async detectAnomalies(data) {
    try {
      const endpoint = models.anomalyDetection.endpoint;
      const response = await this.makeRequest('POST', endpoint, data);
      return response;
    } catch (error) {
      this.logger.error('Anomaly detection failed', { error: error.message });
      throw new Error(`Anomaly detection failed: ${error.message}`);
    }
  }

  /**
   * Get model information
   * @param {string} modelName - Name of the model
   * @returns {Promise<Object>} Model information
   */
  async getModelInfo(modelName) {
    try {
      const response = await this.makeRequest('GET', `/models/${modelName}`);
      return response;
    } catch (error) {
      this.logger.error(`Failed to get model info for ${modelName}`, { error: error.message });
      throw new Error(`Failed to get model info: ${error.message}`);
    }
  }

  /**
   * Health check for AI/ML service
   * @returns {Promise<boolean>} Service health status
   */
  async healthCheck() {
    try {
      await this.makeRequest('GET', '/health');
      return true;
    } catch (error) {
      this.logger.error('AI/ML service health check failed', { error: error.message });
      return false;
    }
  }
}

module.exports = new AIClient();