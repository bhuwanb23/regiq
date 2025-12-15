const express = require('express');
const router = express.Router();
const notificationController = require('../controllers/notification.controller');
const { authenticate } = require('../middleware/auth.middleware');

// Apply authentication middleware to all routes
router.use(authenticate);

// Notification CRUD endpoints
router.get('/notifications', notificationController.getAllNotifications);
router.post('/notifications', notificationController.createNotification);
router.get('/notifications/:notificationId', notificationController.getNotificationById);
router.put('/notifications/:notificationId', notificationController.updateNotification);
router.delete('/notifications/:notificationId', notificationController.deleteNotification);
router.put('/notifications/:notificationId/read', notificationController.markAsRead);

// Notification templates
router.get('/notification-templates', notificationController.getAllTemplates);
router.post('/notification-templates', notificationController.createTemplate);
router.get('/notification-templates/:templateId', notificationController.getTemplateById);
router.put('/notification-templates/:templateId', notificationController.updateTemplate);
router.delete('/notification-templates/:templateId', notificationController.deleteTemplate);

// Notification preferences
router.get('/notification-preferences', notificationController.getUserPreferences);
router.put('/notification-preferences', notificationController.updateUserPreferences);

// Notification analytics
router.get('/notification-analytics', notificationController.getAnalytics);

module.exports = router;