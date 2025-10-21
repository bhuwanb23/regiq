#!/usr/bin/env python3
"""
End-to-end tests for REGIQ AI/ML system.
Tests complete workflows from start to finish.
"""

import pytest
import os
import tempfile
from pathlib import Path
from unittest.mock import patch, Mock

from config.env_config import get_env_config
from config.gemini_config import GeminiAPIManager
from scripts.setup_database import setup_database, test_database_connection


@pytest.mark.e2e
class TestCompleteSetupWorkflow:
    """End-to-end tests for complete system setup."""
    
    def test_full_environment_setup(self, temp_dir):
        """Test complete environment setup workflow."""
        # Step 1: Environment configuration
        test_env_file = temp_dir / ".env"
        test_env_file.write_text("""
TESTING=true
GEMINI_API_KEY=test-e2e-api-key
DATABASE_URL=sqlite:///data/e2e_test.db
DEBUG=true
LOG_LEVEL=DEBUG
SECRET_KEY=e2e-test-secret
""")
        
        # Step 2: Load environment
        from config.env_config import EnvironmentConfig
        env_config = EnvironmentConfig(str(test_env_file))
        
        # Step 3: Validate configuration
        validation = env_config.validate_required()
        assert validation['valid']
        
        # Step 4: Initialize API manager
        with patch.dict(os.environ, {'GEMINI_API_KEY': 'test-e2e-api-key'}):
            api_manager = GeminiAPIManager()
            assert api_manager.config.api_key == 'test-e2e-api-key'
    
    def test_database_setup_workflow(self, temp_dir):
        """Test complete database setup workflow."""
        db_path = temp_dir / "e2e_test.db"
        
        # Step 1: Setup database
        success = setup_database(str(db_path))
        assert success
        
        # Step 2: Verify database exists
        assert db_path.exists()
        
        # Step 3: Test database connection
        connection_success = test_database_connection(str(db_path))
        assert connection_success
        
        # Step 4: Verify tables were created
        import sqlite3
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        expected_tables = [
            'user_profiles', 'authentication_logs', 'regulatory_documents',
            'model_bias_analysis', 'system_settings'
        ]
        
        for table in expected_tables:
            assert table in tables
        
        conn.close()
    
    @patch('config.gemini_config.genai.Client')
    def test_api_workflow_complete(self, mock_client_class, temp_dir):
        """Test complete API workflow."""
        # Setup mock
        mock_client = Mock()
        mock_response = Mock()
        mock_response.text = "E2E test response from Gemini"
        mock_client.models.generate_content.return_value = mock_response
        mock_client_class.return_value = mock_client
        
        # Step 1: Initialize API manager
        with patch.dict(os.environ, {'GEMINI_API_KEY': 'test-e2e-key'}):
            api_manager = GeminiAPIManager()
        
        # Step 2: Test basic generation
        response = api_manager.generate_content("E2E test prompt")
        assert response == "E2E test response from Gemini"
        
        # Step 3: Test with different models
        models = ["gemini-2.5-flash", "gemini-1.5-flash"]
        for model in models:
            response = api_manager.generate_content("Test prompt", model=model)
            assert response is not None
        
        # Step 4: Verify API was called
        assert mock_client.models.generate_content.called


