param(
    [Parameter(Mandatory=$true)]
    [string]$ServerIP,
    [Parameter(Mandatory=$true)]
    [string]$KeyPath
)

Write-Host "Fixing and starting R3ALER AI on $ServerIP"

ssh -i $KeyPath ubuntu@$ServerIP @"
# Clean up and organize files
sudo rm -rf /opt/r3aler-ai
sudo mkdir -p /opt/r3aler-ai
sudo chown ubuntu:ubuntu /opt/r3aler-ai

# Copy files to correct location
cp -r /home/ubuntu/application /opt/r3aler-ai/
cp -r /home/ubuntu/AI_Core_Worker /opt/r3aler-ai/
cp -r /home/ubuntu/Database /opt/r3aler-ai/
cp -r /home/ubuntu/data /opt/r3aler-ai/
cp /home/ubuntu/production_config.py /opt/r3aler-ai/

cd /opt/r3aler-ai

# Setup Python environment
python3 -m venv venv
source venv/bin/activate
pip install Flask==2.3.3 openai==1.3.0 requests gunicorn

# Initialize database
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

# Setup nginx
sudo tee /etc/nginx/sites-available/r3aler-ai > /dev/null <<EOF
server {
    listen 80;
    server_name _;
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \\\$host;
        proxy_set_header X-Real-IP \\\$remote_addr;
    }
    location /static {
        alias /opt/r3aler-ai/application/Frontend/static;
    }
}
EOF

sudo ln -sf /etc/nginx/sites-available/r3aler-ai /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Start services
sudo systemctl daemon-reload
sudo systemctl enable r3aler-ai
sudo systemctl start r3aler-ai
sudo systemctl restart nginx

echo "=== Service Status ==="
sudo systemctl status r3aler-ai --no-pager
sudo systemctl status nginx --no-pager

echo "R3ALER AI is now running at: http://$ServerIP"
"@