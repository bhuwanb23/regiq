console.log('🧪 Verifying Regulatory Intelligence Routes...\n');

// Test importing all regulatory intelligence components
try {
  // Test Regulatory Models
  const regulatoryDocument = require('../src/models/regulatoryDocument');
  const complianceResult = require('../src/models/complianceResult');
  const regulatoryAlert = require('../src/models/regulatoryAlert');
  const documentVersion = require('../src/models/documentVersion');
  const documentMetadata = require('../src/models/documentMetadata');
  const documentShare = require('../src/models/documentShare');
  const analysisResult = require('../src/models/analysisResult');
  
  console.log('✅ Regulatory Models: Successfully imported');
  
  // Test Regulatory Service
  const regulatoryService = require('../src/services/regulatory.service');
  console.log('✅ Regulatory Service: Successfully imported');
  
  // Test Regulatory Controller
  const regulatoryController = require('../src/controllers/regulatory.controller');
  console.log('✅ Regulatory Controller: Successfully imported');
  
  // Test Regulatory Routes
  const regulatoryRoutes = require('../src/routes/regulatory.routes');
  console.log('✅ Regulatory Routes: Successfully imported');
  
  console.log('\n📋 Component Method Counts:');
  console.log(`   Regulatory Service Methods: ${Object.keys(regulatoryService).length}`);
  console.log(`   Regulatory Controller Methods: ${Object.keys(regulatoryController).length}`);
  
  console.log('\n🔍 Verifying key service methods:');
  
  // Check Regulatory Service methods
  const serviceMethods = [
    'uploadDocument', 'processDocument', 'searchDocuments', 'checkCompliance',
    'createAlert', 'getAlerts', 'updateAlertStatus', 'createDocumentVersion',
    'getDocumentVersions', 'updateDocumentMetadata', 'getDocumentMetadata',
    'shareDocument', 'getSharedDocuments', 'storeAnalysisResult',
    'getAnalysisResult', 'getDocumentAnalysisResults'
  ];
  
  serviceMethods.forEach(method => {
    console.log(`   ${regulatoryService[method] ? '✅' : '❌'} Regulatory Service.${method}`);
  });
  
  console.log('\n🔍 Verifying key controller methods:');
  
  // Check Regulatory Controller methods
  const controllerMethods = [
    'uploadDocument', 'processDocument', 'searchDocuments', 'checkCompliance',
    'createAlert', 'getAlerts', 'updateAlertStatus', 'createDocumentVersion',
    'getDocumentVersions', 'updateDocumentMetadata', 'getDocumentMetadata',
    'shareDocument', 'getSharedDocuments', 'storeAnalysisResult',
    'getAnalysisResult', 'getDocumentAnalysisResults'
  ];
  
  controllerMethods.forEach(method => {
    console.log(`   ${regulatoryController[method] ? '✅' : '❌'} Regulatory Controller.${method}`);
  });
  
} catch (error) {
  console.log('❌ Component verification failed:', error.message);
}

console.log('\n✅ Regulatory Intelligence components verification completed!');