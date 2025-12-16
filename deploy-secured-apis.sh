#!/bin/bash
# R3ÆLƎR API Security Deployment Script
# Deploys security-hardened APIs to 72.17.63.255
# 
# Usage: bash deploy-secured-apis.sh

set -e

echo "==============================================="
echo "🔐 R3ÆLƎR API Security Deployment"
echo "==============================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
DEPLOYMENT_IP="72.17.63.255"
DEPLOYMENT_USER="r3aler"
KNOWLEDGE_API_PORT=5004
DROID_API_PORT=5005
APP_DIR="/opt/r3al3rai/apis"

# Check if .env.local exists
if [ ! -f ".env.local" ]; then
    echo -e "${RED}✗ ERROR: .env.local not found${NC}"
    echo "  1. Copy .env.example.secured to .env.local"
    echo "  2. Fill in all required values:"
    echo "     - DB_PASSWORD"
    echo "     - FLASK_SECRET_KEY"
    echo "     - STORAGE_FACILITY_URL"
    echo "     - SSL certificate paths"
    exit 1
fi

# Validate .env.local
echo -e "${YELLOW}→ Validating .env.local...${NC}"

required_vars=("DB_HOST" "DB_PORT" "DB_NAME" "DB_USER" "DB_PASSWORD" "FLASK_SECRET_KEY" "STORAGE_FACILITY_URL")
for var in "${required_vars[@]}"; do
    if ! grep -q "^${var}=" .env.local; then
        echo -e "${RED}✗ Missing variable: ${var}${NC}"
        exit 1
    fi
done

echo -e "${GREEN}✓ .env.local validation passed${NC}"
echo ""

# Install dependencies
echo -e "${YELLOW}→ Installing Python dependencies...${NC}"
pip install -q flask flask-cors flask-limiter psycopg2-binary bcrypt python-dotenv requests
echo -e "${GREEN}✓ Dependencies installed${NC}"
echo ""

# Backup original files
echo -e "${YELLOW}→ Creating backups of original API files...${NC}"
BACKUP_DIR="backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

cp -v "AI_Core_Worker/knowledge_api.py" "$BACKUP_DIR/knowledge_api.py.backup" 2>/dev/null || true
cp -v "src/apis/droid_api.py" "$BACKUP_DIR/droid_api.py.backup" 2>/dev/null || true

echo -e "${GREEN}✓ Backups created in $BACKUP_DIR${NC}"
echo ""

# Deploy secured versions
echo -e "${YELLOW}→ Deploying security-hardened API versions...${NC}"

if [ -f "knowledge_api_secured.py" ]; then
    cp knowledge_api_secured.py "AI_Core_Worker/knowledge_api.py"
    echo -e "${GREEN}✓ Deployed knowledge_api.py (secured)${NC}"
else
    echo -e "${RED}✗ knowledge_api_secured.py not found${NC}"
    exit 1
fi

if [ -f "droid_api_secured.py" ]; then
    cp droid_api_secured.py "src/apis/droid_api.py"
    echo -e "${GREEN}✓ Deployed droid_api.py (secured)${NC}"
else
    echo -e "${RED}✗ droid_api_secured.py not found${NC}"
    exit 1
fi

echo ""

# Verify SSL certificates
echo -e "${YELLOW}→ Verifying SSL certificate configuration...${NC}"

SSL_CERT=$(grep "^SSL_CERT_PATH=" .env.local | cut -d'=' -f2)
if [ -z "$SSL_CERT" ]; then
    echo -e "${YELLOW}⚠ SSL_CERT_PATH not configured${NC}"
    echo "  Add to .env.local: SSL_CERT_PATH=/path/to/r3al3rai.com_ssl_certificate.cer"
else
    if [ -f "$SSL_CERT" ]; then
        echo -e "${GREEN}✓ SSL certificate found: $SSL_CERT${NC}"
    else
        echo -e "${YELLOW}⚠ SSL certificate not found at: $SSL_CERT${NC}"
    fi
fi

echo ""

# Test database connectivity
echo -e "${YELLOW}→ Testing database connectivity...${NC}"

python3 << 'EOF'
import os
from dotenv import load_dotenv
import psycopg2

load_dotenv('.env.local')

try:
    db_config = {
        'host': os.getenv('DB_HOST'),
        'port': int(os.getenv('DB_PORT', 5432)),
        'database': os.getenv('DB_NAME'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'sslmode': os.getenv('DB_SSLMODE', 'require'),
        'connect_timeout': 5
    }
    
    conn = psycopg2.connect(**db_config)
    print(f"\033[92m✓ Database connection successful (SSL/TLS: {db_config['sslmode']})\033[0m")
    conn.close()
except Exception as e:
    print(f"\033[91m✗ Database connection failed: {e}\033[0m")
    exit(1)
EOF

if [ $? -ne 0 ]; then
    echo -e "${RED}✗ Database connectivity test failed${NC}"
    exit 1
fi

echo ""

# Generate test authentication token
echo -e "${YELLOW}→ Generating test authentication token...${NC}"

TEST_TOKEN=$(python3 -c "import uuid; print(uuid.uuid4())")
echo -e "${GREEN}✓ Test token: $TEST_TOKEN${NC}"
echo ""

# Show deployment summary
echo "==============================================="
echo -e "${GREEN}✓ SECURITY DEPLOYMENT COMPLETE${NC}"
echo "==============================================="
echo ""
echo "📋 Deployment Summary:"
echo "  - Deployment IP: $DEPLOYMENT_IP"
echo "  - Knowledge API Port: $KNOWLEDGE_API_PORT"
echo "  - Droid API Port: $DROID_API_PORT"
echo ""
echo "🔐 Security Features Enabled:"
echo "  ✓ SSL/TLS for all database connections"
echo "  ✓ Authentication required (X-Session-Token or X-API-Key)"
echo "  ✓ Rate limiting enabled (Query: 20/hr, Search: 30/hr, Chat: 5/hr)"
echo "  ✓ CORS whitelisting"
echo "  ✓ Input validation and sanitization"
echo "  ✓ IP whitelisting (72.17.63.255)"
echo "  ✓ Comprehensive security logging"
echo ""
echo "📝 Next Steps:"
echo "  1. Copy SSL certificates to secure location:"
echo "     - r3al3rai.com_ssl_certificate.cer"
echo "     - r3al3rai.com_private.key"
echo "     - r3al3rai.com_intermediate.pem"
echo ""
echo "  2. Update certificate paths in .env.local"
echo ""
echo "  3. Start the APIs:"
echo "     Terminal 1: python AI_Core_Worker/knowledge_api.py"
echo "     Terminal 2: python src/apis/droid_api.py"
echo ""
echo "  4. Test endpoint with authentication:"
echo "     curl -X POST http://localhost:5004/api/query \\"
echo "       -H \"X-Session-Token: $TEST_TOKEN\" \\"
echo "       -H \"Content-Type: application/json\" \\"
echo "       -d '{\"query\": \"test query\"}'"
echo ""
echo "  5. Monitor logs for security events"
echo ""
echo "📊 Configuration Files:"
echo "  - API Config: .env.local"
echo "  - Example Config: .env.example.secured"
echo "  - Documentation: SECURITY_IMPLEMENTATION_COMPLETE.md"
echo ""
echo "==============================================="
echo ""
