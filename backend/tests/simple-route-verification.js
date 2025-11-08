console.log('🧪 Verifying User Management Components...\n');

// Test importing all user management components
try {
  // Test User Model
  const userModel = require('../src/models/user.js');
  console.log('✅ User Model: Successfully imported');
  
  // Test User Service
  const userService = require('../src/services/user.service.js');
  console.log('✅ User Service: Successfully imported');
  
  // Test User Controller
  const userController = require('../src/controllers/user.controller.js');
  console.log('✅ User Controller: Successfully imported');
  
  // Test User Routes
  const userRoutes = require('../src/routes/user.routes.js');
  console.log('✅ User Routes: Successfully imported');
  
  // Test Auth Middleware
  const authMiddleware = require('../src/middleware/auth.middleware.js');
  console.log('✅ Auth Middleware: Successfully imported');
  
  console.log('\n📋 Component Method Counts:');
  console.log(`   User Service Methods: ${Object.keys(userService).length}`);
  console.log(`   User Controller Methods: ${Object.keys(userController).length}`);
  
  console.log('\n🔍 Verifying key methods:');
  
  // Check User Service methods
  const userServiceMethods = [
    'createUser', 'getAllUsers', 'getUserById', 'updateUser', 
    'deleteUser', 'getUserPreferences', 'updateUserPreferences',
    'getUserActivityLogs', 'updateUserRole', 'getUserAuthLogs',
    'exportUserData', 'restoreUser', 'validateUserData'
  ];
  
  userServiceMethods.forEach(method => {
    console.log(`   ${userService[method] ? '✅' : '❌'} User Service.${method}`);
  });
  
  // Check User Controller methods
  const userControllerMethods = [
    'getAllUsers', 'getUserById', 'createUser', 'updateUser',
    'deleteUser', 'getUserPreferences', 'updateUserPreferences',
    'getUserActivityLogs', 'updateUserRole', 'getUserAuthLogs',
    'exportUserData', 'restoreUser', 'validateUserData'
  ];
  
  userControllerMethods.forEach(method => {
    console.log(`   ${userController[method] ? '✅' : '❌'} User Controller.${method}`);
  });
  
} catch (error) {
  console.log('❌ Component verification failed:', error.message);
}

console.log('\n✅ User Management components verification completed!');