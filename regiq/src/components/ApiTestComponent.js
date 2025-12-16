/**
 * Simple test component to verify API client setup
 */
import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, ScrollView, Button } from 'react-native';
import apiClient from '../services/api';
import { storeToken, getToken, removeToken } from '../utils/storage';
import { login } from '../services/authService';

const ApiTestComponent = () => {
  const [testResults, setTestResults] = useState([]);
  const [isTesting, setIsTesting] = useState(false);

  const addResult = (message, success = true) => {
    setTestResults(prev => [...prev, { message, success, id: Date.now() }]);
  };

  const runTests = async () => {
    setIsTesting(true);
    setTestResults([]);
    
    try {
      // Test 1: API Client Creation
      addResult('API Client created successfully');
      addResult(`Base URL: ${apiClient.defaults.baseURL}`);
      addResult(`Timeout: ${apiClient.defaults.timeout}ms`);
      
      // Test 2: Storage Functions
      await storeToken('test-token');
      addResult('Token stored successfully');
      
      const retrievedToken = await getToken();
      if (retrievedToken === 'test-token') {
        addResult('Token retrieved successfully');
      } else {
        addResult('Token retrieval failed', false);
      }
      
      await removeToken();
      const removedToken = await getToken();
      if (removedToken === null) {
        addResult('Token removed successfully');
      } else {
        addResult('Token removal failed', false);
      }
      
      addResult('All tests completed!');
      
    } catch (error) {
      addResult(`Test failed: ${error.message}`, false);
      console.error('Test error:', error);
    } finally {
      setIsTesting(false);
    }
  };

  return (
    <ScrollView style={styles.container}>
      <Text style={styles.title}>API Client Setup Test</Text>
      
      <Button 
        title={isTesting ? "Running Tests..." : "Run API Client Tests"} 
        onPress={runTests} 
        disabled={isTesting}
      />
      
      <View style={styles.resultsContainer}>
        {testResults.map(result => (
          <View 
            key={result.id} 
            style={[
              styles.resultItem, 
              result.success ? styles.success : styles.error
            ]}
          >
            <Text style={styles.resultText}>{result.message}</Text>
          </View>
        ))}
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#f5f5f5',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20,
    textAlign: 'center',
  },
  resultsContainer: {
    marginTop: 20,
  },
  resultItem: {
    padding: 10,
    marginVertical: 5,
    borderRadius: 5,
  },
  success: {
    backgroundColor: '#d4edda',
    borderLeftWidth: 4,
    borderLeftColor: '#28a745',
  },
  error: {
    backgroundColor: '#f8d7da',
    borderLeftWidth: 4,
    borderLeftColor: '#dc3545',
  },
  resultText: {
    fontSize: 16,
  },
});

export default ApiTestComponent;