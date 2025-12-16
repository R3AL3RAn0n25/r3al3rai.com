#!/usr/bin/env python3
"""
R3ÆLƎR AI: User Authentication & Management API
Handles user registration, login, sessions, and API keys
"""

import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, jsonify, request, session
from flask_cors import CORS
import bcrypt
import secrets
import uuid
from datetime import datetime, timedelta
from functools import wraps
import logging

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)  # For session management
CORS(app, supports_credentials=True)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# PostgreSQL Configuration
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'r3aler_ai',
    'user': 'r3aler_user_2025',
    'password': 'R3AL3RAdmin816'
}

def get_connection():
    """Get database connection"""
    return psycopg2.connect(**DB_CONFIG)

def require_auth(f):
    """Decorator to require authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        session_token = request.headers.get('X-Session-Token')
        
        if not api_key and not session_token:
            return jsonify({'error': 'Authentication required', 'code': 'NO_AUTH'}), 401
        
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        user = None
        
        # Try API key authentication
        if api_key:
            cursor.execute("""
                SELECT user_id, username, subscription_tier, is_active
                FROM user_unit.profiles
                WHERE api_key = %s AND is_active = TRUE
            """, (api_key,))
            user = cursor.fetchone()
        
        # Try session token authentication
        elif session_token:
            cursor.execute("""
                SELECT p.user_id, p.username, p.subscription_tier, p.is_active
                FROM user_unit.profiles p
                JOIN user_unit.sessions s ON p.user_id = s.user_id
                WHERE s.session_id = %s::uuid 
                AND s.expires_at > NOW()
                AND p.is_active = TRUE
            """, (session_token,))
            user = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if not user:
            return jsonify({'error': 'Invalid or expired credentials', 'code': 'INVALID_AUTH'}), 401
        
        # Attach user info to request
        request.current_user = dict(user)
        
        return f(*args, **kwargs)
    
    return decorated_function

@app.route('/api/user/register', methods=['POST'])
def register_user():
    """Register a new user"""
    data = request.get_json()
    
    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '')
    subscription_tier = data.get('subscription_tier', 'free')
    
    # Validation
    if not username or len(username) < 3:
        return jsonify({'error': 'Username must be at least 3 characters'}), 400
    
    if not email or '@' not in email:
        return jsonify({'error': 'Valid email required'}), 400
    
    if not password or len(password) < 8:
        return jsonify({'error': 'Password must be at least 8 characters'}), 400
    
    if subscription_tier not in ['free', 'pro', 'enterprise']:
        subscription_tier = 'free'
    
    # Hash password
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    # Generate API key
    api_key = secrets.token_urlsafe(32)
    
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        # Check if username or email exists
        cursor.execute("""
            SELECT user_id FROM user_unit.profiles
            WHERE username = %s OR email = %s
        """, (username, email))
        
        if cursor.fetchone():
            return jsonify({'error': 'Username or email already exists'}), 409
        
        # Create user
        cursor.execute("""
            INSERT INTO user_unit.profiles (
                username, email, password_hash, subscription_tier, api_key,
                created_at, is_active, preferences
            ) VALUES (%s, %s, %s, %s, %s, NOW(), TRUE, %s::jsonb)
            RETURNING user_id, username, email, subscription_tier, api_key, created_at
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
            'api_key': user['api_key'],
            'note': 'Save your API key - it will not be shown again'
        }), 201
        
    except Exception as e:
        conn.rollback()
        logger.error(f"Registration error: {e}")
        return jsonify({'error': 'Registration failed', 'details': str(e)}), 500
    
    finally:
        cursor.close()
        conn.close()

