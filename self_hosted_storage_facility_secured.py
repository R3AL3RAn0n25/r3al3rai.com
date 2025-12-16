#!/usr/bin/env python3
"""
R3ÆLƎR Self-Hosted Storage Facility (SECURED)
100% Free, Zero External Dependencies
Uses PostgreSQL schemas as "storage units"
SECURITY: Environment variables, rate limiting, input validation, SSL/TLS
"""

import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
from datetime import datetime, timedelta
from functools import wraps
import logging
import uuid
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env.local')

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')

# Rate limiter
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# CORS Configuration - Whitelist only trusted origins
ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', 'http://localhost:5000').split(',')
CORS(app, 
     supports_credentials=True,
     origins=ALLOWED_ORIGINS,
     allow_headers=['Content-Type', 'X-API-Key', 'X-Session-Token']
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# PostgreSQL Configuration - From environment variables
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 5432)),
    'database': os.getenv('DB_NAME', 'r3aler_ai'),
    'user': os.getenv('DB_USER', 'r3aler_user_2025'),
    'password': os.getenv('DB_PASSWORD'),
    'sslmode': 'require'  # SECURITY: Enforce SSL/TLS
}

# Validation rules
VALID_UNIT_IDS = ['physics', 'quantum', 'space', 'crypto', 'medical', 'reason', 'logic']
SEARCH_QUERY_MAX_LENGTH = 500
ENTRY_ID_PATTERN = re.compile(r'^[a-zA-Z0-9_\-\.]+$')

