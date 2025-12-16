const express = require('express');
const userController = require('../../controllers/user.controller');
const { authenticate, authorize } = require('../../middleware/auth.middleware');

const router = express.Router();

// Apply authentication middleware to all routes
router.use(authenticate);

// User Profile Management Endpoints
router.get('/profile', userController.getAuthenticatedUserProfile);
router.put('/profile', userController.updateAuthenticatedUserProfile);

// User Preferences Management
router.get('/preferences', userController.getAuthenticatedUserPreferences);
router.put('/preferences', userController.updateAuthenticatedUserPreferences);

// User Management Endpoints (Admin only for create/delete)
router.get('/', authorize('admin'), userController.getAllUsers);
router.get('/:id', userController.getUserById); // Users can get their own or admins can get any
router.post('/', authorize('admin'), userController.createUser);
router.put('/:id', userController.updateUser); // Users can update their own or admins can update any
router.delete('/:id', authorize('admin'), userController.deleteUser);

// User Role Management (Admin only)
router.put('/:id/roles', authorize('admin'), userController.updateUserRole);

module.exports = router;