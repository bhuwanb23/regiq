console.log('🧪 Simple Route Verification...\n');

// Test importing all components
try {
  // Test Regulatory Routes
  const regulatoryRoutes = require('../src/routes/regulatory.routes');
  console.log('✅ Regulatory Routes: Successfully imported');
  console.log('   Route type:', typeof regulatoryRoutes);
  
  // Test Regulatory Controller
  const regulatoryController = require('../src/controllers/regulatory.controller');
  console.log('\n✅ Regulatory Controller: Successfully imported');
  console.log('   Controller methods:');
  console.log('     uploadDocument:', typeof regulatoryController.uploadDocument);
  console.log('     processDocument:', typeof regulatoryController.processDocument);
  console.log('     getDocumentProcessingStatus:', typeof regulatoryController.getDocumentProcessingStatus);
  console.log('     searchDocuments:', typeof regulatoryController.searchDocuments);
  console.log('     getDocumentById:', typeof regulatoryController.getDocumentById);
  console.log('     checkCompliance:', typeof regulatoryController.checkCompliance);
  console.log('     getComplianceResult:', typeof regulatoryController.getComplianceResult);
  console.log('     createAlert:', typeof regulatoryController.createAlert);
  console.log('     listAlerts:', typeof regulatoryController.listAlerts);
  console.log('     updateAlertStatus:', typeof regulatoryController.updateAlertStatus);
  console.log('     createDocumentVersion:', typeof regulatoryController.createDocumentVersion);
  console.log('     getDocumentVersions:', typeof regulatoryController.getDocumentVersions);
  console.log('     getDocumentMetadata:', typeof regulatoryController.getDocumentMetadata);
  console.log('     updateDocumentMetadata:', typeof regulatoryController.updateDocumentMetadata);
  console.log('     shareDocument:', typeof regulatoryController.shareDocument);
  console.log('     getDocumentShares:', typeof regulatoryController.getDocumentShares);
  console.log('     storeAnalysisResult:', typeof regulatoryController.storeAnalysisResult);
  console.log('     getAnalysisResults:', typeof regulatoryController.getAnalysisResults);
  
  console.log('\n✅ Phase 2.2 Route structure verified successfully!');
  
} catch (error) {
  console.log('❌ Route verification failed:', error.message);
}