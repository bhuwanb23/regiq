const sequelize = require('../src/config/database');

async function testConnection() {
  try {
    await sequelize.authenticate();
    console.log('✅ Database connection successful');
  } catch (error) {
    console.log('❌ Database test failed:', error.message);
  } finally {
    await sequelize.close();
  }
}

testConnection();