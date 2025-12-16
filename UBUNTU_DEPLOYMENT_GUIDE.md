# R3AL3R AI - Ubuntu Server Production Deployment Guide

## 🚀 Complete Production Setup for r3al3rai.com

This guide will deploy R3AL3R AI on Ubuntu Server with HTTPS, Nginx reverse proxy, and Let's Encrypt SSL.

---

## 📋 Prerequisites

### Server Requirements:
- **Ubuntu Server 22.04 LTS** (recommended) or 20.04 LTS
- **Minimum:** 4GB RAM, 2 CPU cores, 40GB storage
- **Recommended:** 8GB RAM, 4 CPU cores, 100GB SSD
- **Root or sudo access**
- **Public IP address**
- **Domain:** r3al3rai.com pointing to server IP

### Local Requirements:
- SSH client (PuTTY, OpenSSH, or WSL)
- Your SSL certificate files (if not using Let's Encrypt)

---

## 🔧 Step-by-Step Deployment

### 1. Configure DNS (BEFORE deploying)

Point your domain to your server:

```
Type: A Record
Name: @
Value: YOUR_SERVER_IP
TTL: 3600

Type: A Record
Name: www
Value: YOUR_SERVER_IP
TTL: 3600
```

**Wait 5-10 minutes for DNS propagation**

Verify:
```bash
nslookup r3al3rai.com
# Should return your server IP
```

---

### 2. Connect to Your Ubuntu Server

```bash
ssh root@YOUR_SERVER_IP
# OR
ssh yourusername@YOUR_SERVER_IP
```

---

### 3. Download Deployment Script

On the server, run:

```bash
cd /tmp
curl -O https://raw.githubusercontent.com/yourusername/r3aler-ai/main/ubuntu-deploy.sh
# OR manually copy ubuntu-deploy.sh to the server
```

If copying manually:
```bash
# On Windows (PowerShell)
scp ubuntu-deploy.sh root@YOUR_SERVER_IP:/tmp/
```

---

### 4. Run Deployment Script

```bash
sudo bash /tmp/ubuntu-deploy.sh
```

This will:
- ✅ Update system packages
- ✅ Install Python 3.11, PostgreSQL, Nginx
- ✅ Create system user `r3aler`
- ✅ Setup PostgreSQL database
- ✅ Create Python virtual environment
- ✅ Install Python packages
- ✅ Configure Nginx reverse proxy
- ✅ Setup Supervisor for service management
- ✅ Obtain Let's Encrypt SSL certificate

**Duration:** 5-10 minutes

---

### 5. Upload R3AL3R AI Code

#### Option A: Using rsync (Recommended)

On your **Windows machine** (in WSL or Git Bash):

```bash
cd "C:\Users\work8\OneDrive\Desktop\r3al3rai\New Folder 1\R3al3r-AI Main Working\R3aler-ai\R3aler-ai"

rsync -avz --progress \
    --exclude='.git' \
    --exclude='.venv' \
    --exclude='__pycache__' \
    --exclude='*.log' \
    --exclude='node_modules' \
    ./ root@YOUR_SERVER_IP:/opt/r3aler-ai/
```

#### Option B: Using SCP

```powershell
# From Windows PowerShell
cd "C:\Users\work8\OneDrive\Desktop\r3al3rai\New Folder 1\R3al3r-AI Main Working\R3aler-ai\R3aler-ai"
scp -r . root@YOUR_SERVER_IP:/opt/r3aler-ai/
```

#### Option C: Using Git

```bash
# On server
cd /opt/r3aler-ai
git clone https://github.com/yourusername/r3aler-ai.git .
```

---

### 6. Configure Environment Variables

On the server:

```bash
nano /opt/r3aler-ai/.env
```

Add:

```bash
# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=r3aler_ai
DB_USER=r3aler_user_2025
DB_PASSWORD=password123

# Security
JWT_SECRET=CHANGE_THIS_TO_RANDOM_STRING
JWT_EXPIRY=3600

# Production
FLASK_ENV=production
FLASK_DEBUG=False

# Domain
DOMAIN=r3al3rai.com
ALLOWED_HOSTS=r3al3rai.com,www.r3al3rai.com
```

Generate secure JWT secret:
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(64))"
```

---

### 7. Set Correct Permissions

```bash
sudo chown -R r3aler:r3aler /opt/r3aler-ai
sudo chmod -R 755 /opt/r3aler-ai
```

---

### 8. Start Services

```bash
# Start all R3AL3R AI services
sudo supervisorctl start r3aler:*

