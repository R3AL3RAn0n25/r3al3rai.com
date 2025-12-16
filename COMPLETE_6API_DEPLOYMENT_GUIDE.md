# R3ÆLƎR AI - Complete 6-API Production Deployment Guide

## System Architecture Overview

The R3ÆLƎR AI system is a **distributed 6-API architecture** designed for maximum scalability, security, and performance. All APIs work together to create a comprehensive AI system with user management, knowledge storage, intelligent reasoning, and system administration capabilities.

### 6-API Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    R3ÆLƎR AI Distributed System                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  Management API (5001)                    User Auth API (5003)       │
│  ├─ System status                         ├─ User registration       │
│  ├─ Environment config                    ├─ Session management      │
│  ├─ Service monitoring                    ├─ API key generation      │
│  └─ Deployment control                    └─ User preferences        │
│                                                                       │
│  Knowledge API (5004)                     Storage Facility (5006)    │
│  ├─ Query processing                      ├─ Physics unit            │
│  ├─ Knowledge search                      ├─ Quantum unit            │
│  ├─ Knowledge ingestion                   ├─ Medical unit            │
│  └─ 30K+ knowledge entries                └─ 7 specialized units     │
│                                                                       │
│  Droid API (5005)                         Enhanced Storage (5007)    │
│  ├─ Adaptive AI responses                 ├─ Advanced analytics      │
│  ├─ LRU caching (1000 entries)            ├─ Optimization tools      │
│  ├─ Session management                    ├─ Facility maintenance    │
│  └─ Rate limited (5/hr chat)              └─ Tools search            │
│                                                                       │
│  ┌─────────────────────────────────────────────────────────────────┐
│  │          PostgreSQL Database (Single Master)                     │
│  │          Host: 127.0.0.1:5432                                   │
│  │          SSL/TLS: Required (sslmode=require)                    │
│  │          Database: r3aler_ai                                    │
│  │          User: r3aler_user_2025                                 │
│  │          Schemas: user_unit, physics_unit, quantum_unit, ...   │
│  └─────────────────────────────────────────────────────────────────┘
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

## Deployment Checklist

### Phase 1: Pre-Deployment Preparation ✅

- [x] Security audit completed (33 vulnerabilities identified and fixed)
- [x] All APIs hardened with bcrypt, rate limiting, and input validation
- [x] PostgreSQL SSL/TLS configured
- [x] Environment variables configured (.env.local)
- [x] Secured API versions created:
  - [x] knowledge_api.py (11 fixes)
  - [x] droid_api.py (12 fixes)
  - [x] user_auth_api_secured.py (10 fixes)
  - [x] self_hosted_storage_facility_secured.py (comprehensive hardening)
  - [x] management_api_secured.py (comprehensive hardening)

### Phase 2: PostgreSQL Setup

#### 1. Database User & Database Setup
```sql
-- Create database user (if not exists)
CREATE USER r3aler_user_2025 WITH ENCRYPTED PASSWORD 'R3al3rSecure2025!@#$%^&*';

-- Create database
CREATE DATABASE r3aler_ai OWNER r3aler_user_2025;

-- Grant privileges
GRANT CONNECT ON DATABASE r3aler_ai TO r3aler_user_2025;
GRANT CREATE ON DATABASE r3aler_ai TO r3aler_user_2025;
```

#### 2. SSL/TLS Configuration (PostgreSQL)
```bash
# Generate self-signed certificate (for testing)
openssl req -x509 -newkey rsa:4096 -keyout server.key -out server.crt -days 365 -nodes

# Or use provided certificate
# Copy r3al3rai.com_ssl_certificate.cer to PostgreSQL SSL directory

# Ensure proper permissions
chmod 600 /etc/postgresql/13/main/server.key
chmod 644 /etc/postgresql/13/main/server.crt
```

#### 3. PostgreSQL Configuration (postgresql.conf)
```
ssl = on
ssl_cert_file = 'path/to/server.crt'
ssl_key_file = 'path/to/server.key'
ssl_protocols = 'TLSv1.2,TLSv1.3'
```

#### 4. Create Schemas & Tables
```bash
# This is handled automatically by each API on startup
# Each API creates its own schema and tables on first run
```

### Phase 3: Environment Configuration

