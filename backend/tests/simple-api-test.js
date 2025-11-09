console.log('🧪 Simple API Verification...\n');

// Test importing all components
try {
  // Test Bias Routes
  const biasRoutes = require('../src/routes/biasAnalysis.routes');
  console.log('✅ Bias Routes: Successfully imported');
  console.log('   Route type:', typeof biasRoutes);
  
  // Test Bias Controller
  const biasController = require('../src/controllers/biasAnalysis.controller');
  console.log('\n✅ Bias Controller: Successfully imported');
  console.log('   Controller methods:');
  console.log('     analyzeModel:', typeof biasController.analyzeModel);
  console.log('     getModelAnalysis:', typeof biasController.getModelAnalysis);
  console.log('     detectDataBias:', typeof biasController.detectDataBias);
  console.log('     getMitigationRecommendations:', typeof biasController.getMitigationRecommendations);
  
  // Test Bias Service
  const biasService = require('../src/services/biasAnalysis.service');
  console.log('\n✅ Bias Service: Successfully imported');
  console.log('   Service methods:');
  console.log('     analyzeModel:', typeof biasService.analyzeModel);
  console.log('     getModelAnalysis:', typeof biasService.getModelAnalysis);
  console.log('     detectDataBias:', typeof biasService.detectDataBias);
  console.log('     getMitigationRecommendations:', typeof biasService.getMitigationRecommendations);
  
  console.log('\n✅ API structure verified successfully!');
  console.log('Note: Database-dependent functionality requires PostgreSQL to be running.');
  
} catch (error) {
  console.log('❌ API verification failed:', error.message);
}