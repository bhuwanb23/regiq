import { useState, useEffect } from 'react';
import { 
  getUserProfile, 
  updateUserProfile,
  getUserPreferences,
  updateUserPreferences
} from '../services/apiClient';

/**
 * Custom hook for managing user profile data
 * @returns {Object} User profile state and management functions
 */
const useUserProfile = () => {
  const [profile, setProfile] = useState(null);
  const [preferences, setPreferences] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  /**
   * Fetch user profile data
   */
  const fetchProfile = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await getUserProfile();
      setProfile(response.data);
    } catch (err) {
      setError(err.message || 'Failed to fetch profile');
      console.error('Error fetching profile:', err);
    } finally {
      setLoading(false);
    }
  };

  /**
   * Update user profile data
   * @param {Object} profileData - Profile data to update
   */
  const updateProfile = async (profileData) => {
    try {
      setLoading(true);
      setError(null);
      const response = await updateUserProfile(profileData);
      setProfile(response.data);
      return response;
    } catch (err) {
      setError(err.message || 'Failed to update profile');
      console.error('Error updating profile:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  /**
   * Fetch user preferences
   */
  const fetchPreferences = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await getUserPreferences();
      setPreferences(response.data);
    } catch (err) {
      setError(err.message || 'Failed to fetch preferences');
      console.error('Error fetching preferences:', err);
    } finally {
      setLoading(false);
    }
  };

  /**
   * Update user preferences
   * @param {Object} preferencesData - Preferences to update
   */
  const updatePreferences = async (preferencesData) => {
    try {
      setLoading(true);
      setError(null);
      const response = await updateUserPreferences(preferencesData);
      setPreferences(response.data);
      return response;
    } catch (err) {
      setError(err.message || 'Failed to update preferences');
      console.error('Error updating preferences:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return {
    // State
    profile,
    preferences,
    loading,
    error,
    
    // Functions
    fetchProfile,
    updateProfile,
    fetchPreferences,
    updatePreferences
  };
};

export default useUserProfile;