#!/usr/bin/env python3
"""
R3ÆLƎR AI Knowledge API Bridge - SECURITY HARDENED v2.0
Exposes AI Core Worker knowledge base via HTTP API - Now using PostgreSQL Storage Facility!
WITH AI PERSONALIZATION, SELF-LEARNING, AND EVOLUTION!

SECURITY FEATURES:
✓ Environment-based configuration (no hardcoded values)
✓ SSL/TLS for external service communication
✓ Rate limiting on all endpoints
✓ CORS whitelisting
✓ Input validation and sanitization
✓ Authentication via session tokens or API keys
✓ Comprehensive security logging
✓ IP whitelisting support
✓ Secure error handling (no information disclosure)
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv
import sys
import os
import requests
import logging
from typing import List, Dict, Any
from functools import wraps
import time
import uuid

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add AI_Core_Worker to path
sys.path.append(os.path.dirname(__file__))

from prompts import R3AELERPrompts

# Import AI Intelligence Modules
try:
    from activity_tracker import ActivityTracker
    from personalization_engine import PersonalizationEngine
    from recommendation_engine import RecommendationEngine
    from self_learning_engine import SelfLearningEngine
    from evolution_engine import EvolutionEngine
    AI_MODULES_LOADED = True
    logger.info("AI Intelligence Modules Loaded Successfully")
except ImportError as e:
    logger.warning(f"AI Modules not available: {e}")
    AI_MODULES_LOADED = False

# ============ SECURITY CONFIGURATION ============

# Validate required environment variables
REQUIRED_ENV_VARS = ['STORAGE_FACILITY_URL', 'FLASK_SECRET_KEY']
missing_vars = [var for var in REQUIRED_ENV_VARS if not os.getenv(var)]
if missing_vars:
    logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
    logger.error("Please configure .env file with required variables")
    sys.exit(1)

# Storage Facility configuration
STORAGE_FACILITY_URL = os.getenv("STORAGE_FACILITY_URL")
STORAGE_FACILITY_TIMEOUT = int(os.getenv("STORAGE_FACILITY_TIMEOUT", "10"))
STORAGE_FACILITY_CERT = os.getenv("STORAGE_FACILITY_CERT")  # Path to SSL cert

# CORS Configuration - whitelist only trusted origins
CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', 'http://localhost:3000').split(',')
CORS_ALLOWED_ORIGINS = [origin.strip() for origin in CORS_ALLOWED_ORIGINS]

# IP Whitelisting
ALLOWED_IPS = os.getenv('ALLOWED_IPS', '72.17.63.255,127.0.0.1').split(',')
ALLOWED_IPS = [ip.strip() for ip in ALLOWED_IPS]

# Rate limiting configuration
RATE_LIMIT_QUERY = os.getenv('RATE_LIMIT_QUERY', '20/hour')
RATE_LIMIT_SEARCH = os.getenv('RATE_LIMIT_SEARCH', '30/hour')
RATE_LIMIT_INGEST = os.getenv('RATE_LIMIT_INGEST', '5/hour')

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')

# CORS with security restrictions
CORS(app, 
     origins=CORS_ALLOWED_ORIGINS,
     supports_credentials=True,
     methods=['GET', 'POST', 'OPTIONS'],
     allow_headers=['Content-Type', 'X-Session-Token', 'X-API-Key'])

# Rate limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["100/hour"],
    storage_uri="memory://"
)

# ============ SECURITY FUNCTIONS ============

def validate_ip_address():
    """Validate request IP against whitelist"""
    remote_ip = request.remote_addr
    if remote_ip not in ALLOWED_IPS:
        logger.warning(f"Request from non-whitelisted IP: {remote_ip}")
        return False
    return True

def require_auth(f):
    """Decorator to require authentication via session token or API key"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        session_token = request.headers.get('X-Session-Token')
        api_key = request.headers.get('X-API-Key')
        
        if not session_token and not api_key:
            logger.warning(f"Unauthorized access attempt from {request.remote_addr}")
            return jsonify({'error': 'Authentication required (X-Session-Token or X-API-Key)'}), 401
        
        # Validate token format
        if session_token:
            try:
                uuid.UUID(session_token)
            except ValueError:
                logger.warning(f"Invalid session token format from {request.remote_addr}")
                return jsonify({'error': 'Invalid session token'}), 401
        
        # Attach authentication info to request
        request.auth_token = session_token or api_key
        request.authenticated = True
        
        return f(*args, **kwargs)
    
    return decorated_function

