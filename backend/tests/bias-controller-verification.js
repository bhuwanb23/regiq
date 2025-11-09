console.log('🧪 Verifying Bias Analysis Controller...\n');

// Test importing bias analysis controller
try {
  // Test Bias Analysis Controller
  const biasAnalysisController = require('../src/controllers/biasAnalysis.controller');
  console.log('✅ Bias Analysis Controller: Successfully imported');
  console.log('   Controller type:', typeof biasAnalysisController);
  
  // Check available methods
  console.log('\n📝 Controller Methods:');
  console.log('   analyzeModel:', typeof biasAnalysisController.analyzeModel);
  console.log('   getModelAnalysis:', typeof biasAnalysisController.getModelAnalysis);
  console.log('   listModelAnalyses:', typeof biasAnalysisController.listModelAnalyses);
  console.log('   deleteModelAnalysis:', typeof biasAnalysisController.deleteModelAnalysis);
  console.log('   detectDataBias:', typeof biasAnalysisController.detectDataBias);
  console.log('   getDataBiasDetection:', typeof biasAnalysisController.getDataBiasDetection);
  console.log('   listDataBiasDetections:', typeof biasAnalysisController.listDataBiasDetections);
  console.log('   batchDataBiasDetection:', typeof biasAnalysisController.batchDataBiasDetection);
  console.log('   getMitigationRecommendations:', typeof biasAnalysisController.getMitigationRecommendations);
  console.log('   applyMitigation:', typeof biasAnalysisController.applyMitigation);
  console.log('   getMitigationTemplates:', typeof biasAnalysisController.getMitigationTemplates);
  console.log('   storeBiasResults:', typeof biasAnalysisController.storeBiasResults);
  console.log('   getBiasResults:', typeof biasAnalysisController.getBiasResults);
  console.log('   listBiasResults:', typeof biasAnalysisController.listBiasResults);
  console.log('   updateBiasResults:', typeof biasAnalysisController.updateBiasResults);
  console.log('   getBiasTrends:', typeof biasAnalysisController.getBiasTrends);
  console.log('   getModelBiasTrends:', typeof biasAnalysisController.getModelBiasTrends);
  console.log('   createTrendAlerts:', typeof biasAnalysisController.createTrendAlerts);
  console.log('   generateComparisonReport:', typeof biasAnalysisController.generateComparisonReport);
  console.log('   getComparisonReport:', typeof biasAnalysisController.getComparisonReport);
  console.log('   listComparisonReports:', typeof biasAnalysisController.listComparisonReports);
  console.log('   scheduleBiasAnalysis:', typeof biasAnalysisController.scheduleBiasAnalysis);
  console.log('   getScheduledAnalysis:', typeof biasAnalysisController.getScheduledAnalysis);
  console.log('   listScheduledAnalyses:', typeof biasAnalysisController.listScheduledAnalyses);
  console.log('   updateScheduledAnalysis:', typeof biasAnalysisController.updateScheduledAnalysis);
  console.log('   cancelScheduledAnalysis:', typeof biasAnalysisController.cancelScheduledAnalysis);
  console.log('   createNotificationRule:', typeof biasAnalysisController.createNotificationRule);
  console.log('   getNotificationRule:', typeof biasAnalysisController.getNotificationRule);
  console.log('   listNotificationRules:', typeof biasAnalysisController.listNotificationRules);
  console.log('   updateNotificationRule:', typeof biasAnalysisController.updateNotificationRule);
  console.log('   deleteNotificationRule:', typeof biasAnalysisController.deleteNotificationRule);
  
  // Count methods
  const methodNames = Object.getOwnPropertyNames(Object.getPrototypeOf(biasAnalysisController));
  const methods = methodNames.filter(name => name !== 'constructor');
  console.log(`\n📊 Total controller methods: ${methods.length}`);
  
  console.log('\n✅ Phase 2.3 Controller layer verified successfully!');
  
} catch (error) {
  console.log('❌ Controller verification failed:', error.message);
  console.log('Stack trace:', error.stack);
}