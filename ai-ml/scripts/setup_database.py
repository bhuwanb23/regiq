#!/usr/bin/env python3
"""
REGIQ AI/ML Database Setup Script
Creates SQLite database structure and initial schema.
"""

import sqlite3
import os
from pathlib import Path
from datetime import datetime
from typing import List, Dict

def create_database_schema() -> Dict[str, str]:
    """Define the database schema for REGIQ AI/ML."""
    
    schema = {
        # User management tables
        "user_profiles": """
            CREATE TABLE IF NOT EXISTS user_profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                full_name VARCHAR(100),
                role VARCHAR(20) DEFAULT 'user',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT 1
            )
        """,
        
        "authentication_logs": """
            CREATE TABLE IF NOT EXISTS authentication_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                action VARCHAR(20) NOT NULL,
                ip_address VARCHAR(45),
                user_agent TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                success BOOLEAN DEFAULT 1,
                FOREIGN KEY (user_id) REFERENCES user_profiles (id)
            )
        """,
        
        # Regulatory documents and analysis
        "regulatory_documents": """
            CREATE TABLE IF NOT EXISTS regulatory_documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title VARCHAR(500) NOT NULL,
                source VARCHAR(100),
                document_type VARCHAR(50),
                url TEXT,
                content TEXT,
                summary TEXT,
                key_points TEXT,
                effective_date DATE,
                deadline_date DATE,
                risk_level VARCHAR(20),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """,
        
        "compliance_alerts": """
            CREATE TABLE IF NOT EXISTS compliance_alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                document_id INTEGER,
                alert_type VARCHAR(50),
                title VARCHAR(200),
                message TEXT,
                severity VARCHAR(20),
                status VARCHAR(20) DEFAULT 'active',
                due_date DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                resolved_at TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES user_profiles (id),
                FOREIGN KEY (document_id) REFERENCES regulatory_documents (id)
            )
        """,
        
        # Model bias analysis
        "model_bias_analysis": """
            CREATE TABLE IF NOT EXISTS model_bias_analysis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                model_name VARCHAR(100),
                model_type VARCHAR(50),
                dataset_name VARCHAR(100),
                bias_score REAL,
                demographic_parity REAL,
                equalized_odds REAL,
                calibration_error REAL,
                individual_fairness REAL,
                flagged_attributes TEXT,
                top_features TEXT,
                recommendations TEXT,
                analysis_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES user_profiles (id)
            )
        """,
        
        "regulatory_compliance": """
            CREATE TABLE IF NOT EXISTS regulatory_compliance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                model_analysis_id INTEGER,
                regulation_name VARCHAR(100),
                compliance_status VARCHAR(20),
                compliance_score REAL,
                gaps_identified TEXT,
                remediation_steps TEXT,
                assessment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (model_analysis_id) REFERENCES model_bias_analysis (id)
            )
        """,
        
        # Risk simulation results
        "risk_simulation_results": """
            CREATE TABLE IF NOT EXISTS risk_simulation_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                simulation_name VARCHAR(100),
                regulation_context TEXT,
                affected_models TEXT,
                noncompliance_probability REAL,
                confidence_interval_lower REAL,
                confidence_interval_upper REAL,
                risk_level VARCHAR(20),
                financial_impact_min REAL,
                financial_impact_max REAL,
                remediation_cost REAL,
                business_disruption_days INTEGER,
                recommendations TEXT,
                mitigation_timeline TEXT,
                simulation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES user_profiles (id)
            )
        """,
        
        # Generated reports
        "generated_reports": """
            CREATE TABLE IF NOT EXISTS generated_reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                report_type VARCHAR(50),
                title VARCHAR(200),
                content TEXT,
                file_path VARCHAR(500),
                format VARCHAR(10),
                status VARCHAR(20) DEFAULT 'generated',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                downloaded_at TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES user_profiles (id)
            )
        """,
        
        # System audit logs
        "system_audit_logs": """
            CREATE TABLE IF NOT EXISTS system_audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                action VARCHAR(100),
                resource_type VARCHAR(50),
                resource_id INTEGER,
                details TEXT,
                ip_address VARCHAR(45),
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES user_profiles (id)
            )
        """,
        
        # Configuration and settings
        "system_settings": """
            CREATE TABLE IF NOT EXISTS system_settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                setting_key VARCHAR(100) UNIQUE NOT NULL,
                setting_value TEXT,
                description TEXT,
                updated_by INTEGER,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (updated_by) REFERENCES user_profiles (id)
            )
        """
    }
    
    return schema

