#!/usr/bin/env python3
"""
Database integration tests for REGIQ AI/ML system.
Tests database operations including CRUD, transactions, and data integrity.
"""

import pytest
import sqlite3
import os
from pathlib import Path
from datetime import datetime

from scripts.setup_database import setup_database, create_database_schema, insert_initial_data
from config.env_config import get_env_config


@pytest.mark.integration
@pytest.mark.database
class TestDatabaseCRUDOperations:
    """Test CRUD operations on the database."""
    
    def test_user_profile_crud(self, test_db):
        """Test CRUD operations for user profiles."""
        cursor = test_db.cursor()
        
        # Create - Insert a new user
        cursor.execute("""
            INSERT INTO test_users (username, email) 
            VALUES (?, ?)
        """, ("test_user", "test@example.com"))
        test_db.commit()
        
        # Read - Retrieve the user
        cursor.execute("""
            SELECT id, username, email, created_at 
            FROM test_users 
            WHERE username = ?
        """, ("test_user",))
        user = cursor.fetchone()
        
        assert user is not None
        assert user[1] == "test_user"
        assert user[2] == "test@example.com"
        assert user[3] is not None  # created_at should be set
        
        # Update - Modify user information
        cursor.execute("""
            UPDATE test_users 
            SET email = ? 
            WHERE username = ?
        """, ("updated@example.com", "test_user"))
        test_db.commit()
        
        # Read again to verify update
        cursor.execute("""
            SELECT email 
            FROM test_users 
            WHERE username = ?
        """, ("test_user",))
        updated_user = cursor.fetchone()
        
        assert updated_user[0] == "updated@example.com"
        
        # Delete - Remove the user
        cursor.execute("DELETE FROM test_users WHERE username = ?", ("test_user",))
        test_db.commit()
        
        # Verify deletion
        cursor.execute("SELECT COUNT(*) FROM test_users WHERE username = ?", ("test_user",))
        count = cursor.fetchone()[0]
        assert count == 0
    
    def test_model_analysis_crud(self, test_db):
        """Test CRUD operations for model analysis records."""
        cursor = test_db.cursor()
        
        # Create - Insert a model analysis record
        cursor.execute("""
            INSERT INTO test_models (name, type, bias_score) 
            VALUES (?, ?, ?)
        """, ("TestModel", "classification", 0.85))
        test_db.commit()
        
        # Read - Retrieve the model analysis
        cursor.execute("""
            SELECT id, name, type, bias_score, created_at 
            FROM test_models 
            WHERE name = ?
        """, ("TestModel",))
        model = cursor.fetchone()
        
        assert model is not None
        assert model[1] == "TestModel"
        assert model[2] == "classification"
        assert model[3] == 0.85
        assert model[4] is not None  # created_at should be set
        
        # Update - Modify bias score
        cursor.execute("""
            UPDATE test_models 
            SET bias_score = ? 
            WHERE name = ?
        """, (0.92, "TestModel"))
        test_db.commit()
        
        # Read again to verify update
        cursor.execute("""
            SELECT bias_score 
            FROM test_models 
            WHERE name = ?
        """, ("TestModel",))
        updated_model = cursor.fetchone()
        
        assert updated_model[0] == 0.92
        
        # Delete - Remove the model analysis
        cursor.execute("DELETE FROM test_models WHERE name = ?", ("TestModel",))
        test_db.commit()
        
        # Verify deletion
        cursor.execute("SELECT COUNT(*) FROM test_models WHERE name = ?", ("TestModel",))
        count = cursor.fetchone()[0]
        assert count == 0


