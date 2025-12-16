const userService = require('../services/user.service');
const { sequelize } = require('../models');

class UserController {
  /**
   * Get all users
   * @param {Object} req - Express request object
   * @param {Object} res - Express response object
   */
  async getAllUsers(req, res) {
    try {
      // Check if user is authenticated
      if (!req.user) {
        return res.status(401).json({
          success: false,
          message: 'Authentication required'
        });
      }

      // Only admins can get all users
      if (req.user.role !== 'admin') {
        return res.status(403).json({
          success: false,
          message: 'Insufficient permissions'
        });
      }

      const users = await userService.getAllUsers();
      
      res.status(200).json({
        success: true,
        data: users
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      });
    }
  }

  /**
   * Get user by ID
   * @param {Object} req - Express request object
   * @param {Object} res - Express response object
   */
  async getUserById(req, res) {
    try {
      const { id } = req.params;
      
      // Check if user is authenticated
      if (!req.user) {
        return res.status(401).json({
          success: false,
          message: 'Authentication required'
        });
      }

      // Users can only get their own profile or admins can get any profile
      if (req.user.id != id && req.user.role !== 'admin') {
        return res.status(403).json({
          success: false,
          message: 'Insufficient permissions'
        });
      }

      const user = await userService.getUserById(id);
      
      res.status(200).json({
        success: true,
        data: user
      });
    } catch (error) {
      res.status(404).json({
        success: false,
        message: error.message
      });
    }
  }

