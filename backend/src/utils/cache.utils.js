const { cache } = require('../config/ai-ml.config');
const winston = require('winston');

/**
 * Cache Utilities for AI/ML Service
 * Handles caching of AI/ML results for improved performance
 */

class CacheManager {
  constructor() {
    this.cache = new Map();
    this.accessTimes = new Map();
    this.ttl = cache.ttl * 1000; // Convert to milliseconds
    this.maxItems = cache.maxItems;
    this.enabled = cache.enabled;
    
    // Initialize logger
    this.logger = winston.createLogger({
      level: 'info',
      format: winston.format.json(),
      transports: [
        new winston.transports.Console(),
      ],
    });
    
    // Start cleanup interval if cache is enabled
    if (this.enabled) {
      this.startCleanupInterval();
    }
  }

  /**
   * Get item from cache
   * @param {string} key - Cache key
   * @returns {any|null} Cached value or null if not found/expired
   */
  get(key) {
    if (!this.enabled) {
      return null;
    }
    
    const item = this.cache.get(key);
    
    if (!item) {
      this.logger.debug(`Cache miss for key: ${key}`);
      return null;
    }
    
    const now = Date.now();
    const itemAge = now - item.timestamp;
    
    // Check if item has expired
    if (itemAge > this.ttl) {
      this.logger.debug(`Cache item expired for key: ${key}`);
      this.cache.delete(key);
      this.accessTimes.delete(key);
      return null;
    }
    
    // Update access time
    this.accessTimes.set(key, now);
    
    this.logger.debug(`Cache hit for key: ${key}`);
    return item.value;
  }

  /**
   * Set item in cache
   * @param {string} key - Cache key
   * @param {any} value - Value to cache
   * @param {number} customTtl - Custom TTL in seconds (optional)
   */
  set(key, value, customTtl = null) {
    if (!this.enabled) {
      return;
    }
    
    const ttl = customTtl ? customTtl * 1000 : this.ttl;
    const timestamp = Date.now();
    
    this.cache.set(key, {
      value,
      timestamp,
      ttl,
    });
    
    this.accessTimes.set(key, timestamp);
    
    this.logger.debug(`Item cached with key: ${key}`);
    
    // Check if we need to evict items
    this.evictIfNeeded();
  }

  /**
   * Delete item from cache
   * @param {string} key - Cache key
   * @returns {boolean} True if item was deleted, false otherwise
   */
  delete(key) {
    if (!this.enabled) {
      return false;
    }
    
    const result = this.cache.delete(key);
    this.accessTimes.delete(key);
    
    if (result) {
      this.logger.debug(`Item deleted from cache with key: ${key}`);
    }
    
    return result;
  }

  /**
   * Clear all items from cache
   */
  clear() {
    this.cache.clear();
    this.accessTimes.clear();
    
    this.logger.info('Cache cleared');
  }

  /**
   * Check if cache has item
   * @param {string} key - Cache key
   * @returns {boolean} True if cache has item, false otherwise
   */
  has(key) {
    if (!this.enabled) {
      return false;
    }
    
    return this.cache.has(key) && this.get(key) !== null;
  }

  /**
   * Get cache statistics
   * @returns {Object} Cache statistics
   */
  getStats() {
    return {
      enabled: this.enabled,
      size: this.cache.size,
      maxItems: this.maxItems,
      ttl: this.ttl,
    };
  }

  /**
   * Evict items if cache is full
   */
  evictIfNeeded() {
    if (this.cache.size <= this.maxItems) {
      return;
    }
    
    // Find least recently used item
    let oldestKey = null;
    let oldestTime = Infinity;
    
    for (const [key, time] of this.accessTimes) {
      if (time < oldestTime) {
        oldestTime = time;
        oldestKey = key;
      }
    }
    
    // Remove oldest item
    if (oldestKey) {
      this.cache.delete(oldestKey);
      this.accessTimes.delete(oldestKey);
      
      this.logger.debug(`Evicted oldest item from cache with key: ${oldestKey}`);
    }
  }

  /**
   * Clean up expired items
   */
  cleanup() {
    if (!this.enabled) {
      return;
    }
    
    const now = Date.now();
    let cleanedCount = 0;
    
    for (const [key, item] of this.cache) {
      const itemAge = now - item.timestamp;
      
      if (itemAge > item.ttl) {
        this.cache.delete(key);
        this.accessTimes.delete(key);
        cleanedCount++;
      }
    }
    
    if (cleanedCount > 0) {
      this.logger.debug(`Cleaned up ${cleanedCount} expired cache items`);
    }
  }

  /**
   * Start cleanup interval
   */
  startCleanupInterval() {
    // Clean up expired items every 30 seconds
    setInterval(() => {
      this.cleanup();
    }, 30000);
  }

  /**
   * Create cache key from parameters
   * @param {string} prefix - Key prefix
   * @param {Object} params - Parameters to include in key
   * @returns {string} Cache key
   */
  createKey(prefix, params) {
    // Sort params to ensure consistent key generation
    const sortedParams = Object.keys(params)
      .sort()
      .map(key => `${key}=${params[key]}`)
      .join('&');
    
    return `${prefix}:${sortedParams}`;
  }

  /**
   * Cache wrapper for async functions
   * @param {string} key - Cache key
   * @param {Function} asyncFunction - Async function to cache
   * @param {number} customTtl - Custom TTL in seconds (optional)
   * @returns {Promise<any>} Cached or fresh value
   */
  async cacheWrapper(key, asyncFunction, customTtl = null) {
    if (!this.enabled) {
      return await asyncFunction();
    }
    
    // Try to get from cache first
    const cachedValue = this.get(key);
    if (cachedValue !== null) {
      return cachedValue;
    }
    
    // If not in cache, execute function and cache result
    try {
      const result = await asyncFunction();
      this.set(key, result, customTtl);
      return result;
    } catch (error) {
      this.logger.error('Error in cache wrapper function', { error: error.message });
      throw error;
    }
  }
}

// Export singleton instance
module.exports = new CacheManager();