@app.route('/api/user/login', methods=['POST'])
def login_user():
    """Login user and create session"""
    data = request.get_json()
    
    username = data.get('username', '').strip()
    password = data.get('password', '')
    
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        # Get user
        cursor.execute("""
            SELECT user_id, username, email, password_hash, subscription_tier, 
                   api_key, is_active, preferences
            FROM user_unit.profiles
            WHERE username = %s
        """, (username,))
        
        user = cursor.fetchone()
        
        if not user:
            return jsonify({'error': 'Invalid credentials'}), 401
        
        if not user['is_active']:
            return jsonify({'error': 'Account is inactive'}), 403
        
        # Verify password
        if not bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Create session
        session_id = str(uuid.uuid4())
        expires_at = datetime.now() + timedelta(days=7)  # 7 day session
        ip_address = request.remote_addr
        user_agent = request.headers.get('User-Agent', '')
        
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
        
        logger.info(f"User logged in: {username} (ID: {user['user_id']})")
        
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'user': {
                'user_id': user['user_id'],
                'username': user['username'],
                'email': user['email'],
                'subscription_tier': user['subscription_tier'],
                'preferences': user['preferences']
            },
            'session_token': session_id,
            'api_key': user['api_key'],
            'expires_at': expires_at.isoformat()
        }), 200
        
    except Exception as e:
        conn.rollback()
        logger.error(f"Login error: {e}")
        return jsonify({'error': 'Login failed', 'details': str(e)}), 500
    
    finally:
        cursor.close()
        conn.close()

@app.route('/api/user/logout', methods=['POST'])
@require_auth
def logout_user():
    """Logout user and invalidate session"""
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
        
        logger.info(f"User logged out: {request.current_user['username']}")
        
        return jsonify({
            'success': True,
            'message': 'Logged out successfully'
        }), 200
        
    finally:
        cursor.close()
        conn.close()

@app.route('/api/user/profile', methods=['GET'])
@require_auth
def get_profile():
    """Get user profile with statistics"""
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
        
        # Get tool preferences count
        cursor.execute("""
            SELECT COUNT(*) as tools_used
            FROM user_unit.tool_preferences
            WHERE user_id = %s
        """, (user_id,))
        
        tools_count = cursor.fetchone()['tools_used']
        
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
                'tools_used': tools_count,
                'first_activity': stats['first_activity'].isoformat() if stats['first_activity'] else None,
                'last_activity': stats['last_activity'].isoformat() if stats['last_activity'] else None
            }
        }), 200
        
    finally:
        cursor.close()
        conn.close()

@app.route('/api/user/preferences', methods=['PUT'])
@require_auth
def update_preferences():
    """Update user preferences"""
    user_id = request.current_user['user_id']
    preferences = request.get_json()
    
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            UPDATE user_unit.profiles
            SET preferences = %s::jsonb
            WHERE user_id = %s
        """, (psycopg2.extras.Json(preferences), user_id))
        
        conn.commit()
        
        return jsonify({
            'success': True,
            'message': 'Preferences updated',
            'preferences': preferences
        }), 200
        
    finally:
        cursor.close()
        conn.close()

@app.route('/api/user/regenerate-api-key', methods=['POST'])
@require_auth
def regenerate_api_key():
    """Generate new API key"""
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

@app.route('/api/user/stats', methods=['GET'])
def get_platform_stats():
    """Get platform statistics (public)"""
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        # Total users
        cursor.execute("SELECT COUNT(*) as total_users FROM user_unit.profiles WHERE is_active = TRUE")
        total_users = cursor.fetchone()['total_users']
        
        # Total activities
        cursor.execute("SELECT COUNT(*) as total_activities FROM user_unit.activity_log")
        total_activities = cursor.fetchone()['total_activities']
        
        # Active sessions
        cursor.execute("SELECT COUNT(*) as active_sessions FROM user_unit.sessions WHERE expires_at > NOW()")
        active_sessions = cursor.fetchone()['active_sessions']
        
        return jsonify({
            'success': True,
            'platform_stats': {
                'total_users': total_users,
                'total_activities': total_activities,
                'active_sessions': active_sessions
            }
        }), 200
        
    finally:
        cursor.close()
        conn.close()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'R3ÆLƎR AI User Authentication API',
        'version': '1.0.0'
    }), 200

if __name__ == '__main__':
    print("\n" + "=" * 70)
    print("🔐 R3ÆLƎR AI USER AUTHENTICATION API")
    print("=" * 70)
    print("✅ User registration and login")
    print("✅ API key management")
    print("✅ Session management")
    print("✅ User preferences")
    print("=" * 70)
    print("\n📊 Endpoints: http://localhost:5004")
    print("   POST /api/user/register")
    print("   POST /api/user/login")
    print("   POST /api/user/logout")
    print("   GET  /api/user/profile")
    print("   PUT  /api/user/preferences")
    print("   POST /api/user/regenerate-api-key")
    print("   GET  /api/user/stats")
    print("\nPress Ctrl+C to stop\n")
    
    app.run(host='0.0.0.0', port=5004, debug=True, use_reloader=False)
