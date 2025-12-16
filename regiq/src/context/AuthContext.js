/**
 * Authentication Context for managing user authentication state globally
 */
import React, { createContext, useContext, useEffect, useState } from 'react';
import { login, logout, getCurrentUser, isAuthenticated } from '../services/authService';
import { getToken } from '../utils/storage';

// Create the AuthContext
const AuthContext = createContext();

// AuthProvider component to wrap the application
export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // Check if user is authenticated on app start
  useEffect(() => {
    checkAuthStatus();
  }, []);

  // Check authentication status
  const checkAuthStatus = async () => {
    try {
      const token = await getToken();
      if (token) {
        const currentUser = await getCurrentUser();
        setUser(currentUser);
        setIsAuthenticated(true);
      }
    } catch (error) {
      console.warn('Not authenticated:', error.message);
      setUser(null);
      setIsAuthenticated(false);
    } finally {
      setIsLoading(false);
    }
  };

  // Handle user login
  const handleLogin = async (email, password) => {
    try {
      setIsLoading(true);
      const userData = await login(email, password);
      setUser(userData.user || userData);
      setIsAuthenticated(true);
      return userData;
    } catch (error) {
      setUser(null);
      setIsAuthenticated(false);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  // Handle user logout
  const handleLogout = async () => {
    try {
      await logout();
      setUser(null);
      setIsAuthenticated(false);
    } catch (error) {
      console.error('Logout error:', error);
      // Even if there's an error, clear local state
      setUser(null);
      setIsAuthenticated(false);
    }
  };

  // Refresh user data
  const refreshUser = async () => {
    try {
      const currentUser = await getCurrentUser();
      setUser(currentUser);
      setIsAuthenticated(true);
    } catch (error) {
      console.error('Failed to refresh user data:', error);
      setUser(null);
      setIsAuthenticated(false);
    }
  };

  // Context value
  const value = {
    user,
    isLoading,
    isAuthenticated,
    login: handleLogin,
    logout: handleLogout,
    refreshUser,
    checkAuthStatus
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

// Custom hook to use the AuthContext
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export default AuthContext;