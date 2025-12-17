const notificationService = require('../../src/services/notification.service');
const { Notification, NotificationTemplate, NotificationPreference, NotificationAnalytics } = require('../../src/models');

// Mock the models
jest.mock('../../src/models', () => ({
  Notification: {
    findAll: jest.fn(),
    findByPk: jest.fn(),
    create: jest.fn(),
    update: jest.fn(),
    destroy: jest.fn(),
    findAndCountAll: jest.fn()
  },
  NotificationTemplate: {
    findAll: jest.fn(),
    findByPk: jest.fn(),
    create: jest.fn(),
    update: jest.fn(),
    destroy: jest.fn(),
    findAndCountAll: jest.fn()
  },
  NotificationPreference: {
    findAll: jest.fn(),
    create: jest.fn(),
    update: jest.fn(),
    destroy: jest.fn(),
    bulkCreate: jest.fn()
  },
  NotificationAnalytics: {
    create: jest.fn(),
    findAll: jest.fn(),
    findAndCountAll: jest.fn()
  },
  sequelize: {
    Op: {}
  }
}));

describe('Notification Service', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('getNotifications', () => {
    it('should return notifications with pagination', async () => {
      const mockNotifications = [
        { id: 1, title: 'Test Notification 1', type: 'info' },
        { id: 2, title: 'Test Notification 2', type: 'warning' }
      ];
      
      const mockResult = {
        data: mockNotifications,
        page: 1,
        limit: 10,
        totalCount: 2
      };
      
      Notification.findAndCountAll.mockResolvedValue({
        count: 2,
        rows: mockNotifications
      });
      
      const result = await notificationService.getNotifications({}, { page: 1, limit: 10 });
      
      expect(Notification.findAndCountAll).toHaveBeenCalled();
      expect(result).toEqual(mockResult);
    });
  });

  describe('createNotification', () => {
    it('should create a new notification', async () => {
      const notificationData = {
        title: 'Test Notification',
        message: 'This is a test notification',
        type: 'info',
        userId: 1
      };
      
      const mockNotification = {
        id: 1,
        ...notificationData,
        toJSON: jest.fn().mockReturnValue({
          id: 1,
          title: 'Test Notification',
          message: 'This is a test notification',
          type: 'info',
          userId: 1
        })
      };
      
      Notification.create.mockResolvedValue(mockNotification);
      
      const result = await notificationService.createNotification(notificationData);
      
      expect(Notification.create).toHaveBeenCalledWith(notificationData);
      expect(result).toEqual(mockNotification);
    });
  });

  describe('getUserPreferences', () => {
    it('should return user preferences', async () => {
      const mockPreferences = [
        { userId: 1, type: 'email', enabled: true },
        { userId: 1, type: 'push', enabled: true }
      ];
      
      NotificationPreference.findAll.mockResolvedValue(mockPreferences);
      
      const result = await notificationService.getUserPreferences(1);
      
      expect(NotificationPreference.findAll).toHaveBeenCalledWith({
        where: { userId: 1 }
      });
      expect(result).toEqual(mockPreferences);
    });
  });

  describe('updateUserPreferences', () => {
    it('should update existing user preferences', async () => {
      const preferencesData = [
        { type: 'email', enabled: false },
        { type: 'push', enabled: true }
      ];
      
      const mockUpdatedPreferences = [
        { userId: 1, type: 'email', enabled: false },
        { userId: 1, type: 'push', enabled: true }
      ];
      
      NotificationPreference.destroy.mockResolvedValue();
      NotificationPreference.bulkCreate.mockResolvedValue(mockUpdatedPreferences);
      
      const result = await notificationService.updateUserPreferences(1, preferencesData);
      
      expect(NotificationPreference.destroy).toHaveBeenCalledWith({
        where: { userId: 1 }
      });
      expect(NotificationPreference.bulkCreate).toHaveBeenCalledWith([
        { type: 'email', enabled: false, userId: 1 },
        { type: 'push', enabled: true, userId: 1 }
      ]);
      expect(result).toEqual(mockUpdatedPreferences);
    });
  });
});