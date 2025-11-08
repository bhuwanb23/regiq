const express = require('express');
const userController = require('../controllers/user.controller');
const { authenticate, authorize } = require('../middleware/auth.middleware');

const router = express.Router();

// Apply authentication middleware to all routes
router.use(authenticate);

// User Profile CRUD Endpoints
router.get('/', authorize('admin'), userController.getAllUsers);
router.get('/:id', userController.getUserById);
router.post('/', authorize('admin'), userController.createUser);
router.put('/:id', userController.updateUser);
router.delete('/:id', authorize('admin'), userController.deleteUser);

// User Preferences Management
router.get('/:id/preferences', userController.getUserPreferences);
router.put('/:id/preferences', userController.updateUserPreferences);

// User Activity Logging
router.get('/:id/activity', userController.getUserActivityLogs);

// User Role Management
router.put('/:id/roles', authorize('admin'), userController.updateUserRole);

// User Authentication Logs
router.get('/:id/auth-logs', userController.getUserAuthLogs);

// User Data Export Functionality
router.get('/:id/export', userController.exportUserData);

// User Account Management
router.post('/:id/restore', authorize('admin'), userController.restoreUser);

// User Data Validation
router.post('/validate', userController.validateUserData);

module.exports = router;