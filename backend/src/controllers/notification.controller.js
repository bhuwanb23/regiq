const notificationService = require('../services/notification.service');

class NotificationController {
  /**
   * Get all notifications with filtering and pagination
   * @param {Object} req - Express request object
   * @param {Object} res - Express response object
   */
  async getAllNotifications(req, res) {
    try {
      // Users can only get their own notifications unless they are admin
      const { page, limit, type, status, priority } = req.query;
      const filters = {};
      
      // Non-admin users can only see their own notifications
      if (req.user.role !== 'admin') {
        filters.userId = req.user.id;
      } else if (req.query.userId) {
        // Admins can filter by userId
        filters.userId = req.query.userId;
      }
      
      if (type) filters.type = type;
      if (status) filters.status = status;
      if (priority) filters.priority = priority;

      const pagination = {
        page: parseInt(page) || 1,
        limit: parseInt(limit) || 10
      };

      const result = await notificationService.getNotifications(filters, pagination);
      res.json({
        success: true,
        data: result.data,
        pagination: {
          page: result.page,
          limit: result.limit,
          totalCount: result.totalCount,
          totalPages: Math.ceil(result.totalCount / result.limit)
        }
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      });
    }
  }

  /**
   * Create a new notification
   * @param {Object} req - Express request object
   * @param {Object} res - Express response object
   */
  async createNotification(req, res) {
    try {
      // Check if user is authenticated
      if (!req.user) {
        return res.status(401).json({
          success: false,
          message: 'Authentication required'
        });
      }

      // Only admins can create notifications
      if (req.user.role !== 'admin') {
        return res.status(403).json({
          success: false,
          message: 'Insufficient permissions'
        });
      }

      const notificationData = req.body;
      const notification = await notificationService.createNotification(notificationData);
      res.status(201).json({
        success: true,
        data: notification
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  /**
   * Get notification by ID
   * @param {Object} req - Express request object
   * @param {Object} res - Express response object
   */
  async getNotificationById(req, res) {
    try {
      const { notificationId } = req.params;
      
      // Check if user is authenticated
      if (!req.user) {
        return res.status(401).json({
          success: false,
          message: 'Authentication required'
        });
      }

      const notification = await notificationService.getNotificationById(notificationId);
      
      // Non-admin users can only access their own notifications
      if (req.user.role !== 'admin' && notification.userId !== req.user.id) {
        return res.status(403).json({
          success: false,
          message: 'Insufficient permissions'
        });
      }
      
      res.json({
        success: true,
        data: notification
      });
    } catch (error) {
      res.status(404).json({
        success: false,
        message: error.message
      });
    }
  }

  /**
   * Update notification
   * @param {Object} req - Express request object
   * @param {Object} res - Express response object
   */
  async updateNotification(req, res) {
    try {
      const { notificationId } = req.params;
      
      // Check if user is authenticated
      if (!req.user) {
        return res.status(401).json({
          success: false,
          message: 'Authentication required'
        });
      }

      // Only admins can update notifications
      if (req.user.role !== 'admin') {
        return res.status(403).json({
          success: false,
          message: 'Insufficient permissions'
        });
      }

      const updateData = req.body;
      const notification = await notificationService.updateNotification(notificationId, updateData);
      res.json({
        success: true,
        data: notification,
        message: 'Notification updated successfully'
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  /**
   * Delete notification
   * @param {Object} req - Express request object
   * @param {Object} res - Express response object
   */
  async deleteNotification(req, res) {
    try {
      const { notificationId } = req.params;
      
      // Check if user is authenticated
      if (!req.user) {
        return res.status(401).json({
          success: false,
          message: 'Authentication required'
        });
      }

      // Only admins can delete notifications
      if (req.user.role !== 'admin') {
        return res.status(403).json({
          success: false,
          message: 'Insufficient permissions'
        });
      }

      await notificationService.deleteNotification(notificationId);
      res.json({
        success: true,
        message: 'Notification deleted successfully'
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  /**
   * Mark notification as read
   * @param {Object} req - Express request object
   * @param {Object} res - Express response object
   */
  async markAsRead(req, res) {
    try {
      const { notificationId } = req.params;
      
      // Check if user is authenticated
      if (!req.user) {
        return res.status(401).json({
          success: false,
          message: 'Authentication required'
        });
      }

      const notification = await notificationService.getNotificationById(notificationId);
      
      // Users can only mark their own notifications as read
      if (req.user.role !== 'admin' && notification.userId !== req.user.id) {
        return res.status(403).json({
          success: false,
          message: 'Insufficient permissions'
        });
      }

      const updatedNotification = await notificationService.markAsRead(notificationId);
      res.json({
        success: true,
        data: updatedNotification,
        message: 'Notification marked as read'
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  /**
   * Get all notification templates
   * @param {Object} req - Express request object
   * @param {Object} res - Express response object
   */
  async getAllTemplates(req, res) {
    try {
      // Anyone can get templates
      const { page, limit, type, isActive } = req.query;
      const filters = {};
      if (type) filters.type = type;
      if (isActive !== undefined) filters.isActive = isActive === 'true';

      const pagination = {
        page: parseInt(page) || 1,
        limit: parseInt(limit) || 10
      };

      const result = await notificationService.getTemplates(filters, pagination);
      res.json({
        success: true,
        data: result.data,
        pagination: {
          page: result.page,
          limit: result.limit,
          totalCount: result.totalCount,
          totalPages: Math.ceil(result.totalCount / result.limit)
        }
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      });
    }
  }

  /**
   * Create a new notification template
   * @param {Object} req - Express request object
   * @param {Object} res - Express response object
   */
  async createTemplate(req, res) {
    try {
      // Check if user is authenticated
      if (!req.user) {
        return res.status(401).json({
          success: false,
          message: 'Authentication required'
        });
      }

      // Only admins can create templates
      if (req.user.role !== 'admin') {
        return res.status(403).json({
          success: false,
          message: 'Insufficient permissions'
        });
      }

      const templateData = req.body;
      const template = await notificationService.createTemplate(templateData);
      res.status(201).json({
        success: true,
        data: template
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  /**
   * Get notification template by ID
   * @param {Object} req - Express request object
   * @param {Object} res - Express response object
   */
  async getTemplateById(req, res) {
    try {
      // Anyone can get a template by ID
      const { templateId } = req.params;
      const template = await notificationService.getTemplateById(templateId);
      res.json({
        success: true,
        data: template
      });
    } catch (error) {
      res.status(404).json({
        success: false,
        message: error.message
      });
    }
  }

  /**
   * Update notification template
   * @param {Object} req - Express request object
   * @param {Object} res - Express response object
   */
  async updateTemplate(req, res) {
    try {
      // Check if user is authenticated
      if (!req.user) {
        return res.status(401).json({
          success: false,
          message: 'Authentication required'
        });
      }

      // Only admins can update templates
      if (req.user.role !== 'admin') {
        return res.status(403).json({
          success: false,
          message: 'Insufficient permissions'
        });
      }

      const { templateId } = req.params;
      const updateData = req.body;
      const template = await notificationService.updateTemplate(templateId, updateData);
      res.json({
        success: true,
        data: template,
        message: 'Template updated successfully'
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  /**
   * Delete notification template
   * @param {Object} req - Express request object
   * @param {Object} res - Express response object
   */
  async deleteTemplate(req, res) {
    try {
      // Check if user is authenticated
      if (!req.user) {
        return res.status(401).json({
          success: false,
          message: 'Authentication required'
        });
      }

      // Only admins can delete templates
      if (req.user.role !== 'admin') {
        return res.status(403).json({
          success: false,
          message: 'Insufficient permissions'
        });
      }

      const { templateId } = req.params;
      await notificationService.deleteTemplate(templateId);
      res.json({
        success: true,
        message: 'Template deleted successfully'
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  /**
   * Get user notification preferences
   * @param {Object} req - Express request object
   * @param {Object} res - Express response object
   */
  async getUserPreferences(req, res) {
    try {
      // Check if user is authenticated
      if (!req.user) {
        return res.status(401).json({
          success: false,
          message: 'Authentication required'
        });
      }

      // Users can only get their own preferences
      const userId = req.user.id;
      const preferences = await notificationService.getUserPreferences(userId);
      res.json({
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
   * Update user notification preferences
   * @param {Object} req - Express request object
   * @param {Object} res - Express response object
   */
  async updateUserPreferences(req, res) {
    try {
      // Check if user is authenticated
      if (!req.user) {
        return res.status(401).json({
          success: false,
          message: 'Authentication required'
        });
      }

      // Users can only update their own preferences
      const userId = req.user.id;
      const preferences = req.body.preferences || req.body;
      const updatedPreferences = await notificationService.updateUserPreferences(userId, preferences);
      res.json({
        success: true,
        data: updatedPreferences,
        message: 'Preferences updated successfully'
      });
    } catch (error) {
      res.status(400).json({
        success: false,
        message: error.message
      });
    }
  }

  /**
   * Get notification analytics
   * @param {Object} req - Express request object
   * @param {Object} res - Express response object
   */
  async getAnalytics(req, res) {
    try {
      // Check if user is authenticated
      if (!req.user) {
        return res.status(401).json({
          success: false,
          message: 'Authentication required'
        });
      }

      // Only admins can access analytics
      if (req.user.role !== 'admin') {
        return res.status(403).json({
          success: false,
          message: 'Insufficient permissions'
        });
      }

      const { page, limit, notificationId } = req.query;
      const filters = {};
      if (notificationId) filters.notificationId = notificationId;

      const pagination = {
        page: parseInt(page) || 1,
        limit: parseInt(limit) || 10
      };

      const result = await notificationService.getAnalytics(filters, pagination);
      res.json({
        success: true,
        data: result.data,
        pagination: {
          page: result.page,
          limit: result.limit,
          totalCount: result.totalCount,
          totalPages: Math.ceil(result.totalCount / result.limit)
        }
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      });
    }
  }
}

module.exports = new NotificationController();