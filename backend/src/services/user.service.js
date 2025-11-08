const { User, AuditLog } = require('../models');
const bcrypt = require('bcryptjs');

class UserService {
  /**
   * Create a new user
   * @param {Object} userData - User data
   * @returns {Object} Created user
   */
  async createUser(userData) {
    try {
      // Hash password if provided
      if (userData.passwordHash) {
        userData.passwordHash = await bcrypt.hash(userData.passwordHash, 12);
      }

      const user = await User.create(userData);
      const userResponse = user.toJSON();
      delete userResponse.passwordHash;
      return userResponse;
    } catch (error) {
      throw new Error(`Failed to create user: ${error.message}`);
    }
  }

  /**
   * Get all users
   * @returns {Array} List of users
   */
  async getAllUsers() {
    try {
      const users = await User.findAll({
        attributes: { exclude: ['passwordHash'] },
        where: { isDeleted: false }
      });
      return users;
    } catch (error) {
      throw new Error(`Failed to fetch users: ${error.message}`);
    }
  }

  /**
   * Get user by ID
   * @param {string} id - User ID
   * @returns {Object} User data
   */
  async getUserById(id) {
    try {
      const user = await User.findByPk(id, {
        attributes: { exclude: ['passwordHash'] }
      });
      
      if (!user || user.isDeleted) {
        throw new Error('User not found');
      }
      
      return user;
    } catch (error) {
      throw new Error(`Failed to fetch user: ${error.message}`);
    }
  }

  /**
   * Update user
   * @param {string} id - User ID
   * @param {Object} userData - User data to update
   * @returns {Object} Updated user
   */
  async updateUser(id, userData) {
    try {
      const user = await User.findByPk(id);
      
      if (!user || user.isDeleted) {
        throw new Error('User not found');
      }

      // Hash password if provided
      if (userData.passwordHash) {
        userData.passwordHash = await bcrypt.hash(userData.passwordHash, 12);
      }

      await user.update(userData);
      
      const userResponse = user.toJSON();
      delete userResponse.passwordHash;
      return userResponse;
    } catch (error) {
      throw new Error(`Failed to update user: ${error.message}`);
    }
  }

  /**
   * Delete user (soft delete)
   * @param {string} id - User ID
   * @returns {Object} Deletion result
   */
  async deleteUser(id) {
    try {
      const user = await User.findByPk(id);
      
      if (!user || user.isDeleted) {
        throw new Error('User not found');
      }

      await user.update({ isDeleted: true, deletedAt: new Date() });
      
      // Log the deletion
      await AuditLog.create({
        userId: id,
        action: 'USER_DELETED',
        entityType: 'User',
        entityId: id,
        details: { message: 'User account deleted' }
      });

      return { message: 'User deleted successfully' };
    } catch (error) {
      throw new Error(`Failed to delete user: ${error.message}`);
    }
  }

  /**
   * Get user preferences
   * @param {string} id - User ID
   * @returns {Object} User preferences
   */
  async getUserPreferences(id) {
    try {
      const user = await User.findByPk(id, {
        attributes: ['preferences']
      });
      
      if (!user || user.isDeleted) {
        throw new Error('User not found');
      }
      
      return user.preferences || {};
    } catch (error) {
      throw new Error(`Failed to fetch user preferences: ${error.message}`);
    }
  }

  /**
   * Update user preferences
   * @param {string} id - User ID
   * @param {Object} preferences - New preferences
   * @returns {Object} Updated preferences
   */
  async updateUserPreferences(id, preferences) {
    try {
      const user = await User.findByPk(id);
      
      if (!user || user.isDeleted) {
        throw new Error('User not found');
      }

      await user.update({ preferences });
      
      // Log the preference update
      await AuditLog.create({
        userId: id,
        action: 'PREFERENCES_UPDATED',
        entityType: 'User',
        entityId: id,
        details: { preferences }
      });

      return preferences;
    } catch (error) {
      throw new Error(`Failed to update user preferences: ${error.message}`);
    }
  }

  /**
   * Get user activity logs
   * @param {string} id - User ID
   * @returns {Array} Activity logs
   */
  async getUserActivityLogs(id) {
    try {
      const logs = await AuditLog.findAll({
        where: { userId: id },
        order: [['createdAt', 'DESC']],
        limit: 50
      });
      
      return logs;
    } catch (error) {
      throw new Error(`Failed to fetch user activity logs: ${error.message}`);
    }
  }

