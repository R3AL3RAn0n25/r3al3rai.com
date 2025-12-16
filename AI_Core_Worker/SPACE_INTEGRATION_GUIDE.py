"""
SPACE ENGINEERING DATASET INTEGRATION GUIDE
============================================

This guide shows you how to integrate the Space Engineering dataset
into your R3ALER AI knowledge base.

Dataset: patrickfleith/synthgenai-space-engineering-instruct-1k
Processed: 100 entries
Categories: Space Mission Engineering

"""

# ============================================================================
# OPTION 1: Load from JSON File (RECOMMENDED)
# ============================================================================

import json

def load_space_engineering_knowledge():
    """
    Load Space Engineering knowledge base from JSON file.
    This is the recommended method for production use.
    """
    with open('space_engineering_knowledge_base.json', 'r', encoding='utf-8') as f:
        space_kb = json.load(f)
    
    # Convert list to dictionary format for knowledge_api.py
    knowledge_dict = {}
    for idx, entry in enumerate(space_kb):
        key = f"space_eng_{entry['keyword']}_{idx}"
        knowledge_dict[key] = {
            "content": f"{entry['question']}\n\n{entry['answer']}",
            "topic": entry['topic'],
            "category": entry['category'],
            "tags": entry['tags'],
            "source": entry['source']
        }
    
    return knowledge_dict


# ============================================================================
# OPTION 2: Direct Integration into knowledge_api.py
# ============================================================================

"""
To add Space Engineering knowledge to your knowledge_api.py:

1. Open: AI_Core_Worker/knowledge_api.py

2. Add this import at the top:
   from space_engineering_kb_import import SPACE_ENGINEERING_KB

3. In the R3AELERPrompts class, update KNOWLEDGE_BASE:
   
   KNOWLEDGE_BASE = {
       # ... existing knowledge ...
       
       **SPACE_ENGINEERING_KB,  # Add Space Engineering knowledge
   }

4. Restart Knowledge API:
   cd application/Backend
   wsl python3 ../AI_Core_Worker/knowledge_api.py
"""


# ============================================================================
# OPTION 3: PostgreSQL Database Storage (ADVANCED)
# ============================================================================