@pytest.mark.integration
@pytest.mark.database
class TestDatabaseTransactions:
    """Test database transaction handling."""
    
    def test_transaction_rollback_on_error(self, test_db):
        """Test that transactions are properly rolled back on error."""
        cursor = test_db.cursor()
        
        # Start with a clean state
        cursor.execute("DELETE FROM test_users")
        test_db.commit()
        
        try:
            # Begin transaction
            cursor.execute("BEGIN")
            
            # Insert valid records
            cursor.execute("""
                INSERT INTO test_users (username, email) 
                VALUES (?, ?)
            """, ("user1", "user1@example.com"))
            
            cursor.execute("""
                INSERT INTO test_users (username, email) 
                VALUES (?, ?)
            """, ("user2", "user2@example.com"))
            
            # This should cause an error (duplicate username)
            cursor.execute("""
                INSERT INTO test_users (username, email) 
                VALUES (?, ?)
            """, ("user1", "duplicate@example.com"))
            
            # If we reach here, the transaction should commit
            cursor.execute("COMMIT")
            
        except sqlite3.IntegrityError:
            # Rollback on error
            cursor.execute("ROLLBACK")
        
        # Verify that no records were inserted due to rollback
        cursor.execute("SELECT COUNT(*) FROM test_users")
        count = cursor.fetchone()[0]
        assert count == 0
    
    def test_successful_transaction_commit(self, test_db):
        """Test that successful transactions are properly committed."""
        cursor = test_db.cursor()
        
        # Start with a clean state
        cursor.execute("DELETE FROM test_users")
        test_db.commit()
        
        # Begin transaction
        cursor.execute("BEGIN")
        
        # Insert multiple records
        users = [
            ("user1", "user1@example.com"),
            ("user2", "user2@example.com"),
            ("user3", "user3@example.com")
        ]
        
        cursor.executemany("""
            INSERT INTO test_users (username, email) 
            VALUES (?, ?)
        """, users)
        
        # Commit transaction
        cursor.execute("COMMIT")
        
        # Verify all records were inserted
        cursor.execute("SELECT COUNT(*) FROM test_users")
        count = cursor.fetchone()[0]
        assert count == 3
        
        # Verify specific records
        cursor.execute("SELECT username FROM test_users ORDER BY username")
        usernames = [row[0] for row in cursor.fetchall()]
        assert usernames == ["user1", "user2", "user3"]


@pytest.mark.integration
@pytest.mark.database
class TestDataIntegrity:
    """Test data integrity constraints."""
    
    def test_unique_constraints(self, test_db):
        """Test that unique constraints are enforced."""
        cursor = test_db.cursor()
        
        # Insert a user
        cursor.execute("""
            INSERT INTO test_users (username, email) 
            VALUES (?, ?)
        """, ("unique_user", "unique@example.com"))
        test_db.commit()
        
        # Attempt to insert another user with the same username (should fail)
        with pytest.raises(sqlite3.IntegrityError):
            cursor.execute("""
                INSERT INTO test_users (username, email) 
                VALUES (?, ?)
            """, ("unique_user", "different@example.com"))
            test_db.commit()
        
        # Attempt to insert another user with the same email (should fail)
        with pytest.raises(sqlite3.IntegrityError):
            cursor.execute("""
                INSERT INTO test_users (username, email) 
                VALUES (?, ?)
            """, ("different_user", "unique@example.com"))
            test_db.commit()
    
    def test_not_null_constraints(self, test_db):
        """Test that NOT NULL constraints are enforced."""
        cursor = test_db.cursor()
        
        # Attempt to insert a user without username (should fail)
        with pytest.raises(sqlite3.IntegrityError):
            cursor.execute("""
                INSERT INTO test_users (email) 
                VALUES (?)
            """, ("test@example.com",))
            test_db.commit()
        
        # Attempt to insert a user without email (should fail)
        with pytest.raises(sqlite3.IntegrityError):
            cursor.execute("""
                INSERT INTO test_users (username) 
                VALUES (?)
            """, ("test_user",))
            test_db.commit()
    
    def test_data_types_and_ranges(self, test_db):
        """Test that data types and ranges are properly handled."""
        cursor = test_db.cursor()
        
        # Insert a model with valid bias score
        cursor.execute("""
            INSERT INTO test_models (name, type, bias_score) 
            VALUES (?, ?, ?)
        """, ("ValidModel", "classification", 0.85))
        test_db.commit()
        
        # Verify the record was inserted correctly
        cursor.execute("""
            SELECT name, type, bias_score 
            FROM test_models 
            WHERE name = ?
        """, ("ValidModel",))
        model = cursor.fetchone()
        
        assert model[0] == "ValidModel"
        assert model[1] == "classification"
        assert model[2] == 0.85


