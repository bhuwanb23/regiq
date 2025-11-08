const request = require('supertest');
const app = require('../src/server');
const { User } = require('../src/models');
const passwordUtils = require('../src/utils/password.utils');

describe('Authentication', () => {
  let testUser;

  beforeAll(async () => {
    // Create a test user
    const hashedPassword = await passwordUtils.hashPassword('TestPass123!');
    testUser = await User.create({
      firstName: 'Test',
      lastName: 'User',
      email: 'test@example.com',
      passwordHash: hashedPassword,
      role: 'analyst'
    });
  });

  afterAll(async () => {
    // Clean up test user
    if (testUser) {
      await User.destroy({ where: { id: testUser.id } });
    }
  });

  describe('POST /auth/register', () => {
    it('should register a new user', async () => {
      const userData = {
        firstName: 'John',
        lastName: 'Doe',
        email: 'john.doe@example.com',
        passwordHash: 'StrongPass123!',
        role: 'analyst'
      };

      const res = await request(app)
        .post('/auth/register')
        .send(userData)
        .expect(201);

      expect(res.body.success).toBe(true);
      expect(res.body.data.user.email).toBe(userData.email);
      expect(res.body.data.user.firstName).toBe(userData.firstName);
      expect(res.body.data.user.lastName).toBe(userData.lastName);
      expect(res.body.data.accessToken).toBeDefined();
      expect(res.body.data.refreshToken).toBeDefined();

      // Clean up created user
      await User.destroy({ where: { email: userData.email } });
    });

    it('should not register a user with existing email', async () => {
      const userData = {
        firstName: 'Test',
        lastName: 'User',
        email: 'test@example.com', // Existing email
        passwordHash: 'StrongPass123!',
        role: 'analyst'
      };

      const res = await request(app)
        .post('/auth/register')
        .send(userData)
        .expect(400);

      expect(res.body.success).toBe(false);
      expect(res.body.message).toBe('User with this email already exists');
    });

    it('should not register a user with weak password', async () => {
      const userData = {
        firstName: 'Jane',
        lastName: 'Doe',
        email: 'jane.doe@example.com',
        passwordHash: 'weak', // Weak password
        role: 'analyst'
      };

      const res = await request(app)
        .post('/auth/register')
        .send(userData)
        .expect(400);

      expect(res.body.success).toBe(false);
      expect(res.body.message).toBe('Password does not meet security requirements');
    });
  });

  describe('POST /auth/login', () => {
    it('should login a user with valid credentials', async () => {
      const credentials = {
        email: 'test@example.com',
        password: 'TestPass123!'
      };

      const res = await request(app)
        .post('/auth/login')
        .send(credentials)
        .expect(200);

      expect(res.body.success).toBe(true);
      expect(res.body.data.user.email).toBe(credentials.email);
      expect(res.body.data.accessToken).toBeDefined();
      expect(res.body.data.refreshToken).toBeDefined();
    });

    it('should not login with invalid email', async () => {
      const credentials = {
        email: 'invalid@example.com',
        password: 'TestPass123!'
      };

      const res = await request(app)
        .post('/auth/login')
        .send(credentials)
        .expect(401);

      expect(res.body.success).toBe(false);
      expect(res.body.message).toBe('Invalid credentials');
    });

    it('should not login with invalid password', async () => {
      const credentials = {
        email: 'test@example.com',
        password: 'WrongPassword123!'
      };

      const res = await request(app)
        .post('/auth/login')
        .send(credentials)
        .expect(401);

      expect(res.body.success).toBe(false);
      expect(res.body.message).toBe('Invalid credentials');
    });
  });

  describe('POST /auth/refresh', () => {
    it('should refresh access token with valid refresh token', async () => {
      // First login to get tokens
      const credentials = {
        email: 'test@example.com',
        password: 'TestPass123!'
      };

      const loginRes = await request(app)
        .post('/auth/login')
        .send(credentials)
        .expect(200);

      // Extract refresh token from cookie
      const cookies = loginRes.headers['set-cookie'];
      const refreshTokenCookie = cookies.find(cookie => cookie.includes('refreshToken'));

      // Refresh token
      const res = await request(app)
        .post('/auth/refresh')
        .set('Cookie', refreshTokenCookie)
        .expect(200);

      expect(res.body.success).toBe(true);
      expect(res.body.data.accessToken).toBeDefined();
    });
  });

  describe('Authentication Middleware', () => {
    it('should protect routes with authentication', async () => {
      const res = await request(app)
        .get('/auth/profile')
        .expect(401);

      expect(res.body.success).toBe(false);
      expect(res.body.message).toBe('Access token is required');
    });

    it('should allow access with valid token', async () => {
      // First login to get token
      const credentials = {
        email: 'test@example.com',
        password: 'TestPass123!'
      };

      const loginRes = await request(app)
        .post('/auth/login')
        .send(credentials)
        .expect(200);

      const accessToken = loginRes.body.data.accessToken;

      // Access protected route
      const res = await request(app)
        .get('/auth/profile')
        .set('Authorization', `Bearer ${accessToken}`)
        .expect(200);

      expect(res.body.success).toBe(true);
      expect(res.body.data.email).toBe(credentials.email);
    });
  });
});