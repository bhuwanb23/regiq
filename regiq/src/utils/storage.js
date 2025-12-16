/**
 * Storage utility for handling JWT tokens and other persisted data
 * Uses React Native's AsyncStorage
 */
import AsyncStorage from '@react-native-async-storage/async-storage';

// Store data in AsyncStorage
export const storeData = async (key, value) => {
  try {
    if (typeof value === 'object') {
      value = JSON.stringify(value);
    }
    await AsyncStorage.setItem(key, value);
  } catch (error) {
    console.error('Error storing data:', error);
  }
};

// Retrieve data from AsyncStorage
export const getData = async (key) => {
  try {
    const value = await AsyncStorage.getItem(key);
    if (value !== null) {
      try {
        return JSON.parse(value);
      } catch (e) {
        return value;
      }
    }
    return null;
  } catch (error) {
    console.error('Error retrieving data:', error);
    return null;
  }
};

// Remove data from AsyncStorage
export const removeData = async (key) => {
  try {
    await AsyncStorage.removeItem(key);
  } catch (error) {
    console.error('Error removing data:', error);
  }
};

// Store authentication token
export const storeToken = async (token) => {
  await storeData('authToken', token);
};

// Retrieve authentication token
export const getToken = async () => {
  return await getData('authToken');
};

// Remove authentication token
export const removeToken = async () => {
  await removeData('authToken');
};

// Store refresh token
export const storeRefreshToken = async (refreshToken) => {
  await storeData('refreshToken', refreshToken);
};

// Retrieve refresh token
export const getRefreshToken = async () => {
  return await getData('refreshToken');
};

// Remove refresh token
export const removeRefreshToken = async () => {
  await removeData('refreshToken');
};

// Clear all authentication data
export const clearAuthData = async () => {
  await removeToken();
  await removeRefreshToken();
};