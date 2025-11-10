const aiMlService = require('../services/ai-ml.service');
const TransformerUtils = require('../utils/transformer.utils');
const jobQueue = require('../utils/job-queue.utils');
const errorHandler = require('../utils/error-handler.utils');
const cache = require('../utils/cache.utils');
const performanceMonitor = require('../utils/performance-monitor.utils');
const { validateInputData } = require('../utils/transformer.utils');

/**
 * AI/ML Controller
 * Handles HTTP requests for AI/ML service operations
 */
class AiMlController {
  /**
   * Analyze regulatory compliance
   * @param {Object} req - Express request object
   * @param {Object} res - Express response object
   */
  async analyzeCompliance(req, res) {
    try {
      const startTime = performanceMonitor.startTiming('analyzeCompliance');
      
      // Validate input data
      const validation = validateInputData(req.body, 'compliance');
      if (!validation.isValid) {
        return res.status(400).json({
          success: false,
          error: {
            message: 'Invalid input data',
            details: validation.errors,
          },
        });
      }
      
      // Transform data for AI/ML service
      const transformedData = TransformerUtils.transformComplianceData(req.body);
      
      // Check cache first
      const cacheKey = cache.createKey('compliance', {
        documentId: transformedData.document_id,
      });
      
      const cachedResult = cache.get(cacheKey);
      if (cachedResult) {
        performanceMonitor.endTiming('analyzeCompliance', startTime, true);
        return res.status(200).json({
          success: true,
          data: cachedResult,
          cached: true,
        });
      }
      
      // Call AI/ML service
      const result = await aiMlService.analyzeCompliance(transformedData);
      
      // Transform result to internal format
      const transformedResult = TransformerUtils.transformComplianceResults(result);
      
      // Cache result
      cache.set(cacheKey, transformedResult, 300); // Cache for 5 minutes
      
      performanceMonitor.endTiming('analyzeCompliance', startTime, true);
      
      res.status(200).json({
        success: true,
        data: transformedResult,
      });
    } catch (error) {
      performanceMonitor.recordError('analyzeCompliance', error);
      const errorResponse = errorHandler.handleAiMlError(error, 'analyzeCompliance', req.body);
      
      res.status(500).json({
        success: false,
        error: {
          message: errorResponse.message,
          code: errorResponse.errorType,
        },
      });
    }
  }

  /**
   * Assess financial risk
   * @param {Object} req - Express request object
   * @param {Object} res - Express response object
   */
  async assessRisk(req, res) {
    try {
      const startTime = performanceMonitor.startTiming('assessRisk');
      
      // Validate input data
      const validation = validateInputData(req.body, 'risk');
      if (!validation.isValid) {
        return res.status(400).json({
          success: false,
          error: {
            message: 'Invalid input data',
            details: validation.errors,
          },
        });
      }
      
      // Transform data for AI/ML service
      const transformedData = TransformerUtils.transformRiskData(req.body);
      
      // Check cache first
      const cacheKey = cache.createKey('risk', {
        companyId: transformedData.company_id,
      });
      
      const cachedResult = cache.get(cacheKey);
      if (cachedResult) {
        performanceMonitor.endTiming('assessRisk', startTime, true);
        return res.status(200).json({
          success: true,
          data: cachedResult,
          cached: true,
        });
      }
      
      // Call AI/ML service
      const result = await aiMlService.assessRisk(transformedData);
      
      // Transform result to internal format
      const transformedResult = TransformerUtils.transformRiskResults(result);
      
      // Cache result
      cache.set(cacheKey, transformedResult, 300); // Cache for 5 minutes
      
      performanceMonitor.endTiming('assessRisk', startTime, true);
      
      res.status(200).json({
        success: true,
        data: transformedResult,
      });
    } catch (error) {
      performanceMonitor.recordError('assessRisk', error);
      const errorResponse = errorHandler.handleAiMlError(error, 'assessRisk', req.body);
      
      res.status(500).json({
        success: false,
        error: {
          message: errorResponse.message,
          code: errorResponse.errorType,
        },
      });
    }
  }

  /**
   * Analyze market sentiment
   * @param {Object} req - Express request object
   * @param {Object} res - Express response object
   */
  async analyzeSentiment(req, res) {
    try {
      const startTime = performanceMonitor.startTiming('analyzeSentiment');
      
      // Validate input data
      const validation = validateInputData(req.body, 'sentiment');
      if (!validation.isValid) {
        return res.status(400).json({
          success: false,
          error: {
            message: 'Invalid input data',
            details: validation.errors,
          },
        });
      }
      
      // Transform data for AI/ML service
      const transformedData = TransformerUtils.transformSentimentData(req.body);
      
      // Check cache first
      const cacheKey = cache.createKey('sentiment', {
        sourceId: transformedData.source_id,
      });
      
      const cachedResult = cache.get(cacheKey);
      if (cachedResult) {
        performanceMonitor.endTiming('analyzeSentiment', startTime, true);
        return res.status(200).json({
          success: true,
          data: cachedResult,
          cached: true,
        });
      }
      
      // Call AI/ML service
      const result = await aiMlService.analyzeSentiment(transformedData);
      
      // Transform result to internal format
      const transformedResult = TransformerUtils.transformSentimentResults(result);
      
      // Cache result
      cache.set(cacheKey, transformedResult, 300); // Cache for 5 minutes
      
      performanceMonitor.endTiming('analyzeSentiment', startTime, true);
      
      res.status(200).json({
        success: true,
        data: transformedResult,
      });
    } catch (error) {
      performanceMonitor.recordError('analyzeSentiment', error);
      const errorResponse = errorHandler.handleAiMlError(error, 'analyzeSentiment', req.body);
      
      res.status(500).json({
        success: false,
        error: {
          message: errorResponse.message,
          code: errorResponse.errorType,
        },
      });
    }
  }