Create `.env.local` in the deployment directory with these variables:

```env
# Flask Configuration
FLASK_SECRET_KEY=a7f9e2b1c4d6e8f0a1b2c3d4e5f6a7b8
FLASK_ENV=production

# Database Configuration
DB_HOST=127.0.0.1
DB_PORT=5432
DB_NAME=r3aler_ai
DB_USER=r3aler_user_2025
DB_PASSWORD=R3al3rSecure2025!@#$%^&*

# CORS Configuration (Whitelist)
CORS_ALLOWED_ORIGINS=http://localhost:5000,http://127.0.0.1:5000,https://r3al3rai.com,https://www.r3al3rai.com

# IP Whitelist (for additional security)
IP_WHITELIST=127.0.0.1,192.168.1.0/24,72.17.63.255

# API Ports
MANAGEMENT_API_PORT=5001
USER_AUTH_API_PORT=5003
KNOWLEDGE_API_PORT=5004
DROID_API_PORT=5005
STORAGE_FACILITY_PORT=5006

# Management API Key (for admin operations)
MANAGEMENT_API_KEY=your_secure_management_api_key_here

# Application Version
APP_VERSION=2.0.0
APP_ENV=production
```

### Phase 4: Deploy All 6 APIs

#### Option A: Manual Deployment

```bash
# 1. Management API (5001) - Start first for system management
python management_api_secured.py &

# 2. User Auth API (5003) - Start before other APIs
python user_auth_api_secured.py &

# 3. Storage Facility APIs
python self_hosted_storage_facility_secured.py &  # Port 5006

# 4. Knowledge & Reasoning APIs
python knowledge_api.py &  # Port 5004
python droid_api.py &      # Port 5005

# Keep processes running with nohup (recommended for production)
nohup python management_api_secured.py > logs/management_api.log 2>&1 &
nohup python user_auth_api_secured.py > logs/user_auth_api.log 2>&1 &
nohup python self_hosted_storage_facility_secured.py > logs/storage_api.log 2>&1 &
nohup python knowledge_api.py > logs/knowledge_api.log 2>&1 &
nohup python droid_api.py > logs/droid_api.log 2>&1 &
```

#### Option B: Systemd Service Deployment (Recommended for Production)

See systemd services section below.

### Phase 5: Verify All APIs are Running

```bash
# Test each API's health endpoint
curl http://localhost:5001/health  # Management API
curl http://localhost:5003/health  # User Auth API
curl http://localhost:5004/health  # Knowledge API
curl http://localhost:5005/health  # Droid API
curl http://localhost:5006/health  # Storage Facility
```

Expected response:
```json
{
  "status": "healthy",
  "service": "R3ÆLƎR ... API (SECURED)",
  "version": "2.0.0",
  "timestamp": "2024-12-15T12:00:00"
}
```

## API Reference

### 1. Management API (Port 5001)

**Purpose**: System monitoring, environment management, service control

**Key Endpoints**:
- `GET /api/system/status` - System health
- `GET /api/system/environment` - Environment config
- `PUT /api/system/environment` - Change environment (auth required)
- `GET /api/services` - List all services
- `GET /api/services/<id>/health` - Check service health
- `GET /api/monitoring/metrics` - CPU, memory, disk
- `GET /api/monitoring/logs` - System logs (auth required)

**Rate Limits**: 50/hour default, 10/hour for environment changes

### 2. User Auth API (Port 5003)

**Purpose**: User management, authentication, session control

**Key Endpoints**:
- `POST /api/user/register` - Create new user (5/hour)
- `POST /api/user/login` - Login & create session (10/hour)
- `POST /api/user/logout` - Logout & invalidate session
- `GET /api/user/profile` - Get user profile (auth required)
- `PUT /api/user/preferences` - Update preferences (auth required)
- `POST /api/user/regenerate-api-key` - Generate new API key (5/hour, auth required)
- `GET /api/user/stats` - Platform statistics (100/hour)

**Authentication**: X-API-Key or X-Session-Token header

**Security Features**:
- Bcrypt hashing (12 salt rounds)
- Rate limiting on auth endpoints
- Session expiration (7 days)
- Input validation (username format, email, password strength)

### 3. Knowledge API (Port 5004)

