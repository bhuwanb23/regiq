console.log('🧪 Verifying Phase 2.2 Regulatory Intelligence API Components...\n');

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
  
  console.log('\n✅ Phase 2.2 Regulatory Intelligence API components verified successfully!');
  console.log('Note: Database-dependent functionality requires PostgreSQL to be running.');
  
} catch (error) {
  console.log('❌ Component verification failed:', error.message);
}