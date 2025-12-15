const notificationService = require('../src/services/notification.service');

async function testNotificationService() {
  try {
    console.log('Testing Notification Service directly...\n');
    
    // Test 1: Create a notification
    console.log('1. Testing createNotification...');
    const notificationData = {
      userId: 1,
      type: 'IN_APP',
      title: 'Direct Service Test',
      message: 'This is a test notification created directly via the service',
      priority: 'NORMAL'
    };
    
    const createdNotification = await notificationService.createNotification(notificationData);
    console.log('   Success! Created notification with ID:', createdNotification.id);
    console.log('   Title:', createdNotification.title);
    
    // Test 2: Get notifications
    console.log('\n2. Testing getNotifications...');
    const notifications = await notificationService.getNotifications();
    console.log('   Success! Found', notifications.data.length, 'notifications');
    if (notifications.data.length > 0) {
      console.log('   First notification title:', notifications.data[0].title);
    }
    
    // Test 3: Get notification by ID
    console.log('\n3. Testing getNotificationById...');
    const fetchedNotification = await notificationService.getNotificationById(createdNotification.id);
    console.log('   Success! Fetched notification with title:', fetchedNotification.title);
    
    console.log('\n✅ All notification service tests completed successfully!');
    
  } catch (error) {
    console.error('❌ Error:', error.message);
    if (error.stack) {
      console.error('Stack trace:', error.stack);
    }
    process.exit(1);
  }
}

testNotificationService();