def create_indexes() -> List[str]:
    """Define database indexes for better performance."""
    
    indexes = [
        # User profiles indexes
        "CREATE INDEX IF NOT EXISTS idx_user_profiles_email ON user_profiles(email)",
        "CREATE INDEX IF NOT EXISTS idx_user_profiles_username ON user_profiles(username)",
        
        # Authentication logs indexes
        "CREATE INDEX IF NOT EXISTS idx_auth_logs_user_id ON authentication_logs(user_id)",
        "CREATE INDEX IF NOT EXISTS idx_auth_logs_timestamp ON authentication_logs(timestamp)",
        
        # Regulatory documents indexes
        "CREATE INDEX IF NOT EXISTS idx_regulatory_docs_source ON regulatory_documents(source)",
        "CREATE INDEX IF NOT EXISTS idx_regulatory_docs_type ON regulatory_documents(document_type)",
        "CREATE INDEX IF NOT EXISTS idx_regulatory_docs_effective_date ON regulatory_documents(effective_date)",
        "CREATE INDEX IF NOT EXISTS idx_regulatory_docs_deadline ON regulatory_documents(deadline_date)",
        
        # Compliance alerts indexes
        "CREATE INDEX IF NOT EXISTS idx_alerts_user_id ON compliance_alerts(user_id)",
        "CREATE INDEX IF NOT EXISTS idx_alerts_status ON compliance_alerts(status)",
        "CREATE INDEX IF NOT EXISTS idx_alerts_due_date ON compliance_alerts(due_date)",
        
        # Model bias analysis indexes
        "CREATE INDEX IF NOT EXISTS idx_bias_analysis_user_id ON model_bias_analysis(user_id)",
        "CREATE INDEX IF NOT EXISTS idx_bias_analysis_model_name ON model_bias_analysis(model_name)",
        "CREATE INDEX IF NOT EXISTS idx_bias_analysis_date ON model_bias_analysis(analysis_date)",
        
        # Risk simulation indexes
        "CREATE INDEX IF NOT EXISTS idx_risk_sim_user_id ON risk_simulation_results(user_id)",
        "CREATE INDEX IF NOT EXISTS idx_risk_sim_date ON risk_simulation_results(simulation_date)",
        
        # Generated reports indexes
        "CREATE INDEX IF NOT EXISTS idx_reports_user_id ON generated_reports(user_id)",
        "CREATE INDEX IF NOT EXISTS idx_reports_type ON generated_reports(report_type)",
        "CREATE INDEX IF NOT EXISTS idx_reports_created_at ON generated_reports(created_at)",
        
        # System audit logs indexes
        "CREATE INDEX IF NOT EXISTS idx_audit_logs_user_id ON system_audit_logs(user_id)",
        "CREATE INDEX IF NOT EXISTS idx_audit_logs_action ON system_audit_logs(action)",
        "CREATE INDEX IF NOT EXISTS idx_audit_logs_timestamp ON system_audit_logs(timestamp)",
    ]
    
    return indexes

