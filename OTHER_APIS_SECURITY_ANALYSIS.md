# Security Issues in Other API Files

## Overview
After analyzing `knowledge_api.py` and `droid_api.py`, we've identified the **same 10 critical security vulnerabilities** present in `user_auth_api.py`, plus additional issues specific to their architecture.

---

## 1. KNOWLEDGE_API.PY (721 lines)
**File Location:** `AI_Core_Worker/knowledge_api.py`

### Security Vulnerabilities

#### ❌ CRITICAL #1: Hardcoded Database Credentials
```python
# Lines 1-30 (VULNERABLE)
STORAGE_FACILITY_URL = os.getenv("STORAGE_FACILITY_URL", "http://localhost:3003")
# No validation if env var missing
```

**Risk:** If `STORAGE_FACILITY_URL` is not set, falls back to localhost (insecure)

**Fix:** Validate and require this environment variable with error handling

---

#### ❌ CRITICAL #2: Unrestricted CORS
```python
# Line 41
app = Flask(__name__)
CORS(app)  # Enable CORS for Node.js backend
```

**Risk:** Allows ANY origin to access all endpoints (CWE-346: Origin Validation Error)

**Fix:** Implement whitelist-based CORS configuration:
```python
CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', 'http://localhost:3000').split(',')
CORS(app, origins=CORS_ALLOWED_ORIGINS, supports_credentials=True)
```

---

#### ❌ HIGH #3: No Authentication/Authorization
```python
# Lines 46-80 (@app.route endpoints)
@app.route('/api/query', methods=['POST'])
def query_with_ai():
    # No @require_auth decorator!
    # Anyone can access this endpoint
```

**Risk:** Unauthenticated users can query the entire AI knowledge base

**Fix:** Add `@require_auth` decorator to all endpoints

---

#### ❌ HIGH #4: No Input Validation
```python
# Lines 73-76
query = (data.get('query') or '').strip()
user_id = data.get('user_id') or get_user_id_from_request() or 'anonymous'
role = data.get('role')
# No length limits, format validation, or injection protection
```

**Risk:** 
- Query injection (NoSQL/SQL injection via Storage Facility)
- Unbounded input size (DoS attack)
- Malicious role values

**Fix:** Implement validation:
```python
if not query or len(query) < 3 or len(query) > 5000:
    return jsonify({'error': 'Query must be 3-5000 characters'}), 400

if not query.replace('_', '').replace('-', '').replace(' ', '').isalnum():
    return jsonify({'error': 'Query contains invalid characters'}), 400

if role and role not in ['user', 'admin', 'developer']:
    role = 'user'
```

---

#### ❌ HIGH #5: No Rate Limiting
```python
# No Flask-Limiter decorator on endpoints
@app.route('/api/query', methods=['POST'])
def query_with_ai():  # Can be called 1000x/second
    ...

@app.route('/api/kb/search', methods=['POST'])
def search_knowledge():  # Can be called unlimited times
    ...
```

**Risk:** DoS attacks, resource exhaustion

**Fix:** Add rate limiting:
```python
from flask_limiter import Limiter

limiter = Limiter(app=app, key_func=get_remote_address)

@app.route('/api/query', methods=['POST'])
@limiter.limit("20/hour")  # 20 queries per hour max
def query_with_ai():
    ...
```

---

#### ❌ HIGH #6: Information Disclosure in Error Messages
```python
# Lines 250-260 (example)
except Exception as e:
    print(f"[R3AL3R AI] Error: {e}")  # Logs to console
    return jsonify({
        'success': False,
        'error': 'R3AL3R AI encountered an error. Please try again.',
        'self_sufficient': True
    }), 500
```

**Risk:** Different error messages for different failures reveal system internals

**Fix:** Use generic error messages, log internally with stack traces:
```python
except Exception as e:
    logger.error(f"Query processing failed: {str(e)}", exc_info=True)
    return jsonify({'error': 'Request failed. Please try again.'}), 500
```

---

#### ❌ MEDIUM #7: Insecure User ID Tracking
```python
# Lines 51-57
def get_user_id_from_request():
    """Extract user_id from request headers or query params"""
    user_id = request.headers.get('X-User-ID')
    if not user_id:
        user_id = request.args.get('user_id')  # VULNERABLE: From query params!
    return user_id
```

**Risk:**
- User ID taken from query params = easy spoofing
- User ID from headers without validation
- No user ID format validation
- Allows user impersonation

