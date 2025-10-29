param(
    [Parameter(Mandatory=$true)]
    [string]$ServerIP,
    [Parameter(Mandatory=$true)]
    [string]$KeyPath
)

# Create deployment package
Remove-Item "deploy-package" -Recurse -Force -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Path "deploy-package"

# Copy essential files
Copy-Item -Path "application" -Destination "deploy-package\application" -Recurse
Copy-Item -Path "AI_Core_Worker" -Destination "deploy-package\AI_Core_Worker" -Recurse
Copy-Item -Path "Database" -Destination "deploy-package\Database" -Recurse
Copy-Item -Path "data" -Destination "deploy-package\data" -Recurse -ErrorAction SilentlyContinue
Copy-Item -Path "production_config.py" -Destination "deploy-package\" -ErrorAction SilentlyContinue

# Create setup script
@"
#!/bin/bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv nginx sqlite3

sudo mkdir -p /home/ubuntu/r3al3rai.com/
sudo chown ubuntu:/home/ubuntu/r3al3rai.com/
cd /home/ubuntu/r3al3rai.com/

python3 -m venv venv
source venv/bin/activate
pip install Flask==2.3.3 openai==1.3.0 requests gunicorn

mkdir -p data logs
sqlite3 data/realer_ai.db < Database/schema.sql

# Create systemd service
sudo tee /home/ubuntu/r3al3rai.com/.service > /dev/null <<EOF
[Unit]
Description=R3ALER AI
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/r3al3rai.com/
Environment=PATH=/home/ubuntu/r3al3rai.com/venv/bin
Environment=FLASK_ENV=production
ExecStart=/home/ubuntu/r3al3rai.com/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:5000 application.Backend.app:app
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Configure nginx
sudo tee /etc/nginx/sites-available/r3al3rai.com > /dev/null <<EOF
server {
    listen 80;
    server_name _;
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
    location /static {
        alias /home/ubuntu/r3al3rai.com/application/Frontend/static;
    }
}
EOF

sudo ln -sf /etc/nginx/sites-available/r3al3rai.com/etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

sudo systemctl daemon-reload
sudo systemctl enable r3al3rai.com
sudo systemctl start r3al3rai.com
sudo systemctl restart nginx

echo "Deployment complete! Access at: http://$(curl -s ifconfig.me)"
"@ | Out-File -FilePath "deploy-package\setup.sh" -Encoding UTF8

# Upload and deploy
scp -i $KeyPath -r deploy-package/* ubuntu@${ServerIP}:/home/ubuntu/
ssh -i $KeyPath ubuntu@$ServerIP "chmod +x setup.sh && ./setup.sh"

Write-Host "Deployed! Access at: http://$ServerIP"