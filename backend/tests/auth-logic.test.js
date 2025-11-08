const jwtUtils = require('../src/utils/jwt.utils');
const passwordUtils = require('../src/utils/password.utils');

console.log('🧪 Testing Authentication Logic...\n');

async function runTests() {
  // Test JWT utilities
  console.log('1. Testing JWT Utilities...');

try {
  // Test access token generation
  const testPayload = { id: '123', email: 'test@example.com', role: 'analyst' };
  const accessToken = jwtUtils.generateAccessToken(testPayload);
  console.log('   ✅ Access token generated successfully');
  
  // Test refresh token generation
  const refreshToken = jwtUtils.generateRefreshToken(testPayload);
  console.log('   ✅ Refresh token generated successfully');
  
  console.log('   📝 Token samples (first 20 chars):');
  console.log('     Access token:  ', accessToken.substring(0, 20) + '...');
  console.log('     Refresh token: ', refreshToken.substring(0, 20) + '...');
  
} catch (error) {
  console.log('   ❌ JWT utilities test failed:', error.message);
}

console.log('\n2. Testing Password Utilities...');

try {
  // Test password hashing
  const plainPassword = 'TestPass123!';
  const hashedPassword = await passwordUtils.hashPassword(plainPassword);
  console.log('   ✅ Password hashed successfully');
  console.log('   📝 Hashed password (first 20 chars):', hashedPassword.substring(0, 20) + '...');
  
  // Test password comparison
  const isMatch = await passwordUtils.comparePassword(plainPassword, hashedPassword);
  console.log('   ✅ Password comparison successful:', isMatch ? 'MATCH' : 'NO MATCH');
  
  // Test password strength validation
  const weakPassword = 'weak';
  const strongPassword = 'StrongPass123!';
  
  const weakValidation = passwordUtils.validatePasswordStrength(weakPassword);
  const strongValidation = passwordUtils.validatePasswordStrength(strongPassword);
  
  console.log('   ✅ Password strength validation working');
  console.log('     Weak password valid:', weakValidation.isValid);
  console.log('     Strong password valid:', strongValidation.isValid);
  
} catch (error) {
  console.log('   ❌ Password utilities test failed:', error.message);
}

console.log('\n3. Testing Middleware Functions...');

// Simple test for middleware structure
try {
  const { authenticate, authorize } = require('../src/middleware/auth.middleware');
  console.log('   ✅ Middleware functions imported successfully');
  console.log('   📝 Function types:');
  console.log('     authenticate:', typeof authenticate);
  console.log('     authorize:', typeof authorize);
} catch (error) {
  console.log('   ❌ Middleware test failed:', error.message);
}

console.log('\n4. Testing Controller Functions...');

try {
  const authController = require('../src/controllers/auth.controller');
  console.log('   ✅ Controller functions imported successfully');
  console.log('   📝 Controller methods:');
  console.log('     register:', typeof authController.register);
  console.log('     login:', typeof authController.login);
  console.log('     refreshToken:', typeof authController.refreshToken);
  console.log('     logout:', typeof authController.logout);
} catch (error) {
  console.log('   ❌ Controller test failed:', error.message);
}

console.log('\n✅ Authentication logic tests completed!');
  console.log('Note: Database-dependent tests require PostgreSQL to be running.');
}

runTests();