const bcrypt = require('bcryptjs');

class PasswordUtils {
  /**
   * Hash a password
   * @param {string} password - Plain text password
   * @param {number} saltRounds - Number of salt rounds (default: 12)
   * @returns {string} Hashed password
   */
  async hashPassword(password, saltRounds = 12) {
    try {
      const salt = await bcrypt.genSalt(saltRounds);
      const hash = await bcrypt.hash(password, salt);
      return hash;
    } catch (error) {
      throw new Error(`Error hashing password: ${error.message}`);
    }
  }

  /**
   * Compare password with hash
   * @param {string} password - Plain text password
   * @param {string} hash - Hashed password
   * @returns {boolean} Whether password matches hash
   */
  async comparePassword(password, hash) {
    try {
      return await bcrypt.compare(password, hash);
    } catch (error) {
      throw new Error(`Error comparing password: ${error.message}`);
    }
  }

  /**
   * Validate password strength
   * @param {string} password - Password to validate
   * @returns {Object} Validation result
   */
  validatePasswordStrength(password) {
    const minLength = 8;
    const hasUpperCase = /[A-Z]/.test(password);
    const hasLowerCase = /[a-z]/.test(password);
    const hasNumbers = /\d/.test(password);
    const hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/.test(password);

    const isValid = password.length >= minLength && 
                   hasUpperCase && 
                   hasLowerCase && 
                   hasNumbers && 
                   hasSpecialChar;

    return {
      isValid,
      minLength: password.length >= minLength,
      hasUpperCase,
      hasLowerCase,
      hasNumbers,
      hasSpecialChar
    };
  }
}

module.exports = new PasswordUtils();