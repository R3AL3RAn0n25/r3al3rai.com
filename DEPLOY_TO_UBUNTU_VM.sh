#!/bin/bash
# Deploy R3ÆLƎR AI to Ubuntu VM (172.17.48.5)

VM_IP="172.17.48.5"

echo "=== Deploying R3ÆLƎR AI to Ubuntu VM ==="

# Install dependencies
echo "[1/6] Installing dependencies..."
sudo apt update
sudo apt install -y nodejs npm postgresql nginx python3-pip

# Setup PostgreSQL
echo "[2/6] Setting up PostgreSQL..."
sudo -u postgres psql << EOF
CREATE DATABASE r3aler_ai;
CREATE USER r3aler_user_2025 WITH PASSWORD 'password123';
GRANT ALL PRIVILEGES ON DATABASE r3aler_ai TO r3aler_user_2025;
\q
EOF

# Create directories
echo "[3/6] Creating directories..."
sudo mkdir -p /var/www/r3aler/html
sudo mkdir -p /var/www/r3aler/backend
sudo chown -R $USER:$USER /var/www/r3aler

# Install PM2
echo "[4/6] Installing PM2..."
sudo npm install -g pm2

# Configure Nginx
echo "[5/6] Configuring Nginx..."
sudo tee /etc/nginx/sites-available/r3aler > /dev/null << 'EOF'
server {
    listen 80;
    server_name _;
    
    location /api/ {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
    
    location / {
        root /var/www/r3aler/html;
        try_files $uri /index.html;
    }
}
EOF

sudo ln -sf /etc/nginx/sites-available/r3aler /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx

echo "[6/6] Setup complete!"
echo ""
echo "VM IP: $VM_IP"
echo "Next: Transfer files from Windows"
echo ""
echo "From Windows PowerShell, run:"
echo "  scp -r application/Backend/build/* user@$VM_IP:/var/www/r3aler/html/"
echo "  scp -r application/Backend/*.js user@$VM_IP:/var/www/r3aler/backend/"
echo "  scp application/Backend/package.json user@$VM_IP:/var/www/r3aler/backend/"