**Purpose**: Knowledge base management, semantic search, ingest

**Key Endpoints**:
- `GET /api/query` - Query knowledge base (20/hour)
- `POST /api/kb/search` - Search knowledge (30/hour, auth required)
- `POST /api/kb/ingest` - Add to knowledge base (5/hour, auth required)
- `GET /health` - Health check

**Features**:
- 30,657+ knowledge entries
- Full-text search with ranking
- Authentication via API key/session token
- CORS whitelist configured

### 4. Droid API (Port 5005)

**Purpose**: Adaptive AI assistant, intelligent responses

**Key Endpoints**:
- `POST /api/droid/create` - Create droid instance
- `POST /api/droid/chat` - Chat with droid (5/hour)
- `GET /health` - Health check

**Features**:
- LRU caching (1000 max, 3600s TTL)
- PostgreSQL integration
- Adaptive response generation
- Rate limited (5/hour chat operations)

### 5. Storage Facility API (Port 5006)

**Purpose**: Knowledge storage across 7 specialized units

**Units**:
- Physics (classical mechanics, thermodynamics)
- Quantum (quantum mechanics, particle physics)
- Space (astronomy, aerospace)
- Crypto (blockchain, cryptocurrency)
- Medical (clinical, biomedical)
- Reason (logic, consciousness)
- Logic (formal logic, mathematical)

**Key Endpoints**:
- `GET /api/facility/status` - Overall status
- `GET /api/facility/units` - List units
- `GET /api/unit/<id>/stats` - Unit statistics
- `POST /api/unit/<id>/search` - Search unit (30/hour, auth required)
- `POST /api/unit/<id>/store` - Store knowledge (10/hour, auth required)

**Features**:
- PostgreSQL schemas per unit
- Full-text search with relevance ranking
- Input validation (query length < 500 chars, max 100 results)
- SSL/TLS required for database

## Security Implementation

### 1. Password Security
- **Hashing Algorithm**: bcrypt with 12 salt rounds
- **Minimum Length**: 12 characters (uppercase, numbers required)
- **Storage**: Never plain text, only salted hashes

### 2. Authentication
- **API Keys**: 32-byte URL-safe tokens
- **Session Tokens**: UUID format, 7-day expiration
- **Rate Limiting**: Per-endpoint limits (5-100 per hour)

### 3. Database Security
- **SSL/TLS**: Required for all connections (sslmode=require)
- **User Account**: Limited privileges (no superuser)
- **Parameterized Queries**: All SQL injections mitigated

### 4. Input Validation
- **Username**: 3-32 chars, alphanumeric + underscore/dash
- **Email**: RFC 5322 compliant validation
- **Queries**: Max 500 characters, whitespace trimmed
- **Entry IDs**: Alphanumeric with dash/underscore/dot

### 5. CORS Configuration
```
Allowed Origins:
- http://localhost:5000
- http://127.0.0.1:5000
- https://r3al3rai.com
- https://www.r3al3rai.com

Headers Allowed:
- Content-Type
- X-API-Key
- X-Session-Token
```

### 6. Rate Limiting
```
Default: 200/day, 50/hour
Registration: 5/hour
Login: 10/hour
Chat (expensive): 5/hour
Search: 30/hour
Storage: 10/hour
Environment changes: 10/hour
```

## Production Deployment to 72.17.63.255

### 1. Copy Files to Production Server

```bash
# Create deployment package
mkdir -p deploy_package_prod
cp .env.local deploy_package_prod/
cp management_api_secured.py deploy_package_prod/
cp user_auth_api_secured.py deploy_package_prod/
cp knowledge_api.py deploy_package_prod/
cp droid_api.py deploy_package_prod/
cp self_hosted_storage_facility_secured.py deploy_package_prod/
cp r3al3rai.com_ssl_certificate.cer deploy_package_prod/

# Transfer to production server
scp -r deploy_package_prod/ user@72.17.63.255:/opt/r3aler/
```

### 2. Install Python Dependencies

```bash
ssh user@72.17.63.255

cd /opt/r3aler/deploy_package_prod

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install required packages
pip install flask==2.3.2 \
            flask-cors==4.0.0 \
            flask-limiter==3.5.0 \
            psycopg2-binary==2.9.7 \
            bcrypt==4.0.1 \
            python-dotenv==1.0.0 \
            requests==2.31.0 \
            psutil==5.9.5
```

