#!/usr/bin/env python3
"""
R3ÆLƎR AI: User Authentication & Management API (SECURED)
Handles user registration, login, sessions, and API keys
SECURITY: Environment variables for credentials, rate limiting, input validation
"""

import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import bcrypt
import secrets
import uuid
import re
from datetime import datetime, timedelta
from functools import wraps
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env.local')

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', secrets.token_hex(32))

# Rate limiter
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# CORS Configuration - Whitelist only trusted origins
ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', 'http://localhost:5000,http://127.0.0.1:5000').split(',')
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
    'password': os.getenv('R3AL3RAdmin816'),
    'sslmode': 'require'  # SECURITY: Enforce SSL/TLS
}

# Validation constants
USERNAME_PATTERN = re.compile(r'^[a-zA-Z0-9_-]{3,32}$')
EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
PASSWORD_MIN_LENGTH = 12
IP_WHITELIST = os.getenv('IP_WHITELIST', '127.0.0.1,192.168.1.0/24').split(',')

def validate_input(data, rules):
    """Validate input against rules - SECURITY: Comprehensive validation"""
    errors = {}
    for field, field_rules in rules.items():
        value = data.get(field, '').strip() if isinstance(data.get(field), str) else data.get(field)
        
        if 'required' in field_rules and (value == '' or value is None):
            errors[field] = f'{field} is required'
            continue
        
        if 'min_length' in field_rules and isinstance(value, str) and len(value) < field_rules['min_length']:
            errors[field] = f'{field} must be at least {field_rules["min_length"]} characters'
        
        if 'max_length' in field_rules and isinstance(value, str) and len(value) > field_rules['max_length']:
            errors[field] = f'{field} must be no more than {field_rules["max_length"]} characters'
        
        if 'pattern' in field_rules and isinstance(value, str):
            if not field_rules['pattern'].match(value):
                errors[field] = f'{field} format is invalid'
        
        if 'choices' in field_rules and value not in field_rules['choices']:
            errors[field] = f'{field} must be one of: {", ".join(field_rules["choices"])}'
    
    return errors

def get_connection():
    """Get database connection with SSL/TLS - SECURITY: Required encryption"""
    try:
        return psycopg2.connect(**DB_CONFIG)
    except psycopg2.Error as e:
        logger.error(f"Database connection error: {str(e)}")
        raise