**Fix:** Use authenticated sessions only:
```python
def get_user_id_from_request():
    """Extract user_id from validated session only"""
    session_token = request.headers.get('X-Session-Token')
    if not session_token:
        raise ValueError("Session token required")
    
    # Validate session against database (see user_auth_api.py)
    # Return ONLY the authenticated user_id
    return get_authenticated_user_id(session_token)
```

---

#### ❌ MEDIUM #8: Unvalidated External Service Calls
```python
# Lines 110-120
try:
    storage_response = requests.post(
        f'{STORAGE_FACILITY_URL}/api/facility/search',
        json={'query': query, 'max_results': 5},
        timeout=5  # Short timeout, but what if STORAGE_FACILITY_URL is malicious?
    )
    # No SSL verification mentioned, no certificate validation
```

**Risk:**
- STORAGE_FACILITY_URL could be compromised/redirected
- Man-in-the-middle attack possible
- No certificate validation

**Fix:** Implement strict validation:
```python
import ssl

def make_secure_request(url, data):
    # Validate URL is in whitelist
    if not url.startswith(os.getenv('STORAGE_FACILITY_URL')):
        raise ValueError("Invalid storage facility URL")
    
    return requests.post(
        url,
        json=data,
        timeout=10,
        verify=True,  # Verify SSL certificate
        cert=('/path/to/client.crt', '/path/to/client.key')  # Client cert if needed
    )
```

---

#### ❌ MEDIUM #9: No Activity Logging/Audit Trail
```python
# Lines 70-100 show print statements, not logging
print(f"[R3AL3R AI] Processing query from {user_id}: {query[:50]}...")
# Should use logging module with proper levels
```

**Risk:**
- No audit trail for security incidents
- Can't trace who accessed what data
- Compliance violations (GDPR, etc.)

**Fix:** Implement comprehensive logging (see user_auth_api.py example)

---

#### ❌ MEDIUM #10: No SQL Injection Prevention
```python
# Lines 150-160 - Assuming Storage Facility passes query directly to DB
storage_response = requests.post(
    f'{STORAGE_FACILITY_URL}/api/facility/search',
    json={'query': query, 'max_results': 5},  # Query never sanitized
    timeout=5
)
```

**Risk:** SQL injection via Storage Facility if query not sanitized there

**Fix:** Ensure Storage Facility uses parameterized queries (not your responsibility, but validate)

---

### Additional Issues Specific to knowledge_api.py

#### ❌ MEDIUM #11: Hardcoded Fallback URLs
```python
# Line 20
STORAGE_FACILITY_URL = os.getenv("STORAGE_FACILITY_URL", "http://localhost:3003")
# Hardcoded localhost fallback = insecure default
```

**Fix:**
```python
STORAGE_FACILITY_URL = os.getenv("STORAGE_FACILITY_URL")
if not STORAGE_FACILITY_URL:
    logger.error("STORAGE_FACILITY_URL not configured")
    sys.exit(1)
```

---

## 2. DROID_API.PY (598 lines)
**File Location:** `src/apis/droid_api.py`

### Security Vulnerabilities

#### ❌ CRITICAL #1: Hardcoded Database Credentials with Weak Defaults
```python
# Lines 447-455
DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'port': os.environ.get('DB_PORT', '5432'),
    'user': os.environ.get('DB_USER', 'r3aler_user_2025'),  # HARDCODED!
    'password': os.environ.get('DB_PASSWORD', 'password123'),  # HARDCODED!
    'database': os.environ.get('DB_NAME', 'r3al3rai_2025')  # HARDCODED!
}
```

**Risk:** 
- Exposed credentials in source code
- Weak default password visible to anyone
- Credentials in git history forever

**Fix:** Require all environment variables, no defaults:
```python
REQUIRED_ENV_VARS = ['DB_HOST', 'DB_PORT', 'DB_NAME', 'DB_USER', 'DB_PASSWORD']
missing = [v for v in REQUIRED_ENV_VARS if not os.getenv(v)]
if missing:
    logger.error(f"Missing required env vars: {', '.join(missing)}")
    sys.exit(1)

DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'port': int(os.getenv('DB_PORT')),
    'database': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
}
```

---

#### ❌ CRITICAL #2: Unrestricted CORS
```python
# Line 444
app = Flask(__name__)
CORS(app)  # Enable CORS for all origins!
```

**Fix:** (same as knowledge_api.py)

---

