#!/usr/bin/env python3
"""
Test Redis client for REGIQ AI/ML Service
"""

import sys
import os

# Add the parent directory to the path so we can import the redis_client
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.api.redis_client import redis_client

def test_redis():
    """Test Redis client functionality."""
    try:
        # Test setting a value
        print("Setting test key...")
        result = redis_client.set("test_key_py", "Hello Redis from Python!", 10)  # Expire in 10 seconds
        print(f"Set result: {result}")
        
        # Test getting a value
        print("Getting test key...")
        value = redis_client.get("test_key_py")
        print(f"Retrieved value: {value}")
        
        # Test checking existence
        print("Checking if key exists...")
        exists = redis_client.exists("test_key_py")
        print(f"Key exists: {exists}")
        
        # Test setting JSON data
        print("Setting JSON data...")
        json_data = {"name": "REGIQ", "type": "AI Compliance Copilot", "version": "1.0"}
        json_result = redis_client.set_json("test_json_key", json_data, 10)
        print(f"Set JSON result: {json_result}")
        
        # Test getting JSON data
        print("Getting JSON data...")
        retrieved_json = redis_client.get_json("test_json_key")
        print(f"Retrieved JSON: {retrieved_json}")
        
        # Test deleting a key
        print("Deleting test key...")
        delete_result = redis_client.delete("test_key_py")
        print(f"Delete result: {delete_result}")
        
        # Verify deletion
        print("Checking if key exists after deletion...")
        exists_after_delete = redis_client.exists("test_key_py")
        print(f"Key exists after deletion: {exists_after_delete}")
        
        # Test flushing all keys
        print("Flushing all keys...")
        flush_result = redis_client.flush_all()
        print(f"Flush result: {flush_result}")
        
        print("Redis test completed successfully!")
        return True
        
    except Exception as e:
        print(f"Redis test failed: {e}")
        return False

if __name__ == "__main__":
    test_redis()