def require_auth(f):
    """Decorator to require authentication - SECURITY: Strict auth checks"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        session_token = request.headers.get('X-Session-Token')
        
        if not api_key and not session_token:
            logger.warning(f"Unauthorized access attempt from {request.remote_addr}")
            return jsonify({'error': 'Authentication required', 'code': 'NO_AUTH'}), 401
        
        try:
            conn = get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            user = None
            
            # Try API key authentication
            if api_key:
                # SECURITY: Validate API key format (should be URL-safe token)
                if not (16 <= len(api_key) <= 256):
                    cursor.close()
                    conn.close()
                    logger.warning(f"Invalid API key format from {request.remote_addr}")
                    return jsonify({'error': 'Invalid authentication', 'code': 'INVALID_AUTH'}), 401
                
                cursor.execute("""
                    SELECT user_id, username, subscription_tier, is_active
                    FROM user_unit.profiles
                    WHERE api_key = %s AND is_active = TRUE
                """, (api_key,))
                user = cursor.fetchone()
            
            # Try session token authentication
            elif session_token:
                # SECURITY: Validate UUID format
                try:
                    uuid.UUID(session_token)
                except ValueError:
                    cursor.close()
                    conn.close()
                    logger.warning(f"Invalid session token format from {request.remote_addr}")
                    return jsonify({'error': 'Invalid authentication', 'code': 'INVALID_AUTH'}), 401
                
                cursor.execute("""
                    SELECT p.user_id, p.username, p.subscription_tier, p.is_active
                    FROM user_unit.profiles p
                    JOIN user_unit.sessions s ON p.user_id = s.user_id
                    WHERE s.session_id = %s::uuid 
                    AND s.expires_at > NOW()
                    AND p.is_active = TRUE
                """, (session_token,))
                user = cursor.fetchone()
                
                # Update last activity
                if user:
                    cursor.execute("""
                        UPDATE user_unit.sessions
                        SET last_activity = NOW()
                        WHERE session_id = %s::uuid
                    """, (session_token,))
                    conn.commit()
            
            cursor.close()
            conn.close()
            
            if not user:
                logger.warning(f"Failed authentication from {request.remote_addr}")
                return jsonify({'error': 'Invalid or expired credentials', 'code': 'INVALID_AUTH'}), 401
            
            # Attach user info to request
            request.current_user = dict(user)
            
            return f(*args, **kwargs)
        
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            return jsonify({'error': 'Authentication failed', 'code': 'AUTH_ERROR'}), 500
    
    return decorated_function

@app.route('/api/user/register', methods=['POST'])
@limiter.limit("5 per hour")  # SECURITY: Rate limit registration
def register_user():
    """Register a new user"""
    try:
        data = request.get_json() or {}
        
        # Input validation
        validation_rules = {
            'username': {'required': True, 'min_length': 3, 'max_length': 32, 'pattern': USERNAME_PATTERN},
            'email': {'required': True, 'pattern': EMAIL_PATTERN},
            'password': {'required': True, 'min_length': PASSWORD_MIN_LENGTH},
            'subscription_tier': {'choices': ['free', 'pro', 'enterprise']}
        }
        
        errors = validate_input(data, validation_rules)
        if errors:
            return jsonify({'error': 'Validation failed', 'details': errors}), 400
        
        username = data['username'].strip()
        email = data['email'].strip().lower()
        password = data['password']
        subscription_tier = data.get('subscription_tier', 'free')
        
        # Check password strength - SECURITY: Enforce strong passwords
        if not re.search(r'[A-Z]', password) or not re.search(r'[0-9]', password):
            return jsonify({'error': 'Password must contain uppercase letters and numbers'}), 400
        
        # Hash password with bcrypt - SECURITY: 12 salt rounds
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(12)).decode('utf-8')
        
        # Generate API key
        api_key = secrets.token_urlsafe(32)
        
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        try:
            # Check if username or email exists
            cursor.execute("""
                SELECT user_id FROM user_unit.profiles
                WHERE LOWER(username) = LOWER(%s) OR LOWER(email) = LOWER(%s)
            """, (username, email))
            
            if cursor.fetchone():
                logger.warning(f"Registration attempt with existing username/email: {username}")
                return jsonify({'error': 'Username or email already registered'}), 409
            
            # Create user
            cursor.execute("""
                INSERT INTO user_unit.profiles (
                    username, email, password_hash, subscription_tier, api_key,
                    created_at, is_active, preferences
                ) VALUES (%s, %s, %s, %s, %s, NOW(), TRUE, %s::jsonb)
                RETURNING user_id, username, email, subscription_tier, created_at
            """, (username, email, password_hash, subscription_tier, api_key, '{}'))
            
            user = dict(cursor.fetchone())
            conn.commit()
            
            logger.info(f"New user registered: {username} (ID: {user['user_id']})")
            
            return jsonify({
                'success': True,
                'message': 'User registered successfully',
                'user': {
                    'user_id': user['user_id'],
                    'username': user['username'],
                    'email': user['email'],
                    'subscription_tier': user['subscription_tier'],
                    'created_at': user['created_at'].isoformat()
                },
                'api_key': api_key,
                'note': 'Save your API key - it will not be shown again'
            }), 201
            
        except Exception as e:
            conn.rollback()
            logger.error(f"Registration error: {str(e)}")
            return jsonify({'error': 'Registration failed', 'code': 'REG_ERROR'}), 500
        
        finally:
            cursor.close()
            conn.close()
    
    except Exception as e:
        logger.error(f"Unexpected error in register: {str(e)}")
        return jsonify({'error': 'Server error', 'code': 'SERVER_ERROR'}), 500

@app.route('/api/user/login', methods=['POST'])
@limiter.limit("10 per hour")  # SECURITY: Rate limit login attempts
def login_user():
    """Login user and create session"""
    try:
        data = request.get_json() or {}
        
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        if not username or not password:
            logger.warning(f"Login attempt without credentials from {request.remote_addr}")
            return jsonify({'error': 'Username and password required'}), 400
        
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        try:
            # Get user
            cursor.execute("""
                SELECT user_id, username, email, password_hash, subscription_tier, 
                       api_key, is_active, preferences
                FROM user_unit.profiles
                WHERE LOWER(username) = LOWER(%s)
            """, (username,))
            
            user = cursor.fetchone()
            
            if not user:
                logger.warning(f"Login attempt with non-existent user: {username}")
                return jsonify({'error': 'Invalid credentials'}), 401
            
            if not user['is_active']:
                logger.warning(f"Login attempt on inactive account: {username}")
                return jsonify({'error': 'Account is inactive'}), 403
            
            # Verify password
            if not bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
                logger.warning(f"Failed password for user: {username} from {request.remote_addr}")
                return jsonify({'error': 'Invalid credentials'}), 401
            
            # Create session
            session_id = str(uuid.uuid4())
            expires_at = datetime.now() + timedelta(days=7)
            ip_address = request.remote_addr
            user_agent = request.headers.get('User-Agent', '')[:500]  # Limit to 500 chars
            
            cursor.execute("""
                INSERT INTO user_unit.sessions (
                    session_id, user_id, started_at, last_activity, 
                    expires_at, ip_address, user_agent
                ) VALUES (%s::uuid, %s, NOW(), NOW(), %s, %s::inet, %s)
            """, (session_id, user['user_id'], expires_at, ip_address, user_agent))
            
            # Update last login
            cursor.execute("""
                UPDATE user_unit.profiles
                SET last_login = NOW()
                WHERE user_id = %s
            """, (user['user_id'],))
            
            conn.commit()
            
            logger.info(f"User login successful: {username} from {request.remote_addr}")
            
            return jsonify({
                'success': True,
                'message': 'Login successful',
                'user': {
                    'user_id': user['user_id'],
                    'username': user['username'],
                    'email': user['email'],
                    'subscription_tier': user['subscription_tier']
                },
                'session_token': session_id,
                'expires_at': expires_at.isoformat()
            }), 200
            
        except Exception as e:
            conn.rollback()
            logger.error(f"Login error: {str(e)}")
            return jsonify({'error': 'Login failed', 'code': 'LOGIN_ERROR'}), 500
        
        finally:
            cursor.close()
            conn.close()
    
    except Exception as e:
        logger.error(f"Unexpected error in login: {str(e)}")
        return jsonify({'error': 'Server error', 'code': 'SERVER_ERROR'}), 500

@app.route('/api/user/logout', methods=['POST'])
@require_auth
@limiter.limit("30 per hour")
def logout_user():
    """Logout user and invalidate session"""
    try:
        session_token = request.headers.get('X-Session-Token')
        
        if not session_token:
            return jsonify({'message': 'No active session'}), 200
        
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                DELETE FROM user_unit.sessions
                WHERE session_id = %s::uuid
            """, (session_token,))
            
            conn.commit()
            
            logger.info(f"User logout: {request.current_user['username']}")
            
            return jsonify({
                'success': True,
                'message': 'Logged out successfully'
            }), 200
            
        finally:
            cursor.close()
            conn.close()
    
    except Exception as e:
        logger.error(f"Logout error: {str(e)}")
        return jsonify({'error': 'Logout failed', 'code': 'LOGOUT_ERROR'}), 500

