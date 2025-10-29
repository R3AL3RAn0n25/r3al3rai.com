# R3ÆLƎR AI AWS Deployment Script
param(
    [Parameter(Mandatory=$true)]
    [string]$PublicIP,
    
    [Parameter(Mandatory=$true)]
    [string]$KeyPath
)

Write-Host "Deploying R3ÆLƎR AI to AWS EC2: $PublicIP"

# Create deployment package
$DeployPath = ".\deploy-package"
if (Test-Path $DeployPath) { Remove-Item $DeployPath -Recurse -Force }
New-Item -ItemType Directory -Path $DeployPath

# Copy application files
Copy-Item -Path ".\application" -Destination "$DeployPath\application" -Recurse
Copy-Item -Path ".\AI_Core_Worker" -Destination "$DeployPath\AI_Core_Worker" -Recurse
Copy-Item -Path ".\Database" -Destination "$DeployPath\Database" -Recurse
Copy-Item -Path ".\data" -Destination "$DeployPath\data" -Recurse -ErrorAction SilentlyContinue
Copy-Item -Path ".\production_config.py" -Destination "$DeployPath\" -ErrorAction SilentlyContinue

# Create requirements.txt for python dependencies
@"
Flask==2.3.3
openai==1.3.0
requests
gunicorn
"@ | Out-File -FilePath "$DeployPath\requirements.txt" -Encoding UTF8

# Create server setup script
$SetupScript = @"
#!/bin/bash
set -e

echo "Setting up R3ÆLƎR AI on Ubuntu..."

# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install dependencies (Python, Nginx, Node.js)
sudo apt-get install -y python3 python3-pip python3-venv nginx sqlite3 git curl
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Create application directory
sudo rm -rf /opt/r3aler-ai
sudo mkdir -p /opt/r3aler-ai
# Check if the R3ÆLƎR AI directory exists and move its contents, otherwise move from home
if [ -d "/home/ubuntu/R3ÆLƎR AI" ]; then
    sudo mv "/home/ubuntu/R3ÆLƎR AI"/* /opt/r3aler-ai/
else
    sudo mv /home/ubuntu/* /opt/r3aler-ai/
fi
sudo chown -R ubuntu:ubuntu /opt/r3aler-ai
cd /opt/r3aler-ai

# Build Frontend
echo "Building frontend..."
if [ -d "/opt/r3aler-ai/application/Frontend" ]; then
    cd /opt/r3aler-ai/application/Frontend
    npm install
    npm run build
fi

# Create virtual environment
cd /opt/r3aler-ai
python3 -m venv venv
source venv/bin/activate

# Install Python packages
pip install -r requirements.txt

# Create database
mkdir -p data
sqlite3 data/realer_ai.db < Database/schema.sql || echo "Database already exists or schema failed."

# Set up systemd service
sudo tee /etc/systemd/system/r3aler-ai.service > /dev/null <<EOF
[Unit]
Description=R3ALER AI Application
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/opt/r3aler-ai
Environment=PATH=/opt/r3aler-ai/venv/bin
Environment=FLASK_ENV=production
Environment=PYTHONPATH=/opt/r3aler-ai
ExecStart=/opt/r3aler-ai/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:5000 application.Backend.app:app
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Configure Nginx
sudo tee /etc/nginx/sites-available/r3aler-ai > /dev/null <<EOF
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
        alias /opt/r3aler-ai/application/Frontend/dist; # Point to the 'dist' or 'build' folder
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
EOF

sudo ln -sf /etc/nginx/sites-available/r3aler-ai /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Start services
sudo systemctl daemon-reload
sudo systemctl enable r3aler-ai
sudo systemctl start r3aler-ai
sudo systemctl enable nginx
sudo systemctl restart nginx

# Configure firewall
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw --force enable

echo "R3ÆLƎR AI deployment completed!"
echo "Application should be accessible at: http://$(curl -s ifconfig.me)"
"@

$SetupScript | Out-File -FilePath "$DeployPath\setup.sh" -Encoding UTF8

Write-Host "Deployment package created. Uploading to server..."

# Upload files using SCP (requires OpenSSH or PuTTY)
scp -i $KeyPath -r $DeployPath/* "ubuntu@${PublicIP}:/home/ubuntu/R3ÆLƎR AI/"

# Execute setup script
ssh -i $KeyPath ubuntu@$PublicIP "mv '/home/ubuntu/R3ÆLƎR AI/setup.sh' /home/ubuntu/ && chmod +x /home/ubuntu/setup.sh && sudo /home/ubuntu/setup.sh"

Write-Host "Deployment completed! Application should be available at: http://$PublicIP"