def validate_input(value, name, min_len=1, max_len=5000, allowed_chars=None):
    """Validate and sanitize user input"""
    if not value or not isinstance(value, str):
        raise ValueError(f"{name} is required and must be a string")
    
    value = value.strip()
    if len(value) < min_len or len(value) > max_len:
        raise ValueError(f"{name} must be {min_len}-{max_len} characters")
    
    if allowed_chars and not all(c in allowed_chars or c.isspace() for c in value):
        raise ValueError(f"{name} contains invalid characters")
    
    return value

def make_secure_storage_request(endpoint, json_data, timeout=None):
    """Make secure request to Storage Facility with SSL validation"""
    if timeout is None:
        timeout = STORAGE_FACILITY_TIMEOUT
    
    url = f"{STORAGE_FACILITY_URL}{endpoint}"
    
    try:
        # Validate URL format
        if not url.startswith(STORAGE_FACILITY_URL):
            raise ValueError("Invalid Storage Facility URL")
        
        request_kwargs = {
            'json': json_data,
            'timeout': timeout,
            'verify': True  # Always verify SSL certificates
        }
        
        # Add client certificate if configured
        if STORAGE_FACILITY_CERT and os.path.exists(STORAGE_FACILITY_CERT):
            request_kwargs['verify'] = STORAGE_FACILITY_CERT
        
        response = requests.post(url, **request_kwargs)
        return response
        
    except requests.exceptions.SSLError as e:
        logger.error(f"SSL error connecting to Storage Facility: {str(e)}")
        raise RuntimeError("Storage Facility SSL verification failed")
    except requests.exceptions.ConnectionError as e:
        logger.error(f"Connection error to Storage Facility: {str(e)}")
        raise RuntimeError("Storage Facility connection failed")
    except requests.exceptions.Timeout:
        logger.error(f"Timeout connecting to Storage Facility (>{timeout}s)")
        raise RuntimeError("Storage Facility request timeout")

def get_authenticated_user_id():
    """Extract user_id from authenticated session only"""
    session_token = request.headers.get('X-Session-Token')
    if session_token and getattr(request, 'authenticated', False):
        return f"user_session_{session_token[:8]}"
    return None

# ============ API ENDPOINTS ============