# Check status
sudo supervisorctl status

# Expected output:
# r3aler:backend     RUNNING   pid 1234, uptime 0:00:05
# r3aler:intelligence RUNNING   pid 1235, uptime 0:00:05
# r3aler:knowledge   RUNNING   pid 1236, uptime 0:00:05
# r3aler:storage     RUNNING   pid 1237, uptime 0:00:05
```

---

### 9. Verify Deployment

#### Check Service Logs:
```bash
# View all logs
tail -f /var/log/r3aler/*.log

# Individual services
tail -f /var/log/r3aler/backend.log
tail -f /var/log/r3aler/knowledge.log
tail -f /var/log/r3aler/storage.log
```

#### Test Endpoints:
```bash
# Storage Facility
curl http://localhost:3003/health

# Knowledge API
curl http://localhost:5004/health

# Backend
curl http://localhost:3002/
```

#### Check Nginx:
```bash
sudo nginx -t
sudo systemctl status nginx
```

#### Test HTTPS:
```bash
curl -I https://r3al3rai.com
# Should return: HTTP/2 200
```

---

### 10. Open Firewall Ports

```bash
# Allow HTTPS
sudo ufw allow 443/tcp

# Allow HTTP (for Let's Encrypt renewal)
sudo ufw allow 80/tcp

# Allow SSH
sudo ufw allow 22/tcp

# Enable firewall
sudo ufw enable

# Check status
sudo ufw status
```

---

## 🔄 Service Management

### Supervisor Commands:

```bash
# Start all services
sudo supervisorctl start r3aler:*

# Stop all services
sudo supervisorctl stop r3aler:*

# Restart all services
sudo supervisorctl restart r3aler:*

# Status
sudo supervisorctl status

# Individual service
sudo supervisorctl restart r3aler:knowledge
```

### Nginx Commands:

```bash
# Test configuration
sudo nginx -t

# Reload (without downtime)
sudo systemctl reload nginx

# Restart
sudo systemctl restart nginx

# Status
sudo systemctl status nginx

# View logs
sudo tail -f /var/log/nginx/error.log
```

### PostgreSQL Commands:

```bash
# Connect to database
sudo -u postgres psql -d r3aler_ai

# Check connection
sudo -u postgres psql -c "\l"

# Backup database
sudo -u postgres pg_dump r3aler_ai > backup.sql

# Restore database
sudo -u postgres psql r3aler_ai < backup.sql
```

---

## 🔐 SSL Certificate Management

### Let's Encrypt Auto-Renewal

Certificates renew automatically via cron. To test:

```bash
# Dry run
sudo certbot renew --dry-run

# Force renewal (if needed)
sudo certbot renew --force-renewal

# Check certificate expiry
sudo certbot certificates
```

### Using Your Own Certificate

If you have your own SSL certificate (like the one in `C:\Users\work8\OneDrive\Desktop\_.r3al3rai.com_ssl_certificate_INTERMEDIATE`):

```bash
# Upload certificates to server
scp -r "C:\Users\work8\OneDrive\Desktop\_.r3al3rai.com_ssl_certificate_INTERMEDIATE\*" root@YOUR_SERVER_IP:/etc/ssl/r3al3rai/

# Update Nginx config
sudo nano /etc/nginx/sites-available/r3al3rai

# Change these lines:
ssl_certificate /etc/ssl/r3al3rai/fullchain.pem;
ssl_certificate_key /etc/ssl/r3al3rai/private.key;

# Test and reload
sudo nginx -t
sudo systemctl reload nginx
```

---

## 🐛 Troubleshooting

### Services Won't Start

```bash
# Check logs
tail -f /var/log/r3aler/*.log

# Check Python environment
sudo -u r3aler /opt/r3aler-ai/.venv/bin/python --version

# Reinstall dependencies
sudo -u r3aler /opt/r3aler-ai/.venv/bin/pip install -r /opt/r3aler-ai/requirements.txt
```

### Database Connection Errors

```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Check connection
sudo -u postgres psql -c "SELECT version();"

# Reset password
sudo -u postgres psql -c "ALTER USER r3aler_user_2025 WITH PASSWORD 'password123';"
```

### Nginx 502 Bad Gateway

```bash
# Check if backend services are running
sudo supervisorctl status

# Check port bindings
sudo netstat -tlnp | grep -E "3002|3003|5004|5010"

# Check Nginx error log
sudo tail -f /var/log/nginx/error.log
```

### SSL Certificate Issues

```bash
# Check certificate
sudo certbot certificates

# Renew manually
sudo certbot renew

# Check Nginx SSL config
sudo nginx -t
```

---

## 📊 Monitoring

### View Real-Time Logs:

```bash
# All services
sudo tail -f /var/log/r3aler/*.log

# Specific service
sudo tail -f /var/log/r3aler/knowledge.log

# Nginx access
sudo tail -f /var/log/nginx/access.log

# Nginx errors
sudo tail -f /var/log/nginx/error.log
```

### System Resources:

```bash
# CPU and Memory
htop

# Disk usage
df -h

# Service memory usage
ps aux | grep python
```

---

## 🔄 Updates and Maintenance

### Update R3AL3R AI Code:

```bash
# On your local machine
cd "C:\Users\work8\OneDrive\Desktop\r3al3rai\New Folder 1\R3al3r-AI Main Working\R3aler-ai\R3aler-ai"
bash upload-to-ubuntu.sh

# On server
sudo chown -R r3aler:r3aler /opt/r3aler-ai
sudo supervisorctl restart r3aler:*
```

### Update System Packages:

```bash
sudo apt-get update
sudo apt-get upgrade -y
sudo systemctl restart r3aler
```

---

## 🚀 Performance Optimization

### Increase Worker Threads:

Edit `/opt/r3aler-ai/AI_Core_Worker/run_knowledge.py`:

```python
serve(knowledge_api.app, host='0.0.0.0', port=5004, threads=8)  # Increase from 4 to 8
```

### Enable Nginx Caching:

Add to `/etc/nginx/sites-available/r3al3rai`:

```nginx
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=r3aler_cache:10m inactive=60m;
proxy_cache_key "$scheme$request_method$host$request_uri";
```

### PostgreSQL Optimization:

```bash
sudo nano /etc/postgresql/14/main/postgresql.conf

# Add:
shared_buffers = 256MB
effective_cache_size = 1GB
maintenance_work_mem = 64MB
```

---

## 📞 Support

- **Logs:** `/var/log/r3aler/`
- **Config:** `/opt/r3aler-ai/`
- **Nginx:** `/etc/nginx/sites-available/r3al3rai`
- **Supervisor:** `/etc/supervisor/conf.d/r3aler-ai.conf`

---

## ✅ Deployment Checklist

- [ ] DNS configured (r3al3rai.com → server IP)
- [ ] Ubuntu server provisioned
- [ ] SSH access confirmed
- [ ] `ubuntu-deploy.sh` executed successfully
- [ ] Code uploaded to `/opt/r3aler-ai/`
- [ ] `.env` file configured
- [ ] Permissions set (`chown r3aler:r3aler`)
- [ ] Services started (`supervisorctl start r3aler:*`)
- [ ] All services showing RUNNING status
- [ ] Nginx running (`systemctl status nginx`)
- [ ] Firewall configured (ports 80, 443, 22)
- [ ] SSL certificate obtained (Let's Encrypt or custom)
- [ ] HTTPS working (https://r3al3rai.com)
- [ ] All API endpoints responding
- [ ] Logs clean (no errors)

---

**🎉 Your R3AL3R AI is now live on Ubuntu with HTTPS!**

Access: **https://r3al3rai.com**
