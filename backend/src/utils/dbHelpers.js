const sequelize = require('../config/database');

class DatabaseHelpers {
  // Test database connection
  async testConnection() {
    try {
      await sequelize.authenticate();
      console.log('✅ Database connection has been established successfully.');
      return true;
    } catch (error) {
      console.error('❌ Unable to connect to the database:', error);
      return false;
    }
  }

  // Sync database models
  async syncDatabase() {
    try {
      await sequelize.sync({ alter: true });
      console.log('✅ Database models synchronized successfully.');
      return true;
    } catch (error) {
      console.error('❌ Error synchronizing database models:', error);
      return false;
    }
  }

  // Close database connection
  async closeConnection() {
    try {
      await sequelize.close();
      console.log('✅ Database connection closed successfully.');
      return true;
    } catch (error) {
      console.error('❌ Error closing database connection:', error);
      return false;
    }
  }
}

module.exports = new DatabaseHelpers();