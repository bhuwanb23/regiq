const { User } = require('./src/models');

async function getUserInfo() {
  try {
    // Find the test user
    const user = await User.findOne({
      where: { email: 'test@example.com' }
    });

    if (!user) {
      console.log('Test user not found');
      process.exit(1);
    }

    console.log('User ID:', user.id);
    console.log('User Email:', user.email);
    
    process.exit(0);
  } catch (error) {
    console.error('Error getting user info:', error.message);
    process.exit(1);
  }
}

getUserInfo();