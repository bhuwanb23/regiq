const request = require('supertest');
const app = require('../src/server').app;
const { Alert, User } = require('../src/models');
const alertService = require('../src/services/alert.service');
const passwordUtils = require('../src/utils/password.utils');

describe('Alert API', () => {
  let testAlert;
  let authToken;
  let testUser;

  beforeAll(async () => {
    // Create a test user
    const hashedPassword = await passwordUtils.hashPassword('TestPass123!');
    testUser = await User.create({
      firstName: 'Test',
      lastName: 'User',
      email: 'test.alert@example.com',
      passwordHash: hashedPassword,
      role: 'analyst'
    });

    // Login to get auth token
    const loginRes = await request(app)
      .post('/auth/login')
      .send({
        email: 'test.alert@example.com',
        password: 'TestPass123!'
      });

    authToken = loginRes.body.data.accessToken;

    // Create a test alert for testing
    testAlert = await alertService.createAlert({
      type: 'TEST_ALERT',
      severity: 'HIGH',
      message: 'Test alert message',
      details: { test: true }
    });
  });

  afterAll(async () => {
    // Clean up test data
    await Alert.destroy({ where: { id: testAlert.id } });
    if (testUser) {
      await User.destroy({ where: { id: testUser.id } });
    }
  });

  describe('GET /alerts', () => {
    it('should get all alerts with pagination', async () => {
      const response = await request(app)
        .get('/alerts')
        .set('Authorization', `Bearer ${authToken}`)
        .query({ page: 1, limit: 10 })
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(Array.isArray(response.body.data)).toBe(true);
    });
  });

  describe('PUT /alerts/:alertId/resolve', () => {
    it('should resolve an alert', async () => {
      const response = await request(app)
        .put(`/alerts/${testAlert.id}/resolve`)
        .set('Authorization', `Bearer ${authToken}`)
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(response.body.data.resolved).toBe(true);
    });
  });

  describe('GET /alerts/statistics', () => {
    it('should get alert statistics', async () => {
      const response = await request(app)
        .get('/alerts/statistics')
        .set('Authorization', `Bearer ${authToken}`)
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(response.body.data).toHaveProperty('totalAlerts');
      expect(response.body.data).toHaveProperty('unresolvedAlerts');
    });
  });
});

describe('Alert Service', () => {
  describe('createAlert', () => {
    it('should create a new alert', async () => {
      const alertData = {
        type: 'SERVICE_TEST_ALERT',
        severity: 'MEDIUM',
        message: 'Service test alert message',
        details: { serviceTest: true }
      };

      const alert = await alertService.createAlert(alertData);
      
      expect(alert.type).toBe(alertData.type);
      expect(alert.severity).toBe(alertData.severity);
      expect(alert.message).toBe(alertData.message);
      expect(alert.resolved).toBe(false);
      
      // Clean up
      await Alert.destroy({ where: { id: alert.id } });
    });
  });

  describe('getAllAlerts', () => {
    let testAlert1, testAlert2;

    beforeAll(async () => {
      testAlert1 = await alertService.createAlert({
        type: 'FILTER_TEST_1',
        severity: 'HIGH',
        message: 'Filter test 1'
      });

      testAlert2 = await alertService.createAlert({
        type: 'FILTER_TEST_2',
        severity: 'MEDIUM',
        message: 'Filter test 2'
      });
    });

    afterAll(async () => {
      await Alert.destroy({ where: { id: [testAlert1.id, testAlert2.id] } });
    });

    it('should get all alerts with filtering', async () => {
      const result = await alertService.getAllAlerts({
        type: 'FILTER_TEST_1'
      });

      expect(result.data.length).toBeGreaterThan(0);
      expect(result.data[0].type).toBe('FILTER_TEST_1');
    });

    it('should get alerts with pagination', async () => {
      const result = await alertService.getAllAlerts({}, { page: 1, limit: 1 });
      
      expect(result.data.length).toBe(1);
      expect(result.page).toBe(1);
      expect(result.limit).toBe(1);
    });
  });

  describe('resolveAlert', () => {
    let testAlert;

    beforeAll(async () => {
      testAlert = await alertService.createAlert({
        type: 'RESOLVE_TEST',
        severity: 'LOW',
        message: 'Resolve test alert'
      });
    });

    afterAll(async () => {
      await Alert.destroy({ where: { id: testAlert.id } });
    });

    it('should resolve an alert', async () => {
      const resolvedAlert = await alertService.resolveAlert(testAlert.id);
      
      expect(resolvedAlert.resolved).toBe(true);
      expect(resolvedAlert.resolvedAt).toBeDefined();
    });
  });

  describe('getAlertStatistics', () => {
    let testAlert;

    beforeAll(async () => {
      testAlert = await alertService.createAlert({
        type: 'STATS_TEST',
        severity: 'HIGH',
        message: 'Stats test alert'
      });
    });

    afterAll(async () => {
      await Alert.destroy({ where: { id: testAlert.id } });
    });

    it('should get alert statistics', async () => {
      const statistics = await alertService.getAlertStatistics();
      
      expect(statistics.totalAlerts).toBeGreaterThanOrEqual(1);
      expect(statistics.unresolvedAlerts).toBeGreaterThanOrEqual(1);
      expect(Array.isArray(statistics.alertsByType)).toBe(true);
      expect(Array.isArray(statistics.alertsBySeverity)).toBe(true);
    });
  });
});