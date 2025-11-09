console.log('🧪 Testing Regulatory Intelligence Logic...\n');

// Test importing regulatory models
try {
  const regulatoryDocument = require('../src/models/regulatoryDocument');
  const complianceResult = require('../src/models/complianceResult');
  const regulatoryAlert = require('../src/models/regulatoryAlert');
  const documentVersion = require('../src/models/documentVersion');
  const documentMetadata = require('../src/models/documentMetadata');
  const documentShare = require('../src/models/documentShare');
  const analysisResult = require('../src/models/analysisResult');
  
  console.log('✅ Regulatory models imported successfully');
  console.log('📝 Model types:');
  console.log('   RegulatoryDocument:', typeof regulatoryDocument);
  console.log('   ComplianceResult:', typeof complianceResult);
  console.log('   RegulatoryAlert:', typeof regulatoryAlert);
  console.log('   DocumentVersion:', typeof documentVersion);
  console.log('   DocumentMetadata:', typeof documentMetadata);
  console.log('   DocumentShare:', typeof documentShare);
  console.log('   AnalysisResult:', typeof analysisResult);
} catch (error) {
  console.log('❌ Regulatory models import test failed:', error.message);
}

// Test importing regulatory service
try {
  const regulatoryService = require('../src/services/regulatory.service');
  console.log('\n✅ Regulatory service imported successfully');
  console.log('📝 Service methods:');
  console.log('   uploadDocument:', typeof regulatoryService.uploadDocument);
  console.log('   processDocument:', typeof regulatoryService.processDocument);
  console.log('   searchDocuments:', typeof regulatoryService.searchDocuments);
  console.log('   checkCompliance:', typeof regulatoryService.checkCompliance);
  console.log('   createAlert:', typeof regulatoryService.createAlert);
  console.log('   createDocumentVersion:', typeof regulatoryService.createDocumentVersion);
  console.log('   updateDocumentMetadata:', typeof regulatoryService.updateDocumentMetadata);
  console.log('   shareDocument:', typeof regulatoryService.shareDocument);
  console.log('   storeAnalysisResult:', typeof regulatoryService.storeAnalysisResult);
} catch (error) {
  console.log('❌ Regulatory service import test failed:', error.message);
}

// Test importing regulatory controller
try {
  const regulatoryController = require('../src/controllers/regulatory.controller');
  console.log('\n✅ Regulatory controller imported successfully');
  console.log('📝 Controller methods:');
  console.log('   uploadDocument:', typeof regulatoryController.uploadDocument);
  console.log('   processDocument:', typeof regulatoryController.processDocument);
  console.log('   searchDocuments:', typeof regulatoryController.searchDocuments);
  console.log('   checkCompliance:', typeof regulatoryController.checkCompliance);
  console.log('   createAlert:', typeof regulatoryController.createAlert);
  console.log('   createDocumentVersion:', typeof regulatoryController.createDocumentVersion);
  console.log('   updateDocumentMetadata:', typeof regulatoryController.updateDocumentMetadata);
  console.log('   shareDocument:', typeof regulatoryController.shareDocument);
  console.log('   storeAnalysisResult:', typeof regulatoryController.storeAnalysisResult);
} catch (error) {
  console.log('❌ Regulatory controller import test failed:', error.message);
}

// Test importing regulatory routes
try {
  const regulatoryRoutes = require('../src/routes/regulatory.routes');
  console.log('\n✅ Regulatory routes imported successfully');
  console.log('📝 Route module type:', typeof regulatoryRoutes);
} catch (error) {
  console.log('❌ Regulatory routes import test failed:', error.message);
}

console.log('\n✅ Regulatory intelligence logic tests completed!');
console.log('Note: Database-dependent tests require PostgreSQL to be running.');