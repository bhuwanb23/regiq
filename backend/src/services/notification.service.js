const { Notification, NotificationTemplate, NotificationPreference, NotificationAnalytics, sequelize } = require('../models');
const { Op } = require('sequelize');
const winston = require('winston');
const websocketService = require('./websocket.service');

class NotificationService {
  constructor() {
    // Initialize logger
    this.logger = winston.createLogger({
      level: 'info',
      format: winston.format.json(),
      transports: [
        new winston.transports.Console(),
      ],
    });
  }

  /**
   * Create a new notification
   * @param {Object} notificationData - Notification data
   * @returns {Object} Created notification
   */
  async createNotification(notificationData) {
    try {
      const notification = await Notification.create(notificationData);
      
      this.logger.info('Notification created', { 
        notificationId: notification.id, 
        type: notification.type,
        userId: notification.userId
      });

      // Broadcast notification via WebSocket for real-time delivery
      this.broadcastNotification(notification);

      return notification;
    } catch (error) {
      this.logger.error('Failed to create notification', { error: error.message, notificationData });
      throw new Error(`Failed to create notification: ${error.message}`);
    }
  }

  /**
   * Get notifications with filtering and pagination
   * @param {Object} filters - Filter criteria
   * @param {Object} pagination - Pagination options
   * @returns {Array} Notifications
   */
  async getNotifications(filters = {}, pagination = {}) {
    try {
      const { page = 1, limit = 10 } = pagination;
      const offset = (page - 1) * limit;

      const whereClause = {};
      if (filters.userId) whereClause.userId = filters.userId;
      if (filters.type) whereClause.type = filters.type;
      if (filters.status) whereClause.status = filters.status;
      if (filters.priority) whereClause.priority = filters.priority;

      const notifications = await Notification.findAndCountAll({
        where: whereClause,
        limit,
        offset,
        order: [['createdAt', 'DESC']]
      });

      return {
        data: notifications.rows,
        totalCount: notifications.count,
        page,
        limit
      };
    } catch (error) {
      this.logger.error('Failed to get notifications', { error: error.message });
      throw new Error(`Failed to get notifications: ${error.message}`);
    }
  }

  /**
   * Get notification by ID
   * @param {string} notificationId - Notification ID
   * @returns {Object} Notification
   */
  async getNotificationById(notificationId) {
    try {
      const notification = await Notification.findByPk(notificationId);
      
      if (!notification) {
        throw new Error('Notification not found');
      }

      return notification;
    } catch (error) {
      this.logger.error('Failed to get notification', { error: error.message, notificationId });
      throw new Error(`Failed to get notification: ${error.message}`);
    }
  }

  /**
   * Update notification
   * @param {string} notificationId - Notification ID
   * @param {Object} updateData - Update data
   * @returns {Object} Updated notification
   */
  async updateNotification(notificationId, updateData) {
    try {
      const notification = await Notification.findByPk(notificationId);
      
      if (!notification) {
        throw new Error('Notification not found');
      }

      const updatedNotification = await notification.update(updateData);
      
      this.logger.info('Notification updated', { notificationId });
      return updatedNotification;
    } catch (error) {
      this.logger.error('Failed to update notification', { error: error.message, notificationId });
      throw new Error(`Failed to update notification: ${error.message}`);
    }
  }

  /**
   * Delete notification
   * @param {string} notificationId - Notification ID
   * @returns {boolean} Success status
   */
  async deleteNotification(notificationId) {
    try {
      const notification = await Notification.findByPk(notificationId);
      
      if (!notification) {
        throw new Error('Notification not found');
      }

      await notification.destroy();
      
      this.logger.info('Notification deleted', { notificationId });
      return true;
    } catch (error) {
      this.logger.error('Failed to delete notification', { error: error.message, notificationId });
      throw new Error(`Failed to delete notification: ${error.message}`);
    }
  }

  /**
   * Mark notification as read
   * @param {string} notificationId - Notification ID
   * @returns {Object} Updated notification
   */
  async markAsRead(notificationId) {
    try {
      const notification = await Notification.findByPk(notificationId);
      
      if (!notification) {
        throw new Error('Notification not found');
      }

      const updatedNotification = await notification.update({
        status: 'READ',
        readAt: new Date()
      });
      
      this.logger.info('Notification marked as read', { notificationId });
      return updatedNotification;
    } catch (error) {
      this.logger.error('Failed to mark notification as read', { error: error.message, notificationId });
      throw new Error(`Failed to mark notification as read: ${error.message}`);
    }
  }

