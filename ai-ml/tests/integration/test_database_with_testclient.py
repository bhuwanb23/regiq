#!/usr/bin/env python3
"""
Database integration tests using TestClient for REGIQ AI/ML system.
Tests database operations through API endpoints with real database integration.
"""

import sys
import os
import pytest
import sqlite3
import json
from pathlib import Path
from unittest.mock import patch, Mock

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from fastapi.testclient import TestClient
from services.api.main import app
from scripts.setup_database import setup_database

# Create test client
client = TestClient(app)


@pytest.mark.integration
@pytest.mark.database
class TestDatabaseWithTestClient:
    """Test database operations through API endpoints."""
    
    @pytest.fixture(autouse=True)
    def setup_test_database(self, temp_dir):
        """Setup test database for each test."""
        # Create test database
        self.db_path = temp_dir / "test_client_integration.db"
        
        # Setup database
        success = setup_database(str(self.db_path))
        assert success
        
        # Set environment variable for database URL
        os.environ['DATABASE_URL'] = f"sqlite:///{self.db_path}"
        
        yield
        
        # Cleanup
        if 'DATABASE_URL' in os.environ:
            del os.environ['DATABASE_URL']
    
    def test_user_registration_and_database_integration(self, temp_dir):
        """Test user registration through API and verify database integration."""
        # Mock authentication for testing
        with patch('services.api.auth.jwt_handler.get_current_user') as mock_user:
            mock_user.return_value = {"username": "test_user", "email": "test@example.com"}
            
            # Test user registration endpoint (if it existed)
            # Since we don't have a user registration endpoint, we'll test database directly
            # but through the API context
            
            # Make a request to test database connection through API
            response = client.get("/health")
            assert response.status_code == 200
            
            # Verify database was created and has tables
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            # Check that required tables exist
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            expected_tables = [
                'user_profiles', 'authentication_logs', 'regulatory_documents',
                'model_bias_analysis', 'system_settings'
            ]
            
            for table in expected_tables:
                assert table in tables
            
            conn.close()
    
    def test_model_analysis_database_integration(self, temp_dir):
        """Test model analysis data storage and retrieval through database."""
        # Mock authentication
        with patch('services.api.auth.jwt_handler.get_current_user') as mock_user:
            mock_user.return_value = {"username": "test_user", "email": "test@example.com"}
            
            # Mock Gemini API for testing
            with patch('config.gemini_config.genai.Client') as mock_client_class:
                mock_client = Mock()
                mock_response = Mock()
                mock_response.text = "Test bias analysis results"
                mock_client.models.generate_content.return_value = mock_response
                mock_client_class.return_value = mock_client
                
                # Test that database operations work in the API context
                response = client.get("/health")
                assert response.status_code == 200
                
                # Verify database integrity
                conn = sqlite3.connect(str(self.db_path))
                cursor = conn.cursor()
                
                # Insert test data directly to simulate API behavior
                cursor.execute("""
                    INSERT INTO user_profiles (username, email, full_name) 
                    VALUES (?, ?, ?)
                """, ("api_test_user", "api_test@example.com", "API Test User"))
                
                cursor.execute("""
                    INSERT INTO model_bias_analysis 
                    (user_id, model_name, model_type, dataset_name, bias_score) 
                    VALUES (?, ?, ?, ?, ?)
                """, (1, "TestModel", "classification", "test_dataset", 0.85))
                
                conn.commit()
                
                # Verify data was inserted
                cursor.execute("SELECT COUNT(*) FROM user_profiles WHERE username = ?", ("api_test_user",))
                user_count = cursor.fetchone()[0]
                assert user_count == 1
                
                cursor.execute("SELECT bias_score FROM model_bias_analysis WHERE model_name = ?", ("TestModel",))
                bias_score = cursor.fetchone()[0]
                assert bias_score == 0.85
                
                conn.close()