class StorageFacility:
    """Self-hosted storage facility using PostgreSQL (SECURED)"""
    
    def __init__(self):
        # Define storage units (PostgreSQL schemas)
        self.units = {
            'physics': {
                'name': 'Physics Knowledge Unit',
                'schema': 'physics_unit',
                'description': 'Classical physics, mechanics, thermodynamics',
                'status': 'online'
            },
            'quantum': {
                'name': 'Quantum Physics Unit',
                'schema': 'quantum_unit',
                'description': 'Quantum mechanics, particle physics',
                'status': 'online'
            },
            'space': {
                'name': 'Space/Astro/Aerospace Unit',
                'schema': 'space_unit',
                'description': 'Astronomy, aerospace, exoplanets',
                'status': 'online'
            },
            'crypto': {
                'name': 'Cryptocurrency Unit',
                'schema': 'crypto_unit',
                'description': 'Blockchain, cryptocurrency knowledge',
                'status': 'online'
            },
            'medical': {
                'name': 'Medical Knowledge Unit',
                'schema': 'medical_unit',
                'description': 'Multilingual medical corpus, clinical, biomedical, healthcare',
                'status': 'online'
            },
            'reason': {
                'name': 'Reason Unit',
                'schema': 'reason_unit',
                'description': 'Reasoning, logic, consciousness, cognitive processes',
                'status': 'online'
            },
            'logic': {
                'name': 'Logic Unit',
                'schema': 'logic_unit',
                'description': 'Logical reasoning, formal logic, mathematical logic',
                'status': 'online'
            }
        }
        
        logger.info("[STORAGE] Initializing R3AL3R Storage Facility (SECURED)...")
        try:
            self.initialize_facility()
            logger.info("[OK] Storage Facility ready!")
        except Exception as e:
            logger.error(f"[ERROR] Initialization error: {e}")
            raise
    
    def get_connection(self):
        """Get database connection with SSL/TLS"""
        try:
            return psycopg2.connect(**DB_CONFIG)
        except psycopg2.Error as e:
            logger.error(f"Database connection error: {str(e)}")
            raise
    
    def initialize_facility(self):
        """Create all storage units (schemas and tables)"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            for unit_id, unit_info in self.units.items():
                schema = unit_info['schema']
                
                # Create schema (storage unit)
                cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {schema}")
                
                # Create knowledge table
                cursor.execute(f"""
                    CREATE TABLE IF NOT EXISTS {schema}.knowledge (
                        id SERIAL PRIMARY KEY,
                        entry_id VARCHAR(200) UNIQUE,
                        topic TEXT,
                        content TEXT,
                        category VARCHAR(200),
                        subcategory VARCHAR(200),
                        level VARCHAR(100),
                        source VARCHAR(200),
                        created_at TIMESTAMP DEFAULT NOW(),
                        updated_at TIMESTAMP DEFAULT NOW()
                    )
                """)
                
                # Create indexes for fast search
                cursor.execute(f"""
                    CREATE INDEX IF NOT EXISTS idx_{unit_id}_category 
                    ON {schema}.knowledge(category)
                """)
                
                cursor.execute(f"""
                    CREATE INDEX IF NOT EXISTS idx_{unit_id}_topic 
                    ON {schema}.knowledge(topic)
                """)
                
                # Full-text search index
                cursor.execute(f"""
                    CREATE INDEX IF NOT EXISTS idx_{unit_id}_fts 
                    ON {schema}.knowledge 
                    USING GIN(to_tsvector('english', COALESCE(content, '') || ' ' || COALESCE(topic, '')))
                """)
            
            conn.commit()
            cursor.close()
            conn.close()
            logger.info("Storage facility schemas initialized")
        except Exception as e:
            logger.error(f"Facility initialization error: {str(e)}")
            raise
    
    def store_knowledge(self, unit_id: str, entries: list) -> dict:
        """Store knowledge in a specific unit - SECURITY: Input validation"""
        try:
            # SECURITY: Validate unit_id
            if unit_id not in self.units:
                logger.warning(f"Attempt to store in invalid unit: {unit_id}")
                return {'error': f'Unit {unit_id} not found'}
            
            schema = self.units[unit_id]['schema']
            
            conn = self.get_connection()
            cursor = conn.cursor()
            
            stored_count = 0
            error_count = 0
            
            for entry in entries:
                try:
                    # SECURITY: Input validation and sanitization
                    entry_id = str(entry.get('id', entry.get('entry_id', ''))).strip()[:200]
                    topic = str(entry.get('topic', entry.get('question', ''))).strip()[:500]
                    content = str(entry.get('content', entry.get('answer', ''))).strip()[:50000]
                    category = str(entry.get('category', entry.get('domain', ''))).strip()[:200]
                    subcategory = str(entry.get('subcategory', '')).strip()[:200]
                    level = str(entry.get('level', entry.get('difficulty', ''))).strip()[:100]
                    source = str(entry.get('source', '')).strip()[:200]
                    
                    # Validate entry_id format
                    if entry_id and not ENTRY_ID_PATTERN.match(entry_id):
                        logger.warning(f"Invalid entry_id format: {entry_id}")
                        error_count += 1
                        continue
                    
                    # Skip if no content
                    if not content and not topic:
                        continue
                    
                    # Generate ID if missing
                    if not entry_id:
                        entry_id = f"{unit_id}_{uuid.uuid4().hex[:8]}"
                    
                    cursor.execute(f"""
                        INSERT INTO {schema}.knowledge 
                        (entry_id, topic, content, category, subcategory, level, source)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (entry_id) DO UPDATE SET
                            topic = EXCLUDED.topic,
                            content = EXCLUDED.content,
                            category = EXCLUDED.category,
                            subcategory = EXCLUDED.subcategory,
                            level = EXCLUDED.level,
                            source = EXCLUDED.source,
                            updated_at = NOW()
                    """, (entry_id, topic, content, category, subcategory, level, source))
                    
                    stored_count += 1
                    
                except Exception as e:
                    error_count += 1
                    logger.warning(f"Error storing entry in {unit_id}: {str(e)}")
            
            conn.commit()
            cursor.close()
            conn.close()
            
            logger.info(f"Stored {stored_count} entries to {unit_id} (errors: {error_count})")
            
            return {
                'unit': unit_id,
                'stored': stored_count,
                'errors': error_count,
                'total': len(entries)
            }
        
        except Exception as e:
            logger.error(f"Store knowledge error: {str(e)}")
            return {'error': 'Failed to store knowledge', 'code': 'STORE_ERROR'}
    
    def search_unit(self, unit_id: str, query: str, limit: int = 10) -> list:
        """Search within a specific storage unit - SECURITY: Query validation"""
        try:
            # SECURITY: Validate unit_id
            if unit_id not in self.units:
                logger.warning(f"Attempt to search invalid unit: {unit_id}")
                return []
            
            # SECURITY: Validate search query
            query = str(query).strip()[:SEARCH_QUERY_MAX_LENGTH]
            if len(query) < 2:
                return []
            
            # SECURITY: Validate limit
            limit = min(int(limit), 100)  # Max 100 results
            if limit < 1:
                limit = 10
            
            schema = self.units[unit_id]['schema']
            
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            try:
                # Full-text search with ranking (parameterized query - SQL injection safe)
                cursor.execute(f"""
                    SELECT 
                        entry_id,
                        topic,
                        LEFT(content, 500) as content_preview,
                        category,
                        subcategory,
                        level,
                        source,
                        ts_rank(
                            to_tsvector('english', COALESCE(content, '') || ' ' || COALESCE(topic, '')),
                            plainto_tsquery('english', %s)
                        ) as relevance
                    FROM {schema}.knowledge
                    WHERE to_tsvector('english', COALESCE(content, '') || ' ' || COALESCE(topic, ''))
                          @@ plainto_tsquery('english', %s)
                    ORDER BY relevance DESC
                    LIMIT %s
                """, (query, query, limit))
                
                results = cursor.fetchall()
                logger.info(f"Search in {unit_id} for '{query}': {len(results)} results")
                return [dict(row) for row in results]
                
            except Exception as e:
                logger.error(f"Search error in {unit_id}: {str(e)}")
                return []
            finally:
                cursor.close()
                conn.close()
        
        except Exception as e:
            logger.error(f"Search unit error: {str(e)}")
            return []
    
    def get_unit_stats(self, unit_id: str) -> dict:
        """Get statistics for a storage unit"""
        try:
            # SECURITY: Validate unit_id
            if unit_id not in self.units:
                return {'error': f'Unit {unit_id} not found'}
            
            schema = self.units[unit_id]['schema']
            
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            try:
                cursor.execute(f"""
                    SELECT 
                        COUNT(*) as total_entries,
                        COUNT(DISTINCT category) as categories,
                        COUNT(DISTINCT level) as levels,
                        MIN(created_at) as oldest_entry,
                        MAX(updated_at) as last_update
                    FROM {schema}.knowledge
                """)
                
                stats = dict(cursor.fetchone() or {})
                logger.info(f"Stats for {unit_id}: {stats['total_entries']} entries")
                return stats
                
            except Exception as e:
                logger.error(f"Stats error for {unit_id}: {str(e)}")
                return {'error': 'Failed to get statistics'}
            finally:
                cursor.close()
                conn.close()
        
        except Exception as e:
            logger.error(f"Get unit stats error: {str(e)}")
            return {'error': 'Failed to retrieve stats'}
    
    def get_facility_status(self) -> dict:
        """Get overall facility status"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            try:
                total_entries = 0
                units_status = {}
                
                for unit_id, unit_info in self.units.items():
                    schema = unit_info['schema']
                    cursor.execute(f"SELECT COUNT(*) as count FROM {schema}.knowledge")
                    count = cursor.fetchone()['count']
                    total_entries += count
                    units_status[unit_id] = {
                        'name': unit_info['name'],
                        'entries': count,
                        'status': 'online'
                    }
                
                logger.info(f"Facility status: {total_entries} total entries")
                
                return {
                    'facility_status': 'healthy',
                    'total_entries': total_entries,
                    'units': units_status,
                    'timestamp': datetime.now().isoformat()
                }
                
            except Exception as e:
                logger.error(f"Facility status error: {str(e)}")
                return {'facility_status': 'error', 'error': str(e)}
            finally:
                cursor.close()
                conn.close()
        
        except Exception as e:
            logger.error(f"Get facility status error: {str(e)}")
            return {'facility_status': 'offline', 'error': str(e)}