  /**
   * Create a notification template
   * @param {Object} templateData - Template data
   * @returns {Object} Created template
   */
  async createTemplate(templateData) {
    try {
      const template = await NotificationTemplate.create(templateData);
      
      this.logger.info('Notification template created', { templateId: template.id });
      return template;
    } catch (error) {
      this.logger.error('Failed to create notification template', { error: error.message, templateData });
      throw new Error(`Failed to create notification template: ${error.message}`);
    }
  }

  /**
   * Get notification templates
   * @param {Object} filters - Filter criteria
   * @param {Object} pagination - Pagination options
   * @returns {Array} Templates
   */
  async getTemplates(filters = {}, pagination = {}) {
    try {
      const { page = 1, limit = 10 } = pagination;
      const offset = (page - 1) * limit;

      const whereClause = {};
      if (filters.type) whereClause.type = filters.type;
      if (filters.isActive !== undefined) whereClause.isActive = filters.isActive;

      const templates = await NotificationTemplate.findAndCountAll({
        where: whereClause,
        limit,
        offset,
        order: [['createdAt', 'DESC']]
      });

      return {
        data: templates.rows,
        totalCount: templates.count,
        page,
        limit
      };
    } catch (error) {
      this.logger.error('Failed to get notification templates', { error: error.message });
      throw new Error(`Failed to get notification templates: ${error.message}`);
    }
  }

  /**
   * Get notification template by ID
   * @param {string} templateId - Template ID
   * @returns {Object} Template
   */
  async getTemplateById(templateId) {
    try {
      const template = await NotificationTemplate.findByPk(templateId);
      
      if (!template) {
        throw new Error('Notification template not found');
      }

      return template;
    } catch (error) {
      this.logger.error('Failed to get notification template', { error: error.message, templateId });
      throw new Error(`Failed to get notification template: ${error.message}`);
    }
  }

  /**
   * Update notification template
   * @param {string} templateId - Template ID
   * @param {Object} updateData - Update data
   * @returns {Object} Updated template
   */
  async updateTemplate(templateId, updateData) {
    try {
      const template = await NotificationTemplate.findByPk(templateId);
      
      if (!template) {
        throw new Error('Notification template not found');
      }

      const updatedTemplate = await template.update(updateData);
      
      this.logger.info('Notification template updated', { templateId });
      return updatedTemplate;
    } catch (error) {
      this.logger.error('Failed to update notification template', { error: error.message, templateId });
      throw new Error(`Failed to update notification template: ${error.message}`);
    }
  }

  /**
   * Delete notification template
   * @param {string} templateId - Template ID
   * @returns {boolean} Success status
   */
  async deleteTemplate(templateId) {
    try {
      const template = await NotificationTemplate.findByPk(templateId);
      
      if (!template) {
        throw new Error('Notification template not found');
      }

      await template.destroy();
      
      this.logger.info('Notification template deleted', { templateId });
      return true;
    } catch (error) {
      this.logger.error('Failed to delete notification template', { error: error.message, templateId });
      throw new Error(`Failed to delete notification template: ${error.message}`);
    }
  }

  /**
   * Get user notification preferences
   * @param {string} userId - User ID
   * @returns {Array} User preferences
   */
  async getUserPreferences(userId) {
    try {
      const preferences = await NotificationPreference.findAll({
        where: { userId }
      });
      
      return preferences;
    } catch (error) {
      this.logger.error('Failed to get user notification preferences', { error: error.message, userId });
      throw new Error(`Failed to get user notification preferences: ${error.message}`);
    }
  }

  /**
   * Update user notification preferences
   * @param {string} userId - User ID
   * @param {Array} preferences - Preferences data
   * @returns {Array} Updated preferences
   */
  async updateUserPreferences(userId, preferences) {
    try {
      // Delete existing preferences for this user
      await NotificationPreference.destroy({
        where: { userId }
      });

      // Create new preferences
      const preferenceRecords = preferences.map(pref => ({
        ...pref,
        userId
      }));

      const createdPreferences = await NotificationPreference.bulkCreate(preferenceRecords);
      
      this.logger.info('User notification preferences updated', { userId });
      return createdPreferences;
    } catch (error) {
      this.logger.error('Failed to update user notification preferences', { error: error.message, userId });
      throw new Error(`Failed to update user notification preferences: ${error.message}`);
    }
  }

  /**
   * Record notification analytics
   * @param {Object} analyticsData - Analytics data
   * @returns {Object} Created analytics record
   */
  async recordAnalytics(analyticsData) {
    try {
      const analytics = await NotificationAnalytics.create(analyticsData);
      
      this.logger.info('Notification analytics recorded', { 
        analyticsId: analytics.id, 
        notificationId: analytics.notificationId 
      });
      return analytics;
    } catch (error) {
      this.logger.error('Failed to record notification analytics', { error: error.message, analyticsData });
      throw new Error(`Failed to record notification analytics: ${error.message}`);
    }
  }