  /**
   * Update user role (admin only)
   * @param {string} id - User ID
   * @param {string} role - New role
   * @returns {Object} Updated user
   */
  async updateUserRole(id, role) {
    try {
      const user = await User.findByPk(id);
      
      if (!user || user.isDeleted) {
        throw new Error('User not found');
      }

      await user.update({ role });
      
      // Log the role update
      await AuditLog.create({
        userId: id,
        action: 'ROLE_UPDATED',
        entityType: 'User',
        entityId: id,
        details: { oldRole: user.role, newRole: role }
      });

      const userResponse = user.toJSON();
      delete userResponse.passwordHash;
      return userResponse;
    } catch (error) {
      throw new Error(`Failed to update user role: ${error.message}`);
    }
  }

  /**
   * Get user authentication logs
   * @param {string} id - User ID
   * @returns {Array} Authentication logs
   */
  async getUserAuthLogs(id) {
    try {
      const logs = await AuditLog.findAll({
        where: { 
          userId: id,
          action: {
            [sequelize.Op.in]: ['LOGIN', 'LOGOUT', 'FAILED_LOGIN']
          }
        },
        order: [['createdAt', 'DESC']],
        limit: 50
      });
      
      return logs;
    } catch (error) {
      throw new Error(`Failed to fetch user authentication logs: ${error.message}`);
    }
  }

  /**
   * Export user data (GDPR compliance)
   * @param {string} id - User ID
   * @returns {Object} User data for export
   */
  async exportUserData(id) {
    try {
      const user = await User.findByPk(id);
      
      if (!user || user.isDeleted) {
        throw new Error('User not found');
      }

      // Get user activity logs
      const activityLogs = await this.getUserActivityLogs(id);
      
      // Get user auth logs
      const authLogs = await this.getUserAuthLogs(id);
      
      // Prepare export data
      const exportData = {
        user: {
          id: user.id,
          firstName: user.firstName,
          lastName: user.lastName,
          email: user.email,
          role: user.role,
          createdAt: user.createdAt,
          updatedAt: user.updatedAt
        },
        preferences: user.preferences,
        activityLogs: activityLogs.map(log => ({
          id: log.id,
          action: log.action,
          timestamp: log.createdAt,
          details: log.details
        })),
        authLogs: authLogs.map(log => ({
          id: log.id,
          action: log.action,
          timestamp: log.createdAt,
          ipAddress: log.ipAddress
        }))
      };

      return exportData;
    } catch (error) {
      throw new Error(`Failed to export user data: ${error.message}`);
    }
  }

  /**
   * Restore deleted user (admin only)
   * @param {string} id - User ID
   * @returns {Object} Restored user
   */
  async restoreUser(id) {
    try {
      const user = await User.findByPk(id);
      
      if (!user) {
        throw new Error('User not found');
      }

      await user.update({ isDeleted: false, deletedAt: null });
      
      // Log the restoration
      await AuditLog.create({
        userId: id,
        action: 'USER_RESTORED',
        entityType: 'User',
        entityId: id,
        details: { message: 'User account restored' }
      });

      const userResponse = user.toJSON();
      delete userResponse.passwordHash;
      return userResponse;
    } catch (error) {
      throw new Error(`Failed to restore user: ${error.message}`);
    }
  }

  /**
   * Validate user data
   * @param {Object} userData - User data to validate
   * @returns {Object} Validation result
   */
  async validateUserData(userData) {
    try {
      const errors = [];
      
      // Validate email format
      if (userData.email && !/\S+@\S+\.\S+/.test(userData.email)) {
        errors.push('Invalid email format');
      }
      
      // Validate role
      const validRoles = ['admin', 'analyst', 'compliance_officer'];
      if (userData.role && !validRoles.includes(userData.role)) {
        errors.push('Invalid role');
      }
      
      // Validate password strength
      if (userData.passwordHash) {
        const passwordErrors = this.validatePasswordStrength(userData.passwordHash);
        if (passwordErrors.length > 0) {
          errors.push(...passwordErrors);
        }
      }
      
      return {
        isValid: errors.length === 0,
        errors
      };
    } catch (error) {
      throw new Error(`Failed to validate user data: ${error.message}`);
    }
  }

  /**
   * Validate password strength
   * @param {string} password - Password to validate
   * @returns {Array} Validation errors
   */
  validatePasswordStrength(password) {
    const errors = [];
    
    if (password.length < 8) {
      errors.push('Password must be at least 8 characters long');
    }
    
    if (!/[A-Z]/.test(password)) {
      errors.push('Password must contain at least one uppercase letter');
    }
    
    if (!/[a-z]/.test(password)) {
      errors.push('Password must contain at least one lowercase letter');
    }
    
    if (!/\d/.test(password)) {
      errors.push('Password must contain at least one number');
    }
    
    if (!/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
      errors.push('Password must contain at least one special character');
    }
    
    return errors;
  }
}

module.exports = new UserService();