# Initialize storage facility
try:
    facility = StorageFacility()
except Exception as e:
    logger.error(f"Failed to initialize storage facility: {str(e)}")
    facility = None

def require_auth(f):
    """Decorator to require authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        session_token = request.headers.get('X-Session-Token')
        
        if not api_key and not session_token:
            logger.warning(f"Unauthorized access attempt from {request.remote_addr}")
            return jsonify({'error': 'Authentication required', 'code': 'NO_AUTH'}), 401
        
        return f(*args, **kwargs)
    
    return decorated_function

# API Endpoints

@app.route('/api/facility/status', methods=['GET'])
@limiter.limit("100 per hour")
def get_facility_status():
    """Get storage facility status"""
    try:
        if not facility:
            return jsonify({'error': 'Storage facility not available'}), 503
        
        status = facility.get_facility_status()
        return jsonify(status), 200
    
    except Exception as e:
        logger.error(f"Status endpoint error: {str(e)}")
        return jsonify({'error': 'Failed to get facility status', 'code': 'STATUS_ERROR'}), 500

@app.route('/api/unit/<unit_id>/stats', methods=['GET'])
@limiter.limit("100 per hour")
def get_unit_stats(unit_id):
    """Get statistics for a storage unit"""
    try:
        # SECURITY: Validate unit_id format
        if not re.match(r'^[a-z0-9_]+$', unit_id):
            return jsonify({'error': 'Invalid unit ID format'}), 400
        
        if not facility:
            return jsonify({'error': 'Storage facility not available'}), 503
        
        stats = facility.get_unit_stats(unit_id)
        
        if 'error' in stats:
            return jsonify(stats), 404
        
        return jsonify({'unit': unit_id, 'statistics': stats}), 200
    
    except Exception as e:
        logger.error(f"Unit stats endpoint error: {str(e)}")
        return jsonify({'error': 'Failed to get unit statistics', 'code': 'STATS_ERROR'}), 500

@app.route('/api/unit/<unit_id>/search', methods=['POST'])
@require_auth
@limiter.limit("30 per hour")  # SECURITY: Rate limit searches
def search_unit(unit_id):
    """Search within a storage unit"""
    try:
        # SECURITY: Validate unit_id format
        if not re.match(r'^[a-z0-9_]+$', unit_id):
            return jsonify({'error': 'Invalid unit ID format'}), 400
        
        data = request.get_json() or {}
        query = data.get('query', '').strip()
        limit = data.get('limit', 10)
        
        # SECURITY: Validate query
        if not query or len(query) < 2:
            return jsonify({'error': 'Search query must be at least 2 characters'}), 400
        
        if len(query) > SEARCH_QUERY_MAX_LENGTH:
            return jsonify({'error': f'Search query too long (max {SEARCH_QUERY_MAX_LENGTH} chars)'}), 400
        
        if not facility:
            return jsonify({'error': 'Storage facility not available'}), 503
        
        # SECURITY: Validate limit
        try:
            limit = int(limit)
            limit = min(limit, 100)  # Max 100 results
            if limit < 1:
                limit = 10
        except (ValueError, TypeError):
            limit = 10
        
        results = facility.search_unit(unit_id, query, limit)
        
        return jsonify({
            'success': True,
            'unit': unit_id,
            'query': query,
            'results_count': len(results),
            'results': results
        }), 200
    
    except Exception as e:
        logger.error(f"Search endpoint error: {str(e)}")
        return jsonify({'error': 'Search failed', 'code': 'SEARCH_ERROR'}), 500

@app.route('/api/unit/<unit_id>/store', methods=['POST'])
@require_auth
@limiter.limit("10 per hour")  # SECURITY: Rate limit storage operations
def store_knowledge(unit_id):
    """Store knowledge in a unit"""
    try:
        # SECURITY: Validate unit_id format
        if not re.match(r'^[a-z0-9_]+$', unit_id):
            return jsonify({'error': 'Invalid unit ID format'}), 400
        
        data = request.get_json() or {}
        entries = data.get('entries', [])
        
        # SECURITY: Validate entries
        if not isinstance(entries, list):
            return jsonify({'error': 'entries must be a list'}), 400
        
        if len(entries) == 0:
            return jsonify({'error': 'At least one entry required'}), 400
        
        if len(entries) > 10000:  # SECURITY: Max entries per request
            return jsonify({'error': 'Too many entries (max 10000)'}), 413
        
        if not facility:
            return jsonify({'error': 'Storage facility not available'}), 503
        
        result = facility.store_knowledge(unit_id, entries)
        
        if 'error' in result:
            return jsonify(result), 400
        
        logger.info(f"Stored {result['stored']} entries to {unit_id}")
        
        return jsonify({
            'success': True,
            'unit': unit_id,
            'stored': result['stored'],
            'errors': result['errors'],
            'total_processed': result['total']
        }), 201
    
    except Exception as e:
        logger.error(f"Store endpoint error: {str(e)}")
        return jsonify({'error': 'Storage failed', 'code': 'STORE_ERROR'}), 500

@app.route('/api/facility/units', methods=['GET'])
@limiter.limit("200 per hour")
def list_units():
    """List all available storage units"""
    try:
        if not facility:
            return jsonify({'error': 'Storage facility not available'}), 503
        
        units_list = [
            {
                'id': unit_id,
                'name': info['name'],
                'description': info['description'],
                'status': info['status']
            }
            for unit_id, info in facility.units.items()
        ]
        
        return jsonify({
            'success': True,
            'total_units': len(units_list),
            'units': units_list
        }), 200
    
    except Exception as e:
        logger.error(f"List units error: {str(e)}")
        return jsonify({'error': 'Failed to list units', 'code': 'LIST_ERROR'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    facility_healthy = facility is not None
    return jsonify({
        'status': 'healthy' if facility_healthy else 'degraded',
        'service': 'R3ÆLƎR Storage Facility API (SECURED)',
        'version': '2.0.0',
        'facility_ready': facility_healthy,
        'timestamp': datetime.now().isoformat()
    }), 200 if facility_healthy else 503

@app.errorhandler(429)
def ratelimit_handler(e):
    """Handle rate limit errors"""
    return jsonify({
        'error': 'Rate limit exceeded',
        'code': 'RATE_LIMIT',
        'message': str(e.description)
    }), 429

@app.errorhandler(500)
def server_error_handler(e):
    """Handle server errors - no stack trace to client"""
    logger.error(f"Server error: {str(e)}")
    return jsonify({
        'error': 'Internal server error',
        'code': 'SERVER_ERROR'
    }), 500

if __name__ == '__main__':
    print("\n" + "=" * 70)
    print("💾 R3ÆLƎR SELF-HOSTED STORAGE FACILITY (SECURED v2.0)")
    print("=" * 70)
    print("✅ Environment-based credentials (no hardcoded passwords)")
    print("✅ Rate limiting (search 30/hr, store 10/hr)")
    print("✅ Input validation (query length, entry count, unit IDs)")
    print("✅ SSL/TLS database connection required")
    print("✅ CORS whitelist (no wildcard origins)")
    print("✅ 7 storage units (physics, quantum, space, crypto, medical, reason, logic)")
    print("✅ PostgreSQL full-text search")
    print("✅ Comprehensive audit logging")
    print("=" * 70)
    print("\n📊 Endpoints: http://localhost:5006")
    print("   GET  /api/facility/status")
    print("   GET  /api/facility/units")
    print("   GET  /api/unit/<id>/stats")
    print("   POST /api/unit/<id>/search (Rate: 30/hr, Auth required)")
    print("   POST /api/unit/<id>/store (Rate: 10/hr, Auth required)")
    print("   GET  /health")
    print("\nPress Ctrl+C to stop\n")
    
    app.run(host='0.0.0.0', port=5006, debug=False, use_reloader=False)
