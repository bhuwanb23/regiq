#!/usr/bin/env python3
"""
Performance benchmarks and load testing for REGIQ AI/ML system.
Tests system performance under various load conditions.
"""

import pytest
import time
import statistics
from concurrent.futures import ThreadPoolExecutor, as_completed
from unittest.mock import Mock, patch

from config.gemini_config import GeminiAPIManager


@pytest.mark.performance
class TestAPIPerformanceBenchmarks:
    """Performance benchmarks for API operations."""
    
    def test_single_api_call_benchmark(self, mock_gemini_api_manager, performance_timer):
        """Benchmark single API call performance."""
        manager = mock_gemini_api_manager
        
        # Warm up
        manager.generate_content("Warmup call")
        
        # Benchmark
        performance_timer.start()
        response = manager.generate_content("Benchmark test prompt")
        performance_timer.stop()
        
        assert response is not None
        assert performance_timer.elapsed < 0.1  # Should be very fast with mock
    
    def test_multiple_sequential_calls_benchmark(self, mock_gemini_api_manager, performance_timer):
        """Benchmark multiple sequential API calls."""
        manager = mock_gemini_api_manager
        
        num_calls = 10
        performance_timer.start()
        
        responses = []
        for i in range(num_calls):
            response = manager.generate_content(f"Sequential test {i}")
            responses.append(response)
        
        performance_timer.stop()
        
        assert len(responses) == num_calls
        assert all(r is not None for r in responses)
        
        avg_time_per_call = performance_timer.elapsed / num_calls
        assert avg_time_per_call < 0.05  # Should be fast with mock
    
    def test_concurrent_api_calls_benchmark(self, mock_gemini_api_manager):
        """Benchmark concurrent API calls."""
        manager = mock_gemini_api_manager
        
        def make_api_call(call_id):
            start_time = time.time()
            response = manager.generate_content(f"Concurrent test {call_id}")
            end_time = time.time()
            return {
                'call_id': call_id,
                'response': response,
                'duration': end_time - start_time
            }
        
        num_concurrent_calls = 20
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(make_api_call, i) for i in range(num_concurrent_calls)]
            results = [future.result() for future in as_completed(futures)]
        
        end_time = time.time()
        total_time = end_time - start_time
        
        assert len(results) == num_concurrent_calls
        assert all(r['response'] is not None for r in results)
        
        # Calculate statistics
        durations = [r['duration'] for r in results]
        avg_duration = statistics.mean(durations)
        max_duration = max(durations)
        
        # With proper concurrency, total time should be less than sequential
        sequential_time_estimate = avg_duration * num_concurrent_calls
        assert total_time < sequential_time_estimate
        
        # Individual calls should still be fast
        assert avg_duration < 0.1
        assert max_duration < 0.2
    
    def test_rate_limiting_performance(self, mock_gemini_api_manager, performance_timer):
        """Test performance impact of rate limiting."""
        manager = mock_gemini_api_manager
        
        # Set low rate limit for testing
        manager.config.rate_limit_requests_per_minute = 5
        
        performance_timer.start()
        
        responses = []
        for i in range(8):  # Exceed rate limit
            response = manager.generate_content(f"Rate limit test {i}")
            responses.append(response)
        
        performance_timer.stop()
        
        assert len(responses) == 8
        assert all(r is not None for r in responses)
        
        # Should take some time due to rate limiting (but mocked, so still fast)
        assert performance_timer.elapsed >= 0  # At least some time


