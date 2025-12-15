const redisClient = require('./src/config/redis');

async function testRedis() {
  try {
    // Connect to Redis
    await redisClient.connect();
    
    // Test setting a value
    console.log('Setting test key...');
    await redisClient.set('test_key', 'Hello Redis!', 10); // Expire in 10 seconds
    
    // Test getting a value
    console.log('Getting test key...');
    const value = await redisClient.get('test_key');
    console.log('Retrieved value:', value);
    
    // Test checking existence
    console.log('Checking if key exists...');
    const exists = await redisClient.exists('test_key');
    console.log('Key exists:', exists);
    
    // Test deleting a key
    console.log('Deleting test key...');
    await redisClient.del('test_key');
    
    // Verify deletion
    console.log('Checking if key exists after deletion...');
    const existsAfterDelete = await redisClient.exists('test_key');
    console.log('Key exists after deletion:', existsAfterDelete);
    
    // Disconnect
    await redisClient.disconnect();
    
    console.log('Redis test completed successfully!');
  } catch (error) {
    console.error('Redis test failed:', error);
  }
}

testRedis();