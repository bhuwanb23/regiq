const { Sequelize } = require('sequelize');

// Create Sequelize instance using environment variables
const sequelize = new Sequelize(
  process.env.DB_NAME || 'regiq_backend',
  process.env.DB_USER || 'regiq_user',
  process.env.DB_PASSWORD || 'regiq_password',
  {
    host: process.env.DB_HOST || 'localhost',
    port: process.env.DB_PORT || 5432,
    dialect: 'postgres',
    logging: process.env.NODE_ENV === 'development' ? console.log : false,
    pool: {
      max: 10,
      min: 0,
      acquire: 30000,
      idle: 10000
    }
  }
);

module.exports = sequelize;