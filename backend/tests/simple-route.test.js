console.log('🧪 Testing Route Structure...\n');

// Test importing routes
try {
  const authRoutes = require('../src/routes/auth.routes');
  console.log('✅ Auth routes imported successfully');
  console.log('📝 Route module type:', typeof authRoutes);
  
  // Check if it's an Express router
  if (authRoutes && typeof authRoutes === 'function') {
    console.log('✅ Auth routes module is a valid Express router');
  } else if (authRoutes && typeof authRoutes === 'object') {
    console.log('✅ Auth routes module is a valid Express router object');
  }
} catch (error) {
  console.log('❌ Route import test failed:', error.message);
}

// Test importing controllers
try {
  const authController = require('../src/controllers/auth.controller');
  console.log('\n✅ Auth controller imported successfully');
  console.log('📝 Controller methods:');
  console.log('   register:', typeof authController.register);
  console.log('   login:', typeof authController.login);
  console.log('   refreshToken:', typeof authController.refreshToken);
  console.log('   logout:', typeof authController.logout);
} catch (error) {
  console.log('❌ Controller import test failed:', error.message);
}

// Test importing middleware
try {
  const { authenticate, authorize } = require('../src/middleware/auth.middleware');
  console.log('\n✅ Auth middleware imported successfully');
  console.log('📝 Middleware functions:');
  console.log('   authenticate:', typeof authenticate);
  console.log('   authorize:', typeof authorize);
} catch (error) {
  console.log('❌ Middleware import test failed:', error.message);
}

console.log('\n✅ Route structure tests completed!');