@app.route('/api/user/profile', methods=['GET'])
@require_auth
@limiter.limit("60 per hour")
def get_profile():
    """Get user profile with statistics"""
    try:
        user_id = request.current_user['user_id']
        
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        try:
            # Get user profile
            cursor.execute("""
                SELECT user_id, username, email, subscription_tier, 
                       created_at, last_login, preferences
                FROM user_unit.profiles
                WHERE user_id = %s
            """, (user_id,))
            
            profile = dict(cursor.fetchone())
            
            # Get activity statistics
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_activities,
                    COUNT(DISTINCT activity_type) as activity_types,
                    MIN(timestamp) as first_activity,
                    MAX(timestamp) as last_activity
                FROM user_unit.activity_log
                WHERE user_id = %s
            """, (user_id,))
            
            stats = dict(cursor.fetchone())
            
            return jsonify({
                'success': True,
                'profile': {
                    'user_id': profile['user_id'],
                    'username': profile['username'],
                    'email': profile['email'],
                    'subscription_tier': profile['subscription_tier'],
                    'created_at': profile['created_at'].isoformat(),
                    'last_login': profile['last_login'].isoformat() if profile['last_login'] else None,
                    'preferences': profile['preferences']
                },
                'statistics': {
                    'total_activities': stats['total_activities'],
                    'activity_types': stats['activity_types'],
                    'first_activity': stats['first_activity'].isoformat() if stats['first_activity'] else None,
                    'last_activity': stats['last_activity'].isoformat() if stats['last_activity'] else None
                }
            }), 200
            
        finally:
            cursor.close()
            conn.close()
    
    except Exception as e:
        logger.error(f"Profile retrieval error: {str(e)}")
        return jsonify({'error': 'Failed to retrieve profile', 'code': 'PROFILE_ERROR'}), 500

@app.route('/api/user/preferences', methods=['PUT'])
@require_auth
@limiter.limit("30 per hour")
def update_preferences():
    """Update user preferences"""
    try:
        user_id = request.current_user['user_id']
        preferences = request.get_json() or {}
        
        # Validate preferences (max 10KB)
        import json
        if len(json.dumps(preferences)) > 10240:
            return jsonify({'error': 'Preferences too large (max 10KB)'}), 400
        
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                UPDATE user_unit.profiles
                SET preferences = %s::jsonb
                WHERE user_id = %s
            """, (psycopg2.extras.Json(preferences), user_id))
            
            conn.commit()
            
            logger.info(f"Preferences updated for user {user_id}")
            
            return jsonify({
                'success': True,
                'message': 'Preferences updated',
                'preferences': preferences
            }), 200
            
        finally:
            cursor.close()
            conn.close()
    
    except Exception as e:
        logger.error(f"Preference update error: {str(e)}")
        return jsonify({'error': 'Failed to update preferences', 'code': 'PREF_ERROR'}), 500

