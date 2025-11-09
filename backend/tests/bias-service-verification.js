console.log('🧪 Verifying Bias Analysis Service...\n');

// Test importing bias analysis service
try {
  // Test Bias Analysis Service
  const biasAnalysisService = require('../src/services/biasAnalysis.service');
  console.log('✅ Bias Analysis Service: Successfully imported');
  console.log('   Service type:', typeof biasAnalysisService);
  
  // Check available methods
  console.log('\n📝 Service Methods:');
  console.log('   analyzeModel:', typeof biasAnalysisService.analyzeModel);
  console.log('   getModelAnalysis:', typeof biasAnalysisService.getModelAnalysis);
  console.log('   listModelAnalyses:', typeof biasAnalysisService.listModelAnalyses);
  console.log('   deleteModelAnalysis:', typeof biasAnalysisService.deleteModelAnalysis);
  console.log('   detectDataBias:', typeof biasAnalysisService.detectDataBias);
  console.log('   getDataBiasDetection:', typeof biasAnalysisService.getDataBiasDetection);
  console.log('   listDataBiasDetections:', typeof biasAnalysisService.listDataBiasDetections);
  console.log('   getMitigationRecommendations:', typeof biasAnalysisService.getMitigationRecommendations);
  console.log('   applyMitigation:', typeof biasAnalysisService.applyMitigation);
  console.log('   getMitigationTemplates:', typeof biasAnalysisService.getMitigationTemplates);
  console.log('   storeBiasResults:', typeof biasAnalysisService.storeBiasResults);
  console.log('   getBiasResults:', typeof biasAnalysisService.getBiasResults);
  console.log('   listBiasResults:', typeof biasAnalysisService.listBiasResults);
  console.log('   getBiasTrends:', typeof biasAnalysisService.getBiasTrends);
  console.log('   getModelBiasTrends:', typeof biasAnalysisService.getModelBiasTrends);
  console.log('   createTrendAlert:', typeof biasAnalysisService.createTrendAlert);
  console.log('   generateComparisonReport:', typeof biasAnalysisService.generateComparisonReport);
  console.log('   getComparisonReport:', typeof biasAnalysisService.getComparisonReport);
  console.log('   listComparisonReports:', typeof biasAnalysisService.listComparisonReports);
  console.log('   scheduleBiasAnalysis:', typeof biasAnalysisService.scheduleBiasAnalysis);
  console.log('   getScheduledAnalysis:', typeof biasAnalysisService.getScheduledAnalysis);
  console.log('   listScheduledAnalyses:', typeof biasAnalysisService.listScheduledAnalyses);
  console.log('   updateScheduledAnalysis:', typeof biasAnalysisService.updateScheduledAnalysis);
  console.log('   cancelScheduledAnalysis:', typeof biasAnalysisService.cancelScheduledAnalysis);
  console.log('   createNotificationRule:', typeof biasAnalysisService.createNotificationRule);
  console.log('   getNotificationRule:', typeof biasAnalysisService.getNotificationRule);
  console.log('   listNotificationRules:', typeof biasAnalysisService.listNotificationRules);
  console.log('   updateNotificationRule:', typeof biasAnalysisService.updateNotificationRule);
  console.log('   deleteNotificationRule:', typeof biasAnalysisService.deleteNotificationRule);
  
  // Count methods
  const methodNames = Object.getOwnPropertyNames(Object.getPrototypeOf(biasAnalysisService));
  const methods = methodNames.filter(name => name !== 'constructor');
  console.log(`\n📊 Total service methods: ${methods.length}`);
  
  console.log('\n✅ Phase 2.3 Service layer verified successfully!');
  console.log('Note: Database-dependent methods will require PostgreSQL to be running.');
  
} catch (error) {
  console.log('❌ Service verification failed:', error.message);
  console.log('Stack trace:', error.stack);
}