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
      
      // Users can only get their own profile or admins can get any profile
      if (req.user.id !== id && req.user.role !== 'admin') {
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
      
      // Users can only update their own profile or admins can update any profile
      if (req.user.id !== id && req.user.role !== 'admin') {
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
      
      // Users can only get their own preferences or admins can get any preferences
      if (req.user.id !== id && req.user.role !== 'admin') {
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
      
      // Users can only update their own preferences or admins can update any preferences
      if (req.user.id !== id && req.user.role !== 'admin') {
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
   * Update user role
   * @param {Object} req - Express request object
   * @param {Object} res - Express response object
   */
  async updateUserRole(req, res) {
    try {
      const { id } = req.params;
      
      // Only admins can update roles
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
   * Get user authentication logs
   * @param {Object} req - Express request object
   * @param {Object} res - Express response object
   */
  async getUserAuthLogs(req, res) {
    try {
      const { id } = req.params;
      
      // Users can only get their own auth logs or admins can get any logs
      if (req.user.id !== id && req.user.role !== 'admin') {
        return res.status(403).json({
          success: false,
          message: 'Insufficient permissions'
        });
      }

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
      
      // Users can only export their own data or admins can export any data
      if (req.user.id !== id && req.user.role !== 'admin') {
        return res.status(403).json({
          success: false,
          message: 'Insufficient permissions'
        });
      }

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
      
      // Only admins can restore users
      if (req.user.role !== 'admin') {
        return res.status(403).json({
          success: false,
          message: 'Insufficient permissions'
        });
      }

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
}

module.exports = new UserController();