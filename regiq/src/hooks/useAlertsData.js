import { useState, useEffect, useCallback } from 'react';
import {
  getNotifications,
  markNotificationAsRead,
  snoozeNotification,
} from '../services/apiClient';

/**
 * useAlertsData — fetches the authenticated user's notifications from the
 * backend (/api/notifications) and exposes mark-as-read / snooze actions.
 *
 * Falls back to an empty list (not mock data) on error so the UI can
 * surface an authentic "no alerts / failed to load" state instead of
 * pretending stale data is real.
 */
const useAlertsData = () => {
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState(null);

  const fetchAlerts = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await getNotifications();
      // Backend response shape: { success, data: [...] } (via apiClient interceptor).
      const list = Array.isArray(response?.data)
        ? response.data
        : Array.isArray(response?.data?.notifications)
          ? response.data.notifications
          : Array.isArray(response)
            ? response
            : [];
      setAlerts(list);
      return list;
    } catch (err) {
      setError(err?.message || 'Failed to load alerts');
      setAlerts([]);
      return [];
    } finally {
      setLoading(false);
    }
  }, []);

  const refreshAlerts = useCallback(async () => {
    setRefreshing(true);
    try {
      await fetchAlerts();
    } finally {
      setRefreshing(false);
    }
  }, [fetchAlerts]);

  const markAsRead = useCallback(async (id) => {
    // Optimistic update.
    setAlerts((prev) =>
      prev.map((a) => (a.id === id ? { ...a, isRead: true, status: 'read' } : a))
    );
    try {
      await markNotificationAsRead(id);
    } catch (err) {
      // Revert on failure.
      setAlerts((prev) =>
        prev.map((a) => (a.id === id ? { ...a, isRead: false, status: 'unread' } : a))
      );
      setError(err?.message || 'Failed to mark alert as read');
    }
  }, []);

  const snooze = useCallback(async (id) => {
    setAlerts((prev) => prev.filter((a) => a.id !== id));
    try {
      await snoozeNotification(id);
    } catch (err) {
      setError(err?.message || 'Failed to snooze alert');
      // Reload to bring back the snoozed alert if the server rejected it.
      fetchAlerts();
    }
  }, [fetchAlerts]);

  useEffect(() => {
    fetchAlerts();
  }, [fetchAlerts]);

  return {
    alerts,
    loading,
    refreshing,
    error,
    refreshAlerts,
    markAsRead,
    snooze,
  };
};

export default useAlertsData;
