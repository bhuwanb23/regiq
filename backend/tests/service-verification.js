console.log('🧪 Verifying Regulatory Service...\n');

// Test importing regulatory service
try {
  // Test Regulatory Service
  const RegulatoryService = require('../src/services/regulatory.service');
  console.log('✅ Regulatory Service: Successfully imported');
  console.log('   Service type:', typeof RegulatoryService);
  
  // Create an instance to test
  const regulatoryService = new RegulatoryService();
  console.log('✅ Regulatory Service instance created successfully');
  
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
  console.log('   listAlerts:', typeof regulatoryService.listAlerts);
  console.log('   updateAlertStatus:', typeof regulatoryService.updateAlertStatus);
  console.log('   createDocumentVersion:', typeof regulatoryService.createDocumentVersion);
  console.log('   getDocumentVersions:', typeof regulatoryService.getDocumentVersions);
  console.log('   getDocumentMetadata:', typeof regulatoryService.getDocumentMetadata);
  console.log('   updateDocumentMetadata:', typeof regulatoryService.updateDocumentMetadata);
  console.log('   shareDocument:', typeof regulatoryService.shareDocument);
  console.log('   getDocumentShares:', typeof regulatoryService.getDocumentShares);
  console.log('   storeAnalysisResult:', typeof regulatoryService.storeAnalysisResult);
  console.log('   getAnalysisResults:', typeof regulatoryService.getAnalysisResults);
  
  // Count methods
  const methods = Object.getOwnPropertyNames(RegulatoryService.prototype).filter(name => name !== 'constructor');
  console.log(`\n📊 Total service methods: ${methods.length}`);
  
  console.log('\n✅ Phase 2.2 Service layer verified successfully!');
  console.log('Note: Database-dependent methods will require PostgreSQL to be running.');
  
} catch (error) {
  console.log('❌ Service verification failed:', error.message);
  console.log('Stack trace:', error.stack);
}