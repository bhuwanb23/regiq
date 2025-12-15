const auditService = require('../services/audit.service');

/**
 * Middleware to log user activities
 * @param {Object} req - Express request object
 * @param {Object} res - Express response object
 * @param {Function} next - Next middleware function
 */
const logUserActivity = (action, entityType) => {
  return async (req, res, next) => {
    try {
      // Capture the original send function
      const originalSend = res.send;
      
      // Override the send function to log after response is sent
      res.send = function(data) {
        // Log the activity
        const logData = {
          userId: req.user?.id || null,
          action: action,
          entityType: entityType,
          entityId: req.params.id || req.params.entityId || null,
          details: {
            method: req.method,
            url: req.originalUrl,
            params: req.params,
            query: req.query,
            body: req.body,
            userAgent: req.get('User-Agent'),
            ipAddress: req.ip
          }
        };
        
        // Log the activity asynchronously without blocking the response
        auditService.logActivity(logData).catch(err => {
          console.error('Failed to log user activity:', err);
        });
        
        // Call the original send function
        originalSend.call(this, data);
      };
      
      next();
    } catch (error) {
      console.error('Audit middleware error:', error);
      next();
    }
  };
};

module.exports = {
  logUserActivity
};