@pytest.mark.integration
@pytest.mark.database
class TestDatabaseMigrations:
    """Test database schema migrations."""
    
    def test_database_setup_creates_all_tables(self, temp_dir):
        """Test that database setup creates all required tables."""
        db_path = temp_dir / "migration_test.db"
        
        # Setup database
        success = setup_database(str(db_path))
        assert success
        
        # Connect to database and check tables
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Get all table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        # Check for expected tables
        expected_tables = [
            'user_profiles', 'authentication_logs', 'regulatory_documents',
            'compliance_alerts', 'model_bias_analysis', 'regulatory_compliance',
            'risk_simulation_results', 'generated_reports', 'system_audit_logs',
            'system_settings'
        ]
        
        for table in expected_tables:
            assert table in tables, f"Table {table} not found in database"
        
        conn.close()
    
    def test_database_schema_validity(self):
        """Test that the database schema is valid."""
        schema = create_database_schema()
        
        # Test with in-memory database
        conn = sqlite3.connect(':memory:')
        cursor = conn.cursor()
        
        # Create all tables
        for table_name, create_sql in schema.items():
            try:
                cursor.execute(create_sql)
            except sqlite3.Error as e:
                pytest.fail(f"Invalid SQL for table {table_name}: {e}")
        
        # Verify tables were created
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        created_tables = [row[0] for row in cursor.fetchall()]
        
        assert len(created_tables) >= 10  # Should have at least 10 tables
        
        conn.close()
    
    def test_initial_data_insertion(self):
        """Test that initial data is properly inserted."""
        conn = sqlite3.connect(':memory:')
        cursor = conn.cursor()
        
        # Create required tables first
        schema = create_database_schema()
        for table_name, create_sql in schema.items():
            cursor.execute(create_sql)
        
        # Insert initial data
        insert_initial_data(cursor)
        conn.commit()
        
        # Verify system settings were inserted
        cursor.execute("SELECT COUNT(*) FROM system_settings")
        settings_count = cursor.fetchone()[0]
        assert settings_count > 0
        
        # Verify default admin user was created
        cursor.execute("SELECT username, role FROM user_profiles WHERE role = 'admin'")
        admin_user = cursor.fetchone()
        assert admin_user is not None
        assert admin_user[0] == 'admin'
        
        conn.close()


@pytest.mark.integration
@pytest.mark.database
class TestDatabasePerformance:
    """Test database performance with larger datasets."""
    
    def test_bulk_insert_performance(self, test_db, performance_timer):
        """Test performance of bulk insert operations."""
        cursor = test_db.cursor()
        
        # Generate test data
        users = [(f"user_{i}", f"user_{i}@example.com") for i in range(1000)]
        
        performance_timer.start()
        
        # Bulk insert
        cursor.executemany("""
            INSERT INTO test_users (username, email) 
            VALUES (?, ?)
        """, users)
        test_db.commit()
        
        performance_timer.stop()
        
        # Verify all records were inserted
        cursor.execute("SELECT COUNT(*) FROM test_users WHERE username LIKE 'user_%'")
        count = cursor.fetchone()[0]
        assert count == 1000
        
        # Performance should be reasonable (less than 2 seconds for 1000 records)
        assert performance_timer.elapsed < 2.0
    
    def test_query_performance_with_indexes(self, test_db, performance_timer):
        """Test query performance with proper indexing."""
        cursor = test_db.cursor()
        
        # Insert test data
        models = [(f"Model_{i}", "classification", 0.5 + (i % 50) / 100) for i in range(1000)]
        cursor.executemany("""
            INSERT INTO test_models (name, type, bias_score) 
            VALUES (?, ?, ?)
        """, models)
        test_db.commit()
        
        performance_timer.start()
        
        # Query with filter that should use index
        cursor.execute("""
            SELECT name, bias_score 
            FROM test_models 
            WHERE bias_score > 0.8 
            ORDER BY bias_score DESC
        """)
        results = cursor.fetchall()
        
        performance_timer.stop()
        
        # Verify we got results
        assert len(results) > 0
        
        # Performance should be reasonable (less than 1 second)
        assert performance_timer.elapsed < 1.0