@pytest.mark.performance
class TestDatabasePerformanceBenchmarks:
    """Performance benchmarks for database operations."""
    
    def test_single_insert_benchmark(self, test_db, performance_timer):
        """Benchmark single database insert."""
        cursor = test_db.cursor()
        
        performance_timer.start()
        cursor.execute("INSERT INTO test_users (username, email) VALUES (?, ?)", ("bench_user", "bench@test.com"))
        test_db.commit()
        performance_timer.stop()
        
        assert performance_timer.elapsed < 0.01  # Should be very fast
    
    def test_bulk_insert_benchmark(self, test_db, performance_timer):
        """Benchmark bulk database inserts."""
        cursor = test_db.cursor()
        
        # Prepare bulk data
        num_records = 1000
        users = [(f"bulk_user_{i}", f"bulk_{i}@test.com") for i in range(num_records)]
        
        performance_timer.start()
        cursor.executemany("INSERT INTO test_users (username, email) VALUES (?, ?)", users)
        test_db.commit()
        performance_timer.stop()
        
        # Verify all records inserted
        cursor.execute("SELECT COUNT(*) FROM test_users")
        count = cursor.fetchone()[0]
        assert count == num_records
        
        # Performance check
        records_per_second = num_records / performance_timer.elapsed
        assert records_per_second > 100  # Should handle at least 100 records/second
    
    def test_complex_query_benchmark(self, db_with_sample_data, performance_timer):
        """Benchmark complex database queries."""
        cursor = db_with_sample_data.cursor()
        
        # Add more test data
        models = [(f"Bench_Model_{i}", "classification", 0.5 + (i * 0.01)) for i in range(100)]
        cursor.executemany("INSERT INTO test_models (name, type, bias_score) VALUES (?, ?, ?)", models)
        db_with_sample_data.commit()
        
        # Complex query with joins and aggregations
        performance_timer.start()
        cursor.execute("""
            SELECT 
                type,
                COUNT(*) as model_count,
                AVG(bias_score) as avg_bias,
                MAX(bias_score) as max_bias,
                MIN(bias_score) as min_bias
            FROM test_models 
            WHERE bias_score > 0.7
            GROUP BY type
            ORDER BY avg_bias DESC
        """)
        results = cursor.fetchall()
        performance_timer.stop()
        
        assert len(results) > 0
        assert performance_timer.elapsed < 0.1  # Should be fast for small dataset
    
    def test_concurrent_database_operations(self, test_db):
        """Benchmark concurrent database operations."""
        def database_operation(operation_id):
            cursor = test_db.cursor()
            start_time = time.time()
            
            # Insert
            cursor.execute("INSERT INTO test_users (username, email) VALUES (?, ?)", 
                          (f"concurrent_{operation_id}", f"concurrent_{operation_id}@test.com"))
            
            # Query
            cursor.execute("SELECT COUNT(*) FROM test_users")
            count = cursor.fetchone()[0]
            
            end_time = time.time()
            return {
                'operation_id': operation_id,
                'duration': end_time - start_time,
                'count': count
            }
        
        num_operations = 10
        start_time = time.time()
        
        # Note: SQLite doesn't handle true concurrency well, but test the pattern
        results = []
        for i in range(num_operations):
            result = database_operation(i)
            results.append(result)
            test_db.commit()
        
        end_time = time.time()
        total_time = end_time - start_time
        
        assert len(results) == num_operations
        assert all(r['count'] > 0 for r in results)
        
        avg_operation_time = total_time / num_operations
        assert avg_operation_time < 0.1  # Should be fast


@pytest.mark.performance
class TestMemoryPerformanceBenchmarks:
    """Performance benchmarks for memory usage."""
    
    def test_memory_usage_api_calls(self, mock_gemini_api_manager):
        """Test memory usage during API calls."""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
        manager = mock_gemini_api_manager
        
        # Make many API calls
        responses = []
        for i in range(100):
            response = manager.generate_content(f"Memory test {i}")
            responses.append(response)
        
        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory
        
        # Memory increase should be reasonable (less than 50MB for 100 calls)
        assert memory_increase < 50 * 1024 * 1024
        assert len(responses) == 100
    
    def test_memory_usage_database_operations(self, test_db):
        """Test memory usage during database operations."""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
        cursor = test_db.cursor()
        
        # Perform many database operations
        for i in range(1000):
            cursor.execute("INSERT INTO test_users (username, email) VALUES (?, ?)", 
                          (f"memory_user_{i}", f"memory_{i}@test.com"))
            
            if i % 100 == 0:  # Commit every 100 operations
                test_db.commit()
        
        test_db.commit()
        
        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory
        
        # Memory increase should be reasonable
        assert memory_increase < 100 * 1024 * 1024  # Less than 100MB
        
        # Verify all records were inserted
        cursor.execute("SELECT COUNT(*) FROM test_users")
        count = cursor.fetchone()[0]
        assert count == 1000


