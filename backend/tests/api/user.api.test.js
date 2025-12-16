const request = require('supertest');
const { app, server } = require('../../src/server');
const { User } = require('../../src/models');
const jwtUtils = require('../../src/utils/jwt.utils');
const passwordUtils = require('../../src/utils/password.utils');

describe('API User Management Endpoints', () => {
  let adminUser, analystUser, adminToken, analystToken;

  beforeAll(async () => {
    // Create test users
    const adminPassword = await passwordUtils.hashPassword('AdminPass123!');
    const analystPassword = await passwordUtils.hashPassword('AnalystPass123!');

    adminUser = await User.create({
      firstName: 'Admin',
      lastName: 'User',
      email: 'admin@test.com',
      passwordHash: adminPassword,
      role: 'admin'
    });

    analystUser = await User.create({
      firstName: 'Analyst',
      lastName: 'User',
      email: 'analyst@test.com',
      passwordHash: analystPassword,
      role: 'analyst'
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
    // Clean up test users
    await User.destroy({
      where: {
        email: ['admin@test.com', 'analyst@test.com']
      }
    });
    
    server.close();
  });

  describe('GET /api/users/profile', () => {
    it('should get authenticated user profile', async () => {
      const response = await request(app)
        .get('/api/users/profile')
        .set('Authorization', `Bearer ${analystToken}`)
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(response.body.data.email).toBe(analystUser.email);
      expect(response.body.data.firstName).toBe(analystUser.firstName);
    });

    it('should fail without authentication', async () => {
      const response = await request(app)
        .get('/api/users/profile')
        .expect(401);

      expect(response.body.success).toBe(false);
      expect(response.body.message).toBe('Access token is required');
    });
  });

  describe('PUT /api/users/profile', () => {
    it('should update authenticated user profile', async () => {
      const response = await request(app)
        .put('/api/users/profile')
        .set('Authorization', `Bearer ${analystToken}`)
        .send({
          firstName: 'Updated',
          lastName: 'Analyst'
        })
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(response.body.message).toBe('Profile updated successfully');
    });

    it('should not allow changing role through profile update', async () => {
      const response = await request(app)
        .put('/api/users/profile')
        .set('Authorization', `Bearer ${analystToken}`)
        .send({
          role: 'admin'
        })
        .expect(200);

      // Role should not be changed
      const updatedUser = await User.findByPk(analystUser.id);
      expect(updatedUser.role).toBe('analyst');
    });
  });

  describe('GET /api/users/preferences', () => {
    it('should get authenticated user preferences', async () => {
      const response = await request(app)
        .get('/api/users/preferences')
        .set('Authorization', `Bearer ${analystToken}`)
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(response.body.data).toHaveProperty('theme');
      expect(response.body.data).toHaveProperty('notifications');
      expect(response.body.data).toHaveProperty('language');
    });
  });

  describe('PUT /api/users/preferences', () => {
    it('should update authenticated user preferences', async () => {
      const newPreferences = {
        theme: 'dark',
        notifications: false,
        language: 'es'
      };

      const response = await request(app)
        .put('/api/users/preferences')
        .set('Authorization', `Bearer ${analystToken}`)
        .send(newPreferences)
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(response.body.data.theme).toBe('dark');
      expect(response.body.data.notifications).toBe(false);
      expect(response.body.data.language).toBe('es');
    });
  });

  describe('GET /api/users', () => {
    it('should allow admin to get all users', async () => {
      const response = await request(app)
        .get('/api/users')
        .set('Authorization', `Bearer ${adminToken}`)
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(Array.isArray(response.body.data)).toBe(true);
    });

    it('should not allow analyst to get all users', async () => {
      const response = await request(app)
        .get('/api/users')
        .set('Authorization', `Bearer ${analystToken}`)
        .expect(403);

      expect(response.body.success).toBe(false);
      expect(response.body.message).toBe('Insufficient permissions');
    });
  });

  describe('GET /api/users/:id', () => {
    it('should allow user to get their own profile', async () => {
      const response = await request(app)
        .get(`/api/users/${analystUser.id}`)
        .set('Authorization', `Bearer ${analystToken}`)
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(response.body.data.email).toBe(analystUser.email);
    });

    it('should allow admin to get any user profile', async () => {
      const response = await request(app)
        .get(`/api/users/${analystUser.id}`)
        .set('Authorization', `Bearer ${adminToken}`)
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(response.body.data.email).toBe(analystUser.email);
    });

    it('should not allow user to get another user\'s profile', async () => {
      const response = await request(app)
        .get(`/api/users/${adminUser.id}`)
        .set('Authorization', `Bearer ${analystToken}`)
        .expect(403);

      expect(response.body.success).toBe(false);
      expect(response.body.message).toBe('Insufficient permissions');
    });
  });

  describe('POST /api/users', () => {
    it('should allow admin to create new user', async () => {
      const response = await request(app)
        .post('/api/users')
        .set('Authorization', `Bearer ${adminToken}`)
        .send({
          firstName: 'New',
          lastName: 'User',
          email: 'newuser@test.com',
          passwordHash: 'NewPass123!',
          role: 'analyst'
        })
        .expect(201);

      expect(response.body.success).toBe(true);
      expect(response.body.message).toBe('User created successfully');
      
      // Clean up
      await User.destroy({ where: { email: 'newuser@test.com' } });
    });

    it('should not allow analyst to create new user', async () => {
      const response = await request(app)
        .post('/api/users')
        .set('Authorization', `Bearer ${analystToken}`)
        .send({
          firstName: 'New',
          lastName: 'User',
          email: 'newuser2@test.com',
          passwordHash: 'NewPass123!',
          role: 'analyst'
        })
        .expect(403);

      expect(response.body.success).toBe(false);
      expect(response.body.message).toBe('Insufficient permissions');
    });
  });

  describe('PUT /api/users/:id', () => {
    it('should allow user to update their own profile', async () => {
      const response = await request(app)
        .put(`/api/users/${analystUser.id}`)
        .set('Authorization', `Bearer ${analystToken}`)
        .send({
          firstName: 'Updated',
          lastName: 'Analyst'
        })
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(response.body.message).toBe('User updated successfully');
    });

    it('should allow admin to update any user profile', async () => {
      const response = await request(app)
        .put(`/api/users/${analystUser.id}`)
        .set('Authorization', `Bearer ${adminToken}`)
        .send({
          firstName: 'Admin',
          lastName: 'Updated'
        })
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(response.body.message).toBe('User updated successfully');
    });
  });

  describe('DELETE /api/users/:id', () => {
    it('should allow admin to delete user', async () => {
      // Create a test user to delete
      const testUserPassword = await passwordUtils.hashPassword('TestPass123!');
      const testUser = await User.create({
        firstName: 'Test',
        lastName: 'Delete',
        email: 'testdelete@test.com',
        passwordHash: testUserPassword,
        role: 'analyst'
      });

      const response = await request(app)
        .delete(`/api/users/${testUser.id}`)
        .set('Authorization', `Bearer ${adminToken}`)
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(response.body.message).toBe('User deleted successfully');
    });

    it('should not allow analyst to delete user', async () => {
      const response = await request(app)
        .delete(`/api/users/${adminUser.id}`)
        .set('Authorization', `Bearer ${analystToken}`)
        .expect(403);

      expect(response.body.success).toBe(false);
      expect(response.body.message).toBe('Insufficient permissions');
    });
  });

  describe('PUT /api/users/:id/roles', () => {
    it('should allow admin to update user role', async () => {
      const response = await request(app)
        .put(`/api/users/${analystUser.id}/roles`)
        .set('Authorization', `Bearer ${adminToken}`)
        .send({
          role: 'compliance_officer'
        })
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(response.body.message).toBe('User role updated successfully');
    });

    it('should not allow analyst to update user role', async () => {
      const response = await request(app)
        .put(`/api/users/${analystUser.id}/roles`)
        .set('Authorization', `Bearer ${analystToken}`)
        .send({
          role: 'admin'
        })
        .expect(403);

      expect(response.body.success).toBe(false);
      expect(response.body.message).toBe('Insufficient permissions');
    });
  });
});