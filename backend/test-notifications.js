const axios = require('axios');

async function testNotifications() {
  try {
    console.log('Testing Notification API endpoints...\n');
    
    // Test 1: Get notifications (should be empty initially)
    console.log('1. Testing GET /notifications...');
    const getResponse = await axios.get('http://localhost:3000/notifications/notifications');
    console.log('   Status:', getResponse.status);
    console.log('   Success:', getResponse.data.success);
    console.log('   Count:', getResponse.data.data.length);
    
    // Test 2: Create a notification
    console.log('\n2. Testing POST /notifications...');
    const notificationData = {
      userId: '123e4567-e89b-12d3-a456-426614174000',
      type: 'IN_APP',
      title: 'Test Notification',
      message: 'This is a test notification',
      priority: 'NORMAL'
    };
    
    const createResponse = await axios.post('http://localhost:3000/notifications/notifications', notificationData);
    console.log('   Status:', createResponse.status);
    console.log('   Success:', createResponse.data.success);
    console.log('   Created ID:', createResponse.data.data.id);
    
    // Test 3: Get notifications again (should have one now)
    console.log('\n3. Testing GET /notifications again...');
    const getResponse2 = await axios.get('http://localhost:3000/notifications/notifications');
    console.log('   Status:', getResponse2.status);
    console.log('   Success:', getResponse2.data.success);
    console.log('   Count:', getResponse2.data.data.length);
    
    // Test 4: Get specific notification
    console.log('\n4. Testing GET /notifications/:id...');
    const notificationId = createResponse.data.data.id;
    const getByIdResponse = await axios.get(`http://localhost:3000/notifications/notifications/${notificationId}`);
    console.log('   Status:', getByIdResponse.status);
    console.log('   Success:', getByIdResponse.data.success);
    console.log('   Title:', getByIdResponse.data.data.title);
    
    // Test 5: Update notification
    console.log('\n5. Testing PUT /notifications/:id...');
    const updateData = {
      status: 'READ',
      readAt: new Date()
    };
    
    const updateResponse = await axios.put(`http://localhost:3000/notifications/notifications/${notificationId}`, updateData);
    console.log('   Status:', updateResponse.status);
    console.log('   Success:', updateResponse.data.success);
    console.log('   Message:', updateResponse.data.message);
    
    // Test 6: Mark as read endpoint
    console.log('\n6. Testing PUT /notifications/:id/read...');
    const markAsReadResponse = await axios.put(`http://localhost:3000/notifications/notifications/${notificationId}/read`);
    console.log('   Status:', markAsReadResponse.status);
    console.log('   Success:', markAsReadResponse.data.success);
    console.log('   Message:', markAsReadResponse.data.message);
    
    // Test 7: Delete notification
    console.log('\n7. Testing DELETE /notifications/:id...');
    const deleteResponse = await axios.delete(`http://localhost:3000/notifications/notifications/${notificationId}`);
    console.log('   Status:', deleteResponse.status);
    console.log('   Success:', deleteResponse.data.success);
    console.log('   Message:', deleteResponse.data.message);
    
    // Test 8: Get notifications again (should be empty now)
    console.log('\n8. Testing GET /notifications final check...');
    const getResponse3 = await axios.get('http://localhost:3000/notifications/notifications');
    console.log('   Status:', getResponse3.status);
    console.log('   Success:', getResponse3.data.success);
    console.log('   Count:', getResponse3.data.data.length);
    
    console.log('\nAll tests completed successfully!');
  } catch (error) {
    console.error('Error during testing:');
    if (error.response) {
      console.error('  Status:', error.response.status);
      console.error('  Data:', error.response.data);
      console.error('  Headers:', error.response.headers);
    } else if (error.request) {
      console.error('  Request error:', error.request);
    } else {
      console.error('  Message:', error.message);
      console.error('  Stack:', error.stack);
    }
  }
}

testNotifications();