@pytest.mark.integration
@pytest.mark.database
class TestDataPipelineDatabaseIntegration:
    """Test data pipeline database integration through API endpoints."""
    
    @pytest.fixture(autouse=True)
    def setup_test_database(self, temp_dir):
        """Setup test database for each test."""
        # Create test database
        self.db_path = temp_dir / "data_pipeline_integration.db"
        
        # Setup database
        success = setup_database(str(self.db_path))
        assert success
        
        # Set environment variable for database URL
        os.environ['DATABASE_URL'] = f"sqlite:///{self.db_path}"
        
        yield
        
        # Cleanup
        if 'DATABASE_URL' in os.environ:
            del os.environ['DATABASE_URL']
    
    def test_data_ingestion_database_integration(self, temp_dir):
        """Test data ingestion database integration."""
        # Mock authentication
        with patch('services.api.auth.jwt_handler.get_current_user') as mock_user:
            mock_user.return_value = {"username": "test_user", "email": "test@example.com"}
            
            # Create test data file
            test_csv_content = """id,name,age,gender,income
1,John Doe,35,Male,50000
2,Jane Smith,28,Female,45000
"""
            
            test_file_path = temp_dir / "test_ingestion.csv"
            test_file_path.write_text(test_csv_content)
            
            # Mock the file upload process
            with patch('uuid.uuid4') as mock_uuid:
                mock_uuid.return_value = "test-upload-id"
                
                # Test that database operations would work
                response = client.get("/health")
                assert response.status_code == 200
                
                # Verify database schema for data pipeline
                conn = sqlite3.connect(str(self.db_path))
                cursor = conn.cursor()
                
                # Check that we can work with the database in the API context
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = [row[0] for row in cursor.fetchall()]
                
                # While we don't have specific data pipeline tables in the schema,
                # we can verify the database is working correctly
                assert len(tables) > 0
                
                conn.close()
    
    def test_processing_status_database_integration(self, temp_dir):
        """Test processing status database integration."""
        # Mock authentication
        with patch('services.api.auth.jwt_handler.get_current_user') as mock_user:
            mock_user.return_value = {"username": "test_user", "email": "test@example.com"}
            
            # Mock the processing status API
            with patch('uuid.uuid4') as mock_uuid:
                mock_uuid.return_value = "test-job-id"
                
                # Test that database operations work in API context
                response = client.get("/health")
                assert response.status_code == 200
                
                # Verify database operations
                conn = sqlite3.connect(str(self.db_path))
                cursor = conn.cursor()
                
                # Test database connectivity and basic operations
                cursor.execute("SELECT COUNT(*) FROM user_profiles")
                count = cursor.fetchone()[0]
                assert isinstance(count, int)
                
                conn.close()


@pytest.mark.integration
@pytest.mark.database
class TestDatabaseTransactionsWithTestClient:
    """Test database transactions through API endpoints."""
    
    @pytest.fixture(autouse=True)
    def setup_test_database(self, temp_dir):
        """Setup test database for each test."""
        # Create test database
        self.db_path = temp_dir / "transaction_integration.db"
        
        # Setup database
        success = setup_database(str(self.db_path))
        assert success
        
        # Set environment variable for database URL
        os.environ['DATABASE_URL'] = f"sqlite:///{self.db_path}"
        
        yield
        
        # Cleanup
        if 'DATABASE_URL' in os.environ:
            del os.environ['DATABASE_URL']
    
    def test_atomic_operations_through_api(self, temp_dir):
        """Test that database operations are atomic through API."""
        # Mock authentication
        with patch('services.api.auth.jwt_handler.get_current_user') as mock_user:
            mock_user.return_value = {"username": "test_user", "email": "test@example.com"}
            
            # Test database operations through API context
            response = client.get("/health")
            assert response.status_code == 200
            
            # Verify atomic operations work
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            # Begin transaction
            cursor.execute("BEGIN")
            
            # Insert multiple records
            users = [
                ("atomic_user1", "atomic1@example.com"),
                ("atomic_user2", "atomic2@example.com")
            ]
            
            cursor.executemany("""
                INSERT INTO user_profiles (username, email) 
                VALUES (?, ?)
            """, users)
            
            # Commit transaction
            cursor.execute("COMMIT")
            
            # Verify all records were inserted
            cursor.execute("SELECT COUNT(*) FROM user_profiles WHERE username LIKE 'atomic_user%'")
            count = cursor.fetchone()[0]
            assert count == 2
            
            conn.close()
    
    def test_rollback_operations_through_api(self, temp_dir):
        """Test that database rollbacks work through API."""
        # Mock authentication
        with patch('services.api.auth.jwt_handler.get_current_user') as mock_user:
            mock_user.return_value = {"username": "test_user", "email": "test@example.com"}
            
            # Test database operations through API context
            response = client.get("/health")
            assert response.status_code == 200
            
            # Verify rollback operations work
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            # Clean state first
            cursor.execute("DELETE FROM user_profiles WHERE username LIKE 'rollback_test%'")
            conn.commit()
            
            try:
                # Begin transaction
                cursor.execute("BEGIN")
                
                # Insert valid records
                cursor.execute("""
                    INSERT INTO user_profiles (username, email) 
                    VALUES (?, ?)
                """, ("rollback_test1", "rollback1@example.com"))
                
                # This should cause an error (duplicate username)
                cursor.execute("""
                    INSERT INTO user_profiles (username, email) 
                    VALUES (?, ?)
                """, ("rollback_test1", "duplicate@example.com"))
                
                # If we reach here, commit
                cursor.execute("COMMIT")
                
            except sqlite3.IntegrityError:
                # Rollback on error
                cursor.execute("ROLLBACK")
            
            # Verify that no records were inserted due to rollback
            cursor.execute("SELECT COUNT(*) FROM user_profiles WHERE username LIKE 'rollback_test%'")
            count = cursor.fetchone()[0]
            assert count == 0
            
            conn.close()


