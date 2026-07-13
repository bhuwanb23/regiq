const express = require('express');
const userController = require('../../controllers/user.controller');
const { authenticate, authorize } = require('../../middleware/auth.middleware');

const router = express.Router();

// ── Public Routes (No Authentication) - For Development ────────────────
// TODO: Add authentication middleware before production
router.get('/profile', userController.getPublicUserProfile);
router.put('/profile', userController.updatePublicUserProfile);
router.get('/preferences', userController.getPublicUserPreferences);
router.put('/preferences', userController.updatePublicUserPreferences);

// ── Protected Routes (With Authentication) ─────────────────────────────
// Apply authentication middleware to admin/protected routes
router.get('/', authorize('admin'), userController.getAllUsers);
router.get('/:id', userController.getUserById);
router.post('/', authorize('admin'), userController.createUser);
router.put('/:id', userController.updateUser);
router.delete('/:id', authorize('admin'), userController.deleteUser);
router.put('/:id/roles', authorize('admin'), userController.updateUserRole);

module.exports = router;