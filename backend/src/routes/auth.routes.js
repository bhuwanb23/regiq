const express = require('express');
const authController = require('../controllers/auth.controller');
const { authenticate, authorize } = require('../middleware/auth.middleware');

const router = express.Router();

// Public routes
router.post('/register', authController.register);
router.post('/login', authController.login);
router.post('/refresh', authController.refreshToken);
router.post('/logout', authController.logout);

// Protected: returns the authenticated user's profile.
router.get('/profile', authenticate, (req, res) => {
  const user = req.user || {};
  const profile = typeof user.toJSON === 'function' ? user.toJSON() : { ...user };
  delete profile.passwordHash;
  res.json({
    success: true,
    data: profile
  });
});

// Protected admin-only stub for permission tests.
router.get('/admin', authenticate, authorize('admin'), (req, res) => {
  res.json({
    success: true,
    message: 'Admin endpoint reachable'
  });
});

module.exports = router;