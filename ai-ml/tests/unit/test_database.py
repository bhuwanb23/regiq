#!/usr/bin/env python3
"""
Unit tests for database operations.
Tests database setup, connections, and basic CRUD operations.
"""

import pytest
import sqlite3
from pathlib import Path

from scripts.setup_database import create_database_schema, create_indexes, insert_initial_data


class TestDatabaseSchema:
    """Test cases for database schema creation."""
    
    def test_create_database_schema(self):
        """Test database schema creation."""
        schema = create_database_schema()
        
        assert isinstance(schema, dict)
        assert "user_profiles" in schema
        assert "model_bias_analysis" in schema
        assert "regulatory_documents" in schema
        assert len(schema) >= 10  # Should have at least 10 tables
    
    def test_schema_sql_validity(self):
        """Test that schema SQL is valid."""
        schema = create_database_schema()
        
        # Test with in-memory database
        conn = sqlite3.connect(':memory:')
        cursor = conn.cursor()
        
        for table_name, create_sql in schema.items():
            try:
                cursor.execute(create_sql)
                assert True  # SQL executed successfully
            except sqlite3.Error as e:
                pytest.fail(f"Invalid SQL for table {table_name}: {e}")
        
        conn.close()
    
    def test_create_indexes(self):
        """Test index creation."""
        indexes = create_indexes()
        
        assert isinstance(indexes, list)
        assert len(indexes) > 0
        
        # Test index SQL validity
        conn = sqlite3.connect(':memory:')
        cursor = conn.cursor()
        
        # Create a sample table first
        cursor.execute("""
            CREATE TABLE user_profiles (
                id INTEGER PRIMARY KEY,
                email VARCHAR(100),
                username VARCHAR(50)
            )
        """)
        
        # Test a sample index
        sample_index = "CREATE INDEX IF NOT EXISTS idx_user_profiles_email ON user_profiles(email)"
        cursor.execute(sample_index)
        
        conn.close()