  /**
   * Get notification analytics
   * @param {Object} filters - Filter criteria
   * @param {Object} pagination - Pagination options
   * @returns {Array} Analytics data
   */
  async getAnalytics(filters = {}, pagination = {}) {
    try {
      const { page = 1, limit = 10 } = pagination;
      const offset = (page - 1) * limit;

      const whereClause = {};
      if (filters.notificationId) whereClause.notificationId = filters.notificationId;
      if (filters.userId) whereClause.userId = filters.userId;

      const analytics = await NotificationAnalytics.findAndCountAll({
        where: whereClause,
        limit,
        offset,
        order: [['createdAt', 'DESC']]
      });

      return {
        data: analytics.rows,
        totalCount: analytics.count,
        page,
        limit
      };
    } catch (error) {
      this.logger.error('Failed to get notification analytics', { error: error.message });
      throw new Error(`Failed to get notification analytics: ${error.message}`);
    }
  }

  /**
   * Broadcast notification via WebSocket for real-time delivery
   * @param {Object} notification - Notification object
   */
  broadcastNotification(notification) {
    try {
      // Broadcast notification to user via WebSocket
      websocketService.broadcastJobUpdate(`user_${notification.userId}`, {
        type: 'NOTIFICATION',
        notification: {
          id: notification.id,
          type: notification.type,
          title: notification.title,
          message: notification.message,
          priority: notification.priority,
          createdAt: notification.createdAt
        }
      });
    } catch (error) {
      this.logger.error('Failed to broadcast notification', { error: error.message, notificationId: notification.id });
    }
  }

  /**
   * Send scheduled notifications that are due
   */
  async sendScheduledNotifications() {
    try {
      const now = new Date();
      
      // Find pending scheduled notifications that are due
      const dueNotifications = await Notification.findAll({
        where: {
          status: 'PENDING',
          scheduledAt: {
            [Op.lte]: now
          }
        }
      });

      for (const notification of dueNotifications) {
        // Check user preferences before sending
        const canSend = await this.canSendNotification(
          notification.userId, 
          notification.type, 
          notification.channel
        );

        if (canSend) {
          // In a real implementation, this would send the notification
          // through the appropriate channel (email, push, etc.)
          
          // Update notification status
          await notification.update({
            status: 'SENT',
            sentAt: now
          });

          this.logger.info('Scheduled notification sent', { notificationId: notification.id });
        }
      }
    } catch (error) {
      this.logger.error('Failed to send scheduled notifications', { error: error.message });
    }
  }

  /**
   * Check if a notification can be sent based on user preferences
   * @param {string} userId - User ID
   * @param {string} notificationType - Notification type
   * @param {string} channel - Notification channel
   * @returns {boolean} Whether notification can be sent
   */
  async canSendNotification(userId, notificationType, channel) {
    try {
      const preference = await NotificationPreference.findOne({
        where: {
          userId,
          notificationType,
          channel,
          isEnabled: true
        }
      });

      return !!preference;
    } catch (error) {
      this.logger.error('Failed to check notification preference', { 
        error: error.message, 
        userId, 
        notificationType, 
        channel 
      });
      // Default to allowing notification if we can't check preferences
      return true;
    }
  }
  /**
   * Send scheduled notifications
   * @returns {Promise<void>}
   */
  async sendScheduledNotifications() {
    try {
      const now = new Date();
      
      // Find pending notifications that are scheduled for now or earlier
      const notifications = await Notification.findAll({
        where: {
          status: 'PENDING',
          scheduledAt: {
            [Op.lte]: now
          }
        }
      });
      
      // Send each notification
      for (const notification of notifications) {
        try {
          // Update notification status to SENT
          await notification.update({
            status: 'SENT',
            sentAt: new Date()
          });
          
          // Broadcast notification via WebSocket
          this.broadcastNotification(notification);
          
          this.logger.info('Scheduled notification sent', { notificationId: notification.id });
        } catch (error) {
          // Update notification status to FAILED
          await notification.update({
            status: 'FAILED'
          });
          
          this.logger.error('Failed to send scheduled notification', { 
            error: error.message, 
            notificationId: notification.id 
          });
        }
      }
    } catch (error) {
      this.logger.error('Failed to process scheduled notifications', { error: error.message });
      throw error;
    }
  }
  
  /**
   * Broadcast notification via WebSocket
   * @param {Object} notification - Notification to broadcast
   */
  broadcastNotification(notification) {
    try {
      websocketService.broadcastToUser(notification.userId, 'notification', notification);
    } catch (error) {
      this.logger.error('Failed to broadcast notification', { 
        error: error.message, 
        notificationId: notification.id 
      });
    }
  }
}

module.exports = new NotificationService();