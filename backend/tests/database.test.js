const sequelize = require('../src/config/database');
const { User } = require('../src/models');
const dbHelpers = require('../src/utils/dbHelpers');

describe('Database Integration', () => {
  beforeAll(async () => {
    // Test database connection
    const isConnected = await dbHelpers.testConnection();
    if (!isConnected) {
      throw new Error('Database connection failed');
    }
  });

  afterAll(async () => {
    // Close database connection
    await dbHelpers.closeConnection();
  });

  describe('User Model', () => {
    it('should create a new user', async () => {
      const userData = {
        firstName: 'John',
        lastName: 'Doe',
        email: 'john.doe@example.com',
        passwordHash: 'hashed_password_here'
      };

      const user = await User.create(userData);
      
      expect(user.firstName).toBe(userData.firstName);
      expect(user.lastName).toBe(userData.lastName);
      expect(user.email).toBe(userData.email);
      expect(user.id).toBeDefined();
      expect(user.createdAt).toBeDefined();
      expect(user.updatedAt).toBeDefined();

      // Clean up
      await user.destroy();
    });

    it('should find a user by email', async () => {
      const userData = {
        firstName: 'Jane',
        lastName: 'Smith',
        email: 'jane.smith@example.com',
        passwordHash: 'hashed_password_here'
      };

      // Create user
      const createdUser = await User.create(userData);
      
      // Find user by email
      const foundUser = await User.findOne({
        where: { email: userData.email }
      });

      expect(foundUser).toBeDefined();
      expect(foundUser.email).toBe(userData.email);

      // Clean up
      await createdUser.destroy();
    });

    it('should update a user', async () => {
      const userData = {
        firstName: 'Bob',
        lastName: 'Johnson',
        email: 'bob.johnson@example.com',
        passwordHash: 'hashed_password_here'
      };

      // Create user
      const user = await User.create(userData);
      
      // Update user
      const updatedData = { firstName: 'Robert' };
      await user.update(updatedData);
      
      expect(user.firstName).toBe(updatedData.firstName);

      // Clean up
      await user.destroy();
    });

    it('should delete a user', async () => {
      const userData = {
        firstName: 'Alice',
        lastName: 'Brown',
        email: 'alice.brown@example.com',
        passwordHash: 'hashed_password_here'
      };

      // Create user
      const user = await User.create(userData);
      const userId = user.id;
      
      // Delete user
      await user.destroy();
      
      // Try to find deleted user
      const deletedUser = await User.findByPk(userId);
      expect(deletedUser).toBeNull();
    });
  });
});