const express = require('express');
const authController = require('../controllers/auth.controller');
const { authenticate, authorize } = require('../middleware/auth.middleware');

const router = express.Router();

// Public routes
router.post('/register', authController.register);
router.post('/login', authController.login);
router.post('/refresh', authController.refreshToken);
router.post('/logout', authController.logout);

// Protected routes (example)
router.get('/profile', authenticate, (req, res) => {
  const user = req.user.toJSON();
  delete user.passwordHash;
  
  res.json({
    success: true,
    data: user
  });
});

router.get('/admin', authenticate, authorize('admin'), (req, res) => {
  res.json({
    success: true,
    message: 'Admin access granted',
    data: req.user
  });
});

module.exports = router;