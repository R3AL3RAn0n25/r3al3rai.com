"""
Example: How to integrate Physics Knowledge into your AI
"""

# OPTION 1: Add endpoint to knowledge_api.py to load physics data
# ================================================================

# Add this at the top of knowledge_api.py:
import json
from pathlib import Path

# Global cache for physics knowledge
PHYSICS_KNOWLEDGE_CACHE = None

def load_physics_knowledge():
    """Load physics knowledge from JSON file (cached)"""
    global PHYSICS_KNOWLEDGE_CACHE
    
    if PHYSICS_KNOWLEDGE_CACHE is None:
        json_path = Path(__file__).parent / 'physics_knowledge_base.json'
        with open(json_path, 'r', encoding='utf-8') as f:
            PHYSICS_KNOWLEDGE_CACHE = json.load(f)
    
    return PHYSICS_KNOWLEDGE_CACHE

# Add this route to knowledge_api.py:
@app.route('/api/kb/physics/search', methods=['POST'])
def search_physics():
    """Search physics knowledge base
    Body: { query: string, limit?: number }
    """
    data = request.get_json(silent=True) or {}
    query = (data.get('query') or '').lower().strip()
    limit = int(data.get('limit', 10))
    
    if not query:
        return jsonify({'success': False, 'error': 'query required'}), 400
    
    # Load physics knowledge
    physics_data = load_physics_knowledge()
    
    # Simple search - find matching questions or answers
    results = []
    for entry in physics_data:
        if (query in entry.get('question', '').lower() or 
            query in entry.get('answer', '').lower() or
            query in entry.get('category', '').lower()):
            results.append({
                'topic': entry['topic'],
                'question': entry['question'][:200] + '...' if len(entry['question']) > 200 else entry['question'],
                'answer': entry['answer'][:300] + '...' if len(entry['answer']) > 300 else entry['answer'],
                'category': entry.get('category', 'Physics'),
                'source': entry.get('source', 'HuggingFace')
            })
            
            if len(results) >= limit:
                break
    
    return jsonify({
        'success': True,
        'query': query,
        'results': results,
        'total_found': len(results)
    })

@app.route('/api/kb/physics/random', methods=['GET'])
def get_random_physics():
    """Get random physics problem"""
    import random
    physics_data = load_physics_knowledge()
    problem = random.choice(physics_data)
    
    return jsonify({
        'success': True,
        'problem': problem
    })

@app.route('/api/kb/physics/stats', methods=['GET'])
def get_physics_stats():
    """Get physics knowledge base statistics"""
    physics_data = load_physics_knowledge()
    
    return jsonify({
        'success': True,
        'total_problems': len(physics_data),
        'categories': list(set(p.get('category', 'Physics') for p in physics_data)),
        'source': 'HuggingFace: multimodal-reasoning-lab/Physics'
    })


# OPTION 2: Store in PostgreSQL Database
# =======================================

# SQL to create physics_knowledge table:
CREATE_PHYSICS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS physics_knowledge (
    id SERIAL PRIMARY KEY,
    topic VARCHAR(255) NOT NULL,
    question TEXT NOT NULL,
    reasoning TEXT,
    answer TEXT NOT NULL,
    category VARCHAR(100) DEFAULT 'Physics',
    source VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Full text search index
    search_vector tsvector GENERATED ALWAYS AS (
        to_tsvector('english', coalesce(question, '') || ' ' || coalesce(answer, ''))
    ) STORED
);

-- Create index for faster searching
CREATE INDEX IF NOT EXISTS idx_physics_search ON physics_knowledge USING GIN(search_vector);
CREATE INDEX IF NOT EXISTS idx_physics_category ON physics_knowledge(category);
"""

# Python code to import JSON into PostgreSQL:
def import_physics_to_postgres():
    """Import physics_knowledge_base.json into PostgreSQL"""
    import psycopg2
    import json
    
    # Load JSON
    with open('AI_Core_Worker/physics_knowledge_base.json', 'r') as f:
        physics_data = json.load(f)
    
    # Connect to database
    conn = psycopg2.connect(
        host='localhost',
        port=5432,
        database='r3aler_ai',
        user='r3aler_user_2025',
        password='postgres'
    )
    cur = conn.cursor()
    
    # Create table
    cur.execute(CREATE_PHYSICS_TABLE_SQL)
    
    # Insert data
    for entry in physics_data:
        cur.execute("""
            INSERT INTO physics_knowledge (topic, question, reasoning, answer, category, source)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            entry['topic'],
            entry['question'],
            entry.get('reasoning', ''),
            entry['answer'],
            entry.get('category', 'Physics'),
            entry.get('source', 'HuggingFace')
        ))
    
    conn.commit()
    cur.close()
    conn.close()
    
    print(f"✓ Imported {len(physics_data)} physics problems to PostgreSQL")


# OPTION 3: Add to prompts.py KNOWLEDGE_BASE
# ===========================================

# Add to AI_Core_Worker/prompts.py:
# (Already generated in physics_kb_import.py - just copy it over)

from physics_kb_import import PHYSICS_KNOWLEDGE_BASE

# Then merge into existing KNOWLEDGE_BASE:
class R3AELERPrompts:
    KNOWLEDGE_BASE = {
        # ... existing knowledge ...
        **PHYSICS_KNOWLEDGE_BASE  # Add physics knowledge
    }


# RECOMMENDATION
# ==============
print("""
RECOMMENDED APPROACH: Option 2 (JSON File with caching)

Why?
✓ Fast (loaded once, cached in memory)
✓ Easy to update (just regenerate JSON)
✓ No database overhead
✓ Can fetch more problems anytime
✓ Already implemented above

Just add the routes to knowledge_api.py and restart the Knowledge API service!

Then test with:
curl -X POST http://localhost:5001/api/kb/physics/search \\
  -H "Content-Type: application/json" \\
  -d '{"query": "atwood machine", "limit": 3}'
""")
