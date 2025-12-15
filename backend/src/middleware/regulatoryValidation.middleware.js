const Joi = require('joi');

// Validation schema for regulation queries
const regulationQuerySchema = Joi.object({
  page: Joi.number().integer().min(1).default(1),
  limit: Joi.number().integer().min(1).max(100).default(20),
  jurisdiction: Joi.string().max(100),
  documentType: Joi.string().max(100),
  status: Joi.string().valid('pending', 'processed', 'archived'),
  category: Joi.string().max(100),
  q: Joi.string().max(255)
});

// Validation schema for regulation search
const regulationSearchSchema = Joi.object({
  page: Joi.number().integer().min(1).default(1),
  limit: Joi.number().integer().min(1).max(100).default(20),
  jurisdiction: Joi.string().max(100),
  documentType: Joi.string().max(100),
  category: Joi.string().max(100),
  q: Joi.string().max(255),
  dateFrom: Joi.date().iso(),
  dateTo: Joi.date().iso()
});

// Validation schema for deadlines queries
const deadlinesQuerySchema = Joi.object({
  page: Joi.number().integer().min(1).default(1),
  limit: Joi.number().integer().min(1).max(100).default(20),
  jurisdiction: Joi.string().max(100),
  documentType: Joi.string().max(100)
});

// Validation schema for regulation ID parameter
const regulationIdSchema = Joi.object({
  id: Joi.number().integer().positive().required()
});

const validateRegulationQuery = (req, res, next) => {
  const { error, value } = regulationQuerySchema.validate(req.query);
  if (error) {
    return res.status(400).json({
      success: false,
      message: 'Invalid query parameters',
      errors: error.details.map(detail => detail.message)
    });
  }
  
  req.query = value;
  next();
};

const validateRegulationSearch = (req, res, next) => {
  const { error, value } = regulationSearchSchema.validate(req.query);
  if (error) {
    return res.status(400).json({
      success: false,
      message: 'Invalid search parameters',
      errors: error.details.map(detail => detail.message)
    });
  }
  
  req.query = value;
  next();
};

const validateDeadlinesQuery = (req, res, next) => {
  const { error, value } = deadlinesQuerySchema.validate(req.query);
  if (error) {
    return res.status(400).json({
      success: false,
      message: 'Invalid deadlines query parameters',
      errors: error.details.map(detail => detail.message)
    });
  }
  
  req.query = value;
  next();
};

const validateRegulationId = (req, res, next) => {
  const { error, value } = regulationIdSchema.validate(req.params);
  if (error) {
    return res.status(400).json({
      success: false,
      message: 'Invalid regulation ID',
      errors: error.details.map(detail => detail.message)
    });
  }
  
  req.params = value;
  next();
};

module.exports = {
  validateRegulationQuery,
  validateRegulationSearch,
  validateDeadlinesQuery,
  validateRegulationId
};