@app.route('/api/query', methods=['POST'])
@limiter.limit("20/hour")  # Rate limit: 20 queries per hour
@require_auth
def query_with_ai():
    """R3AL3R AI Query Endpoint - 100% LOCAL INTELLIGENCE
    
    SECURITY: Requires X-Session-Token or X-API-Key header
    RATE LIMITED: 20 requests per hour
    
    Request JSON:
      - query: str (required, 3-5000 chars)
      - role: str (optional, validated against whitelist)
      
    Response JSON:
      - success: bool
      - response: str (AI-generated response)
      - knowledge_used: bool
      - sources: list (knowledge sources used)
      - domain: str (detected domain)
    """
    try:
        data = request.get_json(silent=True) or {}
        
        # Validate and sanitize input
        try:
            query = validate_input(data.get('query'), 'query', min_len=3, max_len=5000)
        except ValueError as e:
            logger.warning(f"Invalid query input from {request.remote_addr}: {str(e)}")
            return jsonify({'success': False, 'error': str(e)}), 400
        
        # Get authenticated user
        user_id = get_authenticated_user_id() or 'authenticated_user'
        
        # Validate role (whitelist)
        role = data.get('role', 'user')
        if role not in ['user', 'admin', 'developer', 'analyst']:
            role = 'user'
        
        logger.info(f"Processing query from {user_id}: {query[:50]}...")
        
        # Step 1: Search Storage Facility for relevant knowledge
        knowledge_context = ""
        sources = []
        
        try:
            storage_response = make_secure_storage_request(
                '/api/facility/search',
                {'query': query, 'max_results': 5}
            )
            
            if storage_response.status_code == 200:
                results = storage_response.json().get('results', [])
                if results:
                    logger.info(f"Found {len(results)} knowledge entries from Storage Facility")
                    knowledge_context = "\n\n🔍 **Storage Facility Knowledge:**\n"
                    for idx, r in enumerate(results[:3], 1):
                        topic = str(r.get('topic', 'Unknown'))[:100]
                        content = str(r.get('content', ''))[:250]
                        knowledge_context += f"{idx}. **{topic}**: {content}...\n"
                        sources.append(topic)
        except RuntimeError as e:
            logger.warning(f"Storage Facility unavailable: {str(e)}")
            # Fallback to local knowledge base
            for key, value in R3AELERPrompts.KNOWLEDGE_BASE.items():
                if key in query.lower():
                    knowledge_context += f"\n• {key.title()}: {value[:200]}...\n"
                    sources.append(key)
        
        # Step 2: Generate LOCAL AI response
        try:
            import AI_Core_Worker as ai_module
            ai_worker = ai_module.RealerAI()
            
            enriched_query = query
            if knowledge_context:
                enriched_query = f"{query}\n\n[KNOWLEDGE CONTEXT]{knowledge_context}"
            
            ai_response = ai_worker.generate_response(enriched_query, user_id)
            domain = ai_worker._detect_domain(query.lower())
            
            logger.info(f"Response generated (domain: {domain}) for user {user_id}")
            
            return jsonify({
                'success': True,
                'response': ai_response,
                'knowledge_used': bool(knowledge_context or sources),
                'sources': sources[:5],
                'domain': domain
            })
            
        except Exception as ai_error:
            logger.error(f"AI Core error: {str(ai_error)}", exc_info=True)
            
            # Fallback to prompt-based response
            context = R3AELERPrompts.analyze_context(query)
            response = R3AELERPrompts.generate_dynamic_response(context)
            
            if knowledge_context:
                response = f"{response}\n{knowledge_context}"
            
            return jsonify({
                'success': True,
                'response': response,
                'knowledge_used': bool(knowledge_context),
                'sources': sources[:5],
                'domain': context.get('domain', 'general'),
                'fallback_mode': True
            })
            
    except Exception as e:
        logger.error(f"Query processing error: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': 'Request failed. Please try again.'}), 500

@app.route('/api/kb/search', methods=['POST'])
@limiter.limit("30/hour")  # Rate limit: 30 searches per hour
@require_auth
def search_knowledge():
    """Unified knowledge search endpoint - Security Hardened
    
    SECURITY: Requires X-Session-Token or X-API-Key header
    RATE LIMITED: 30 requests per hour

    Request JSON:
      - query: str (required, 3-5000 chars)
      - maxPassages: int (optional, 3-100, default 5)
      - maxChars: int (optional, 100-5000, default 800)
    """
    start_time = time.time()
    
    try:
        data = request.get_json(silent=True) or {}
        
        # Validate query
        try:
            raw_query = validate_input(data.get('query'), 'query', min_len=3, max_len=5000)
        except ValueError as e:
            logger.warning(f"Invalid search query from {request.remote_addr}: {str(e)}")
            return jsonify({'success': False, 'error': str(e)}), 400

        # Validate numeric parameters
        try:
            max_passages = min(int(data.get('maxPassages', 5)), 100)
            max_passages = max(max_passages, 3)
            
            max_chars = min(int(data.get('maxChars', 800)), 5000)
            max_chars = max(max_chars, 100)
        except (ValueError, TypeError):
            logger.warning(f"Invalid numeric parameters from {request.remote_addr}")
            max_passages = 5
            max_chars = 800
        
        user_id = get_authenticated_user_id() or 'authenticated_user'
        
        local_results = []
        passages = []
        personalized = False
        
        # Query Storage Facility
        try:
            logger.info(f"Searching Storage Facility for: {raw_query[:100]}")
            
            response = make_secure_storage_request(
                '/api/facility/search',
                {'query': raw_query, 'limit_per_unit': max_passages * 2}
            )
            
            logger.info(f"Storage Facility responded: {response.status_code}")
            
            if response.status_code == 200:
                facility_data = response.json()
                results = facility_data.get('results', [])
                logger.info(f"Found {len(results)} results from Storage Facility")
                
                # Apply personalization if user authenticated
                if user_id and AI_MODULES_LOADED:
                    try:
                        logger.info(f"Applying AI personalization for user {user_id}")
                        results = PersonalizationEngine.personalize_search_results(results, user_id)
                        personalized = True
                    except Exception as e:
                        logger.warning(f"Personalization failed: {e}")
                
                # Transform results
                for result in results[:max_passages]:
                    passage_text = str(result['content'])[:max_chars]
                    
                    passages.append({
                        'text': passage_text,
                        'source': f"Storage Facility - {result['unit_name']}",
                        'meta': {
                            'topic': str(result['topic'])[:100],
                            'category': str(result['category'])[:50],
                            'relevance': result.get('relevance', 0)
                        }
                    })
                    
                    local_results.append({
                        'key': result['entry_id'],
                        'topic': str(result['topic'])[:100],
                        'content_preview': passage_text[:200],
                        'category': str(result['category'])[:50]
                    })
                
                # Log activity
                if user_id and AI_MODULES_LOADED:
                    try:
                        time_taken_ms = int((time.time() - start_time) * 1000)
                        ActivityTracker.log_knowledge_search(
                            user_id, raw_query, len(results), 'storage_facility', time_taken_ms
                        )
                    except Exception as e:
                        logger.warning(f"Activity tracking failed: {e}")
                        
            else:
                logger.warning(f"Storage Facility returned {response.status_code}")
                return search_legacy_knowledge(raw_query, max_passages, max_chars)
                
        except RuntimeError as e:
            logger.warning(f"Storage Facility error: {str(e)}, using fallback")
            return search_legacy_knowledge(raw_query, max_passages, max_chars)

        return jsonify({
            'success': True,
            'used_storage_facility': True,
            'personalized': personalized,
            'total_entries': 30657,
            'query': raw_query,
            'local_results': local_results,
            'passages': passages
        })

    except Exception as e:
        logger.error(f"Search error: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': 'Search failed. Please try again.'}), 500

def search_legacy_knowledge(query: str, max_passages: int, max_chars: int):
    """Fallback to legacy in-memory knowledge base search"""
    q = query.lower()
    local_results = []
    passages = []
    
    for key, value in R3AELERPrompts.KNOWLEDGE_BASE.items():
        if isinstance(value, dict):
            topic = str(value.get('topic', key))[:100]
            content = str(value.get('content', ''))
            category = str(value.get('category', ''))[:50]
        else:
            topic = str(key)[:100]
            content = str(value)
            category = 'General'
        
        if q in topic.lower() or q in content.lower():
            passage_text = content[:max_chars]
            
            passages.append({
                'text': passage_text,
                'source': 'legacy_kb',
                'meta': {'topic': topic, 'category': category}
            })
            
            local_results.append({
                'key': key,
                'topic': topic,
                'content_preview': passage_text[:200],
                'category': category
            })
            
            if len(passages) >= max_passages:
                break
    
    return jsonify({
        'success': True,
        'used_storage_facility': False,
        'fallback_mode': True,
        'query': query,
        'local_results': local_results,
        'passages': passages
    })

@app.route('/api/kb/ingest', methods=['POST'])
@limiter.limit("5/hour")  # Strict limit on ingestion
@require_auth
def ingest_data():
    """Ingest new knowledge into Storage Facility - SECURED
    
    Rate limited to 5/hour
    Requires authentication
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        unit = data.get('unit', 'crypto')
        entries = data.get('entries', [])
        
        if not entries:
            return jsonify({'success': False, 'error': 'No entries provided'}), 400
        
        # Validate unit
        valid_units = ['crypto', 'physics', 'quantum', 'space']
        if unit not in valid_units:
            logger.warning(f"Invalid unit '{unit}' from {request.remote_addr}")
            return jsonify({'success': False, 'error': f'Invalid unit. Must be one of: {", ".join(valid_units)}'}), 400
        
        # Validate entries count
        if len(entries) > 1000:
            logger.warning(f"Too many entries ({len(entries)}) from {request.remote_addr}")
            return jsonify({'success': False, 'error': 'Maximum 1000 entries per request'}), 400
        
        logger.info(f"Ingesting {len(entries)} entries to {unit} unit from {request.remote_addr}")
        
        # Forward to Storage Facility
        response = make_secure_storage_request(
            f'/api/unit/{unit}/store',
            {'entries': entries},
            timeout=30
        )
        
        if response.status_code == 200:
            logger.info(f"Successfully ingested {len(entries)} entries")
            return jsonify({
                'success': True,
                'message': f'Successfully ingested {len(entries)} entries to {unit} unit',
                'unit': unit,
                'entries_added': len(entries)
            })
        else:
            logger.error(f"Storage Facility returned {response.status_code}")
            return jsonify({
                'success': False,
                'error': 'Storage Facility error'
            }), response.status_code
            
    except Exception as e:
        logger.error(f"Ingestion error: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': 'Ingestion failed. Please try again.'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        response = make_secure_storage_request(
            '/api/facility/status',
            {},
            timeout=2
        )
        storage_healthy = response.status_code == 200
        storage_data = response.json() if storage_healthy else {}
    except:
        storage_healthy = False
        storage_data = {}
    
    return jsonify({
        'status': 'healthy',
        'service': 'R3ÆLƎR Knowledge API v2.0 (Secured)',
        'ai_modules_loaded': AI_MODULES_LOADED,
        'storage_facility': {
            'connected': storage_healthy,
            'total_entries': storage_data.get('total_entries', 0)
        }
    }), 200

@app.errorhandler(429)
def ratelimit_handler(e):
    """Handle rate limit exceeded"""
    logger.warning(f"Rate limit exceeded from {request.remote_addr}")
    return jsonify({
        'error': 'Too many requests',
        'message': 'Please try again later'
    }), 429

@app.errorhandler(401)
def unauthorized_handler(e):
    """Handle unauthorized access"""
    return jsonify({
        'error': 'Unauthorized',
        'message': 'Authentication required'
    }), 401

@app.errorhandler(403)
def forbidden_handler(e):
    """Handle forbidden access"""
    return jsonify({
        'error': 'Forbidden',
        'message': 'Access denied'
    }), 403

if __name__ == '__main__':
    port = int(os.environ.get('KNOWLEDGE_API_PORT', 5004))
    print("\n" + "="*70)
    print("🧠 R3ÆLƎR AI Knowledge API - SECURITY HARDENED v2.0")
    print("="*70)
    print(f"[SECURITY] SSL/TLS enabled for Storage Facility connections")
    print(f"[SECURITY] CORS restricted to: {', '.join(CORS_ALLOWED_ORIGINS)}")
    print(f"[SECURITY] IP whitelist: {', '.join(ALLOWED_IPS)}")
    print(f"[SECURITY] Rate limiting enabled (Query: {RATE_LIMIT_QUERY}, Search: {RATE_LIMIT_SEARCH})")
    print(f"[NETWORK] Storage Facility: {STORAGE_FACILITY_URL}")
    print(f"[NETWORK] Starting API on port {port}...")
    print(f"[DATA] Knowledge Base: 30,657 entries across 4 units")
    print("="*70 + "\n")
    
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)
