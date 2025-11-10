const { rateLimiting } = require('../config/ai-ml.config');
const winston = require('winston');

/**
 * Rate Limiting Middleware for AI/ML Service
 * Limits the number of requests to prevent abuse and protect external services
 */

// In-memory store for rate limiting
const rateLimitStore = new Map();

// Initialize logger
const logger = winston.createLogger({
  level: 'info',
  format: winston.format.json(),
  transports: [
    new winston.transports.Console(),
  ],
});

/**
 * AI/ML Service Rate Limiting Middleware
 * @param {Object} req - Express request object
 * @param {Object} res - Express response object
 * @param {Function} next - Express next function
 */
const aiMlRateLimiter = (req, res, next) => {
  if (!rateLimiting.enabled) {
    return next();
  }
  
  const clientId = getClientIdentifier(req);
  const currentTime = Date.now();
  const windowMs = rateLimiting.windowMs;
  const maxRequests = rateLimiting.maxRequests;
  
  // Get client data from store
  let clientData = rateLimitStore.get(clientId);
  
  // If no client data exists, create new entry
  if (!clientData) {
    clientData = {
      requests: [],
      resetTime: currentTime + windowMs,
    };
    rateLimitStore.set(clientId, clientData);
  }
  
  // Reset window if it has expired
  if (currentTime >= clientData.resetTime) {
    clientData.requests = [];
    clientData.resetTime = currentTime + windowMs;
  }
  
  // Add current request
  clientData.requests.push(currentTime);
  
  // Check if limit has been exceeded
  if (clientData.requests.length > maxRequests) {
    const retryAfter = Math.ceil((clientData.resetTime - currentTime) / 1000);
    
    logger.warn('Rate limit exceeded', {
      clientId,
      requestCount: clientData.requests.length,
      maxRequests,
      retryAfter,
    });
    
    return res.status(429).json({
      success: false,
      error: {
        message: rateLimiting.message,
        code: 'RATE_LIMIT_EXCEEDED',
        retryAfter,
      },
    });
  }
  
  // Set rate limit headers
  res.set({
    'X-RateLimit-Limit': maxRequests,
    'X-RateLimit-Remaining': maxRequests - clientData.requests.length,
    'X-RateLimit-Reset': new Date(clientData.resetTime).toISOString(),
  });
  
  next();
};

/**
 * Get client identifier for rate limiting
 * @param {Object} req - Express request object
 * @returns {string} Client identifier
 */
function getClientIdentifier(req) {
  // Use IP address as client identifier
  let clientId = req.ip || req.connection.remoteAddress;
  
  // If we have a user, use user ID as well
  if (req.user && req.user.id) {
    clientId = `${clientId}-${req.user.id}`;
  }
  
  // If we have an API key, use that as well
  const apiKey = req.headers['x-api-key'] || req.headers['authorization'];
  if (apiKey) {
    clientId = `${clientId}-${apiKey.substring(0, 10)}`;
  }
  
  return clientId;
}

/**
 * Clean up old rate limit data
 */
function cleanupRateLimitData() {
  const currentTime = Date.now();
  let cleanedCount = 0;
  
  for (const [clientId, clientData] of rateLimitStore) {
    // Remove data that is more than 2 windows old
    if (currentTime >= clientData.resetTime + (rateLimiting.windowMs * 2)) {
      rateLimitStore.delete(clientId);
      cleanedCount++;
    }
  }
  
  if (cleanedCount > 0) {
    logger.debug(`Cleaned up ${cleanedCount} old rate limit entries`);
  }
}

// Start cleanup interval
setInterval(cleanupRateLimitData, rateLimiting.windowMs);

/**
 * Get rate limit statistics
 * @returns {Object} Rate limit statistics
 */
function getRateLimitStats() {
  return {
    activeClients: rateLimitStore.size,
    windowMs: rateLimiting.windowMs,
    maxRequests: rateLimiting.maxRequests,
  };
}

module.exports = {
  aiMlRateLimiter,
  getRateLimitStats,
};