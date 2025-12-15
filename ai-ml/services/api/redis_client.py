#!/usr/bin/env python3
"""
Redis Client for REGIQ AI/ML Service
Provides caching functionality for the FastAPI application.
"""

import redis
import os
import json
import logging
from typing import Optional, Union
from functools import wraps
import time

# Configure logger
logger = logging.getLogger(__name__)

class RedisClient:
    """Redis client wrapper for caching operations."""
    
    def __init__(self):
        """Initialize Redis client with configuration from environment variables."""
        # Get Redis configuration from environment variables
        self.redis_host = os.getenv('REDIS_HOST', 'localhost')
        self.redis_port = int(os.getenv('REDIS_PORT', 6379))
        self.redis_password = os.getenv('REDIS_PASSWORD', None)
        self.redis_url = os.getenv('REDIS_URL', f'redis://{self.redis_host}:{self.redis_port}')
        
        # Create Redis client
        try:
            if self.redis_url:
                self.client = redis.from_url(self.redis_url)
            else:
                self.client = redis.Redis(
                    host=self.redis_host,
                    port=self.redis_port,
                    password=self.redis_password,
                    decode_responses=True
                )
            
            # Test connection
            self.client.ping()
            logger.info("Redis connection established")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            self.client = None
    
    def get(self, key: str) -> Optional[str]:
        """
        Get value by key from Redis.
        
        Args:
            key (str): Cache key
            
        Returns:
            Optional[str]: Cached value or None if not found
        """
        try:
            if not self.client:
                return None
                
            value = self.client.get(key)
            if value:
                logger.debug(f"Cache hit for key: {key}")
            else:
                logger.debug(f"Cache miss for key: {key}")
            return value
        except Exception as e:
            logger.error(f"Error getting key {key} from Redis: {e}")
            return None
    
    def set(self, key: str, value: Union[str, dict], expire_seconds: Optional[int] = None) -> bool:
        """
        Set value by key in Redis with optional expiration.
        
        Args:
            key (str): Cache key
            value (Union[str, dict]): Value to cache
            expire_seconds (Optional[int]): Expiration time in seconds
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if not self.client:
                return False
                
            # Convert dict to JSON string if needed
            if isinstance(value, dict):
                value = json.dumps(value)
                
            if expire_seconds:
                result = self.client.setex(key, expire_seconds, value)
            else:
                result = self.client.set(key, value)
                
            if result:
                logger.debug(f"Cache set for key: {key}")
            return result
        except Exception as e:
            logger.error(f"Error setting key {key} in Redis: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """
        Delete key from Redis.
        
        Args:
            key (str): Cache key to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if not self.client:
                return False
                
            result = self.client.delete(key)
            if result:
                logger.debug(f"Cache deleted for key: {key}")
            return result > 0
        except Exception as e:
            logger.error(f"Error deleting key {key} from Redis: {e}")
            return False
    
    def exists(self, key: str) -> bool:
        """
        Check if key exists in Redis.
        
        Args:
            key (str): Cache key to check
            
        Returns:
            bool: True if key exists, False otherwise
        """
        try:
            if not self.client:
                return False
                
            result = self.client.exists(key)
            return result == 1
        except Exception as e:
            logger.error(f"Error checking existence of key {key} in Redis: {e}")
            return False
    
    def flush_all(self) -> bool:
        """
        Flush all keys from Redis.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if not self.client:
                return False
                
            self.client.flushall()
            logger.info("All Redis keys flushed")
            return True
        except Exception as e:
            logger.error(f"Error flushing Redis keys: {e}")
            return False
    
    def get_json(self, key: str) -> Optional[dict]:
        """
        Get JSON value by key from Redis.
        
        Args:
            key (str): Cache key
            
        Returns:
            Optional[dict]: Cached JSON value or None if not found
        """
        try:
            value = self.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.error(f"Error parsing JSON for key {key}: {e}")
            return None
    
    def set_json(self, key: str, value: dict, expire_seconds: Optional[int] = None) -> bool:
        """
        Set JSON value by key in Redis with optional expiration.
        
        Args:
            key (str): Cache key
            value (dict): JSON value to cache
            expire_seconds (Optional[int]): Expiration time in seconds
            
        Returns:
            bool: True if successful, False otherwise
        """
        return self.set(key, json.dumps(value), expire_seconds)

# Create singleton instance
redis_client = RedisClient()

def cache_result(expire_seconds: int = 300):
    """
    Decorator to cache function results in Redis.
    
    Args:
        expire_seconds (int): Cache expiration time in seconds (default: 5 minutes)
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key from function name and arguments
            cache_key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"
            
            # Try to get cached result
            cached_result = redis_client.get_json(cache_key)
            if cached_result is not None:
                return cached_result
            
            # Execute function and cache result
            start_time = time.time()
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            
            # Cache the result
            redis_client.set_json(cache_key, result, expire_seconds)
            logger.info(f"Cached result for {func.__name__} (executed in {execution_time:.2f}s)")
            
            return result
        return wrapper
    return decorator