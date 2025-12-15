const { User } = require('../src/models');

async function listUsers() {
  try {
    // Sync database
    // await sequelize.sync();
    
    // Get all users
    const users = await User.findAll();
    
    console.log('Existing users:');
    users.forEach(user => {
      console.log(`- ${user.firstName} ${user.lastName} (${user.email}) - Role: ${user.role}`);
    });
    
    process.exit(0);
  } catch (error) {
    console.error('Error:', error.message);
    process.exit(1);
  }
}

listUsers();