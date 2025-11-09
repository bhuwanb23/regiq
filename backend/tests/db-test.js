const sequelize = require('../src/config/database');
const { ModelAnalysis } = require('../src/models');

async function testConnection() {
  try {
    await sequelize.authenticate();
    console.log('✅ Database connection successful');
    
    // Try to query the ModelAnalysis table
    const analyses = await ModelAnalysis.findAll();
    console.log('✅ ModelAnalysis query successful, found:', analyses.length, 'records');
    
  } catch (error) {
    console.log('❌ Database test failed:', error.message);
    console.log('Error stack:', error.stack);
  } finally {
    await sequelize.close();
  }
}

testConnection();