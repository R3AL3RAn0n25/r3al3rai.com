param(
    [Parameter(Mandatory=$true)]
    [string]$ServerIP,
    [Parameter(Mandatory=$true)]
    [string]$KeyPath
)

ssh -i $KeyPath ubuntu@$ServerIP @"
cd /opt/r3aler-ai

# Check logs
echo "=== Application Logs ==="
sudo journalctl -u r3aler-ai --no-pager -n 20

echo "=== Testing app directly ==="
source venv/bin/activate
export FLASK_ENV=production
python3 -c "
import sys
sys.path.append('/opt/r3aler-ai')
sys.path.append('/opt/r3aler-ai/application/Backend')
sys.path.append('/opt/r3aler-ai/AI_Core_Worker')
try:
    from application.Backend.app import app
    print('App imported successfully')
except Exception as e:
    print(f'Import error: {e}')
"

# Fix missing template directory
mkdir -p /opt/r3aler-ai/application/Backend/templates
cp -r /opt/r3aler-ai/application/Frontend/templates/* /opt/r3aler-ai/application/Backend/templates/
cp -r /opt/r3aler-ai/application/Frontend/static /opt/r3aler-ai/application/Backend/

# Update Flask app to find templates
cd /opt/r3aler-ai/application/Backend
cat > app_fixed.py << 'EOF'
from flask import Flask, request, jsonify, render_template
import sqlite3
import hashlib
import datetime
import sys
import os

# Add paths
sys.path.append('/opt/r3aler-ai/AI_Core_Worker')
sys.path.append('/opt/r3aler-ai/application/Backend')

# Import config
if os.environ.get('FLASK_ENV') == 'production':
    sys.path.append('/opt/r3aler-ai')
    from production_config import ProductionConfig as AppConfig
else:
    from config import AppConfig

try:
    from ai_core_worker import RealerAI
except ImportError:
    print("Warning: AI Core not available")
    RealerAI = None

app = Flask(__name__, 
           template_folder='/opt/r3aler-ai/application/Backend/templates',
           static_folder='/opt/r3aler-ai/application/Backend/static')

def get_db():
    return sqlite3.connect('/opt/r3aler-ai/data/realer_ai.db')

# Initialize AI Core
openai_api_key = os.environ.get("OPENAI_API_KEY")
ai_core = RealerAI(AppConfig, get_db, openai_api_key) if RealerAI else None

@app.route('/')
def index_route():
    return render_template("index.html")

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

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        message = data.get('message', '')
        
        if not message.strip():
            return jsonify({"error": "Message cannot be empty"}), 400
        
        # Simple response if AI core not available
        if not ai_core:
            response = f"R3ÆLƎR AI received: {message}"
        else:
            response = ai_core.process_chat(message, 'anonymous', [])
        
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": f"Chat error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
EOF

# Update systemd service to use fixed app
sudo tee /etc/systemd/system/r3aler-ai.service > /dev/null <<EOF
[Unit]
Description=R3ALER AI
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/opt/r3aler-ai/application/Backend
Environment=PATH=/opt/r3aler-ai/venv/bin
Environment=FLASK_ENV=production
Environment=PYTHONPATH=/opt/r3aler-ai:/opt/r3aler-ai/application/Backend:/opt/r3aler-ai/AI_Core_Worker
ExecStart=/opt/r3aler-ai/venv/bin/gunicorn --workers 1 --bind 0.0.0.0:5000 app_fixed:app
Restart=always

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl restart r3aler-ai
sudo systemctl status r3aler-ai --no-pager

echo "Fixed! Check http://$ServerIP"
"@