@pytest.mark.e2e
class TestUserWorkflows:
    """End-to-end tests for user workflows."""
    
    def test_new_user_setup_workflow(self, db_with_sample_data, mock_gemini_api_manager):
        """Test complete new user setup workflow."""
        cursor = db_with_sample_data.cursor()
        api_manager = mock_gemini_api_manager
        
        # Step 1: Create new user
        cursor.execute(
            "INSERT INTO test_users (username, email) VALUES (?, ?)",
            ("new_e2e_user", "e2e@example.com")
        )
        db_with_sample_data.commit()
        
        # Step 2: User makes first API call
        response = api_manager.generate_content("Hello, I'm a new user!")
        assert response == "This is a test response from Gemini API"
        
        # Step 3: Store user's first model analysis
        cursor.execute(
            "INSERT INTO test_models (name, type, bias_score) VALUES (?, ?, ?)",
            ("User_First_Model", "classification", 0.75)
        )
        db_with_sample_data.commit()
        
        # Step 4: Verify complete workflow
        cursor.execute("SELECT username FROM test_users WHERE email = ?", ("e2e@example.com",))
        user = cursor.fetchone()
        assert user[0] == "new_e2e_user"
        
        cursor.execute("SELECT name FROM test_models WHERE name = ?", ("User_First_Model",))
        model = cursor.fetchone()
        assert model[0] == "User_First_Model"
    
    def test_model_analysis_workflow(self, db_with_sample_data, mock_gemini_api_manager):
        """Test complete model analysis workflow."""
        cursor = db_with_sample_data.cursor()
        api_manager = mock_gemini_api_manager
        
        # Step 1: User uploads model data
        model_data = {
            'name': 'E2E_Test_Model',
            'type': 'classification',
            'initial_bias_score': 0.82
        }
        
        # Step 2: Generate analysis prompt
        analysis_prompt = f"Analyze bias in {model_data['type']} model with score {model_data['initial_bias_score']}"
        
        # Step 3: Get AI analysis
        ai_analysis = api_manager.generate_content(analysis_prompt)
        assert ai_analysis is not None
        
        # Step 4: Store analysis results
        cursor.execute(
            "INSERT INTO test_models (name, type, bias_score) VALUES (?, ?, ?)",
            (model_data['name'], model_data['type'], model_data['initial_bias_score'])
        )
        db_with_sample_data.commit()
        
        # Step 5: Generate recommendations
        recommendations = api_manager.generate_content("Provide bias mitigation recommendations")
        assert recommendations is not None
        
        # Step 6: Verify complete analysis workflow
        cursor.execute("SELECT * FROM test_models WHERE name = ?", (model_data['name'],))
        stored_model = cursor.fetchone()
        assert stored_model is not None
        assert stored_model[1] == model_data['name']  # name column
        assert stored_model[2] == model_data['type']  # type column
    
    def test_report_generation_workflow(self, db_with_sample_data, mock_gemini_api_manager):
        """Test complete report generation workflow."""
        cursor = db_with_sample_data.cursor()
        api_manager = mock_gemini_api_manager
        
        # Step 1: Get model data for report
        cursor.execute("SELECT name, type, bias_score FROM test_models")
        models = cursor.fetchall()
        assert len(models) > 0
        
        # Step 2: Generate executive summary
        summary_prompt = f"Generate executive summary for {len(models)} AI models"
        executive_summary = api_manager.generate_content(summary_prompt)
        assert executive_summary is not None
        
        # Step 3: Generate detailed analysis for each model
        detailed_analyses = []
        for model in models[:2]:  # Test with first 2 models
            analysis_prompt = f"Detailed bias analysis for {model[0]} ({model[1]}) with score {model[2]}"
            analysis = api_manager.generate_content(analysis_prompt)
            detailed_analyses.append(analysis)
        
        assert len(detailed_analyses) == 2
        assert all(analysis is not None for analysis in detailed_analyses)
        
        # Step 4: Generate recommendations
        recommendations = api_manager.generate_content("Provide actionable bias mitigation recommendations")
        assert recommendations is not None
        
        # Step 5: Simulate report compilation
        report_data = {
            'executive_summary': executive_summary,
            'detailed_analyses': detailed_analyses,
            'recommendations': recommendations,
            'model_count': len(models)
        }
        
        # Verify complete report workflow
        assert report_data['model_count'] > 0
        assert report_data['executive_summary'] is not None
        assert len(report_data['detailed_analyses']) > 0