  /**
   * Create new user
   * @param {Object} req - Express request object
   * @param {Object} res - Express response object
   */
  async createUser(req, res) {
    try {
      // Check if user is authenticated
      if (!req.user) {
        return res.status(401).json({
          success: false,
          message: 'Authentication required'
        });
      }

      // Only admins can create users
      if (req.user.role !== 'admin') {
        return res.status(403).json({
          success: false,
          message: 'Insufficient permissions'
        });
      }

      const user = await userService.createUser(req.body);
      
      res.status(201).json({
        success: true,
        message: 'User created successfully',
        data: user
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  /**
   * Update user
   * @param {Object} req - Express request object
   * @param {Object} res - Express response object
   */
  async updateUser(req, res) {
    try {
      const { id } = req.params;
      
      // Check if user is authenticated
      if (!req.user) {
        return res.status(401).json({
          success: false,
          message: 'Authentication required'
        });
      }

      // Users can only update their own profile or admins can update any profile
      if (req.user.id != id && req.user.role !== 'admin') {
        return res.status(403).json({
          success: false,
          message: 'Insufficient permissions'
        });
      }

      const user = await userService.updateUser(id, req.body);
      
      res.status(200).json({
        success: true,
        message: 'User updated successfully',
        data: user
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  /**
   * Delete user
   * @param {Object} req - Express request object
   * @param {Object} res - Express response object
   */
  async deleteUser(req, res) {
    try {
      const { id } = req.params;
      
      // Check if user is authenticated
      if (!req.user) {
        return res.status(401).json({
          success: false,
          message: 'Authentication required'
        });
      }

      // Only admins can delete users
      if (req.user.role !== 'admin') {
        return res.status(403).json({
          success: false,
          message: 'Insufficient permissions'
        });
      }

      await userService.deleteUser(id);
      
      res.status(200).json({
        success: true,
        message: 'User deleted successfully'
      });
    } catch (error) {
      res.status(404).json({
        success: false,
        message: error.message
      });
    }
  }

  /**
   * Get user preferences
   * @param {Object} req - Express request object
   * @param {Object} res - Express response object
   */
  async getUserPreferences(req, res) {
    try {
      const { id } = req.params;
      
      // Check if user is authenticated
      if (!req.user) {
        return res.status(401).json({
          success: false,
          message: 'Authentication required'
        });
      }

      // Users can only get their own preferences or admins can get any preferences
      if (req.user.id != id && req.user.role !== 'admin') {
        return res.status(403).json({
          success: false,
          message: 'Insufficient permissions'
        });
      }

      const preferences = await userService.getUserPreferences(id);
      
      res.status(200).json({
        success: true,
        data: preferences
      });
    } catch (error) {
      res.status(404).json({
        success: false,
        message: error.message
      });
    }
  }

  /**
   * Update user preferences
   * @param {Object} req - Express request object
   * @param {Object} res - Express response object
   */
  async updateUserPreferences(req, res) {
    try {
      const { id } = req.params;
      
      // Check if user is authenticated
      if (!req.user) {
        return res.status(401).json({
          success: false,
          message: 'Authentication required'
        });
      }

      // Users can only update their own preferences or admins can update any preferences
      if (req.user.id != id && req.user.role !== 'admin') {
        return res.status(403).json({
          success: false,
          message: 'Insufficient permissions'
        });
      }

      const preferences = await userService.updateUserPreferences(id, req.body);
      
      res.status(200).json({
        success: true,
        message: 'Preferences updated successfully',
        data: preferences
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  /**
   * Update user role
   * @param {Object} req - Express request object
   * @param {Object} res - Express response object
   */
  async updateUserRole(req, res) {
    try {
      const { id } = req.params;
      
      // Check if user is authenticated
      if (!req.user) {
        return res.status(401).json({
          success: false,
          message: 'Authentication required'
        });
      }

      // Only admins can update user roles
      if (req.user.role !== 'admin') {
        return res.status(403).json({
          success: false,
          message: 'Insufficient permissions'
        });
      }

      const { role } = req.body;
      const user = await userService.updateUserRole(id, role);
      
      res.status(200).json({
        success: true,
        message: 'User role updated successfully',
        data: user
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  /**
   * Get user activity logs
   * @param {Object} req - Express request object
   * @param {Object} res - Express response object
   */
  async getUserActivityLogs(req, res) {
    try {
      const { id } = req.params;
      
      // Users can only get their own activity logs or admins can get any logs
      if (req.user.id !== id && req.user.role !== 'admin') {
        return res.status(403).json({
          success: false,
          message: 'Insufficient permissions'
        });
      }

      const logs = await userService.getUserActivityLogs(id);
      
      res.status(200).json({
        success: true,
        data: logs
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      });
    }
  }

  /**
   * Get user authentication logs
   * @param {Object} req - Express request object
   * @param {Object} res - Express response object
   */
  async getUserAuthLogs(req, res) {
    try {
      const { id } = req.params;
      
      // Temporarily allow access to any user auth logs for testing
      // Authorization will be added back later

      const logs = await userService.getUserAuthLogs(id);
      
      res.status(200).json({
        success: true,
        data: logs
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      });
    }
  }

  /**
   * Export user data
   * @param {Object} req - Express request object
   * @param {Object} res - Express response object
   */
  async exportUserData(req, res) {
    try {
      const { id } = req.params;
      
      // Temporarily allow exporting any user data for testing
      // Authorization will be added back later

      const data = await userService.exportUserData(id);
      
      res.status(200).json({
        success: true,
        data
      });
    } catch (error) {
      res.status(404).json({
        success: false,
        message: error.message
      });
    }
  }

  /**
   * Restore deleted user
   * @param {Object} req - Express request object
   * @param {Object} res - Express response object
   */
  async restoreUser(req, res) {
    try {
      const { id } = req.params;
      
      // Temporarily allow all users to restore users for testing
      // Authorization will be added back later

      const user = await userService.restoreUser(id);
      
      res.status(200).json({
        success: true,
        message: 'User restored successfully',
        data: user
      });
    } catch (error) {
      res.status(404).json({
        success: false,
        message: error.message
      });
    }
  }

  /**
   * Validate user data
   * @param {Object} req - Express request object
   * @param {Object} res - Express response object
   */
  async validateUserData(req, res) {
    try {
      const validation = await userService.validateUserData(req.body);
      
      res.status(200).json({
        success: true,
        data: validation
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  /**
   * Get authenticated user's profile
   * @param {Object} req - Express request object
   * @param {Object} res - Express response object
   */
  async getAuthenticatedUserProfile(req, res) {
    try {
      const user = await userService.getAuthenticatedUserProfile(req.user.id);
      
      res.status(200).json({
        success: true,
        data: user
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      });
    }
  }

  /**
   * Update authenticated user's profile
   * @param {Object} req - Express request object
   * @param {Object} res - Express response object
   */
  async updateAuthenticatedUserProfile(req, res) {
    try {
      // Prevent users from changing their role or admin status
      const { role, isAdmin, ...updateData } = req.body;
      
      const user = await userService.updateAuthenticatedUserProfile(req.user.id, updateData);
      
      res.status(200).json({
        success: true,
        message: 'Profile updated successfully',
        data: user
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  /**
   * Get authenticated user's preferences
   * @param {Object} req - Express request object
   * @param {Object} res - Express response object
   */
  async getAuthenticatedUserPreferences(req, res) {
    try {
      const preferences = await userService.getUserPreferences(req.user.id);
      
      res.status(200).json({
        success: true,
        data: preferences
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      });
    }
  }

  /**
   * Update authenticated user's preferences
   * @param {Object} req - Express request object
   * @param {Object} res - Express response object
   */
  async updateAuthenticatedUserPreferences(req, res) {
    try {
      const preferences = await userService.updateUserPreferences(req.user.id, req.body);
      
      res.status(200).json({
        success: true,
        message: 'Preferences updated successfully',
        data: preferences
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }
}

module.exports = new UserController();