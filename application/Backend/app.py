from flask import Flask, request, jsonify, render_template
from flask_cors import CORS  # Import the CORS library
import sqlite3
import hashlib
import datetime
import sys
import os

# Your configuration imports
if os.environ.get('FLASK_ENV') == 'production':
    from production_config import ProductionConfig as AppConfig
else:
    from config import AppConfig

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'AI_Core_Worker'))
sys.path.append(os.path.dirname(__file__))
from ai_core_worker import RealerAI

# --- APP INITIALIZATION ---
# Point Flask to the React build directory for static files and the main index.html
app = Flask(__name__, static_folder='../../build/static', template_folder='../../build')
# This is the crucial line to allow your frontend to communicate with this backend
CORS(app)

def get_db():
    return sqlite3.connect(AppConfig.DATABASE_PATH)

# Serve React App
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    return render_template('index.html')

# Initialize AI Core with optional OpenAI integration
openai_api_key = os.environ.get("OPENAI_API_KEY")
ai_core = RealerAI(AppConfig, get_db, openai_api_key)


# --- ROUTE FOR THE AI VOICE INTERFACE ---
@app.route('/api/process-command', methods=['POST'])
def process_command():
    try:
        data = request.json
        # 1. Accept the incoming message from the 'text' key to match the frontend
        user_text = data.get('text', '')
        user_id = data.get('user_id', 'anonymous') # Assuming you might send this later
        conversation_history = data.get('conversation_history', []) # Assuming you might send this later

        if not user_text.strip():
            return jsonify({"error": "Message cannot be empty"}), 400

        # Process message through your AI Core
        ai_response = ai_core.process_chat(user_text, user_id, conversation_history)

        # 2. Send the response back in the 'responseText' key to match the frontend
        return jsonify({
            "responseText": ai_response
        })

    except Exception as e:
        # Provide a clear error message back to the frontend if something goes wrong
        error_message = f"AI processing error: {str(e)}"
        print(error_message) # Also print to backend console for debugging
        return jsonify({"responseText": f"An internal error occurred: {str(e)}"}), 500


# --- YOUR EXISTING ROUTES (UNCHANGED) ---

@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute('SELECT id, username FROM users WHERE username = ? AND password_hash = ?', (username, password_hash))
            user = cursor.fetchone()
        finally:
            cursor.close()
            db.close()
        if user:
            return jsonify({'token': 'mock-token', 'success': True})
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/register', methods=['POST'])
def register():
    try:
        data = request.json
        full_name = data.get('full_name')
        date_of_birth = data.get('date_of_birth')
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')

        if not all([full_name, date_of_birth, email, username, password]):
            return jsonify({"success": False, "error": "All fields required"}), 400

        system_email = f"@{username}@R3ÆLƎRAI.com"
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
            if cursor.fetchone():
                return jsonify({"success": False, "error": "Username already exists"}), 400
            cursor.execute('INSERT INTO users (username, password_hash, email) VALUES (?, ?, ?)', (username, password_hash, email))
            db.commit()
        finally:
            cursor.close()
            db.close()
        return jsonify({"success": True, "username": username, "system_email": system_email})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/generate-code', methods=['POST'])
def generate_code():
    try:
        data = request.json
        language = data.get('language', '')
        task = data.get('task', '')
        requirements = data.get('requirements', '')
        if not language or not task:
            return jsonify({"error": "Language and task are required"}), 400
        result = ai_core.generate_code_with_ai(language, task, requirements)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": f"Code generation error: {str(e)}"}), 500

@app.route('/api/forensic-analysis', methods=['POST'])
def forensic_analysis():
    try:
        data = request.json
        file_info = data.get('file_info', '')
        analysis_type = data.get('analysis_type', '')
        if not file_info or not analysis_type:
            return jsonify({"error": "File info and analysis type are required"}), 400
        result = ai_core.analyze_forensics_with_ai(file_info, analysis_type)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": f"Forensic analysis error: {str(e)}"}), 500

@app.route('/api/ai-status', methods=['GET'])
def ai_status():
    try:
        openai_available = bool(getattr(ai_core, 'openai_integration', None))
        adaptability_level = getattr(ai_core, 'adaptability_level', None)
        total_insights = len(getattr(ai_core, 'insights', []))
        knowledge_sources = None
        try:
            heart = getattr(ai_core, 'heart', None)
            if heart and hasattr(heart, 'get_db'):
                db_list = heart.get_db()
                knowledge_sources = len(db_list) if hasattr(db_list, '__len__') else 0
            else:
                knowledge_sources = 0
        except Exception:
            knowledge_sources = 0
        return jsonify({
            "openai_available": openai_available,
            "adaptability_level": adaptability_level,
            "total_insights": total_insights,
            "knowledge_sources": knowledge_sources,
            "status": "ok"
        })
    except Exception as e:
        return jsonify({
            "status": "error", "error": str(e), "openai_available": False,
            "adaptability_level": None, "total_insights": 0, "knowledge_sources": 0
        }), 200


# --- START THE SERVER ---
if __name__ == "__main__":
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    # 3. Run on port 3000 to match the frontend
    app.run(host="0.0.0.0", port=3000, debug=debug_mode)