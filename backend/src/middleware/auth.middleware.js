const jwtUtils = require('../utils/jwt.utils');
const { User } = require('../models');

/**
 * Authentication middleware
 * Verifies JWT token and attaches user to request
 */
async function authenticate(req, res, next) {
  try {
    // Get token from header or cookie
    let token = req.headers.authorization;
    
    if (token && token.startsWith('Bearer ')) {
      token = token.substring(7);
    } else if (req.cookies && req.cookies.accessToken) {
      token = req.cookies.accessToken;
    } else {
      return res.status(401).json({
        success: false,
        message: 'Access token is required'
      });
    }

    // Verify token
    const decoded = await jwtUtils.verifyAccessToken(token);
    
    // Get user from database
    const user = await User.findByPk(decoded.id);
    if (!user) {
      return res.status(401).json({
        success: false,
        message: 'User not found'
      });
    }

    // Attach user to request
    req.user = user;
    next();
  } catch (error) {
    res.status(401).json({
      success: false,
      message: 'Invalid or expired token'
    });
  }
}

/**
 * Role-based access control middleware
 * @param {...string} roles - Allowed roles
 */
function authorize(...roles) {
  return (req, res, next) => {
    if (!req.user) {
      return res.status(401).json({
        success: false,
        message: 'Authentication required'
      });
    }

    if (!roles.includes(req.user.role)) {
      return res.status(403).json({
        success: false,
        message: 'Insufficient permissions'
      });
    }

    next();
  };
}

module.exports = {
  authenticate,
  authorize
};