def insert_initial_data(cursor: sqlite3.Cursor) -> None:
    """Insert initial system data."""
    
    # Insert default system settings
    settings = [
        ('app_version', '1.0.0', 'Current application version'),
        ('max_file_upload_size', '100', 'Maximum file upload size in MB'),
        ('default_bias_threshold', '0.8', 'Default bias score threshold'),
        ('simulation_iterations', '10000', 'Default Monte Carlo iterations'),
        ('report_retention_days', '365', 'Report retention period in days'),
    ]
    
    cursor.executemany(
        "INSERT OR IGNORE INTO system_settings (setting_key, setting_value, description) VALUES (?, ?, ?)",
        settings
    )
    
    # Insert default admin user (for development)
    cursor.execute("""
        INSERT OR IGNORE INTO user_profiles (username, email, full_name, role) 
        VALUES ('admin', 'admin@regiq.com', 'System Administrator', 'admin')
    """)

def setup_database(db_path: str = "data/regiq_local.db") -> bool:
    """Set up the complete database structure."""
    
    print("🗄️  Setting up REGIQ AI/ML Database")
    print("="*50)
    
    # Ensure data directory exists
    db_file = Path(db_path)
    db_file.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print(f"📁 Database file: {db_path}")
        
        # Create tables
        schema = create_database_schema()
        print(f"\n📋 Creating {len(schema)} tables...")
        
        for table_name, create_sql in schema.items():
            try:
                cursor.execute(create_sql)
                print(f"✅ {table_name:<25} - Created")
            except Exception as e:
                print(f"❌ {table_name:<25} - Error: {e}")
                return False
        
        # Create indexes
        indexes = create_indexes()
        print(f"\n🔍 Creating {len(indexes)} indexes...")
        
        for i, index_sql in enumerate(indexes, 1):
            try:
                cursor.execute(index_sql)
                print(f"✅ Index {i:<3} - Created")
            except Exception as e:
                print(f"❌ Index {i:<3} - Error: {e}")
        
        # Insert initial data
        print(f"\n📊 Inserting initial data...")
        insert_initial_data(cursor)
        print("✅ Initial data inserted")
        
        # Commit changes
        conn.commit()
        
        # Test database connection
        cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'")
        table_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT setting_value FROM system_settings WHERE setting_key='app_version'")
        version = cursor.fetchone()
        
        conn.close()
        
        print(f"\n🎉 Database setup complete!")
        print(f"   📊 Tables created: {table_count}")
        print(f"   🔢 App version: {version[0] if version else 'Unknown'}")
        print(f"   📁 Database location: {os.path.abspath(db_path)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        return False

def test_database_connection(db_path: str = "data/regiq_local.db") -> bool:
    """Test database connection and basic operations."""
    
    print(f"\n🧪 Testing database connection...")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Test basic query
        cursor.execute("SELECT COUNT(*) FROM user_profiles")
        user_count = cursor.fetchone()[0]
        
        # Test insert/update/delete
        test_user = f"test_user_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        cursor.execute(
            "INSERT INTO user_profiles (username, email, full_name) VALUES (?, ?, ?)",
            (test_user, f"{test_user}@test.com", "Test User")
        )
        
        cursor.execute("SELECT id FROM user_profiles WHERE username = ?", (test_user,))
        test_id = cursor.fetchone()[0]
        
        cursor.execute("DELETE FROM user_profiles WHERE id = ?", (test_id,))
        
        conn.commit()
        conn.close()
        
        print(f"✅ Database connection test successful")
        print(f"   👥 Current users: {user_count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Database connection test failed: {e}")
        return False

def main():
    """Main database setup function."""
    print("🚀 REGIQ AI/ML Database Setup")
    print("="*60)
    
    # Setup database
    success = setup_database()
    
    if success:
        # Test connection
        test_success = test_database_connection()
        
        if test_success:
            print(f"\n✨ Database is ready for development!")
            print(f"   Next: Run 'python scripts/verify_installation.py' to verify environment")
        else:
            print(f"\n⚠️  Database created but connection test failed")
    else:
        print(f"\n❌ Database setup failed")

if __name__ == "__main__":
    main()
