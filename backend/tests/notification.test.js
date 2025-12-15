const request = require('supertest');
const { app } = require('../src/server');
const { sequelize, Notification, NotificationTemplate, NotificationPreference } = require('../src/models');

describe('Notification API', () => {
  beforeAll(async () => {
    // Sync database
    await sequelize.sync({ force: true });
  });

  afterAll(async () => {
    // Close database connection
    await sequelize.close();
  });

  describe('POST /notifications', () => {
    it('should create a new notification', async () => {
      const notificationData = {
        userId: '123e4567-e89b-12d3-a456-426614174000',
        type: 'IN_APP',
        title: 'Test Notification',
        message: 'This is a test notification',
        priority: 'NORMAL'
      };

      const response = await request(app)
        .post('/notifications')
        .send(notificationData)
        .expect(201);

      expect(response.body.success).toBe(true);
      expect(response.body.data.title).toBe(notificationData.title);
      expect(response.body.data.type).toBe(notificationData.type);
    });
  });

  describe('GET /notifications', () => {
    it('should retrieve notifications', async () => {
      const response = await request(app)
        .get('/notifications')
        .query({ limit: 10 })
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(Array.isArray(response.body.data)).toBe(true);
    });
  });
});

describe('Audit API', () => {
  describe('GET /audit/audit-logs', () => {
    it('should retrieve audit logs', async () => {
      const response = await request(app)
        .get('/audit/audit-logs')
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(Array.isArray(response.body.data)).toBe(true);
    });
  });
});