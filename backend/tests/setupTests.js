// Setup file for Jest tests
const mongoose = require('mongoose');

// Mock environment variables
process.env.NODE_ENV = 'test';
process.env.JWT_SECRET = 'test-secret-key';
process.env.DATABASE_URL = 'sqlite::memory:'; // Use in-memory SQLite for tests

// Mock console.error to reduce noise in test output
console.error = jest.fn();

// Close MongoDB connection after all tests
afterAll(async () => {
  await mongoose.connection.close();
});

// Clear all mocks after each test
afterEach(() => {
  jest.clearAllMocks();
});