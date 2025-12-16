#!/bin/bash

# R3AL3R AI - Ubuntu Server Production Deployment
# Run this on your Ubuntu server to deploy R3AL3R AI with HTTPS

set -e  # Exit on error

echo "================================================================"
echo "          R3AL3R AI - UBUNTU PRODUCTION DEPLOYMENT"
echo "================================================================"
echo ""

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   echo "⚠️  This script should be run as root or with sudo"
   echo "   Run: sudo bash ubuntu-deploy.sh"
   exit 1
fi

# Configuration
DOMAIN="r3al3rai.com"
PROJECT_DIR="/opt/r3aler-ai"
USER="r3aler"
PYTHON_VERSION="3.12"

echo "[1/10] Updating system packages..."
apt-get update
apt-get upgrade -y
echo "✓ System updated"

echo ""
echo "[2/10] Installing dependencies..."
apt-get install -y \
    python${PYTHON_VERSION} \
    python${PYTHON_VERSION}-venv \
    python3-pip \
    postgresql \
    postgresql-contrib \
    nginx \
    certbot \
    python3-certbot-nginx \
    git \
    curl \
    build-essential \
    libpq-dev \
    supervisor
echo "✓ Dependencies installed"

echo ""
echo "[3/10] Creating system user: $USER..."
if ! id "$USER" &>/dev/null; then
    useradd -r -s /bin/bash -d $PROJECT_DIR -m $USER
    echo "✓ User created: $USER"
else
    echo "✓ User already exists: $USER"
fi

echo ""
echo "[4/10] Setting up PostgreSQL..."
sudo -u postgres psql -c "CREATE USER r3aler_user_2025 WITH PASSWORD 'password123';" 2>/dev/null || echo "  User already exists"
sudo -u postgres psql -c "CREATE DATABASE r3aler_ai OWNER r3aler_user_2025;" 2>/dev/null || echo "  Database already exists"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE r3aler_ai TO r3aler_user_2025;" 2>/dev/null
echo "✓ PostgreSQL configured"

echo ""
echo "[5/10] Creating project directory..."
mkdir -p $PROJECT_DIR
chown -R $USER:$USER $PROJECT_DIR
echo "✓ Directory created: $PROJECT_DIR"

echo ""
echo "[6/10] Setting up Python virtual environment..."
sudo -u $USER python${PYTHON_VERSION} -m venv $PROJECT_DIR/.venv
sudo -u $USER $PROJECT_DIR/.venv/bin/pip install --upgrade pip setuptools wheel
echo "✓ Virtual environment created"

echo ""
echo "[7/10] Installing Python packages..."
cat > $PROJECT_DIR/requirements.txt <<'EOF'
flask==3.0.0
flask-cors==4.0.0
waitress==3.0.0
psycopg2-binary==2.9.9
python-dotenv==1.0.0
requests==2.31.0
pyjwt==2.8.0
bcrypt==4.1.2
torch==2.9.1
numpy==1.26.4
EOF

sudo -u $USER $PROJECT_DIR/.venv/bin/pip install -r $PROJECT_DIR/requirements.txt
echo "✓ Python packages installed"

echo ""
echo "[8/10] Configuring Nginx..."
cat > /etc/nginx/sites-available/r3al3rai <<'NGINXCONF'
# R3AL3R AI - Production Nginx Configuration

upstream r3aler_backend {
    server 127.0.0.1:3002;
}

upstream r3aler_storage {
    server 127.0.0.1:3003;
}

upstream r3aler_knowledge {
    server 127.0.0.1:5004;
}

upstream r3aler_intelligence {
    server 127.0.0.1:5010;
}

# HTTP -> HTTPS redirect
server {
    listen 80;
    listen [::]:80;
    server_name r3al3rai.com www.r3al3rai.com;
    
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }
    
    location / {
        return 301 https://$server_name$request_uri;
    }
}

