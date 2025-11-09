console.log('🧪 Verifying Bias Analysis Routes...\n');

// Test importing bias analysis routes
try {
  // Test Bias Analysis Routes
  const biasAnalysisRoutes = require('../src/routes/biasAnalysis.routes');
  console.log('✅ Bias Analysis Routes: Successfully imported');
  console.log('   Route type:', typeof biasAnalysisRoutes);
  
  console.log('\n✅ Phase 2.3 Routes verified successfully!');
  
} catch (error) {
  console.log('❌ Routes verification failed:', error.message);
}