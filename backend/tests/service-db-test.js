const { ModelAnalysis } = require('../src/models');

async function testService() {
  try {
    // Try to query the ModelAnalysis table
    const analyses = await ModelAnalysis.findAll();
    console.log('✅ ModelAnalysis query successful, found:', analyses.length, 'records');
    
  } catch (error) {
    console.log('❌ ModelAnalysis test failed:', error.message);
    console.log('Error stack:', error.stack);
  }
}

testService();