#### ❌ HIGH #3: No Authentication Required
```python
# Lines 468-480
@app.route('/api/droid/chat', methods=['POST'])
def droid_chat():
    """Process chat message through the Droid"""
    try:
        data = request.json
        user_id = data.get('user_id', 'default_user')  # No authentication!
        # Anyone can send messages as any user!
```

**Risk:** Complete impersonation - user can chat as anyone

**Fix:** Require authentication with session token validation

---

#### ❌ HIGH #4: User Impersonation via user_id Parameter
```python
# Line 472
user_id = data.get('user_id', 'default_user')  # Taken from request body!
```

**Risk:** Attacker can set `user_id` to any value = impersonate other users

**Fix:** Extract user_id from authenticated session only:
```python
@require_auth
def droid_chat():
    user_id = request.current_user['user_id']  # From validated token, not request
    # ... rest of function
```

---

#### ❌ HIGH #5: No Rate Limiting on Expensive Operations
```python
# Lines 468-480 - chat endpoint can be called unlimited times
@app.route('/api/droid/chat', methods=['POST'])
def droid_chat():
    # AI processing is expensive - no rate limiting!
```

**Risk:** DoS attack - attacker floods with chat requests

**Fix:** Add strict rate limiting:
```python
@app.route('/api/droid/chat', methods=['POST'])
@limiter.limit("5/hour")  # Very strict for expensive AI operations
def droid_chat():
    ...
```

---

#### ❌ HIGH #6: Insecure Database Connection
```python
# Lines 61-71
try:
    self.conn = psycopg2.connect(
        host=db_config['host'],
        port=db_config['port'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database']
    )
    # No SSL/TLS connection (sslmode not set)
```

**Risk:** Database credentials transmitted in plaintext over network

**Fix:** Use encrypted connections:
```python
self.conn = psycopg2.connect(
    host=db_config['host'],
    port=db_config['port'],
    user=db_config['user'],
    password=db_config['password'],
    database=db_config['database'],
    sslmode='require',  # Force SSL/TLS
    sslrootcert='/path/to/ca-cert.pem',  # Certificate validation
    connect_timeout=10
)
```

---

#### ❌ HIGH #7: SQL Injection via Dynamic Queries
```python
# Lines 163-180 (in adapt_to_user method)
cur.execute("""
    INSERT INTO droid_profiles 
    (user_id, likes, dislikes, habits, financial_goals, 
     interaction_count, questions_asked, adaptability_level, last_interaction, updated_at)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
    ...
""", (
    self.user_id,  # User_id comes from untrusted source!
    ...
))
```

**Risk:** While using parameterized queries (good!), user_id is not validated

**Fix:** Validate user_id format:
```python
import uuid

def __init__(self, user_id, db_config):
    try:
        # Validate user_id is valid UUID format
        uuid.UUID(user_id)
    except ValueError:
        raise ValueError(f"Invalid user_id format: {user_id}")
    
    self.user_id = user_id
    ...
```

---

#### ❌ MEDIUM #8: No Input Validation on Chat Messages
```python
# Lines 472-480
data = request.json
user_id = data.get('user_id', 'default_user')
message = data.get('message', '')
context = data.get('context', {})
max_questions = data.get('max_questions', 10)

# No validation on any of these values!
```

**Risk:**
- Unbounded message size (DoS via memory exhaustion)
- Malicious context dict
- max_questions can be set to 0 or negative
- Injection attacks via message content

**Fix:** Add validation:
```python
if not message or len(message) < 1 or len(message) > 10000:
    return jsonify({'error': 'Message must be 1-10000 characters'}), 400

if not isinstance(context, dict) or len(context) > 100:
    return jsonify({'error': 'Invalid context'}), 400

max_questions = min(int(data.get('max_questions', 10)), 100)  # Cap at 100
if max_questions < 1:
    max_questions = 1
```

---

#### ❌ MEDIUM #9: Insecure Error Handling
```python
# Lines 475-490 (approximate)
except Exception as e:
    logging.error(f"Failed to create droid for {user_id}: {e}")
    return None  # Returns None without HTTP response
```

**Risk:**
- Inconsistent error responses
- Stack traces might be exposed
- Hard to debug for legitimate users

**Fix:** Implement consistent error handling (see user_auth_api.py)

---

#### ❌ MEDIUM #10: No Database Connection Pooling
```python
# Lines 61-71
# Each droid instance creates its own database connection
self.conn = psycopg2.connect(...)
# With multiple users = connection explosion
```