class TestDatabaseOperations:
    """Test cases for database operations."""
    
    def test_database_connection(self, test_db):
        """Test database connection."""
        assert test_db is not None
        
        # Test basic query
        cursor = test_db.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        
        assert result[0] == 1
    
    def test_insert_user(self, test_db):
        """Test inserting a user."""
        cursor = test_db.cursor()
        
        cursor.execute(
            "INSERT INTO test_users (username, email) VALUES (?, ?)",
            ("testuser", "test@example.com")
        )
        test_db.commit()
        
        # Verify insertion
        cursor.execute("SELECT username, email FROM test_users WHERE username = ?", ("testuser",))
        result = cursor.fetchone()
        
        assert result[0] == "testuser"
        assert result[1] == "test@example.com"
    
    def test_insert_model(self, test_db):
        """Test inserting a model record."""
        cursor = test_db.cursor()
        
        cursor.execute(
            "INSERT INTO test_models (name, type, bias_score) VALUES (?, ?, ?)",
            ("TestModel", "classification", 0.85)
        )
        test_db.commit()
        
        # Verify insertion
        cursor.execute("SELECT name, type, bias_score FROM test_models WHERE name = ?", ("TestModel",))
        result = cursor.fetchone()
        
        assert result[0] == "TestModel"
        assert result[1] == "classification"
        assert result[2] == 0.85
    
    def test_query_with_sample_data(self, db_with_sample_data):
        """Test querying database with sample data."""
        cursor = db_with_sample_data.cursor()
        
        # Test user count
        cursor.execute("SELECT COUNT(*) FROM test_users")
        user_count = cursor.fetchone()[0]
        assert user_count == 3
        
        # Test model count
        cursor.execute("SELECT COUNT(*) FROM test_models")
        model_count = cursor.fetchone()[0]
        assert model_count == 3
        
        # Test specific query
        cursor.execute("SELECT name FROM test_models WHERE bias_score > 0.8")
        high_bias_models = cursor.fetchall()
        assert len(high_bias_models) == 2  # TestModel1 and TestModel3
    
    def test_update_record(self, db_with_sample_data):
        """Test updating a record."""
        cursor = db_with_sample_data.cursor()
        
        # Update bias score
        cursor.execute(
            "UPDATE test_models SET bias_score = ? WHERE name = ?",
            (0.95, "TestModel1")
        )
        db_with_sample_data.commit()
        
        # Verify update
        cursor.execute("SELECT bias_score FROM test_models WHERE name = ?", ("TestModel1",))
        result = cursor.fetchone()
        assert result[0] == 0.95
    
    def test_delete_record(self, db_with_sample_data):
        """Test deleting a record."""
        cursor = db_with_sample_data.cursor()
        
        # Delete a user
        cursor.execute("DELETE FROM test_users WHERE username = ?", ("testuser1",))
        db_with_sample_data.commit()
        
        # Verify deletion
        cursor.execute("SELECT COUNT(*) FROM test_users WHERE username = ?", ("testuser1",))
        count = cursor.fetchone()[0]
        assert count == 0
        
        # Verify other users still exist
        cursor.execute("SELECT COUNT(*) FROM test_users")
        total_count = cursor.fetchone()[0]
        assert total_count == 2
    
    def test_transaction_rollback(self, test_db):
        """Test transaction rollback."""
        cursor = test_db.cursor()
        
        try:
            # Start transaction
            cursor.execute("INSERT INTO test_users (username, email) VALUES (?, ?)", ("user1", "user1@test.com"))
            cursor.execute("INSERT INTO test_users (username, email) VALUES (?, ?)", ("user2", "user2@test.com"))
            
            # This should fail due to duplicate username
            cursor.execute("INSERT INTO test_users (username, email) VALUES (?, ?)", ("user1", "duplicate@test.com"))
            
            test_db.commit()
            pytest.fail("Should have raised an exception")
            
        except sqlite3.IntegrityError:
            test_db.rollback()
            
            # Verify no users were inserted
            cursor.execute("SELECT COUNT(*) FROM test_users")
            count = cursor.fetchone()[0]
            assert count == 0


class TestDatabaseInitialization:
    """Test cases for database initialization."""
    
    def test_initial_data_insertion(self):
        """Test initial data insertion function."""
        conn = sqlite3.connect(':memory:')
        cursor = conn.cursor()
        
        # Create system_settings table
        cursor.execute("""
            CREATE TABLE system_settings (
                id INTEGER PRIMARY KEY,
                setting_key VARCHAR(100) UNIQUE,
                setting_value TEXT,
                description TEXT
            )
        """)
        
        # Create user_profiles table
        cursor.execute("""
            CREATE TABLE user_profiles (
                id INTEGER PRIMARY KEY,
                username VARCHAR(50) UNIQUE,
                email VARCHAR(100) UNIQUE,
                full_name VARCHAR(100),
                role VARCHAR(20)
            )
        """)
        
        # Insert initial data
        insert_initial_data(cursor)
        conn.commit()
        
        # Verify system settings
        cursor.execute("SELECT COUNT(*) FROM system_settings")
        settings_count = cursor.fetchone()[0]
        assert settings_count > 0
        
        # Verify admin user
        cursor.execute("SELECT username, role FROM user_profiles WHERE role = 'admin'")
        admin_user = cursor.fetchone()
        assert admin_user is not None
        assert admin_user[0] == 'admin'
        
        conn.close()
    
    def test_database_file_creation(self, temp_dir):
        """Test database file creation."""
        db_path = temp_dir / "test_creation.db"
        
        # Create database
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE test_table (id INTEGER PRIMARY KEY)")
        conn.commit()
        conn.close()
        
        # Verify file exists
        assert db_path.exists()
        assert db_path.is_file()
        
        # Verify we can reconnect
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        conn.close()
        
        assert len(tables) == 1
        assert tables[0][0] == 'test_table'
