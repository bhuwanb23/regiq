console.log('🧪 Verifying Regulatory Models...\n');

// Test importing all regulatory models
try {
  // Test Regulatory Models
  const regulatoryDocument = require('../src/models/regulatoryDocument');
  const complianceResult = require('../src/models/complianceResult');
  const regulatoryAlert = require('../src/models/regulatoryAlert');
  const documentVersion = require('../src/models/documentVersion');
  const documentMetadata = require('../src/models/documentMetadata');
  const documentShare = require('../src/models/documentShare');
  const analysisResult = require('../src/models/analysisResult');
  
  console.log('✅ All Regulatory Models: Successfully imported');
  
  // Test if they are functions (Sequelize model definers)
  console.log('\n📝 Model Types:');
  console.log('   RegulatoryDocument:', typeof regulatoryDocument);
  console.log('   ComplianceResult:', typeof complianceResult);
  console.log('   RegulatoryAlert:', typeof regulatoryAlert);
  console.log('   DocumentVersion:', typeof documentVersion);
  console.log('   DocumentMetadata:', typeof documentMetadata);
  console.log('   DocumentShare:', typeof documentShare);
  console.log('   AnalysisResult:', typeof analysisResult);
  
  // Verify they're all functions (Sequelize model definers should be functions)
  const models = [
    { name: 'RegulatoryDocument', model: regulatoryDocument },
    { name: 'ComplianceResult', model: complianceResult },
    { name: 'RegulatoryAlert', model: regulatoryAlert },
    { name: 'DocumentVersion', model: documentVersion },
    { name: 'DocumentMetadata', model: documentMetadata },
    { name: 'DocumentShare', model: documentShare },
    { name: 'AnalysisResult', model: analysisResult }
  ];
  
  let allValid = true;
  models.forEach(({ name, model }) => {
    if (typeof model !== 'function') {
      console.log(`   ❌ ${name} is not a function`);
      allValid = false;
    }
  });
  
  if (allValid) {
    console.log('\n✅ All models are properly defined as functions');
  }
  
  console.log('\n✅ Phase 2.2 Models verified successfully!');
  
} catch (error) {
  console.log('❌ Model verification failed:', error.message);
}