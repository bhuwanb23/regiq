const express = require('express');
const userController = require('../controllers/user.controller');

const router = express.Router();

// User Profile CRUD Endpoints
router.get('/', userController.getAllUsers);
router.get('/:id', userController.getUserById);
router.post('/', userController.createUser);
router.put('/:id', userController.updateUser);
router.delete('/:id', userController.deleteUser);

// User Preferences Management
router.get('/:id/preferences', userController.getUserPreferences);
router.put('/:id/preferences', userController.updateUserPreferences);

// User Activity Logging
router.get('/:id/activity', userController.getUserActivityLogs);

// User Role Management
router.put('/:id/roles', userController.updateUserRole);

// User Authentication Logs
router.get('/:id/auth-logs', userController.getUserAuthLogs);

// User Data Export Functionality
router.get('/:id/export', userController.exportUserData);

// User Account Management
router.post('/:id/restore', userController.restoreUser);

// User Data Validation
router.post('/validate', userController.validateUserData);

module.exports = router;