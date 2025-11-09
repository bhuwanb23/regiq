const biasAnalysisService = require('../src/services/biasAnalysis.service');

async function testService() {
  try {
    const analyses = await biasAnalysisService.listModelAnalyses();
    console.log('✅ ModelAnalysis service successful, found:', analyses.length, 'records');
    
  } catch (error) {
    console.log('❌ ModelAnalysis service failed:', error.message);
    console.log('Error stack:', error.stack);
  }
}

testService();