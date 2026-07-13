const redis = require('redis');
const winston = require('winston');

class RedisClient {
  constructor() {
    // Get Redis configuration from environment variables
    this.redisUrl = process.env.REDIS_URL || 'redis://localhost:6379';
    
    // Create Redis client
    this.client = redis.createClient({
      url: this.redisUrl
    });

    // Handle connection events
    this.client.on('connect', () => {
      winston.info('Redis client connected');
    });

    this.client.on('ready', () => {
      winston.info('Redis client ready');
    });

    this.client.on('error', (err) => {
      winston.error('Redis client error:', err);
    });

    this.client.on('reconnecting', () => {
      winston.info('Redis client reconnecting');
    });

    this.client.on('end', () => {
      winston.info('Redis client disconnected');
    });
  }

  async connect() {
    try {
      await this.client.connect();
      winston.info('Redis connection established');
    } catch (error) {
      winston.error('Failed to connect to Redis:', error);
      throw error;
    }
  }

  async disconnect() {
    try {
      await this.client.quit();
      winston.info('Redis connection closed');
    } catch (error) {
      winston.error('Error closing Redis connection:', error);
    }
  }

  // Get value by key
  async get(key) {
    try {
      const value = await this.client.get(key);
      return value;
    } catch (error) {
      winston.error(`Error getting key ${key} from Redis:`, error);
      throw error;
    }
  }

  // Set value by key with optional expiration
  async set(key, value, expireSeconds = null) {
    try {
      if (expireSeconds) {
        await this.client.setEx(key, expireSeconds, value);
      } else {
        await this.client.set(key, value);
      }
      return true;
    } catch (error) {
      winston.error(`Error setting key ${key} in Redis:`, error);
      throw error;
    }
  }

  // Delete key
  async del(key) {
    try {
      await this.client.del(key);
      return true;
    } catch (error) {
      winston.error(`Error deleting key ${key} from Redis:`, error);
      throw error;
    }
  }

  // Check if key exists
  async exists(key) {
    try {
      const result = await this.client.exists(key);
      return result === 1;
    } catch (error) {
      winston.error(`Error checking existence of key ${key} in Redis:`, error);
      throw error;
    }
  }

  // Flush all keys
  async flushAll() {
    try {
      await this.client.flushAll();
      winston.info('All Redis keys flushed');
      return true;
    } catch (error) {
      winston.error('Error flushing Redis keys:', error);
      throw error;
    }
  }
}

// Export singleton instance
module.exports = new RedisClient();