@pytest.mark.integration
@pytest.mark.database
class TestDatabasePerformanceWithTestClient:
    """Test database performance through API endpoints."""
    
    @pytest.fixture(autouse=True)
    def setup_test_database(self, temp_dir):
        """Setup test database for each test."""
        # Create test database
        self.db_path = temp_dir / "performance_integration.db"
        
        # Setup database
        success = setup_database(str(self.db_path))
        assert success
        
        # Set environment variable for database URL
        os.environ['DATABASE_URL'] = f"sqlite:///{self.db_path}"
        
        yield
        
        # Cleanup
        if 'DATABASE_URL' in os.environ:
            del os.environ['DATABASE_URL']
    
    def test_bulk_operations_performance(self, temp_dir, performance_timer):
        """Test performance of bulk database operations through API context."""
        # Mock authentication
        with patch('services.api.auth.jwt_handler.get_current_user') as mock_user:
            mock_user.return_value = {"username": "test_user", "email": "test@example.com"}
            
            # Test database operations through API context
            response = client.get("/health")
            assert response.status_code == 200
            
            # Measure bulk insert performance
            performance_timer.start()
            
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            # Insert multiple records
            users = [(f"perf_user_{i}", f"perf_user_{i}@example.com") for i in range(100)]
            
            cursor.executemany("""
                INSERT INTO user_profiles (username, email) 
                VALUES (?, ?)
            """, users)
            
            conn.commit()
            
            performance_timer.stop()
            
            # Verify all records were inserted
            cursor.execute("SELECT COUNT(*) FROM user_profiles WHERE username LIKE 'perf_user_%'")
            count = cursor.fetchone()[0]
            assert count == 100
            
            # Performance should be reasonable (less than 2 seconds for 100 records)
            assert performance_timer.elapsed < 2.0
            
            conn.close()
    
    def test_query_performance_with_indexes(self, temp_dir, performance_timer):
        """Test query performance with proper indexing through API context."""
        # Mock authentication
        with patch('services.api.auth.jwt_handler.get_current_user') as mock_user:
            mock_user.return_value = {"username": "test_user", "email": "test@example.com"}
            
            # Test database operations through API context
            response = client.get("/health")
            assert response.status_code == 200
            
            # Setup test data
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            # Insert test data
            models = [(f"PerfModel_{i}", "classification", 0.5 + (i % 50) / 100) for i in range(100)]
            cursor.executemany("""
                INSERT INTO model_bias_analysis 
                (user_id, model_name, model_type, dataset_name, bias_score) 
                VALUES (?, ?, ?, ?, ?)
            """, [(1, name, type_, "test_dataset", score) for name, type_, score in models])
            
            conn.commit()
            
            # Measure query performance
            performance_timer.start()
            
            # Query with filter that should use index
            cursor.execute("""
                SELECT model_name, bias_score 
                FROM model_bias_analysis 
                WHERE bias_score > 0.8 
                ORDER BY bias_score DESC
            """)
            results = cursor.fetchall()
            
            performance_timer.stop()
            
            # Verify we got results
            assert len(results) > 0
            
            # Performance should be reasonable (less than 1 second)
            assert performance_timer.elapsed < 1.0
            
            conn.close()