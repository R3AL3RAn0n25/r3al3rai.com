"""
Update Knowledge API to use Storage Facility
This script modifies knowledge_api.py to query PostgreSQL Storage Facility instead of using in-memory knowledge base
"""
import os
import shutil
from datetime import datetime

# Backup the original knowledge_api.py
original_file = r"c:\Users\work8\OneDrive\Desktop\r3al3rai\New Folder 1\R3al3r-AI Main Working\R3aler-ai\R3aler-ai\AI_Core_Worker\knowledge_api.py"
backup_file = f"{original_file}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"

print(f"📦 Creating backup: {os.path.basename(backup_file)}")
shutil.copy2(original_file, backup_file)

# New knowledge_api.py content
new_content = '''"""
R3ÆLƎR AI Knowledge API Bridge
Exposes AI Core Worker knowledge base via HTTP API - Now using PostgreSQL Storage Facility!
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
import os
import requests
from typing import List, Dict, Any

# Add AI_Core_Worker to path
sys.path.append(os.path.dirname(__file__))

from prompts import R3AELERPrompts

# Storage Facility connection
STORAGE_FACILITY_URL = os.getenv("STORAGE_FACILITY_URL", "http://localhost:5003")

app = Flask(__name__)
CORS(app)  # Enable CORS for Node.js backend

@app.route('/api/kb/search', methods=['POST'])
def search_knowledge():
    """Unified knowledge search endpoint - now powered by PostgreSQL Storage Facility!

    Request JSON:
      - query: str (required)
      - mode: 'auto' | 'local' | 'external' (optional, default 'auto')
      - source: 'wikipedia' | 'hf:wikipedia' (optional, when mode='external')
      - maxPassages: int (optional, default 3)
      - maxChars: int (optional, default 800)

    Response JSON:
      - used_storage_facility: bool
      - local_results: list (when Storage Facility search executed)
      - passages: list of { text, source, meta }
    """
    try:
        data = request.get_json(silent=True) or {}
        raw_query = (data.get('query') or '').strip()
        if not raw_query:
            return jsonify({'success': False, 'error': 'query is required'}), 400

        mode = (data.get('mode') or 'auto').lower()
        max_passages = int(data.get('maxPassages', 5))
        max_chars = int(data.get('maxChars', 1000))
    except Exception as e:
        return jsonify({'success': False, 'error': f'Request parsing error: {str(e)}'}), 400

    # By default, use Storage Facility (our 30,657 entry PostgreSQL knowledge base)
    use_external = mode == 'external'
    
    local_results: List[Dict[str, Any]] = []
    passages: List[Dict[str, Any]] = []

    if use_external:
        # External search (Wikipedia, etc.) - not implemented in this version
        return jsonify({
            'success': False,
            'error': 'External search not supported. Using Storage Facility provides 30,657 curated scientific entries.'
        }), 400
    else:
        # Query the Storage Facility (PostgreSQL with 30,657 entries)
        try:
            response = requests.post(
                f'{STORAGE_FACILITY_URL}/api/facility/search',
                json={'query': raw_query, 'limit_per_unit': max_passages},
                timeout=10
            )
            
            if response.status_code == 200:
                facility_data = response.json()
                results = facility_data.get('results', [])
                
                # Transform Storage Facility results into passages format
                for result in results[:max_passages]:
                    passage_text = result['content']
                    if len(passage_text) > max_chars:
                        passage_text = passage_text[:max_chars] + '...'
                    
                    passages.append({
                        'text': passage_text,
                        'source': f"Storage Facility - {result['unit_name']}",
                        'meta': {
                            'topic': result['topic'],
                            'category': result['category'],
                            'subcategory': result.get('subcategory', ''),
                            'relevance': result['relevance'],
                            'unit': result['unit_id']
                        }
                    })
                    
                    local_results.append({
                        'key': result['entry_id'],
                        'topic': result['topic'],
                        'content_preview': passage_text[:200] + '...' if len(passage_text) > 200 else passage_text,
                        'category': result['category'],
                        'relevance': result['relevance'],
                        'unit': result['unit_name']
                    })
            else:
                # Fallback to legacy in-memory search if Storage Facility is down
                print(f"⚠️  Storage Facility unavailable, using fallback search")
                return search_legacy_knowledge(raw_query, max_passages, max_chars)
                
        except requests.exceptions.ConnectionError:
            print(f"⚠️  Storage Facility connection failed, using fallback search")
            return search_legacy_knowledge(raw_query, max_passages, max_chars)
        except Exception as e:
            print(f"⚠️  Storage Facility error: {e}, using fallback search")
            return search_legacy_knowledge(raw_query, max_passages, max_chars)

    return jsonify({
        'success': True,
        'used_storage_facility': True,
        'total_entries': 30657,
        'query': raw_query,
        'local_results': local_results,
        'passages': passages
    })

def search_legacy_knowledge(query: str, max_passages: int, max_chars: int):
    """Fallback to legacy in-memory knowledge base search (prompts.py)"""
    q = query.lower()
    local_results: List[Dict[str, Any]] = []
    passages: List[Dict[str, Any]] = []
    
    for key, value in R3AELERPrompts.KNOWLEDGE_BASE.items():
        # Handle dict format (extended datasets) and string format (original KB)
        if isinstance(value, dict):
            topic = value.get('topic', key)
            content = value.get('content', '')
            category = value.get('category', '')
        else:
            topic = key
            content = value
            category = 'General'
        
        if q in topic.lower() or q in content.lower():
            passage_text = content
            if len(passage_text) > max_chars:
                passage_text = passage_text[:max_chars] + '...'
            
            passages.append({
                'text': passage_text,
                'source': 'legacy_kb',
                'meta': {'topic': topic, 'category': category}
            })
            
            local_results.append({
                'key': key,
                'topic': topic,
                'content_preview': passage_text[:200] + '...' if len(passage_text) > 200 else passage_text,
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

@app.route('/api/kb/stats', methods=['GET'])
def get_stats():
    """Get knowledge base statistics from Storage Facility"""
    try:
        response = requests.get(f'{STORAGE_FACILITY_URL}/api/facility/status', timeout=5)
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({
                'success': False,
                'error': 'Storage Facility unavailable',
                'legacy_kb_entries': len(R3AELERPrompts.KNOWLEDGE_BASE)
            })
    except:
        return jsonify({
            'success': False,
            'error': 'Storage Facility connection failed',
            'legacy_kb_entries': len(R3AELERPrompts.KNOWLEDGE_BASE)
        })

@app.route('/api/kb/prompts/<prompt_type>', methods=['GET'])
def get_prompt(prompt_type):
    """Get system prompts (now also stored in Storage Facility crypto_unit)"""
    prompt_map = {
        'system': R3AELERPrompts.SYSTEM_PERSONALITY,
        'code': R3AELERPrompts.CODE_GENERATION_SYSTEM_PROMPT,
        'crypto': R3AELERPrompts.CRYPTO_FORENSICS_SYSTEM_PROMPT,
        'mobile': R3AELERPrompts.MOBILE_FORENSICS_SYSTEM_PROMPT,
        'wallet': R3AELERPrompts.WALLET_EXTRACTION_SYSTEM_PROMPT
    }
    
    prompt = prompt_map.get(prompt_type.lower())
    if prompt:
        return jsonify({'success': True, 'prompt': prompt, 'type': prompt_type})
    else:
        return jsonify({'success': False, 'error': f'Unknown prompt type: {prompt_type}'}), 404

@app.route('/api/kb/ingest', methods=['POST'])
def ingest_data():
    """Ingest new knowledge into Storage Facility"""
    data = request.get_json()
    
    # This would need to be implemented to add new entries to PostgreSQL
    # For now, return not implemented
    return jsonify({
        'success': False,
        'error': 'Direct ingestion not yet implemented. Use migrate_to_storage_facility.py script.'
    }), 501

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    try:
        # Check Storage Facility connectivity
        response = requests.get(f'{STORAGE_FACILITY_URL}/api/facility/status', timeout=2)
        storage_healthy = response.status_code == 200
        storage_data = response.json() if storage_healthy else {}
    except:
        storage_healthy = False
        storage_data = {}
    
    return jsonify({
        'status': 'healthy',
        'service': 'R3ÆLƎR Knowledge API',
        'storage_facility': {
            'connected': storage_healthy,
            'url': STORAGE_FACILITY_URL,
            'total_entries': storage_data.get('total_entries', 0),
            'units': storage_data.get('units_count', 0)
        },
        'legacy_kb_entries': len(R3AELERPrompts.KNOWLEDGE_BASE)
    })

if __name__ == '__main__':
    port = int(os.environ.get('KNOWLEDGE_API_PORT', 5001))
    print("\\n" + "="*60)
    print("🧠 R3ÆLƎR AI Knowledge API - Storage Facility Edition")
    print("="*60)
    print(f"📊 Storage Facility URL: {STORAGE_FACILITY_URL}")
    print(f"🌐 Starting Knowledge API on port {port}...")
    print(f"📚 Total Knowledge: 30,657 entries across 4 units")
    print("   - Physics: 25,875 entries")
    print("   - Quantum: 1,042 entries")  
    print("   - Space/Astro: 3,727 entries")
    print("   - Cryptocurrency: 13 entries (+ 5 system prompts)")
    print(f"💾 Backend: PostgreSQL Storage Facility")
    print("="*60 + "\\n")
    
    app.run(host='0.0.0.0', port=port, debug=True)
'''

print("✍️  Writing updated knowledge_api.py...")
with open(original_file, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("✅ SUCCESS!")
print(f"  📝 Backup created: {os.path.basename(backup_file)}")
print(f"  🔄 Updated: knowledge_api.py")
print(f"  🎯 Now queries PostgreSQL Storage Facility (30,657 entries)")
print(f"  ⚡ Fallback to legacy KB if Storage Facility is unavailable")