# HTTPS Server
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name r3al3rai.com www.r3al3rai.com;

    # SSL Configuration (will be added by certbot)
    ssl_certificate /etc/letsencrypt/live/r3al3rai.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/r3al3rai.com/privkey.pem;
    
    # SSL Security
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    
    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    
    # Max upload size
    client_max_body_size 100M;
    
    # API Endpoints
    location /api/facility/ {
        proxy_pass http://r3aler_storage;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        proxy_read_timeout 300s;
        proxy_connect_timeout 75s;
    }
    
    location /api/query {
        proxy_pass http://r3aler_knowledge;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        proxy_read_timeout 300s;
    }
    
    location /api/kb/ {
        proxy_pass http://r3aler_knowledge;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        proxy_read_timeout 300s;
    }
    
    location /api/intelligence/ {
        proxy_pass http://r3aler_intelligence;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
    
    # Main application
    location / {
        proxy_pass http://r3aler_backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
    
    # Static files caching
    location ~* \.(jpg|jpeg|png|gif|ico|css|js|svg|woff|woff2|ttf)$ {
        proxy_pass http://r3aler_backend;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
NGINXCONF

ln -sf /etc/nginx/sites-available/r3al3rai /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t
systemctl reload nginx
echo "✓ Nginx configured"

echo ""
echo "[9/10] Configuring Supervisor for service management..."
cat > /etc/supervisor/conf.d/r3aler-ai.conf <<'SUPCONF'
[group:r3aler]
programs=storage,knowledge,intelligence,backend

[program:storage]
directory=/opt/r3aler-ai/AI_Core_Worker
command=/opt/r3aler-ai/.venv/bin/python run_storage.py
user=r3aler
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/r3aler/storage.log
environment=PATH="/opt/r3aler-ai/.venv/bin:%(ENV_PATH)s"

[program:knowledge]
directory=/opt/r3aler-ai/AI_Core_Worker
command=/opt/r3aler-ai/.venv/bin/python run_knowledge.py
user=r3aler
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/r3aler/knowledge.log
environment=PATH="/opt/r3aler-ai/.venv/bin:%(ENV_PATH)s"

[program:intelligence]
directory=/opt/r3aler-ai/AI_Core_Worker
command=/opt/r3aler-ai/.venv/bin/python run_intelligence.py
user=r3aler
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/r3aler/intelligence.log
environment=PATH="/opt/r3aler-ai/.venv/bin:%(ENV_PATH)s"

[program:backend]
directory=/opt/r3aler-ai/application/Backend
command=/opt/r3aler-ai/.venv/bin/python run_backend.py
user=r3aler
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/r3aler/backend.log
environment=PATH="/opt/r3aler-ai/.venv/bin:%(ENV_PATH)s"
SUPCONF

mkdir -p /var/log/r3aler
chown -R $USER:$USER /var/log/r3aler
supervisorctl reread
supervisorctl update
echo "✓ Supervisor configured"

echo ""
echo "[10/10] Setting up SSL with Let's Encrypt..."
mkdir -p /var/www/certbot
echo "⚠️  IMPORTANT: Make sure DNS is pointing to this server before continuing!"
read -p "Is DNS configured? (y/n): " dns_ready
if [[ $dns_ready == "y" || $dns_ready == "Y" ]]; then
    certbot --nginx -d r3al3rai.com -d www.r3al3rai.com --non-interactive --agree-tos --email admin@r3al3rai.com
    echo "✓ SSL certificate obtained"
else
    echo "⚠️  Skipping SSL setup. Run manually later:"
    echo "   sudo certbot --nginx -d r3al3rai.com -d www.r3al3rai.com"
fi

echo ""
echo "================================================================"
echo "                    DEPLOYMENT COMPLETE!"
echo "================================================================"
echo ""
echo "✅ R3AL3R AI is now deployed on Ubuntu!"
echo ""
echo "Project Directory: $PROJECT_DIR"
echo "Service User: $USER"
echo "Logs Directory: /var/log/r3aler/"
echo ""
echo "NEXT STEPS:"
echo "1. Upload your R3AL3R AI code to $PROJECT_DIR"
echo "2. Set environment variables in /opt/r3aler-ai/.env"
echo "3. Start services: sudo supervisorctl start r3aler:*"
echo "4. Check status: sudo supervisorctl status"
echo "5. View logs: tail -f /var/log/r3aler/*.log"
echo "6. Test: https://r3al3rai.com"
echo ""
echo "SERVICE MANAGEMENT:"
echo "  Start all:   sudo supervisorctl start r3aler:*"
echo "  Stop all:    sudo supervisorctl stop r3aler:*"
echo "  Restart all: sudo supervisorctl restart r3aler:*"
echo "  Status:      sudo supervisorctl status"
echo ""
echo "NGINX MANAGEMENT:"
echo "  Test config: sudo nginx -t"
echo "  Reload:      sudo systemctl reload nginx"
echo "  Status:      sudo systemctl status nginx"
echo ""
echo "SSL RENEWAL (automatic):"
echo "  certbot renew --dry-run  # Test renewal"
echo ""
echo "================================================================"
