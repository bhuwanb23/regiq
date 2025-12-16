const axios = require('axios');
const { User } = require('../src/models');
const jwtUtils = require('../src/utils/jwt.utils');
const passwordUtils = require('../src/utils/password.utils');

// Base URL for the API
const BASE_URL = 'http://localhost:3000';

// Test users
let adminUser, analystUser, adminToken, analystToken;

async function setupTestUsers() {
  try {
    console.log('Setting up test users...');
    
    // Create test users
    const adminPassword = await passwordUtils.hashPassword('AdminPass123!');
    const analystPassword = await passwordUtils.hashPassword('AnalystPass123!');

    adminUser = await User.create({
      firstName: 'Admin',
      lastName: 'User',
      email: 'admin_api@test.com',
      passwordHash: adminPassword,
      role: 'admin'
    });

    analystUser = await User.create({
      firstName: 'Analyst',
      lastName: 'User',
      email: 'analyst_api@test.com',
      passwordHash: analystPassword,
      role: 'analyst'
    });

    // Generate tokens
    adminToken = jwtUtils.generateAccessToken({
      id: adminUser.id,
      email: adminUser.email,
      role: adminUser.role
    });

    analystToken = jwtUtils.generateAccessToken({
      id: analystUser.id,
      email: analystUser.email,
      role: analystUser.role
    });

    console.log('Test users created successfully!');
  } catch (error) {
    console.error('Error setting up test users:', error.message);
  }
}

async function testProfileEndpoints() {
  try {
    console.log('\n=== Testing Profile Endpoints ===');
    
    // Test get authenticated user profile
    console.log('1. Testing GET /api/users/profile (analyst)');
    const profileResponse = await axios.get(`${BASE_URL}/api/users/profile`, {
      headers: {
        'Authorization': `Bearer ${analystToken}`
      }
    });
    console.log('   Success:', profileResponse.data.success);
    console.log('   User:', profileResponse.data.data.email);
    
    // Test update authenticated user profile
    console.log('2. Testing PUT /api/users/profile (analyst)');
    const updateProfileResponse = await axios.put(`${BASE_URL}/api/users/profile`, 
      {
        firstName: 'Updated',
        lastName: 'Analyst'
      },
      {
        headers: {
          'Authorization': `Bearer ${analystToken}`
        }
      }
    );
    console.log('   Success:', updateProfileResponse.data.success);
    console.log('   Message:', updateProfileResponse.data.message);
    
  } catch (error) {
    console.error('Error testing profile endpoints:', error.message);
  }
}

async function testPreferencesEndpoints() {
  try {
    console.log('\n=== Testing Preferences Endpoints ===');
    
    // Test get authenticated user preferences
    console.log('1. Testing GET /api/users/preferences (analyst)');
    const prefResponse = await axios.get(`${BASE_URL}/api/users/preferences`, {
      headers: {
        'Authorization': `Bearer ${analystToken}`
      }
    });
    console.log('   Success:', prefResponse.data.success);
    console.log('   Theme:', prefResponse.data.data.theme);
    
    // Test update authenticated user preferences
    console.log('2. Testing PUT /api/users/preferences (analyst)');
    const updatePrefResponse = await axios.put(`${BASE_URL}/api/users/preferences`, 
      {
        theme: 'dark',
        notifications: false,
        language: 'es'
      },
      {
        headers: {
          'Authorization': `Bearer ${analystToken}`
        }
      }
    );
    console.log('   Success:', updatePrefResponse.data.success);
    console.log('   Updated preferences:', updatePrefResponse.data.data);
    
  } catch (error) {
    console.error('Error testing preferences endpoints:', error.message);
  }
}

async function testUserManagementEndpoints() {
  try {
    console.log('\n=== Testing User Management Endpoints ===');
    
    // Test get all users (admin only)
    console.log('1. Testing GET /api/users (admin)');
    const usersResponse = await axios.get(`${BASE_URL}/api/users`, {
      headers: {
        'Authorization': `Bearer ${adminToken}`
      }
    });
    console.log('   Success:', usersResponse.data.success);
    console.log('   Users count:', usersResponse.data.data.length);
    
    // Test get all users (analyst - should fail)
    console.log('2. Testing GET /api/users (analyst - should fail)');
    try {
      await axios.get(`${BASE_URL}/api/users`, {
        headers: {
          'Authorization': `Bearer ${analystToken}`
        }
      });
      console.log('   Unexpected success!');
    } catch (error) {
      console.log('   Correctly failed with status:', error.response.status);
      console.log('   Message:', error.response.data.message);
    }
    
    // Test get specific user (own profile)
    console.log('3. Testing GET /api/users/:id (own profile)');
    const userResponse = await axios.get(`${BASE_URL}/api/users/${analystUser.id}`, {
      headers: {
        'Authorization': `Bearer ${analystToken}`
      }
    });
    console.log('   Success:', userResponse.data.success);
    console.log('   User email:', userResponse.data.data.email);
    
  } catch (error) {
    console.error('Error testing user management endpoints:', error.message);
  }
}

async function cleanupTestUsers() {
  try {
    console.log('\nCleaning up test users...');
    
    // Clean up test users
    await User.destroy({
      where: {
        email: ['admin_api@test.com', 'analyst_api@test.com']
      }
    });
    
    console.log('Test users cleaned up successfully!');
  } catch (error) {
    console.error('Error cleaning up test users:', error.message);
  }
}

async function main() {
  console.log('Starting User API Tests...\n');
  
  await setupTestUsers();
  await testProfileEndpoints();
  await testPreferencesEndpoints();
  await testUserManagementEndpoints();
  await cleanupTestUsers();
  
  console.log('\nUser API Tests completed!');
}

// Run the tests
if (require.main === module) {
  main().catch(console.error);
}

module.exports = {
  setupTestUsers,
  testProfileEndpoints,
  testPreferencesEndpoints,
  testUserManagementEndpoints,
  cleanupTestUsers
};