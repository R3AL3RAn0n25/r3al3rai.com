# R3ÆLƎR AI AWS Server Setup Script
# This script ONLY configures the server environment. It does NOT upload any files.
# It assumes all necessary application files are already on the server at /home/ubuntu/R3ÆLƎR AI/
param(
    [Parameter(Mandatory=$true)]
    [string]$PublicIP,

    [Parameter(Mandatory=$true)]
    [string]$KeyPath
)

Write-Host "--- Starting Server Configuration for R3ÆLƎR AI on $PublicIP ---"

# This is the script that will be executed on the remote server.
$RemoteSetupScript = @"

# Exit immediately if a command exits with a non-zero status.
set -e

echo "--- Setting up R3ÆLƎR AI Server Environment ---"

# Define source and destination directories
SOURCE_DIR="/home/ubuntu/R3ÆLƎR\ AI"
APP_DIR="/opt/r3aler-ai"

# --- 1. System Preparation ---
echo "Updating system packages..."
sudo apt-get update && sudo apt-get upgrade -y

echo "Installing dependencies (Python, Nginx, Node.js)..."
sudo apt-get install -y python3 python3-pip python3-venv nginx sqlite3 git curl
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# --- 2. Application Setup ---
echo "Preparing application directory at $APP_DIR..."
sudo rm -rf "$APP_DIR"
sudo mkdir -p "$APP_DIR"
sudo cp -r "$SOURCE_DIR"/* "$APP_DIR"/
sudo chown -R ubuntu:ubuntu "$APP_DIR"
cd "$APP_DIR"

# --- 3. Frontend Build ---
echo "Building frontend application (npm install & build)..."
npm install
npm run build

# --- 4. Backend Setup ---
echo "Setting up Python backend environment..."
python3 -m venv venv
source venv/bin/activate
pip install Flask==2.3.3 openai==1.3.0 requests gunicorn

echo "Initializing database..."
mkdir -p data logs
sqlite3 data/realer_ai.db < Database/schema.sql || echo "Database already exists or schema failed."

# --- 5. Create a wrapper to run the Flask App correctly ---
echo "Creating application runner..."
tee /opt/r3aler-ai/run.py > /dev/null <<'EOF'
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, '/opt/r3aler-ai')

# Import the app object from the backend module
from backend.app import app

EOF

# --- 5. Service Configuration ---
echo "Configuring systemd service for the backend..."
sudo tee /etc/systemd/system/r3aler-ai.service > /dev/null <<'EOF'
[Unit]
Description=R3ALER AI Application
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/opt/r3aler-ai
Environment="PATH=/opt/r3aler-ai/venv/bin"
Environment="FLASK_ENV=production"
Environment="PYTHONPATH=/opt/r3aler-ai"
ExecStart=/opt/r3aler-ai/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:5000 run:app
Restart=always

[Install]
WantedBy=multi-user.target
EOF

echo "Configuring Nginx web server..."
sudo tee /etc/nginx/sites-available/r3aler-ai > /dev/null <<'EOF'
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    location /static {
        # Serves static files from the frontend build output
        alias /opt/r3aler-ai/build/static;
    }
}
EOF

sudo ln -sf /etc/nginx/sites-available/r3aler-ai /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# --- 6. Start Services ---
echo "Starting and enabling services..."
sudo systemctl daemon-reload
sudo systemctl enable r3aler-ai
sudo systemctl restart r3aler-ai
sudo systemctl enable nginx
sudo systemctl restart nginx

echo "--- Final Service Status ---"
sleep 2 # Wait a moment for services to stabilize
sudo systemctl status r3aler-ai --no-pager
sudo systemctl status nginx --no-pager

echo "--- Server setup complete! Application should be live. ---"
"@

# Convert Windows line endings (\r\n) to Unix line endings (\n) to prevent script errors on Linux.
$CleanRemoteSetupScript = $RemoteSetupScript -replace "`r`n", "`n"

Write-Host "Connecting to server to run the setup script..."
ssh -i $KeyPath ubuntu@$PublicIP $CleanRemoteSetupScript

Write-Host "Configuration finished. Application should be available at: http://$PublicIP"