  /**
   * Detect anomalies in data
   * @param {Object} req - Express request object
   * @param {Object} res - Express response object
   */
  async detectAnomalies(req, res) {
    try {
      const startTime = performanceMonitor.startTiming('detectAnomalies');
      
      // Validate input data
      const validation = validateInputData(req.body, 'anomaly');
      if (!validation.isValid) {
        return res.status(400).json({
          success: false,
          error: {
            message: 'Invalid input data',
            details: validation.errors,
          },
        });
      }
      
      // Transform data for AI/ML service
      const transformedData = TransformerUtils.transformAnomalyData(req.body);
      
      // Check cache first
      const cacheKey = cache.createKey('anomalies', {
        datasetId: transformedData.dataset_id,
      });
      
      const cachedResult = cache.get(cacheKey);
      if (cachedResult) {
        performanceMonitor.endTiming('detectAnomalies', startTime, true);
        return res.status(200).json({
          success: true,
          data: cachedResult,
          cached: true,
        });
      }
      
      // Call AI/ML service
      const result = await aiMlService.detectAnomalies(transformedData);
      
      // Transform result to internal format
      const transformedResult = TransformerUtils.transformAnomalyResults(result);
      
      // Cache result
      cache.set(cacheKey, transformedResult, 300); // Cache for 5 minutes
      
      performanceMonitor.endTiming('detectAnomalies', startTime, true);
      
      res.status(200).json({
        success: true,
        data: transformedResult,
      });
    } catch (error) {
      performanceMonitor.recordError('detectAnomalies', error);
      const errorResponse = errorHandler.handleAiMlError(error, 'detectAnomalies', req.body);
      
      res.status(500).json({
        success: false,
        error: {
          message: errorResponse.message,
          code: errorResponse.errorType,
        },
      });
    }
  }

  /**
   * Process AI/ML job asynchronously
   * @param {Object} req - Express request object
   * @param {Object} res - Express response object
   */
  async processJobAsync(req, res) {
    try {
      const { type, data } = req.body;
      
      // Validate job type
      const validTypes = ['compliance', 'risk', 'sentiment', 'anomaly'];
      if (!validTypes.includes(type)) {
        return res.status(400).json({
          success: false,
          error: {
            message: 'Invalid job type',
            validTypes,
          },
        });
      }
      
      // Add job to queue
      const jobId = jobQueue.addJob(type, data, async (jobData) => {
        switch (type) {
          case 'compliance':
            return await aiMlService.analyzeCompliance(jobData);
          case 'risk':
            return await aiMlService.assessRisk(jobData);
          case 'sentiment':
            return await aiMlService.analyzeSentiment(jobData);
          case 'anomaly':
            return await aiMlService.detectAnomalies(jobData);
          default:
            throw new Error(`Unsupported job type: ${type}`);
        }
      });
      
      res.status(202).json({
        success: true,
        message: 'Job queued for processing',
        jobId,
      });
    } catch (error) {
      const errorResponse = errorHandler.handleAiMlError(error, 'processJobAsync', req.body);
      
      res.status(500).json({
        success: false,
        error: {
          message: errorResponse.message,
          code: errorResponse.errorType,
        },
      });
    }
  }

  /**
   * Get job status
   * @param {Object} req - Express request object
   * @param {Object} res - Express response object
   */
  async getJobStatus(req, res) {
    try {
      const { jobId } = req.params;
      
      const jobStatus = jobQueue.getJobStatus(jobId);
      
      if (!jobStatus) {
        return res.status(404).json({
          success: false,
          error: {
            message: 'Job not found',
          },
        });
      }
      
      res.status(200).json({
        success: true,
        data: jobStatus,
      });
    } catch (error) {
      const errorResponse = errorHandler.handleAiMlError(error, 'getJobStatus', req.params);
      
      res.status(500).json({
        success: false,
        error: {
          message: errorResponse.message,
          code: errorResponse.errorType,
        },
      });
    }
  }

  /**
   * Get AI/ML service health status
   * @param {Object} req - Express request object
   * @param {Object} res - Express response object
   */
  async getHealthStatus(req, res) {
    try {
      const isHealthy = await aiMlService.healthCheck();
      
      res.status(200).json({
        success: true,
        data: {
          status: isHealthy ? 'healthy' : 'unhealthy',
          timestamp: new Date().toISOString(),
        },
      });
    } catch (error) {
      const errorResponse = errorHandler.handleAiMlError(error, 'getHealthStatus');
      
      res.status(500).json({
        success: false,
        error: {
          message: errorResponse.message,
          code: errorResponse.errorType,
        },
      });
    }
  }

  /**
   * Get performance metrics
   * @param {Object} req - Express request object
   * @param {Object} res - Express response object
   */
  async getMetrics(req, res) {
    try {
      const metrics = performanceMonitor.getAllMetrics();
      const systemMetrics = performanceMonitor.getSystemMetrics();
      
      res.status(200).json({
        success: true,
        data: {
          aiMlMetrics: metrics,
          systemMetrics,
        },
      });
    } catch (error) {
      const errorResponse = errorHandler.handleAiMlError(error, 'getMetrics');
      
      res.status(500).json({
        success: false,
        error: {
          message: errorResponse.message,
          code: errorResponse.errorType,
        },
      });
    }
  }
}

module.exports = new AiMlController();