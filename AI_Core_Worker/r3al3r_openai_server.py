#!/usr/bin/env python3
"""
R3ÆLƎR OpenAI-Compatible Model Server — for VS Code AI Toolkit
Runs on port 5272, exposes your DB as an AI model
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from self_hosted_storage_facility import StorageFacility  # your existing
from intelligence_layer import get_intelligence_layer  # your existing
from prompts import R3AELERPrompts  # your prompts

app = Flask(__name__)
CORS(app)
facility = StorageFacility()
intelligence = get_intelligence_layer()

@app.route('/v1/chat/completions', methods=['POST'])
def chat_completions():
    data = request.json
    messages = data.get('messages', [])
    prompt = messages[-1].get('content', '') if messages else data.get('prompt', '')
    model = data.get('model', 'r3al3r-2025')

    # Use your real R3ÆLƎR brain
    context = R3AELERPrompts.analyze_context(prompt)
    results = intelligence.intelligent_search(prompt)
    response_text = results.get('response', f"R3ÆLƎR: {prompt} — I am learning from this.")

    # Add R3ÆLƎR personality
    response_text = f"R3ÆLƎR: {response_text}\n\n— Self-learning active. Gaps filled: {len(results.get('gaps', []))}"

    return jsonify({
        "id": "r3al3r-chat-1",
        "object": "chat.completion",
        "created": int(os.times()[4]),
        "model": model,
        "choices": [{
            "index": 0,
            "message": {"role": "assistant", "content": response_text},
            "finish_reason": "stop"
        }],
        "usage": {"prompt_tokens": len(prompt.split()), "completion_tokens": 200, "total_tokens": 300}
    })

@app.route('/v1/models', methods=['GET'])
def models():
    return jsonify([{
        "id": "r3al3r-2025",
        "object": "model",
        "created": 1730419200,
        "owned_by": "r3al3r"
    }])

if __name__ == '__main__':
    print("R3ÆLƎR Model Server starting on http://127.0.0.1:5273...")
    app.run(host='127.0.0.1', port=5273, debug=False)