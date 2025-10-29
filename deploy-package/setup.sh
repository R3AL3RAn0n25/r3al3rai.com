#!/bin/bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv nginx sqlite3

sudo mkdir -p /opt/r3aler-ai
sudo chown ubuntu:ubuntu /opt/r3aler-ai
cd /opt/r3aler-ai

python3 -m venv venv
source venv/bin/activate
pip install Flask==2.3.3 openai==1.3.0 requests gunicorn

mkdir -p data logs
sqlite3 data/realer_ai.db < Database/schema.sql

# Create systemd service
sudo tee /etc/systemd/system/r3aler-ai.service > /dev/null <<EOF
[Unit]
Description=R3ALER AI
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/opt/r3aler-ai
Environment=PATH=/opt/r3aler-ai/venv/bin
Environment=FLASK_ENV=production
ExecStart=/opt/r3aler-ai/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:5000 application.Backend.app:app
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Configure nginx
sudo tee /etc/nginx/sites-available/r3aler-ai > /dev/null <<EOF
server {
    listen 80;
    server_name _;
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \System.Management.Automation.Internal.Host.InternalHost;
        proxy_set_header X-Real-IP \;
    }
    location /static {
        alias /opt/r3aler-ai/application/Frontend/static;
    }
}
EOF

sudo ln -sf /etc/nginx/sites-available/r3aler-ai /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

sudo systemctl daemon-reload
sudo systemctl enable r3aler-ai
sudo systemctl start r3aler-ai
sudo systemctl restart nginx

echo "Deployment complete! Access at: http://"
