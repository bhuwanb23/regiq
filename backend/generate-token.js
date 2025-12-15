const { User } = require('./src/models');
const jwtUtils = require('./src/utils/jwt.utils');

async function generateToken() {
  try {
    // Find the test user
    const user = await User.findOne({
      where: { email: 'test@example.com' }
    });

    if (!user) {
      console.log('Test user not found');
      process.exit(1);
    }

    // Generate access token
    const accessToken = jwtUtils.generateAccessToken({
      id: user.id,
      email: user.email,
      role: user.role
    });

    console.log('Access Token:');
    console.log(accessToken);
    
    process.exit(0);
  } catch (error) {
    console.error('Error generating token:', error.message);
    process.exit(1);
  }
}

generateToken();