const express = require('express');
const router = express.Router();
const notificationController = require('../../controllers/notification.controller');
const { authenticate, authorize } = require('../../middleware/auth.middleware');

// Apply authentication middleware to all routes
router.use(authenticate);

// Notification templates (admin only for create/update/delete)
router.get('/templates', notificationController.getAllTemplates);
router.post('/templates', authorize('admin'), notificationController.createTemplate);
router.get('/templates/:templateId', notificationController.getTemplateById);
router.put('/templates/:templateId', authorize('admin'), notificationController.updateTemplate);
router.delete('/templates/:templateId', authorize('admin'), notificationController.deleteTemplate);

// Notification preferences (users can only manage their own preferences)
router.get('/preferences', notificationController.getUserPreferences);
router.put('/preferences', notificationController.updateUserPreferences);

// Notification analytics (admin only)
router.get('/analytics', authorize('admin'), notificationController.getAnalytics);

// Notification CRUD endpoints (user can only access their own notifications)
// These should come last to avoid conflicting with named routes above
router.get('/', notificationController.getAllNotifications);
router.post('/', authorize('admin'), notificationController.createNotification);
router.get('/:notificationId', notificationController.getNotificationById);
router.put('/:notificationId', authorize('admin'), notificationController.updateNotification);
router.delete('/:notificationId', authorize('admin'), notificationController.deleteNotification);
router.put('/:notificationId/read', notificationController.markAsRead);

module.exports = router;