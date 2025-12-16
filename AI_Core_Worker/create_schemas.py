#!/usr/bin/env python3
"""
R3ÆLƎR AI: Create BlackArch & User Units in PostgreSQL
Extends Storage Facility with tool metadata and user management
Preserves existing knowledge base units
"""

import psycopg2
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'r3aler_ai',
    'user': 'r3aler_user_2025',
    'password': 'postgres'
}

def create_schemas():
    """Create BlackArch and User schemas"""
    
    logger.info("=" * 70)
    logger.info("R3ÆLƎR AI: Creating BlackArch & User Units")
    logger.info("=" * 70)
    
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    try:
        # Create blackarch_unit schema
        logger.info("Creating blackarch_unit schema...")
        cursor.execute("CREATE SCHEMA IF NOT EXISTS blackarch_unit")
        
        # Create tools table
        logger.info("Creating blackarch_unit.tools table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS blackarch_unit.tools (
                id SERIAL PRIMARY KEY,
                tool_id VARCHAR(200) UNIQUE NOT NULL,
                name VARCHAR(200) NOT NULL,
                category VARCHAR(100),
                subcategory VARCHAR(100),
                description TEXT,
                usage_example TEXT,
                documentation_url TEXT,
                install_command TEXT,
                dependencies TEXT[],
                typical_use_cases TEXT,
                skill_level VARCHAR(50),
                estimated_size_mb INTEGER,
                license VARCHAR(100),
                legal_notes TEXT,
                ethical_guidelines TEXT,
                official_repo_url TEXT,
                last_updated DATE,
                created_at TIMESTAMP DEFAULT NOW()
            )
        """)
        
        # Create indexes
        logger.info("Creating indexes for blackarch_unit.tools...")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_ba_category ON blackarch_unit.tools(category, subcategory)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_ba_skill ON blackarch_unit.tools(skill_level)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_ba_name ON blackarch_unit.tools(name)")
        
        # Full-text search index
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_ba_fts ON blackarch_unit.tools 
            USING GIN(to_tsvector('english', 
                COALESCE(name, '') || ' ' ||
                COALESCE(description, '') || ' ' || 
                COALESCE(usage_example, '') || ' ' ||
                COALESCE(typical_use_cases, '')))
        """)
        
        # Create user_unit schema
        logger.info("Creating user_unit schema...")
        cursor.execute("CREATE SCHEMA IF NOT EXISTS user_unit")
        
        # User profiles table
        logger.info("Creating user_unit.profiles table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_unit.profiles (
                user_id SERIAL PRIMARY KEY,
                username VARCHAR(100) UNIQUE NOT NULL,
                email VARCHAR(200) UNIQUE,
                password_hash VARCHAR(255),
                subscription_tier VARCHAR(50) DEFAULT 'free',
                api_key VARCHAR(64) UNIQUE,
                created_at TIMESTAMP DEFAULT NOW(),
                last_login TIMESTAMP,
                is_active BOOLEAN DEFAULT TRUE,
                preferences JSONB DEFAULT '{}'::jsonb
            )
        """)
        
        # User tool preferences
        logger.info("Creating user_unit.tool_preferences table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_unit.tool_preferences (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES user_unit.profiles(user_id) ON DELETE CASCADE,
                tool_id VARCHAR(200),
                is_pinned BOOLEAN DEFAULT FALSE,
                is_downloaded BOOLEAN DEFAULT FALSE,
                download_path TEXT,
                last_used TIMESTAMP,
                usage_count INTEGER DEFAULT 0,
                custom_config JSONB,
                UNIQUE(user_id, tool_id)
            )
        """)
        
        # User sessions
        logger.info("Creating user_unit.sessions table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_unit.sessions (
                session_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                user_id INTEGER REFERENCES user_unit.profiles(user_id) ON DELETE CASCADE,
                started_at TIMESTAMP DEFAULT NOW(),
                last_activity TIMESTAMP DEFAULT NOW(),
                expires_at TIMESTAMP,
                ip_address INET,
                user_agent TEXT
            )
        """)
        
        # Activity log
        logger.info("Creating user_unit.activity_log table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_unit.activity_log (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES user_unit.profiles(user_id) ON DELETE CASCADE,
                activity_type VARCHAR(100),
                activity_data JSONB,
                timestamp TIMESTAMP DEFAULT NOW()
            )
        """)
        
        # Create indexes for user tables
        logger.info("Creating indexes for user_unit tables...")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_email ON user_unit.profiles(email)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_api_key ON user_unit.profiles(api_key)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_subscription ON user_unit.profiles(subscription_tier)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_tool_pref_user ON user_unit.tool_preferences(user_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_session_user ON user_unit.sessions(user_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_activity_user ON user_unit.activity_log(user_id, timestamp)")
        
        # Grant permissions
        logger.info("Granting permissions...")
        cursor.execute("GRANT ALL PRIVILEGES ON SCHEMA blackarch_unit TO r3aler_user_2025")
        cursor.execute("GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA blackarch_unit TO r3aler_user_2025")
        cursor.execute("GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA blackarch_unit TO r3aler_user_2025")
        
        cursor.execute("GRANT ALL PRIVILEGES ON SCHEMA user_unit TO r3aler_user_2025")
        cursor.execute("GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA user_unit TO r3aler_user_2025")
        cursor.execute("GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA user_unit TO r3aler_user_2025")
        
        conn.commit()
        
        # Verify schema creation
        logger.info("\n" + "=" * 70)
        logger.info("✅ SCHEMA CREATION COMPLETE!")
        logger.info("=" * 70)
        
        # Show all units
        cursor.execute("""
            SELECT 
                schemaname,
                tablename,
                pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
            FROM pg_tables 
            WHERE schemaname IN ('physics_unit', 'quantum_unit', 'space_unit', 'crypto_unit', 'blackarch_unit', 'user_unit')
            ORDER BY schemaname, tablename
        """)
        
        logger.info("\nR3ÆLƎR AI Storage Facility Units:")
        for row in cursor.fetchall():
            logger.info(f"  {row[0]:20s}.{row[1]:30s} - {row[2]}")
        
        # Show knowledge counts (verify unchanged)
        logger.info("\n" + "=" * 70)
        logger.info("Knowledge Base Verification (Should be unchanged):")
        logger.info("=" * 70)
        
        knowledge_units = [
            ('physics_unit', 'knowledge'),
            ('quantum_unit', 'knowledge'),
            ('space_unit', 'knowledge'),
            ('crypto_unit', 'knowledge')
        ]
        
        for schema, table in knowledge_units:
            cursor.execute(f"SELECT COUNT(*) FROM {schema}.{table}")
            count = cursor.fetchone()[0]
            logger.info(f"  {schema:20s}: {count:6d} entries ✅")
        
        logger.info("\n" + "=" * 70)
        logger.info("🚀 Ready for BlackArch tools migration!")
        logger.info("   Run: python migrate_blackarch_to_storage.py")
        logger.info("=" * 70)
        
    except Exception as e:
        logger.error(f"❌ Error creating schemas: {e}")
        conn.rollback()
        raise
    
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    create_schemas()
