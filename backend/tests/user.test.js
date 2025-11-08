const request = require('supertest');
const app = require('../src/server');
const { User } = require('../src/models');

describe('User Management API', () => {
  let adminUser, regularUser, adminToken, userToken;

  beforeAll(async () => {
    // Create test users
    adminUser = await User.create({
      firstName: 'Admin',
      lastName: 'User',
      email: 'admin@example.com',
      passwordHash: 'hashed_password_here',
      role: 'admin'
    });

    regularUser = await User.create({
      firstName: 'Regular',
      lastName: 'User',
      email: 'user@example.com',
      passwordHash: 'hashed_password_here',
      role: 'analyst'
    });

    // In a real test, we would generate actual tokens
    adminToken = 'admin_jwt_token';
    userToken = 'user_jwt_token';
  });

  afterAll(async () => {
    // Clean up test users
    if (adminUser) {
      await User.destroy({ where: { id: adminUser.id } });
    }
    if (regularUser) {
      await User.destroy({ where: { id: regularUser.id } });
    }
  });

  describe('GET /users', () => {
    it('should allow admin to get all users', async () => {
      const res = await request(app)
        .get('/users')
        .set('Authorization', `Bearer ${adminToken}`)
        .expect(200);

      expect(res.body.success).toBe(true);
      expect(Array.isArray(res.body.data)).toBe(true);
    });

    it('should not allow regular user to get all users', async () => {
      const res = await request(app)
        .get('/users')
        .set('Authorization', `Bearer ${userToken}`)
        .expect(403);

      expect(res.body.success).toBe(false);
      expect(res.body.message).toBe('Insufficient permissions');
    });
  });

  describe('GET /users/:id', () => {
    it('should allow user to get their own profile', async () => {
      const res = await request(app)
        .get(`/users/${regularUser.id}`)
        .set('Authorization', `Bearer ${userToken}`)
        .expect(200);

      expect(res.body.success).toBe(true);
      expect(res.body.data.id).toBe(regularUser.id);
    });

    it('should allow admin to get any user profile', async () => {
      const res = await request(app)
        .get(`/users/${regularUser.id}`)
        .set('Authorization', `Bearer ${adminToken}`)
        .expect(200);

      expect(res.body.success).toBe(true);
      expect(res.body.data.id).toBe(regularUser.id);
    });

    it('should not allow user to get another user\'s profile', async () => {
      const res = await request(app)
        .get(`/users/${adminUser.id}`)
        .set('Authorization', `Bearer ${userToken}`)
        .expect(403);

      expect(res.body.success).toBe(false);
      expect(res.body.message).toBe('Insufficient permissions');
    });
  });

  describe('POST /users', () => {
    it('should allow admin to create a new user', async () => {
      const newUser = {
        firstName: 'Test',
        lastName: 'User',
        email: 'test@example.com',
        passwordHash: 'StrongPass123!',
        role: 'analyst'
      };

      const res = await request(app)
        .post('/users')
        .set('Authorization', `Bearer ${adminToken}`)
        .send(newUser)
        .expect(201);

      expect(res.body.success).toBe(true);
      expect(res.body.data.email).toBe(newUser.email);

      // Clean up
      await User.destroy({ where: { email: newUser.email } });
    });

    it('should not allow regular user to create a new user', async () => {
      const newUser = {
        firstName: 'Test',
        lastName: 'User',
        email: 'test2@example.com',
        passwordHash: 'StrongPass123!',
        role: 'analyst'
      };

      const res = await request(app)
        .post('/users')
        .set('Authorization', `Bearer ${userToken}`)
        .send(newUser)
        .expect(403);

      expect(res.body.success).toBe(false);
      expect(res.body.message).toBe('Insufficient permissions');
    });
  });

  describe('PUT /users/:id', () => {
    it('should allow user to update their own profile', async () => {
      const updates = {
        firstName: 'Updated',
        lastName: 'Name'
      };

      const res = await request(app)
        .put(`/users/${regularUser.id}`)
        .set('Authorization', `Bearer ${userToken}`)
        .send(updates)
        .expect(200);

      expect(res.body.success).toBe(true);
      expect(res.body.data.firstName).toBe(updates.firstName);
    });

    it('should allow admin to update any user profile', async () => {
      const updates = {
        firstName: 'Admin',
        lastName: 'Updated'
      };

      const res = await request(app)
        .put(`/users/${regularUser.id}`)
        .set('Authorization', `Bearer ${adminToken}`)
        .send(updates)
        .expect(200);

      expect(res.body.success).toBe(true);
      expect(res.body.data.firstName).toBe(updates.firstName);
    });
  });

  describe('DELETE /users/:id', () => {
    it('should allow admin to delete a user', async () => {
      // Create a test user to delete
      const testUser = await User.create({
        firstName: 'Delete',
        lastName: 'Me',
        email: 'delete@example.com',
        passwordHash: 'hashed_password_here',
        role: 'analyst'
      });

      const res = await request(app)
        .delete(`/users/${testUser.id}`)
        .set('Authorization', `Bearer ${adminToken}`)
        .expect(200);

      expect(res.body.success).toBe(true);
      expect(res.body.message).toBe('User deleted successfully');
    });

    it('should not allow regular user to delete a user', async () => {
      const res = await request(app)
        .delete(`/users/${adminUser.id}`)
        .set('Authorization', `Bearer ${userToken}`)
        .expect(403);

      expect(res.body.success).toBe(false);
      expect(res.body.message).toBe('Insufficient permissions');
    });
  });

  describe('User Preferences', () => {
    it('should allow user to get their preferences', async () => {
      const res = await request(app)
        .get(`/users/${regularUser.id}/preferences`)
        .set('Authorization', `Bearer ${userToken}`)
        .expect(200);

      expect(res.body.success).toBe(true);
      expect(res.body.data).toBeDefined();
    });

    it('should allow user to update their preferences', async () => {
      const preferences = {
        theme: 'dark',
        notifications: false,
        language: 'es'
      };

      const res = await request(app)
        .put(`/users/${regularUser.id}/preferences`)
        .set('Authorization', `Bearer ${userToken}`)
        .send(preferences)
        .expect(200);

      expect(res.body.success).toBe(true);
      expect(res.body.data.theme).toBe(preferences.theme);
    });
  });

  describe('User Activity Logs', () => {
    it('should allow user to get their activity logs', async () => {
      const res = await request(app)
        .get(`/users/${regularUser.id}/activity`)
        .set('Authorization', `Bearer ${userToken}`)
        .expect(200);

      expect(res.body.success).toBe(true);
      expect(Array.isArray(res.body.data)).toBe(true);
    });
  });

  describe('User Role Management', () => {
    it('should allow admin to update user role', async () => {
      const res = await request(app)
        .put(`/users/${regularUser.id}/roles`)
        .set('Authorization', `Bearer ${adminToken}`)
        .send({ role: 'compliance_officer' })
        .expect(200);

      expect(res.body.success).toBe(true);
      expect(res.body.data.role).toBe('compliance_officer');
    });

    it('should not allow regular user to update user role', async () => {
      const res = await request(app)
        .put(`/users/${adminUser.id}/roles`)
        .set('Authorization', `Bearer ${userToken}`)
        .send({ role: 'admin' })
        .expect(403);

      expect(res.body.success).toBe(false);
      expect(res.body.message).toBe('Insufficient permissions');
    });
  });

  describe('User Authentication Logs', () => {
    it('should allow user to get their auth logs', async () => {
      const res = await request(app)
        .get(`/users/${regularUser.id}/auth-logs`)
        .set('Authorization', `Bearer ${userToken}`)
        .expect(200);

      expect(res.body.success).toBe(true);
      expect(Array.isArray(res.body.data)).toBe(true);
    });
  });

  describe('User Data Export', () => {
    it('should allow user to export their data', async () => {
      const res = await request(app)
        .get(`/users/${regularUser.id}/export`)
        .set('Authorization', `Bearer ${userToken}`)
        .expect(200);

      expect(res.body.success).toBe(true);
      expect(res.body.data.user).toBeDefined();
      expect(res.body.data.preferences).toBeDefined();
    });
  });

  describe('User Data Validation', () => {
    it('should validate user data', async () => {
      const userData = {
        email: 'valid@example.com',
        passwordHash: 'StrongPass123!',
        role: 'analyst'
      };

      const res = await request(app)
        .post('/users/validate')
        .send(userData)
        .expect(200);

      expect(res.body.success).toBe(true);
      expect(res.body.data.isValid).toBe(true);
    });

    it('should reject invalid user data', async () => {
      const userData = {
        email: 'invalid-email',
        passwordHash: 'weak',
        role: 'invalid-role'
      };

      const res = await request(app)
        .post('/users/validate')
        .send(userData)
        .expect(200);

      expect(res.body.success).toBe(true);
      expect(res.body.data.isValid).toBe(false);
      expect(res.body.data.errors.length).toBeGreaterThan(0);
    });
  });
});