import { useState, useEffect } from 'react';
import { 
  getNotificationPreferences, 
  updateNotificationPreferences 
} from '../services/apiClient';

/**
 * Custom hook for managing notification preferences
 * @returns {Object} Notification preferences state and management functions
 */
const useNotificationPreferences = () => {
  const [preferences, setPreferences] = useState({
    regulatoryUpdates: true,
    biasAlerts: true,
    riskWarnings: true,
    reportGeneration: true,
    systemMaintenance: false,
    email: true,
    push: true,
    sms: false
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  /**
   * Fetch notification preferences
   */
  const fetchPreferences = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await getNotificationPreferences();
      setPreferences(response.data);
    } catch (err) {
      setError(err.message || 'Failed to fetch notification preferences');
      console.error('Error fetching notification preferences:', err);
    } finally {
      setLoading(false);
    }
  };

  /**
   * Update notification preferences
   * @param {Object} prefs - Preferences to update
   */
  const updatePreferences = async (prefs) => {
    try {
      setLoading(true);
      setError(null);
      const response = await updateNotificationPreferences(prefs);
      setPreferences(response.data);
      return response;
    } catch (err) {
      setError(err.message || 'Failed to update notification preferences');
      console.error('Error updating notification preferences:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  /**
   * Toggle a specific preference
   * @param {string} key - Preference key to toggle
   */
  const togglePreference = (key) => {
    setPreferences(prev => ({
      ...prev,
      [key]: !prev[key]
    }));
  };

  return {
    // State
    preferences,
    loading,
    error,
    
    // Functions
    fetchPreferences,
    updatePreferences,
    togglePreference
  };
};

export default useNotificationPreferences;