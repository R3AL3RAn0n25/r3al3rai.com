# Run R3ÆLƎR AI from Ubuntu VM

## Setup Ubuntu VM as Production Server

### 1. Install Ubuntu VM
- VirtualBox or VMware
- Ubuntu Server 22.04 LTS
- Bridge network adapter (to get own IP)

### 2. Get VM IP Address
```bash
ip addr show
# Look for IP like 192.168.1.XXX
```

### 3. Install Dependencies on Ubuntu VM
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs

# Install PostgreSQL
sudo apt install -y postgresql postgresql-contrib

# Install Python
sudo apt install -y python3 python3-pip

# Install Nginx
sudo apt install -y nginx
```

### 4. Setup PostgreSQL
```bash
sudo -u postgres psql
CREATE DATABASE r3aler_ai;
CREATE USER r3aler_user_2025 WITH PASSWORD 'password123';
GRANT ALL PRIVILEGES ON DATABASE r3aler_ai TO r3aler_user_2025;
\q
```

### 5. Transfer Files to VM
```powershell
# From Windows, use SCP
scp -r application/Backend/build/* user@VM_IP:/var/www/r3aler/html/
scp -r application/Backend/*.js user@VM_IP:/var/www/r3aler/backend/
scp application/Backend/package.json user@VM_IP:/var/www/r3aler/backend/
```

### 6. Configure Nginx on VM
```bash
sudo nano /etc/nginx/sites-available/r3aler
```

```nginx
server {
    listen 80;
    server_name _;
    
    location /api/ {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location / {
        root /var/www/r3aler/html;
        try_files $uri /index.html;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/r3aler /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 7. Start Backend on VM
```bash
cd /var/www/r3aler/backend
npm install
npm install -g pm2
pm2 start backendserver.js --name r3aler-backend
pm2 startup
pm2 save
```

### 8. Port Forward Router to VM IP
Forward ports 80, 443 to VM IP (192.168.1.XXX)

### 9. Update DNS
Point r3al3rai.com to your public IP (47.215.15.217)

## Quick Deploy Script
```bash
#!/bin/bash
# deploy_to_vm.sh

VM_IP="192.168.1.XXX"  # Change to your VM IP
VM_USER="ubuntu"

# Build frontend
cd application/Frontend
npm run build

# Upload files
scp -r ../Backend/build/* $VM_USER@$VM_IP:/var/www/r3aler/html/
scp -r ../Backend/*.js $VM_USER@$VM_IP:/var/www/r3aler/backend/

# Restart backend
ssh $VM_USER@$VM_IP "cd /var/www/r3aler/backend && pm2 restart r3aler-backend"
```

## Advantages
- ✓ Full control
- ✓ No external dependencies
- ✓ Can run 24/7
- ✓ Self-sufficient
- ✓ Own IP address
