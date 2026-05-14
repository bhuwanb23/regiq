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
// All protected routes require a valid JWT (authenticate) before role check (authorize).
router.get('/', authenticate, authorize('admin'), userController.getAllUsers);
router.get('/:id', authenticate, userController.getUserById);
router.post('/', authenticate, authorize('admin'), userController.createUser);
router.put('/:id', authenticate, userController.updateUser);
router.delete('/:id', authenticate, authorize('admin'), userController.deleteUser);
router.put('/:id/roles', authenticate, authorize('admin'), userController.updateUserRole);

module.exports = router;