### 3. Set Up Systemd Services

See systemd service configuration files below.

## Systemd Services Setup

### r3aler-management-api.service

```ini
[Unit]
Description=R3ÆLƎR Management API
After=network.target postgresql.service
Wants=r3aler-user-auth-api.service

[Service]
Type=simple
User=r3aler
WorkingDirectory=/opt/r3aler/deploy_package_prod
Environment="PATH=/opt/r3aler/deploy_package_prod/venv/bin"
ExecStart=/opt/r3aler/deploy_package_prod/venv/bin/python management_api_secured.py
Restart=on-failure
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

### r3aler-user-auth-api.service

```ini
[Unit]
Description=R3ÆLƎR User Auth API
After=network.target postgresql.service

[Service]
Type=simple
User=r3aler
WorkingDirectory=/opt/r3aler/deploy_package_prod
Environment="PATH=/opt/r3aler/deploy_package_prod/venv/bin"
ExecStart=/opt/r3aler/deploy_package_prod/venv/bin/python user_auth_api_secured.py
Restart=on-failure
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

### r3aler-knowledge-api.service

```ini
[Unit]
Description=R3ÆLƎR Knowledge API
After=network.target postgresql.service r3aler-user-auth-api.service

[Service]
Type=simple
User=r3aler
WorkingDirectory=/opt/r3aler/deploy_package_prod
Environment="PATH=/opt/r3aler/deploy_package_prod/venv/bin"
ExecStart=/opt/r3aler/deploy_package_prod/venv/bin/python knowledge_api.py
Restart=on-failure
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

### r3aler-droid-api.service

```ini
[Unit]
Description=R3ÆLƎR Droid API
After=network.target postgresql.service r3aler-user-auth-api.service

[Service]
Type=simple
User=r3aler
WorkingDirectory=/opt/r3aler/deploy_package_prod
Environment="PATH=/opt/r3aler/deploy_package_prod/venv/bin"
ExecStart=/opt/r3aler/deploy_package_prod/venv/bin/python droid_api.py
Restart=on-failure
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

### r3aler-storage-facility-api.service

```ini
[Unit]
Description=R3ÆLƎR Storage Facility API
After=network.target postgresql.service r3aler-user-auth-api.service

[Service]
Type=simple
User=r3aler
WorkingDirectory=/opt/r3aler/deploy_package_prod
Environment="PATH=/opt/r3aler/deploy_package_prod/venv/bin"
ExecStart=/opt/r3aler/deploy_package_prod/venv/bin/python self_hosted_storage_facility_secured.py
Restart=on-failure
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

### Deploy Services

```bash
sudo cp r3aler-*.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable r3aler-management-api.service
sudo systemctl enable r3aler-user-auth-api.service
sudo systemctl enable r3aler-knowledge-api.service
sudo systemctl enable r3aler-droid-api.service
sudo systemctl enable r3aler-storage-facility-api.service

# Start all services
sudo systemctl start r3aler-management-api.service
sudo systemctl start r3aler-user-auth-api.service
sudo systemctl start r3aler-knowledge-api.service
sudo systemctl start r3aler-droid-api.service
sudo systemctl start r3aler-storage-facility-api.service

# Check status
sudo systemctl status r3aler-*.service
```

## Monitoring & Maintenance

### Health Check Script

```bash
#!/bin/bash

echo "=== R3ÆLƎR AI System Health Check ==="
echo