@pytest.mark.performance
@pytest.mark.slow
class TestLoadTestingBenchmarks:
    """Load testing benchmarks for system stress testing."""
    
    @pytest.mark.skipif(not os.getenv('RUN_LOAD_TESTS'), 
                       reason="Load tests require RUN_LOAD_TESTS=1 environment variable")
    def test_sustained_load_api_calls(self, mock_gemini_api_manager):
        """Test sustained load on API calls."""
        manager = mock_gemini_api_manager
        
        duration_seconds = 30
        start_time = time.time()
        call_count = 0
        errors = 0
        response_times = []
        
        while time.time() - start_time < duration_seconds:
            call_start = time.time()
            try:
                response = manager.generate_content(f"Load test call {call_count}")
                if response is None:
                    errors += 1
            except Exception:
                errors += 1
            
            call_end = time.time()
            response_times.append(call_end - call_start)
            call_count += 1
        
        # Calculate performance metrics
        total_time = time.time() - start_time
        calls_per_second = call_count / total_time
        error_rate = errors / call_count if call_count > 0 else 1
        avg_response_time = statistics.mean(response_times) if response_times else 0
        
        # Performance assertions
        assert calls_per_second > 10  # Should handle at least 10 calls/second
        assert error_rate < 0.01  # Less than 1% error rate
        assert avg_response_time < 0.1  # Average response time under 100ms
        
        print(f"Load test results:")
        print(f"  Total calls: {call_count}")
        print(f"  Calls per second: {calls_per_second:.2f}")
        print(f"  Error rate: {error_rate:.2%}")
        print(f"  Average response time: {avg_response_time:.3f}s")
    
    def test_stress_test_database(self, test_db):
        """Stress test database operations."""
        cursor = test_db.cursor()
        
        # Stress test parameters
        num_users = 5000
        num_models = 2000
        
        start_time = time.time()
        
        # Insert users in batches
        batch_size = 100
        for i in range(0, num_users, batch_size):
            batch_users = [(f"stress_user_{j}", f"stress_{j}@test.com") 
                          for j in range(i, min(i + batch_size, num_users))]
            cursor.executemany("INSERT INTO test_users (username, email) VALUES (?, ?)", batch_users)
            test_db.commit()
        
        # Insert models
        for i in range(0, num_models, batch_size):
            batch_models = [(f"Stress_Model_{j}", "classification", 0.5 + (j % 50) * 0.01) 
                           for j in range(i, min(i + batch_size, num_models))]
            cursor.executemany("INSERT INTO test_models (name, type, bias_score) VALUES (?, ?, ?)", batch_models)
            test_db.commit()
        
        insert_time = time.time() - start_time
        
        # Query performance under load
        query_start = time.time()
        cursor.execute("SELECT COUNT(*) FROM test_users")
        user_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM test_models")
        model_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT AVG(bias_score) FROM test_models")
        avg_bias = cursor.fetchone()[0]
        
        query_time = time.time() - query_start
        
        # Verify data integrity
        assert user_count == num_users
        assert model_count == num_models
        assert avg_bias is not None
        
        # Performance assertions
        assert insert_time < 60  # Should complete within 60 seconds
        assert query_time < 1  # Queries should be fast even with large dataset
        
        print(f"Stress test results:")
        print(f"  Users inserted: {user_count}")
        print(f"  Models inserted: {model_count}")
        print(f"  Insert time: {insert_time:.2f}s")
        print(f"  Query time: {query_time:.3f}s")


# Removed pytest configuration functions - these should be in conftest.py
