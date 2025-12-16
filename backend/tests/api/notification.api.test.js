const request = require('supertest');
const { app, server } = require('../../src/server');
const { User, Notification, NotificationTemplate, NotificationPreference } = require('../../src/models');
const jwtUtils = require('../../src/utils/jwt.utils');
const passwordUtils = require('../../src/utils/password.utils');

describe('API Notification Endpoints', () => {
  let adminUser, analystUser, adminToken, analystToken;
  let testNotification, testTemplate;

  beforeAll(async () => {
    // Create test users
    const adminPassword = await passwordUtils.hashPassword('AdminPass123!');
    const analystPassword = await passwordUtils.hashPassword('AnalystPass123!');

    adminUser = await User.create({
      firstName: 'Admin',
      lastName: 'User',
      email: 'admin_notif_' + Date.now() + '@test.com',
      passwordHash: adminPassword,
      role: 'admin'
    });

    analystUser = await User.create({
      firstName: 'Analyst',
      lastName: 'User',
      email: 'analyst_notif_' + Date.now() + '@test.com',
      passwordHash: analystPassword,
      role: 'analyst'
    });

    // Create test notification
    testNotification = await Notification.create({
      userId: analystUser.id,
      type: 'IN_APP',
      title: 'Test Notification',
      message: 'This is a test notification',
      status: 'PENDING',
      priority: 'NORMAL'
    });

    // Create test template
    testTemplate = await NotificationTemplate.create({
      name: 'Test Template ' + Date.now(),
      type: 'IN_APP',
      subject: 'Test Subject',
      content: 'This is a test template content with {{variable}}',
      variables: ['variable'],
      isActive: true
    });

    // Generate tokens
    adminToken = jwtUtils.generateAccessToken({
      id: adminUser.id,
      email: adminUser.email,
      role: adminUser.role
    });

    analystToken = jwtUtils.generateAccessToken({
      id: analystUser.id,
      email: analystUser.email,
      role: analystUser.role
    });
  });

  afterAll(async () => {
    // Clean up test data
    if (testNotification && testNotification.id) {
      await Notification.destroy({
        where: {
          id: testNotification.id
        }
      });
    }

    if (testTemplate && testTemplate.id) {
      await NotificationTemplate.destroy({
        where: {
          id: testTemplate.id
        }
      });
    }

    if (adminUser && adminUser.id) {
      await User.destroy({
        where: {
          id: adminUser.id
        }
      });
    }

    if (analystUser && analystUser.id) {
      await User.destroy({
        where: {
          id: analystUser.id
        }
      });
    }
    
    server.close();
  });

  describe('GET /api/notifications', () => {
    it('should allow user to get their own notifications', async () => {
      const response = await request(app)
        .get('/api/notifications')
        .set('Authorization', `Bearer ${analystToken}`)
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(Array.isArray(response.body.data)).toBe(true);
      expect(response.body.data.length).toBeGreaterThanOrEqual(1);
    });

    it('should allow admin to get all notifications', async () => {
      const response = await request(app)
        .get('/api/notifications')
        .set('Authorization', `Bearer ${adminToken}`)
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(Array.isArray(response.body.data)).toBe(true);
    });
  });

  describe('POST /api/notifications', () => {
    it('should allow admin to create notification', async () => {
      const response = await request(app)
        .post('/api/notifications')
        .set('Authorization', `Bearer ${adminToken}`)
        .send({
          userId: analystUser.id,
          type: 'IN_APP',
          title: 'Admin Created Notification',
          message: 'This notification was created by admin',
          status: 'PENDING',
          priority: 'HIGH'
        })
        .expect(201);

      expect(response.body.success).toBe(true);
      expect(response.body.data.title).toBe('Admin Created Notification');
    });

    it('should not allow analyst to create notification', async () => {
      const response = await request(app)
        .post('/api/notifications')
        .set('Authorization', `Bearer ${analystToken}`)
        .send({
          userId: analystUser.id,
          type: 'IN_APP',
          title: 'Analyst Created Notification',
          message: 'This should fail',
          status: 'PENDING',
          priority: 'HIGH'
        })
        .expect(403);

      expect(response.body.success).toBe(false);
      expect(response.body.message).toBe('Insufficient permissions');
    });
  });

  describe('GET /api/notifications/:notificationId', () => {
    it('should allow user to get their own notification', async () => {
      const response = await request(app)
        .get(`/api/notifications/${testNotification.id}`)
        .set('Authorization', `Bearer ${analystToken}`)
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(response.body.data.id).toBe(testNotification.id);
    });

    it('should not allow user to get another user\'s notification', async () => {
      // Create a notification for admin user
      const adminNotification = await Notification.create({
        userId: adminUser.id,
        type: 'IN_APP',
        title: 'Admin Notification',
        message: 'This is an admin notification',
        status: 'PENDING',
        priority: 'NORMAL'
      });

      const response = await request(app)
        .get(`/api/notifications/${adminNotification.id}`)
        .set('Authorization', `Bearer ${analystToken}`)
        .expect(403);

      expect(response.body.success).toBe(false);
      expect(response.body.message).toBe('Insufficient permissions');
    });
  });

  describe('PUT /api/notifications/:notificationId/read', () => {
    it('should allow user to mark their own notification as read', async () => {
      const response = await request(app)
        .put(`/api/notifications/${testNotification.id}/read`)
        .set('Authorization', `Bearer ${analystToken}`)
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(response.body.data.status).toBe('READ');
    });
  });

  describe('GET /api/notification-templates', () => {
    it('should allow anyone to get notification templates', async () => {
      const response = await request(app)
        .get('/api/notifications/templates')
        .set('Authorization', `Bearer ${analystToken}`)
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(Array.isArray(response.body.data)).toBe(true);
    });
  });

  describe('POST /api/notification-templates', () => {
    it('should allow admin to create template', async () => {
      const response = await request(app)
        .post('/api/notifications/templates')
        .set('Authorization', `Bearer ${adminToken}`)
        .send({
          name: 'New Template',
          type: 'EMAIL',
          subject: 'New Template Subject',
          content: 'This is a new template',
          isActive: true
        })
        .expect(201);

      expect(response.body.success).toBe(true);
      expect(response.body.data.name).toBe('New Template');
      
      // Clean up
      await NotificationTemplate.destroy({
        where: {
          name: 'New Template'
        }
      });
    });

    it('should not allow analyst to create template', async () => {
      const response = await request(app)
        .post('/api/notifications/templates')
        .set('Authorization', `Bearer ${analystToken}`)
        .send({
          name: 'Unauthorized Template',
          type: 'EMAIL',
          subject: 'Unauthorized Template Subject',
          content: 'This should fail',
          isActive: true
        })
        .expect(403);

      expect(response.body.success).toBe(false);
      expect(response.body.message).toBe('Insufficient permissions');
    });
  });

  describe('GET /api/notification-preferences', () => {
    it('should allow user to get their own preferences', async () => {
      // Create test preferences
      await NotificationPreference.create({
        userId: analystUser.id,
        notificationType: 'REPORT',
        channel: 'EMAIL',
        isEnabled: true
      });

      const response = await request(app)
        .get('/api/notifications/preferences')
        .set('Authorization', `Bearer ${analystToken}`)
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(Array.isArray(response.body.data)).toBe(true);
    });
  });

  describe('PUT /api/notification-preferences', () => {
    it('should allow user to update their own preferences', async () => {
      const preferences = [
        {
          notificationType: 'ALERT',
          channel: 'IN_APP',
          isEnabled: true
        },
        {
          notificationType: 'REPORT',
          channel: 'EMAIL',
          isEnabled: false
        }
      ];

      const response = await request(app)
        .put('/api/notifications/preferences')
        .set('Authorization', `Bearer ${analystToken}`)
        .send({
          preferences
        })
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(response.body.message).toBe('Preferences updated successfully');
      expect(Array.isArray(response.body.data)).toBe(true);
      expect(response.body.data.length).toBe(2);
    });
  });

  describe('GET /api/notification-analytics', () => {
    it('should allow admin to get analytics', async () => {
      const response = await request(app)
        .get('/api/notifications/analytics')
        .set('Authorization', `Bearer ${adminToken}`)
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(Array.isArray(response.body.data)).toBe(true);
    });

    it('should not allow analyst to get analytics', async () => {
      const response = await request(app)
        .get('/api/notifications/analytics')
        .set('Authorization', `Bearer ${analystToken}`)
        .expect(403);

      expect(response.body.success).toBe(false);
      expect(response.body.message).toBe('Insufficient permissions');
    });
  });
});