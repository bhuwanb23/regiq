import { renderHook, act } from '@testing-library/react-hooks';
import useUserProfile from '../../src/hooks/useUserProfile';

// Mock the API client
jest.mock('../../src/services/apiClient', () => ({
  getUserProfile: jest.fn(),
  updateUserProfile: jest.fn(),
  getUserPreferences: jest.fn(),
  updateUserPreferences: jest.fn()
}));

const { getUserProfile, updateUserProfile, getUserPreferences, updateUserPreferences } = require('../../src/services/apiClient');

describe('useUserProfile', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('should fetch user profile', async () => {
    const mockProfile = {
      id: 1,
      firstName: 'John',
      lastName: 'Doe',
      email: 'john.doe@example.com'
    };

    getUserProfile.mockResolvedValue({ data: mockProfile });

    const { result, waitForNextUpdate } = renderHook(() => useUserProfile());

    expect(result.current.loading).toBe(false);
    expect(result.current.profile).toBeNull();

    act(() => {
      result.current.fetchProfile();
    });

    expect(result.current.loading).toBe(true);

    await waitForNextUpdate();

    expect(result.current.loading).toBe(false);
    expect(result.current.profile).toEqual(mockProfile);
    expect(getUserProfile).toHaveBeenCalled();
  });

  it('should update user profile', async () => {
    const mockProfile = {
      id: 1,
      firstName: 'Johnny',
      lastName: 'Doe',
      email: 'john.doe@example.com'
    };

    updateUserProfile.mockResolvedValue({ data: mockProfile });

    const { result, waitForNextUpdate } = renderHook(() => useUserProfile());

    await act(async () => {
      await result.current.updateProfile({ firstName: 'Johnny' });
    });

    expect(updateUserProfile).toHaveBeenCalledWith({ firstName: 'Johnny' });
    expect(result.current.profile).toEqual(mockProfile);
  });

  it('should handle profile fetch error', async () => {
    const errorMessage = 'Failed to fetch profile';
    getUserProfile.mockRejectedValue(new Error(errorMessage));

    const { result, waitForNextUpdate } = renderHook(() => useUserProfile());

    act(() => {
      result.current.fetchProfile();
    });

    try {
      await waitForNextUpdate();
    } catch (error) {
      // Expected error
    }

    expect(result.current.error).toBe(errorMessage);
    expect(result.current.loading).toBe(false);
  });

  it('should fetch user preferences', async () => {
    const mockPreferences = {
      theme: 'dark',
      notifications: true
    };

    getUserPreferences.mockResolvedValue({ data: mockPreferences });

    const { result, waitForNextUpdate } = renderHook(() => useUserProfile());

    act(() => {
      result.current.fetchPreferences();
    });

    await waitForNextUpdate();

    expect(result.current.preferences).toEqual(mockPreferences);
    expect(getUserPreferences).toHaveBeenCalled();
  });

  it('should update user preferences', async () => {
    const mockPreferences = {
      theme: 'light',
      notifications: false
    };

    updateUserPreferences.mockResolvedValue({ data: mockPreferences });

    const { result, waitForNextUpdate } = renderHook(() => useUserProfile());

    await act(async () => {
      await result.current.updatePreferences({ theme: 'light' });
    });

    expect(updateUserPreferences).toHaveBeenCalledWith({ theme: 'light' });
    expect(result.current.preferences).toEqual(mockPreferences);
  });
});