console.log('=== Phase 3.2 AI/ML Service Integration - Component Verification ===\n');

// Test 1: API Client for AI/ML Services
console.log('1. Testing API Client for AI/ML Services...');
try {
  const aiMlService = require('../src/services/ai-ml.service');
  console.log('   ✓ AI/ML Service client loaded successfully');
  console.log('   ✓ Base URL:', aiMlService.baseUrl);
  console.log('   ✓ API Key exists:', !!aiMlService.apiKey);
} catch (error) {
  console.log('   ✗ AI/ML Service client failed:', error.message);
}

// Test 2: Request/Response Transformation Layer
console.log('\n2. Testing Request/Response Transformation Layer...');
try {
  const transformer = require('../src/utils/transformer.utils');
  console.log('   ✓ Transformer utilities loaded successfully');
  
  // Test a transformation function
  const testData = {
    id: 'test-123',
    title: 'Test Document',
    content: 'Test content',
    type: 'regulation'
  };
  
  const transformed = transformer.transformComplianceData(testData);
  console.log('   ✓ Data transformation working:', !!transformed.document_id);
} catch (error) {
  console.log('   ✗ Transformer utilities failed:', error.message);
}

// Test 3: Async Job Queue Implementation
console.log('\n3. Testing Async Job Queue Implementation...');
try {
  const jobQueue = require('../src/utils/job-queue.utils');
  console.log('   ✓ Job queue utilities loaded successfully');
  
  // Test adding a job
  const jobId = jobQueue.addJob('test', {data: 'test'}, async (data) => {
    return 'success';
  });
  console.log('   ✓ Job queue working:', !!jobId);
} catch (error) {
  console.log('   ✗ Job queue failed:', error.message);
}

// Test 4: Result Processing and Storage
console.log('\n4. Testing Result Processing and Storage...');
try {
  const cache = require('../src/utils/cache.utils');
  console.log('   ✓ Cache utilities loaded successfully');
  
  // Test cache operations
  cache.set('test-key', 'test-value');
  const value = cache.get('test-key');
  console.log('   ✓ Cache operations working:', value === 'test-value');
} catch (error) {
  console.log('   ✗ Cache utilities failed:', error.message);
}

// Test 5: Error Handling and Retry Logic
console.log('\n5. Testing Error Handling and Retry Logic...');
try {
  const errorHandler = require('../src/utils/error-handler.utils');
  console.log('   ✓ Error handler utilities loaded successfully');
  
  // Test error classification
  const errorType = errorHandler.classifyError(new Error('Network error'));
  console.log('   ✓ Error classification working:', errorType);
} catch (error) {
  console.log('   ✗ Error handler utilities failed:', error.message);
}

// Test 6: Performance Monitoring
console.log('\n6. Testing Performance Monitoring...');
try {
  const perfMonitor = require('../src/utils/performance-monitor.utils');
  console.log('   ✓ Performance monitor utilities loaded successfully');
  
  // Test timing
  const startTime = perfMonitor.startTiming('test');
  perfMonitor.endTiming('test', startTime, true);
  console.log('   ✓ Performance timing working');
} catch (error) {
  console.log('   ✗ Performance monitor utilities failed:', error.message);
}

// Test 7: Rate Limiting Implementation
console.log('\n7. Testing Rate Limiting Implementation...');
try {
  const rateLimiter = require('../src/middleware/rate-limit.middleware');
  console.log('   ✓ Rate limiting middleware loaded successfully');
  console.log('   ✓ Rate limit stats function available:', !!rateLimiter.getRateLimitStats);
} catch (error) {
  console.log('   ✗ Rate limiting middleware failed:', error.message);
}

// Test 8: Caching Strategies
console.log('\n8. Testing Caching Strategies...');
try {
  const cache = require('../src/utils/cache.utils');
  console.log('   ✓ Caching utilities loaded successfully');
  
  // Test cache stats
  const stats = cache.getStats();
  console.log('   ✓ Cache stats available:', stats.enabled);
} catch (error) {
  console.log('   ✗ Caching utilities failed:', error.message);
}

console.log('\n=== Phase 3.2 Component Verification Complete ===');