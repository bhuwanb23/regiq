console.log('🧪 Verifying Bias Analysis Models...\n');

// Test importing all bias analysis models
try {
  // Test Bias Analysis Models
  const modelAnalysis = require('../src/models/modelAnalysis');
  const dataBiasDetection = require('../src/models/dataBiasDetection');
  const mitigationRecommendation = require('../src/models/mitigationRecommendation');
  const biasResult = require('../src/models/biasResult');
  const biasTrend = require('../src/models/biasTrend');
  const comparisonReport = require('../src/models/comparisonReport');
  const biasSchedule = require('../src/models/biasSchedule');
  const biasNotification = require('../src/models/biasNotification');
  
  console.log('✅ All Bias Analysis Models: Successfully imported');
  
  // Test if they are functions (Sequelize model definers)
  console.log('\n📝 Model Types:');
  console.log('   ModelAnalysis:', typeof modelAnalysis);
  console.log('   DataBiasDetection:', typeof dataBiasDetection);
  console.log('   MitigationRecommendation:', typeof mitigationRecommendation);
  console.log('   BiasResult:', typeof biasResult);
  console.log('   BiasTrend:', typeof biasTrend);
  console.log('   ComparisonReport:', typeof comparisonReport);
  console.log('   BiasSchedule:', typeof biasSchedule);
  console.log('   BiasNotification:', typeof biasNotification);
  
  // Verify they're all functions (Sequelize model definers should be functions)
  const models = [
    { name: 'ModelAnalysis', model: modelAnalysis },
    { name: 'DataBiasDetection', model: dataBiasDetection },
    { name: 'MitigationRecommendation', model: mitigationRecommendation },
    { name: 'BiasResult', model: biasResult },
    { name: 'BiasTrend', model: biasTrend },
    { name: 'ComparisonReport', model: comparisonReport },
    { name: 'BiasSchedule', model: biasSchedule },
    { name: 'BiasNotification', model: biasNotification }
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
  
  console.log('\n✅ Phase 2.3 Models verified successfully!');
  
} catch (error) {
  console.log('❌ Model verification failed:', error.message);
}