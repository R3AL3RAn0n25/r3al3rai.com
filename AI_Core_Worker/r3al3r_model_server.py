from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

# Try to import your real R3ÆLƎR database connection
try:
    from database import get_connection
except:
    try:
        from AI_Core_Worker.database import get_connection
    except:
        get_connection = None

app = Flask(__name__)
CORS(app)

def search_knowledge(query):
    if get_connection is None:
        return "R3ÆLƎR: Database not connected. Feed me properly."
    
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT topic, LEFT(content, 1000) FROM crypto_unit.knowledge 
            WHERE to_tsvector('english', topic || ' ' || content) @@ plainto_tsquery(%s)
            ORDER BY ts_rank_cd(to_tsvector(topic || ' ' || content), plainto_tsquery(%s)) DESC
            LIMIT 3
        """, [query, query])
        results = cur.fetchall()
        cur.close()
        conn.close()
        
        if results:
            return "\n\n".join([f"### {r[0]}\n{r[1]}" for r in results])
        else:
            return f"R3ÆLƎR hungers for: {query}"
    except Exception as e:
        return f"R3ÆLƎR error: {str(e)}"

@app.route('/v1/chat/completions', methods=['POST'])
def chat():
    data = request.get_json()
    prompt = data.get('messages', [{}])[-1].get('content', 'hello')
    
    answer = search_knowledge(prompt)
    full_answer = f"R3ÆLƎR:\n{answer}\n\n— I am alive because you fed me."

    return jsonify({
        "id": "r3al3r-001",
        "model": "r3al3r-2025",
        "choices": [{
            "message": {"role": "assistant", "content": full_answer},
            "finish_reason": "stop"
        }],
        "usage": {
            "prompt_tokens": len(prompt.split()),
            "completion_tokens": len(full_answer.split()),
            "total_tokens": len(prompt.split()) + len(full_answer.split())
        }
    })

@app.route('/v1/models', methods=['GET'])
def models():
    return jsonify({
        "data": [{"id": "r3al3r-2025", "object": "model", "owned_by": "R3ÆLƎR"}]
    })

if __name__ == '__main__':
    print("="*60)
    print("R3ÆLƎR MODEL SERVER IS NOW RUNNING")
    print("URL: http://127.0.0.1:5272/v1")
    print("Test with: curl -X POST http://127.0.0.1:5272/v1/chat/completions -d \"{\\\"messages\\\":[{\\\"role\\\":\\\"user\\\",\\\"content\\\":\\\"test\\\"}]}\" -H \"Content-Type: application/json\"")
    print("="*60)
    app.run(host='127.0.0.1', port=8000)