"""
For production deployments, store knowledge in PostgreSQL:

1. Create knowledge table:
"""

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS knowledge_base (
    id SERIAL PRIMARY KEY,
    topic VARCHAR(500) NOT NULL,
    keyword VARCHAR(200),
    category VARCHAR(200),
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    system_context TEXT,
    language VARCHAR(50) DEFAULT 'English',
    source VARCHAR(500),
    tags JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_knowledge_topic ON knowledge_base(topic);
CREATE INDEX idx_knowledge_keyword ON knowledge_base(keyword);
CREATE INDEX idx_knowledge_category ON knowledge_base(category);
CREATE INDEX idx_knowledge_tags ON knowledge_base USING GIN(tags);
"""

def import_to_postgres():
    """
    Import Space Engineering knowledge into PostgreSQL.
    """
    import psycopg2
    import json
    
    # Database connection
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="r3aler_ai",
        user="r3aler_user_2025",
        password="postgres"
    )
    cur = conn.cursor()
    
    # Create table if not exists
    cur.execute(CREATE_TABLE_SQL)
    
    # Load data
    with open('space_engineering_knowledge_base.json', 'r') as f:
        knowledge = json.load(f)
    
    # Insert entries
    insert_sql = """
    INSERT INTO knowledge_base 
    (topic, keyword, category, question, answer, system_context, language, source, tags)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    for entry in knowledge:
        cur.execute(insert_sql, (
            entry['topic'],
            entry['keyword'],
            entry['category'],
            entry['question'],
            entry['answer'],
            entry.get('system_context', ''),
            entry.get('language', 'English'),
            entry['source'],
            json.dumps(entry['tags'])
        ))
    
    conn.commit()
    cur.close()
    conn.close()
    
    print(f"✅ Imported {len(knowledge)} Space Engineering entries to PostgreSQL!")


# ============================================================================
# OPTION 4: API Endpoint for Knowledge Search
# ============================================================================

"""
Add specialized endpoint in knowledge_api.py for Space Engineering queries:
"""

def add_space_engineering_endpoint():
    """
    Example Flask endpoint for Space Engineering knowledge search.
    Add this to knowledge_api.py:
    """
    code = '''
@app.route('/api/kb/space-engineering/search', methods=['POST'])
def search_space_engineering():
    """Search specifically in Space Engineering knowledge base."""
    data = request.json
    query = data.get('query', '').lower()
    
    if not query:
        return jsonify({"error": "Query required"}), 400
    
    # Load Space Engineering knowledge
    with open('space_engineering_knowledge_base.json', 'r') as f:
        space_kb = json.load(f)
    
    # Search for matches
    results = []
    for entry in space_kb:
        # Check if query matches in question, answer, or keyword
        if (query in entry['question'].lower() or 
            query in entry['answer'].lower() or 
            query in entry['keyword'].lower() or
            query in entry['topic'].lower()):
            
            results.append({
                "topic": entry['topic'],
                "question": entry['question'],
                "answer": entry['answer'][:300] + "...",  # Truncate long answers
                "relevance": "high" if query in entry['question'].lower() else "medium"
            })
    
    # Sort by relevance
    results.sort(key=lambda x: x['relevance'], reverse=True)
    
    return jsonify({
        "success": True,
        "query": query,
        "results": results[:5],  # Return top 5 results
        "total_found": len(results)
    })

@app.route('/api/kb/space-engineering/random', methods=['GET'])
def random_space_fact():
    """Get a random Space Engineering fact."""
    import random
    
    with open('space_engineering_knowledge_base.json', 'r') as f:
        space_kb = json.load(f)
    
    entry = random.choice(space_kb)
    
    return jsonify({
        "success": True,
        "topic": entry['topic'],
        "question": entry['question'],
        "answer": entry['answer']
    })
'''
    return code


# ============================================================================
# TESTING THE INTEGRATION
# ============================================================================

def test_space_knowledge():
    """
    Test that Space Engineering knowledge is accessible.
    """
    import requests
    
    # Test search endpoint
    response = requests.post(
        'http://localhost:5001/api/kb/space-engineering/search',
        json={"query": "satellite calibration"}
    )
    
    if response.status_code == 200:
        print("✅ Space Engineering search working!")
        data = response.json()
        print(f"   Found {data['total_found']} results")
        if data['results']:
            print(f"   Top result: {data['results'][0]['topic']}")
    else:
        print("❌ Search endpoint not working")
    
    # Test random fact
    response = requests.get('http://localhost:5001/api/kb/space-engineering/random')
    
    if response.status_code == 200:
        print("✅ Random fact endpoint working!")
        data = response.json()
        print(f"   Topic: {data['topic']}")
    else:
        print("❌ Random fact endpoint not working")


# ============================================================================
# QUICK START COMMANDS
# ============================================================================

QUICK_START = """
QUICK START: Integrate Space Engineering Dataset
=================================================

1️⃣  VERIFY FILES CREATED:
   ls -lh space_engineering*
   
   You should see:
   - space_engineering_raw.json (150 KB)
   - space_engineering_knowledge_base.json (171 KB)
   - space_engineering_kb_import.py (50 KB)

2️⃣  OPTION A: Simple Integration (Fastest)
   
   Edit: AI_Core_Worker/knowledge_api.py
   
   Add at top:
   ```python
   from space_engineering_kb_import import SPACE_ENGINEERING_KB
   ```
   
   Update KNOWLEDGE_BASE dictionary:
   ```python
   KNOWLEDGE_BASE = {
       # ... existing entries ...
       **SPACE_ENGINEERING_KB
   }
   ```
   
   Restart Knowledge API:
   ```bash
   cd application/Backend
   wsl python3 ../../AI_Core_Worker/knowledge_api.py
   ```

3️⃣  OPTION B: Database Storage (Production)
   
   Run in Python:
   ```python
   from SPACE_INTEGRATION_GUIDE import import_to_postgres
   import_to_postgres()
   ```
   
   Then update knowledge_api.py to query from PostgreSQL

4️⃣  TEST IT WORKS:
   
   Ask R3ALER AI:
   "Explain satellite attitude sensor calibration"
   "What is space mission engineering?"
   "Tell me about spacecraft systems"
   
   The AI should use the Space Engineering knowledge!

5️⃣  VERIFY IN LOGS:
   
   Check that knowledge_api.py is finding matches:
   ```bash
   tail -f logs/knowledge_api.log
   ```

=================================================
Dataset Info:
- Total Entries: 100
- Category: Space Mission Engineering
- Topics: Attitude sensors, spacecraft systems, 
          orbital mechanics, mission planning, etc.
- Format: Q&A with system context
=================================================
"""

if __name__ == '__main__':
    print(QUICK_START)
    print("\n" + "="*60)
    print("💡 Choose integration option above and follow steps!")
    print("="*60)
