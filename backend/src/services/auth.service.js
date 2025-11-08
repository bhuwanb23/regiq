const { User } = require('../models');
const jwtUtils = require('../utils/jwt.utils');
const passwordUtils = require('../utils/password.utils');

class AuthService {
  /**
   * Register a new user
   * @param {Object} userData - User registration data
   * @returns {Object} Registered user and tokens
   */
  async registerUser(userData) {
    try {
      // Check if user already exists
      const existingUser = await User.findOne({
        where: { email: userData.email }
      });

      if (existingUser) {
        throw new Error('User with this email already exists');
      }

      // Validate password strength
      const passwordValidation = passwordUtils.validatePasswordStrength(userData.passwordHash);
      if (!passwordValidation.isValid) {
        throw new Error('Password does not meet security requirements');
      }

      // Hash password
      const hashedPassword = await passwordUtils.hashPassword(userData.passwordHash);
      
      // Create user
      const user = await User.create({
        ...userData,
        passwordHash: hashedPassword
      });

      // Generate tokens
      const accessToken = jwtUtils.generateAccessToken({
        id: user.id,
        email: user.email,
        role: user.role
      });

      const refreshToken = jwtUtils.generateRefreshToken({
        id: user.id,
        email: user.email
      });

      // Remove password from response
      const userResponse = user.toJSON();
      delete userResponse.passwordHash;

      return {
        user: userResponse,
        accessToken,
        refreshToken
      };
    } catch (error) {
      throw new Error(`Registration failed: ${error.message}`);
    }
  }

  /**
   * Login user
   * @param {string} email - User email
   * @param {string} password - User password
   * @returns {Object} User and tokens
   */
  async loginUser(email, password) {
    try {
      // Find user by email
      const user = await User.findOne({ where: { email } });
      if (!user) {
        throw new Error('Invalid credentials');
      }

      // Compare passwords
      const isPasswordValid = await passwordUtils.comparePassword(password, user.passwordHash);
      if (!isPasswordValid) {
        throw new Error('Invalid credentials');
      }

      // Update last login
      await user.update({ lastLogin: new Date() });

      // Generate tokens
      const accessToken = jwtUtils.generateAccessToken({
        id: user.id,
        email: user.email,
        role: user.role
      });

      const refreshToken = jwtUtils.generateRefreshToken({
        id: user.id,
        email: user.email
      });

      // Remove password from response
      const userResponse = user.toJSON();
      delete userResponse.passwordHash;

      return {
        user: userResponse,
        accessToken,
        refreshToken
      };
    } catch (error) {
      throw new Error(`Login failed: ${error.message}`);
    }
  }

  /**
   * Refresh access token
   * @param {string} refreshToken - Refresh token
   * @returns {Object} New access token
   */
  async refreshAccessToken(refreshToken) {
    try {
      // Verify refresh token
      const decoded = await jwtUtils.verifyRefreshToken(refreshToken);
      
      // Find user
      const user = await User.findByPk(decoded.id);
      if (!user) {
        throw new Error('User not found');
      }

      // Generate new access token
      const newAccessToken = jwtUtils.generateAccessToken({
        id: user.id,
        email: user.email,
        role: user.role
      });

      return {
        accessToken: newAccessToken
      };
    } catch (error) {
      throw new Error(`Token refresh failed: ${error.message}`);
    }
  }

  /**
   * Logout user
   * @param {string} refreshToken - Refresh token to invalidate
   * @returns {Object} Logout result
   */
  async logoutUser(refreshToken) {
    try {
      // In a production environment, you would invalidate the refresh token
      // by adding it to a blacklist or removing it from storage
      // For now, we'll just return a success message
      return { message: 'Logout successful' };
    } catch (error) {
      throw new Error(`Logout failed: ${error.message}`);
    }
  }
}

module.exports = new AuthService();