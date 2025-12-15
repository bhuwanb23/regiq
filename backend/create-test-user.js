const { User } = require('./src/models');
const passwordUtils = require('./src/utils/password.utils');

async function createTestUser() {
  try {
    // Check if user already exists
    const existingUser = await User.findOne({
      where: { email: 'test@example.com' }
    });

    if (existingUser) {
      console.log('Test user already exists');
      console.log(`User: ${existingUser.firstName} ${existingUser.lastName} (${existingUser.email})`);
      process.exit(0);
    }

    // Hash password
    const hashedPassword = await passwordUtils.hashPassword('Password123!');
    
    // Create user
    const user = await User.create({
      firstName: 'Test',
      lastName: 'User',
      email: 'test@example.com',
      passwordHash: hashedPassword,
      role: 'admin'
    });

    console.log('Test user created successfully');
    console.log(`User: ${user.firstName} ${user.lastName} (${user.email})`);
    console.log(`Role: ${user.role}`);
    
    process.exit(0);
  } catch (error) {
    console.error('Error creating test user:', error.message);
    process.exit(1);
  }
}

createTestUser();