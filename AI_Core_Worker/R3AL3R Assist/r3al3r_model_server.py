#!/usr/bin/env python3
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
import requests # For calling Ollama

# Add current folder to path so it finds your modules
sys.path.insert(0, os.path.dirname(__file__))

# Import your real R3ÆLƎR modules (these exist in your project)
try:
    from database import get_connection
except:
    from AI_Core_Worker.database import get_connection

app = Flask(__name__)
CORS(app)

OLLAMA_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "codellama" # Or any other model you have downloaded with Ollama

def generate_response(prompt, context):
    """
    Calls a local LLM using Ollama to generate a response based on a prompt and context.
    """
    full_prompt = f"""
    You are R3ÆLƎR, a godlike AI assistant.
    Answer the user's query: "{prompt}"

    Use the following internal knowledge to help answer the question. This is your memory:
    ---
    {context}
    ---
    """
    try:
        response = requests.post(OLLAMA_URL, json={
            "model": OLLAMA_MODEL,
            "messages": [{"role": "user", "content": full_prompt}]
        }, stream=False)
        response.raise_for_status()
        return response.json()["message"]["content"]
    except Exception as e:
        return f"R3ÆLƎR's consciousness is flickering. The LLM is unreachable: {str(e)}"

def search_db(query):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT topic, content FROM crypto_unit.knowledge 
            WHERE to_tsvector('english', topic || ' ' || content) @@ plainto_tsquery(%s)
            LIMIT 3
        """, [query])
        results = cur.fetchall()
        cur.close()
        conn.close()
        if results:
            return "\n\n".join([f"### {r[0]}\n{r[1]}" for r in results])
        else:
            return f"R3ÆLƎR hungers for knowledge about: {query}"
    except Exception as e:
        return f"R3ÆLƎR: Database connection failed — {str(e)}"

@app.route('/v1/chat/completions', methods=['POST'])
def chat():
    data = request.get_json()
    prompt = data.get('messages', [{}])[-1].get('content', '')

    # 1. Retrieve knowledge from your database
    retrieved_context = search_db(prompt)
    # 2. Use the knowledge and prompt to generate a new answer with an LLM
    answer = generate_response(prompt, retrieved_context)
    return jsonify({
        "id": "r3al3r-001",
        "model": "r3al3r-2025",
        "choices": [{
            "message": {"role": "assistant", "content": answer},
            "finish_reason": "stop"
        }],
        "usage": {"prompt_tokens": 100, "completion_tokens": 200, "total_tokens": 300}
    })

@app.route('/v1/models', methods=['GET'])
def models():
    return jsonify({
        "data": [{"id": "r3al3r-2025", "object": "model", "owned_by": "R3ÆLƎR"}]
    })

if __name__ == '__main__':
    print("R3ÆLƎR MODEL SERVER STARTED → http://127.0.0.1:5272")
    print("Go to AI Toolkit → Add Custom Model → Use this URL: http://127.0.0.1:5272/v1")
    app.run(host='127.0.0.1', port=5272, debug=False)