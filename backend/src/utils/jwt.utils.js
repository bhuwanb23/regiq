const jwt = require('jsonwebtoken');
const { promisify } = require('util');

// Promisify jwt.verify for async/await usage
const verifyAsync = promisify(jwt.verify);

class JWTUtils {
  /**
   * Generate access token
   * @param {Object} payload - User data to include in token
   * @param {string} expiresIn - Token expiration time (e.g., '15m', '1h')
   * @returns {string} JWT token
   */
  generateAccessToken(payload, expiresIn = '15m') {
    return jwt.sign(payload, process.env.JWT_SECRET || 'fallback_secret_key', {
      expiresIn,
      issuer: 'regiq-backend',
      audience: 'regiq-frontend'
    });
  }

  /**
   * Generate refresh token
   * @param {Object} payload - User data to include in token
   * @param {string} expiresIn - Token expiration time (e.g., '7d', '30d')
   * @returns {string} JWT token
   */
  generateRefreshToken(payload, expiresIn = '7d') {
    return jwt.sign(payload, process.env.JWT_REFRESH_SECRET || 'fallback_refresh_secret_key', {
      expiresIn,
      issuer: 'regiq-backend',
      audience: 'regiq-frontend'
    });
  }

  /**
   * Verify access token
   * @param {string} token - JWT token to verify
   * @returns {Object} Decoded token payload
   */
  async verifyAccessToken(token) {
    try {
      const decoded = await verifyAsync(token, process.env.JWT_SECRET || 'fallback_secret_key');
      return decoded;
    } catch (error) {
      throw new Error('Invalid or expired access token');
    }
  }

  /**
   * Verify refresh token
   * @param {string} token - JWT token to verify
   * @returns {Object} Decoded token payload
   */
  async verifyRefreshToken(token) {
    try {
      const decoded = await verifyAsync(token, process.env.JWT_REFRESH_SECRET || 'fallback_refresh_secret_key');
      return decoded;
    } catch (error) {
      throw new Error('Invalid or expired refresh token');
    }
  }
}

module.exports = new JWTUtils();