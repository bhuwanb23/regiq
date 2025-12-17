const apiClient = require('../apiClient');

// Mock axios
jest.mock('axios', () => {
  return {
    create: jest.fn(() => ({
      get: jest.fn(),
      post: jest.fn(),
      put: jest.fn(),
      delete: jest.fn(),
      interceptors: {
        request: { use: jest.fn(), eject: jest.fn() },
        response: { use: jest.fn(), eject: jest.fn() },
      },
    })),
    get: jest.fn(),
    post: jest.fn(),
    put: jest.fn(),
    delete: jest.fn(),
  };
});

describe('apiClient', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('should have getUserProfile function', () => {
    expect(typeof apiClient.default.getUserProfile).toBe('function');
  });

  it('should have updateUserProfile function', () => {
    expect(typeof apiClient.default.updateUserProfile).toBe('function');
  });

  it('should have getUserPreferences function', () => {
    expect(typeof apiClient.default.getUserPreferences).toBe('function');
  });

  it('should have updateUserPreferences function', () => {
    expect(typeof apiClient.default.updateUserPreferences).toBe('function');
  });

  it('should have getNotificationPreferences function', () => {
    expect(typeof apiClient.default.getNotificationPreferences).toBe('function');
  });

  it('should have updateNotificationPreferences function', () => {
    expect(typeof apiClient.default.updateNotificationPreferences).toBe('function');
  });
});