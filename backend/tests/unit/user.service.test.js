const userService = require('../../src/services/user.service');
const { User } = require('../../src/models');

// Mock the User model
jest.mock('../../src/models', () => ({
  User: {
    findByPk: jest.fn(),
    create: jest.fn(),
    findAll: jest.fn(),
    update: jest.fn()
  }
}));

describe('User Service', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('getAllUsers', () => {
    it('should return all users', async () => {
      const mockUsers = [
        { id: 1, firstName: 'John', lastName: 'Doe', email: 'john@example.com' },
        { id: 2, firstName: 'Jane', lastName: 'Smith', email: 'jane@example.com' }
      ];
      
      User.findAll.mockResolvedValue(mockUsers);
      
      const result = await userService.getAllUsers();
      
      expect(User.findAll).toHaveBeenCalledWith({
        attributes: { exclude: ['passwordHash'] },
        where: { isDeleted: false }
      });
      expect(result).toEqual(mockUsers);
    });
  });

  describe('getUserById', () => {
    it('should return a user by ID', async () => {
      // The actual service returns the user object directly without calling toJSON()
      const mockUser = { 
        id: 1, 
        firstName: 'John', 
        lastName: 'Doe', 
        email: 'john@example.com'
      };
      
      User.findByPk.mockResolvedValue(mockUser);
      
      const result = await userService.getUserById(1);
      
      expect(User.findByPk).toHaveBeenCalledWith(1, {
        attributes: { exclude: ['passwordHash'] }
      });
      expect(result).toEqual(mockUser);
    });

    it('should throw an error if user not found', async () => {
      User.findByPk.mockResolvedValue(null);
      
      await expect(userService.getUserById(999)).rejects.toThrow('User not found');
    });
  });

  describe('createUser', () => {
    it('should create a new user', async () => {
      const userData = {
        firstName: 'John',
        lastName: 'Doe',
        email: 'john@example.com',
        passwordHash: 'hashedPassword'
      };
      
      const mockUser = {
        ...userData,
        id: 1,
        toJSON: jest.fn().mockReturnValue({
          id: 1,
          firstName: 'John',
          lastName: 'Doe',
          email: 'john@example.com'
        })
      };
      
      User.create.mockResolvedValue(mockUser);
      
      const result = await userService.createUser(userData);
      
      expect(User.create).toHaveBeenCalledWith(userData);
      expect(result).toEqual({
        id: 1,
        firstName: 'John',
        lastName: 'Doe',
        email: 'john@example.com'
      });
    });
  });

  describe('updateUser', () => {
    it('should update an existing user', async () => {
      const userData = { firstName: 'Johnny' };
      const mockUser = {
        id: 1,
        firstName: 'John',
        lastName: 'Doe',
        email: 'john@example.com',
        update: jest.fn().mockResolvedValue(),
        toJSON: jest.fn().mockReturnValue({
          id: 1,
          firstName: 'Johnny',
          lastName: 'Doe',
          email: 'john@example.com'
        })
      };
      
      User.findByPk.mockResolvedValue(mockUser);
      
      const result = await userService.updateUser(1, userData);
      
      expect(User.findByPk).toHaveBeenCalledWith(1);
      expect(mockUser.update).toHaveBeenCalledWith(userData);
      expect(result).toEqual({
        id: 1,
        firstName: 'Johnny',
        lastName: 'Doe',
        email: 'john@example.com'
      });
    });

    it('should throw an error if user not found', async () => {
      User.findByPk.mockResolvedValue(null);
      
      await expect(userService.updateUser(999, {})).rejects.toThrow('User not found');
    });
  });
});