@pytest.mark.e2e
@pytest.mark.slow
class TestSystemPerformanceE2E:
    """End-to-end performance tests."""
    
    def test_high_volume_workflow(self, test_db, mock_gemini_api_manager, performance_timer):
        """Test system performance under high volume."""
        cursor = test_db.cursor()
        api_manager = mock_gemini_api_manager
        
        performance_timer.start()
        
        # Step 1: Create multiple users
        users = [(f"user_{i}", f"user_{i}@test.com") for i in range(50)]
        cursor.executemany("INSERT INTO test_users (username, email) VALUES (?, ?)", users)
        
        # Step 2: Generate multiple API calls
        responses = []
        for i in range(20):
            response = api_manager.generate_content(f"High volume test {i}")
            responses.append(response)
        
        # Step 3: Store multiple model analyses
        models = [(f"Model_{i}", "classification", 0.8 + (i * 0.01)) for i in range(30)]
        cursor.executemany("INSERT INTO test_models (name, type, bias_score) VALUES (?, ?, ?)", models)
        
        test_db.commit()
        performance_timer.stop()
        
        # Verify performance
        assert len(responses) == 20
        assert all(r is not None for r in responses)
        
        cursor.execute("SELECT COUNT(*) FROM test_users")
        user_count = cursor.fetchone()[0]
        assert user_count == 50
        
        cursor.execute("SELECT COUNT(*) FROM test_models")
        model_count = cursor.fetchone()[0]
        assert model_count == 30
        
        # Performance should be reasonable
        assert performance_timer.elapsed < 5.0
    
    def test_error_recovery_workflow(self, test_db, gemini_config_test):
        """Test system error recovery in end-to-end scenario."""
        cursor = test_db.cursor()
        
        # Step 1: Simulate API failure
        with patch('config.gemini_config.genai.Client') as mock_client_class:
            mock_client = Mock()
            mock_client.models.generate_content.side_effect = [
                Exception("API temporarily unavailable"),
                Exception("Rate limit exceeded"),
                Mock(text="Recovery successful")
            ]
            mock_client_class.return_value = mock_client
            
            api_manager = GeminiAPIManager(gemini_config_test)
            
            # Step 2: Attempt API call with retries
            response = api_manager.generate_content("Test error recovery")
            
            # Should succeed after retries
            assert response == "Recovery successful"
            assert mock_client.models.generate_content.call_count == 3
        
        # Step 3: Verify database operations still work
        cursor.execute("INSERT INTO test_users (username, email) VALUES (?, ?)", ("recovery_user", "recovery@test.com"))
        test_db.commit()
        
        cursor.execute("SELECT username FROM test_users WHERE username = ?", ("recovery_user",))
        result = cursor.fetchone()
        assert result[0] == "recovery_user"


@pytest.mark.e2e
class TestSystemIntegrationE2E:
    """End-to-end system integration tests."""
    
    def test_full_system_integration(self, temp_dir):
        """Test complete system integration from setup to operation."""
        # Step 1: Setup environment
        env_file = temp_dir / ".env"
        env_file.write_text("GEMINI_API_KEY=test-integration-key\nTESTING=true")
        
        db_file = temp_dir / "integration.db"
        
        # Step 2: Initialize database
        success = setup_database(str(db_file))
        assert success
        
        # Step 3: Test configuration loading
        with patch.dict(os.environ, {'GEMINI_API_KEY': 'test-integration-key'}):
            from config.env_config import EnvironmentConfig
            env_config = EnvironmentConfig(str(env_file))
            
            validation = env_config.validate_required()
            assert validation['valid']
        
        # Step 4: Test API integration
        with patch('config.gemini_config.genai.Client') as mock_client_class:
            mock_client = Mock()
            mock_client.models.generate_content.return_value = Mock(text="Integration test success")
            mock_client_class.return_value = mock_client
            
            api_manager = GeminiAPIManager()
            response = api_manager.generate_content("Integration test")
            assert response == "Integration test success"
        
        # Step 5: Test database integration
        import sqlite3
        conn = sqlite3.connect(str(db_file))
        cursor = conn.cursor()
        
        cursor.execute("INSERT INTO user_profiles (username, email, full_name) VALUES (?, ?, ?)",
                      ("integration_user", "integration@test.com", "Integration Test User"))
        conn.commit()
        
        cursor.execute("SELECT username FROM user_profiles WHERE email = ?", ("integration@test.com",))
        result = cursor.fetchone()
        assert result[0] == "integration_user"
        
        conn.close()
        
        # Step 6: Verify all components work together
        assert env_file.exists()
        assert db_file.exists()
        assert validation['valid']
        assert response is not None