**Risk:**
- Connection pool exhaustion
- Resource leak if droids are created but not destroyed
- Poor performance under load

**Fix:** Implement connection pooling:
```python
from psycopg2 import pool

db_pool = psycopg2.pool.SimpleConnectionPool(
    minconn=5,
    maxconn=20,  # Maximum 20 connections
    **DB_CONFIG
)

def get_connection():
    return db_pool.getconn()

def release_connection(conn):
    db_pool.putconn(conn)
```

---

#### ❌ MEDIUM #11: Degraded Mode Security
```python
# Lines 71-79
except Exception as e:
    logging.error(f"R3al3rDroid PostgreSQL connection failed: {e}")
    # Continue without database (degraded mode)
    self.conn = None
```

**Risk:**
- App continues operating without database = silent failure
- Behavioral changes between normal/degraded mode
- User doesn't know operations aren't persisted

**Fix:** Fail securely:
```python
except Exception as e:
    logger.error(f"Database connection critical: {str(e)}")
    raise RuntimeError("Database connection required - cannot continue")
```

---

### Additional Issues Specific to droid_api.py

#### ❌ MEDIUM #12: In-Memory Instance Caching Without Limits
```python
# Lines 445-450
droid_instances = {}

def get_droid(user_id):
    if user_id not in droid_instances:
        droid_instances[user_id] = R3al3rDroid(...)
    return droid_instances[user_id]
```

**Risk:**
- Memory leak - droids never deleted
- Attacker creates infinite user_ids = memory exhausted = DoS
- Stale user data cached indefinitely

**Fix:** Implement cache limits with TTL:
```python
from functools import lru_cache
from datetime import datetime, timedelta

droid_cache = {}
CACHE_TTL = 3600  # 1 hour

@lru_cache(maxsize=1000)  # Maximum 1000 cached droids
def get_droid(user_id):
    if user_id in droid_cache:
        droid, created_at = droid_cache[user_id]
        if datetime.now() - created_at < timedelta(seconds=CACHE_TTL):
            return droid
        else:
            del droid_cache[user_id]
    
    droid = R3al3rDroid(user_id, DB_CONFIG)
    droid_cache[user_id] = (droid, datetime.now())
    return droid
```

---

## Summary Table: Vulnerabilities Across APIs

| Vulnerability | user_auth_api.py | knowledge_api.py | droid_api.py |
|---|:---:|:---:|:---:|
| Hardcoded credentials | ❌ FIXED | ❌ VULNERABLE | ❌ VULNERABLE |
| Unrestricted CORS | ❌ FIXED | ❌ VULNERABLE | ❌ VULNERABLE |
| No authentication | ❌ FIXED | ❌ VULNERABLE | ❌ VULNERABLE |
| No input validation | ❌ FIXED | ❌ VULNERABLE | ❌ VULNERABLE |
| No rate limiting | ❌ FIXED | ❌ VULNERABLE | ❌ VULNERABLE |
| Information disclosure | ❌ FIXED | ❌ VULNERABLE | ❌ VULNERABLE |
| User impersonation | ❌ FIXED | ❌ VULNERABLE | ❌ VULNERABLE |
| Unvalidated external calls | ✅ N/A | ❌ VULNERABLE | ✅ N/A |
| No activity logging | ❌ FIXED | ❌ VULNERABLE | ❌ VULNERABLE |
| SQL injection risk | ❌ FIXED | ❌ VULNERABLE | ✅ Using parameterized |
| **Total Vulnerabilities** | **0** | **11** | **12** |

---

## Priority Fixes Needed

### Phase 1 (CRITICAL - Immediate)
1. **knowledge_api.py**: Add authentication + CORS restriction + input validation
2. **droid_api.py**: Remove hardcoded credentials + add authentication + user impersonation fix

### Phase 2 (HIGH - This Week)
3. **knowledge_api.py**: Add rate limiting + logging + input validation
4. **droid_api.py**: Add rate limiting + SSL/TLS + connection pooling

### Phase 3 (MEDIUM - This Month)
5. **knowledge_api.py**: Add external service validation + comprehensive logging
6. **droid_api.py**: Fix cache management + degraded mode handling

---

## Files to Fix
- `AI_Core_Worker/knowledge_api.py` (721 lines) - 11 vulnerabilities
- `src/apis/droid_api.py` (598 lines) - 12 vulnerabilities

**Total vulnerabilities across these two files: 23**