# Check each API
for port in 5001 5003 5004 5005 5006; do
    response=$(curl -s http://localhost:$port/health)
    if echo "$response" | jq -e '.status == "healthy"' > /dev/null 2>&1; then
        echo "✅ Port $port: Healthy"
    else
        echo "❌ Port $port: Unhealthy"
    fi
done

echo
echo "=== Service Logs ==="
journalctl -u r3aler-*.service -n 10 --no-pager

echo
echo "=== System Resources ==="
free -h
df -h /
```

### Backup Strategy

```bash
# Backup PostgreSQL database
pg_dump -h 127.0.0.1 -U r3aler_user_2025 r3aler_ai > backup_r3aler_ai_$(date +%Y%m%d).sql

# Backup .env.local (encrypted)
gpg --encrypt --recipient backup@r3al3rai.com .env.local

# Backup API logs
tar -czf logs_backup_$(date +%Y%m%d).tar.gz /opt/r3aler/logs/
```

## Rollback Procedure

In case of issues:

```bash
# Stop all services
sudo systemctl stop r3aler-*.service

# Restore .env.local from backup
cp .env.local.backup .env.local

# Restore database
psql -h 127.0.0.1 -U r3aler_user_2025 r3aler_ai < backup_r3aler_ai_YYYYMMDD.sql

# Restart services
sudo systemctl start r3aler-*.service

# Verify
sudo systemctl status r3aler-*.service
```

## Testing

### Register New User

```bash
curl -X POST http://localhost:5003/api/user/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@r3al3rai.com",
    "password": "SecurePass123",
    "subscription_tier": "pro"
  }'
```

### Login

```bash
curl -X POST http://localhost:5003/api/user/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "SecurePass123"
  }'
```

### Query Knowledge Base

```bash
curl -X GET "http://localhost:5004/api/query?topic=quantum" \
  -H "X-API-Key: your_api_key_here"
```

### Search Storage Unit

```bash
curl -X POST http://localhost:5006/api/unit/quantum/search \
  -H "X-API-Key: your_api_key_here" \
  -H "Content-Type: application/json" \
  -d '{"query": "superposition", "limit": 10}'
```

## Troubleshooting

### API Not Starting

```bash
# Check logs
journalctl -u r3aler-knowledge-api.service -n 50

# Test database connection
psql -h 127.0.0.1 -U r3aler_user_2025 -d r3aler_ai

# Verify .env.local exists and is readable
ls -la /opt/r3aler/deploy_package_prod/.env.local
```

### Database Connection Issues

```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Test SSL connection
psql -h 127.0.0.1 -U r3aler_user_2025 -d r3aler_ai "sslmode=require"

# Check database user privileges
psql -U postgres -c "\du r3aler_user_2025"
```

### Rate Limiting Issues

If users hit rate limits, adjust in .env.local:

```env
# Rate limit configurations can be adjusted in each API's rate_limiter settings
# Default: 50/hour, Custom: Adjust decorator values
```

## Security Checklist for Production

- [ ] All .env variables configured with secure values
- [ ] PostgreSQL SSL/TLS certificate installed
- [ ] Firewall rules configured (5001-5006)
- [ ] Regular database backups enabled
- [ ] SSL certificate for r3al3rai.com configured (Nginx/Apache)
- [ ] All systemd services enabled and running
- [ ] Health checks configured with monitoring system
- [ ] API logs rotated daily
- [ ] Database user password strong and unique
- [ ] IP whitelist configured if needed
- [ ] CORS origins whitelist verified
- [ ] Rate limiting tested and verified
- [ ] All APIs returning "healthy" on /health endpoint

## Performance Optimization

### Database Optimization

```sql
-- Add indexes for common queries
CREATE INDEX idx_profiles_username ON user_unit.profiles(username);
CREATE INDEX idx_sessions_expires ON user_unit.sessions(expires_at);
CREATE INDEX idx_knowledge_topic ON physics_unit.knowledge(topic);

-- ANALYZE for query planner
ANALYZE;
```

### Cache Configuration

**Knowledge API**: 30,657 entries loaded at startup
**Droid API**: LRU cache with 1000 max entries, 3600s TTL

### Load Balancing (Optional)

For production at scale, consider Nginx reverse proxy:

```nginx
upstream r3aler_apis {
    least_conn;
    server localhost:5004 weight=1;  # Knowledge
    server localhost:5005 weight=1;  # Droid
    server localhost:5006 weight=1;  # Storage
}

server {
    listen 443 ssl http2;
    server_name r3al3rai.com;
    
    ssl_certificate /path/to/r3al3rai.com_ssl_certificate.cer;
    ssl_certificate_key /path/to/private.key;
    
    location /api {
        proxy_pass http://r3aler_apis;
    }
}
```

---

**Last Updated**: 2024-12-15  
**Version**: 2.0.0  
**Status**: Production Ready  
**Deployment Target**: 72.17.63.255:5001-5006
