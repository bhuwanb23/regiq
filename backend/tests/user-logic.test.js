console.log('🧪 Testing User Management Logic...\n');

// Test importing user service
try {
  const userService = require('../src/services/user.service');
  console.log('✅ User service imported successfully');
  console.log('📝 Service methods:');
  console.log('   createUser:', typeof userService.createUser);
  console.log('   getAllUsers:', typeof userService.getAllUsers);
  console.log('   getUserById:', typeof userService.getUserById);
  console.log('   updateUser:', typeof userService.updateUser);
  console.log('   deleteUser:', typeof userService.deleteUser);
  console.log('   getUserPreferences:', typeof userService.getUserPreferences);
  console.log('   updateUserPreferences:', typeof userService.updateUserPreferences);
  console.log('   getUserActivityLogs:', typeof userService.getUserActivityLogs);
  console.log('   updateUserRole:', typeof userService.updateUserRole);
  console.log('   getUserAuthLogs:', typeof userService.getUserAuthLogs);
  console.log('   exportUserData:', typeof userService.exportUserData);
  console.log('   restoreUser:', typeof userService.restoreUser);
  console.log('   validateUserData:', typeof userService.validateUserData);
} catch (error) {
  console.log('❌ User service import test failed:', error.message);
}

// Test importing user controller
try {
  const userController = require('../src/controllers/user.controller');
  console.log('\n✅ User controller imported successfully');
  console.log('📝 Controller methods:');
  console.log('   getAllUsers:', typeof userController.getAllUsers);
  console.log('   getUserById:', typeof userController.getUserById);
  console.log('   createUser:', typeof userController.createUser);
  console.log('   updateUser:', typeof userController.updateUser);
  console.log('   deleteUser:', typeof userController.deleteUser);
  console.log('   getUserPreferences:', typeof userController.getUserPreferences);
  console.log('   updateUserPreferences:', typeof userController.updateUserPreferences);
  console.log('   getUserActivityLogs:', typeof userController.getUserActivityLogs);
  console.log('   updateUserRole:', typeof userController.updateUserRole);
  console.log('   getUserAuthLogs:', typeof userController.getUserAuthLogs);
  console.log('   exportUserData:', typeof userController.exportUserData);
  console.log('   restoreUser:', typeof userController.restoreUser);
  console.log('   validateUserData:', typeof userController.validateUserData);
} catch (error) {
  console.log('❌ User controller import test failed:', error.message);
}

// Test importing user routes
try {
  const userRoutes = require('../src/routes/user.routes');
  console.log('\n✅ User routes imported successfully');
  console.log('📝 Route module type:', typeof userRoutes);
} catch (error) {
  console.log('❌ User routes import test failed:', error.message);
}

console.log('\n✅ User management logic tests completed!');
console.log('Note: Database-dependent tests require PostgreSQL to be running.');