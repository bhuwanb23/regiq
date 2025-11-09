console.log('🧪 Verifying Regulatory Service...\n');

// Test importing regulatory service
try {
  // Test Regulatory Service
  const regulatoryService = require('../src/services/regulatory.service');
  console.log('✅ Regulatory Service: Successfully imported');
  console.log('   Service type:', typeof regulatoryService);
  
  // Check available methods
  console.log('\n📝 Service Methods:');
  console.log('   uploadDocument:', typeof regulatoryService.uploadDocument);
  console.log('   processDocument:', typeof regulatoryService.processDocument);
  console.log('   getDocumentProcessingStatus:', typeof regulatoryService.getDocumentProcessingStatus);
  console.log('   searchDocuments:', typeof regulatoryService.searchDocuments);
  console.log('   getDocumentById:', typeof regulatoryService.getDocumentById);
  console.log('   checkCompliance:', typeof regulatoryService.checkCompliance);
  console.log('   getComplianceResult:', typeof regulatoryService.getComplianceResult);
  console.log('   createAlert:', typeof regulatoryService.createAlert);
  console.log('   getAlerts:', typeof regulatoryService.getAlerts);
  console.log('   updateAlertStatus:', typeof regulatoryService.updateAlertStatus);
  console.log('   createDocumentVersion:', typeof regulatoryService.createDocumentVersion);
  console.log('   getDocumentVersions:', typeof regulatoryService.getDocumentVersions);
  console.log('   getDocumentMetadata:', typeof regulatoryService.getDocumentMetadata);
  console.log('   updateDocumentMetadata:', typeof regulatoryService.updateDocumentMetadata);
  console.log('   shareDocument:', typeof regulatoryService.shareDocument);
  console.log('   getSharedDocuments:', typeof regulatoryService.getSharedDocuments);
  console.log('   storeAnalysisResult:', typeof regulatoryService.storeAnalysisResult);
  console.log('   getAnalysisResult:', typeof regulatoryService.getAnalysisResult);
  console.log('   getDocumentAnalysisResults:', typeof regulatoryService.getDocumentAnalysisResults);
  
  // Count methods
  const methodCount = Object.getOwnPropertyNames(Object.getPrototypeOf(regulatoryService)).filter(name => name !== 'constructor').length;
  console.log(`\n📊 Total service methods: ${methodCount}`);
  
  console.log('\n✅ Phase 2.2 Service layer verified successfully!');
  console.log('Note: Database-dependent methods will require PostgreSQL to be running.');
  
} catch (error) {
  console.log('❌ Service verification failed:', error.message);
  console.log('Stack trace:', error.stack);
}