@app.route('/api/user/regenerate-api-key', methods=['POST'])
@require_auth
@limiter.limit("5 per hour")  # SECURITY: Rate limit key regeneration
def regenerate_api_key():
    """Generate new API key"""
    try:
        user_id = request.current_user['user_id']
        new_api_key = secrets.token_urlsafe(32)
        
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                UPDATE user_unit.profiles
                SET api_key = %s
                WHERE user_id = %s
            """, (new_api_key, user_id))
            
            conn.commit()
            
            logger.info(f"API key regenerated for user {user_id}")
            
            return jsonify({
                'success': True,
                'message': 'API key regenerated',
                'api_key': new_api_key,
                'note': 'Old API key is now invalid'
            }), 200
            
        finally:
            cursor.close()
            conn.close()
    
    except Exception as e:
        logger.error(f"API key regeneration error: {str(e)}")
        return jsonify({'error': 'Failed to regenerate API key', 'code': 'KEY_ERROR'}), 500

@app.route('/api/user/stats', methods=['GET'])
@limiter.limit("100 per hour")  # SECURITY: Rate limit stats (public endpoint but still limited)
def get_platform_stats():
    """Get platform statistics (public)"""
    try:
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        try:
            # Total users
            cursor.execute("SELECT COUNT(*) as total_users FROM user_unit.profiles WHERE is_active = TRUE")
            total_users = cursor.fetchone()['total_users']
            
            # Active sessions
            cursor.execute("SELECT COUNT(*) as active_sessions FROM user_unit.sessions WHERE expires_at > NOW()")
            active_sessions = cursor.fetchone()['active_sessions']
            
            return jsonify({
                'success': True,
                'platform_stats': {
                    'total_users': total_users,
                    'active_sessions': active_sessions
                }
            }), 200
            
        finally:
            cursor.close()
            conn.close()
    
    except Exception as e:
        logger.error(f"Stats retrieval error: {str(e)}")
        return jsonify({'error': 'Failed to retrieve stats', 'code': 'STATS_ERROR'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'R3ÆLƎR AI User Authentication API (SECURED)',
        'version': '2.0.0',
        'timestamp': datetime.now().isoformat()
    }), 200

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
    print("🔐 R3ÆLƎR AI USER AUTHENTICATION API (SECURED v2.0)")
    print("=" * 70)
    print("✅ Environment-based credentials (no hardcoded passwords)")
    print("✅ Rate limiting (registration, login, API key)")
    print("✅ Input validation (username, email, password strength)")
    print("✅ SSL/TLS database connection required")
    print("✅ CORS whitelist (no wildcard origins)")
    print("✅ Secure session management (UUID + expiration)")
    print("✅ Password hashing (bcrypt 12-round)")
    print("✅ Comprehensive audit logging")
    print("=" * 70)
    print("\n📊 Endpoints: http://localhost:5003")
    print("   POST /api/user/register (Rate: 5/hr)")
    print("   POST /api/user/login (Rate: 10/hr)")
    print("   POST /api/user/logout")
    print("   GET  /api/user/profile")
    print("   PUT  /api/user/preferences")
    print("   POST /api/user/regenerate-api-key (Rate: 5/hr)")
    print("   GET  /api/user/stats (Rate: 100/hr)")
    print("   GET  /health")
    print("\nPress Ctrl+C to stop\n")
    
    app.run(host='0.0.0.0', port=5003, debug=False, use_reloader=False)
