const express = require('express');
const authController = require('../controllers/auth.controller');

const router = express.Router();

// Public routes
router.post('/register', authController.register);
router.post('/login', authController.login);
router.post('/refresh', authController.refreshToken);
router.post('/logout', authController.logout);

// Public routes for testing
router.get('/profile', (req, res) => {
  res.json({
    success: true,
    message: 'Profile endpoint accessible without authentication'
  });
});

router.get('/admin', (req, res) => {
  res.json({
    success: true,
    message: 'Admin endpoint accessible without authentication'
  });
});

module.exports = router;