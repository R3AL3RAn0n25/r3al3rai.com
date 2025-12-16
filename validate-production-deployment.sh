#!/bin/bash
# =====================================================================
# R3ÆLƎR Production Deployment Validation Script
# =====================================================================
# This script validates that all files are ready for production deployment
# Run on production server after extracting the deployment package
# =====================================================================

DEPLOY_PATH="${1:-.}"
PROD_IP="72.17.63.255"

echo "========================================================"
echo "🔍 R3ÆLƎR Production Deployment Validation"
echo "========================================================"
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Counters
CHECKS_PASSED=0
CHECKS_FAILED=0
CHECKS_WARNING=0

# =====================================================================
# Function: Check file exists
# =====================================================================
check_file() {
    local file=$1
    local description=$2
    
    if [ -f "$DEPLOY_PATH/$file" ]; then
        echo -e "${GREEN}✓${NC} $description"
        ((CHECKS_PASSED++))
        return 0
    else
        echo -e "${RED}✗${NC} $description (NOT FOUND: $file)"
        ((CHECKS_FAILED++))
        return 1
    fi
}

# =====================================================================
# Function: Check directory exists
# =====================================================================
check_dir() {
    local dir=$1
    local description=$2
    
    if [ -d "$DEPLOY_PATH/$dir" ]; then
        echo -e "${GREEN}✓${NC} $description"
        ((CHECKS_PASSED++))
        return 0
    else
        echo -e "${RED}✗${NC} $description (NOT FOUND: $dir)"
        ((CHECKS_FAILED++))
        return 1
    fi
}

# =====================================================================
# Function: Check configuration value
# =====================================================================
check_config() {
    local config_file=$1
    local key=$2
    local description=$3
    
    if grep -q "^$key=" "$DEPLOY_PATH/$config_file"; then
        value=$(grep "^$key=" "$DEPLOY_PATH/$config_file" | cut -d= -f2)
        echo -e "${GREEN}✓${NC} $description: $value"
        ((CHECKS_PASSED++))
        return 0
    else
        echo -e "${YELLOW}⚠${NC} $description (NOT SET: $key)"
        ((CHECKS_WARNING++))
        return 1
    fi
}

# =====================================================================
# Function: Check Python module
# =====================================================================
check_python_module() {
    local module=$1
    local description=$2
    
    if python3 -c "import $module" 2>/dev/null; then
        echo -e "${GREEN}✓${NC} $description installed"
        ((CHECKS_PASSED++))
        return 0
    else
        echo -e "${RED}✗${NC} $description NOT installed"
        ((CHECKS_FAILED++))
        return 1
    fi
}

# =====================================================================
# Step 1: Check Required Files
# =====================================================================
echo -e "${CYAN}[STEP 1/7] Checking Required Files${NC}"
echo ""

check_dir "AI_Core_Worker" "Knowledge API directory"
check_file "AI_Core_Worker/knowledge_api.py" "Knowledge API"
check_dir "src/apis" "Droid API directory"
check_file "src/apis/droid_api.py" "Droid API"
check_file ".env.local" "Environment configuration"

echo ""

# =====================================================================
# Step 2: Check Environment Configuration
# =====================================================================
echo -e "${CYAN}[STEP 2/7] Checking Environment Configuration${NC}"
echo ""

check_config ".env.local" "DB_HOST" "Database host"
check_config ".env.local" "DB_PORT" "Database port"
check_config ".env.local" "DB_NAME" "Database name"
check_config ".env.local" "DB_USER" "Database user"
check_config ".env.local" "FLASK_SECRET_KEY" "Flask secret key"
check_config ".env.local" "CORS_ORIGINS" "CORS configuration"
check_config ".env.local" "KNOWLEDGE_API_PORT" "Knowledge API port"
check_config ".env.local" "DROID_API_PORT" "Droid API port"

echo ""

# =====================================================================
# Step 3: Check Python Installation
# =====================================================================
echo -e "${CYAN}[STEP 3/7] Checking Python Installation${NC}"
echo ""

PYTHON_VERSION=$(python3 --version 2>&1)
if [[ $? -eq 0 ]]; then
    echo -e "${GREEN}✓${NC} Python installed: $PYTHON_VERSION"
    ((CHECKS_PASSED++))
else
    echo -e "${RED}✗${NC} Python 3 NOT installed"
    ((CHECKS_FAILED++))
fi

echo ""

# =====================================================================
# Step 4: Check Required Python Modules
# =====================================================================
echo -e "${CYAN}[STEP 4/7] Checking Required Python Modules${NC}"
echo ""

check_python_module "flask" "Flask"
check_python_module "flask_cors" "Flask-CORS"
check_python_module "flask_limiter" "Flask-Limiter"
check_python_module "psycopg2" "psycopg2"
check_python_module "bcrypt" "bcrypt"
check_python_module "dotenv" "python-dotenv"
check_python_module "requests" "requests"

echo ""

# =====================================================================
# Step 5: Check Database Configuration
# =====================================================================
echo -e "${CYAN}[STEP 5/7] Checking Database Configuration${NC}"
echo ""

# Extract database config from .env.local
DB_HOST=$(grep "^DB_HOST=" "$DEPLOY_PATH/.env.local" | cut -d= -f2)
DB_PORT=$(grep "^DB_PORT=" "$DEPLOY_PATH/.env.local" | cut -d= -f2)
DB_NAME=$(grep "^DB_NAME=" "$DEPLOY_PATH/.env.local" | cut -d= -f2)
DB_USER=$(grep "^DB_USER=" "$DEPLOY_PATH/.env.local" | cut -d= -f2)

echo -e "${YELLOW}ℹ${NC} Database Configuration:"
echo "  Host: $DB_HOST"
echo "  Port: $DB_PORT"
echo "  Name: $DB_NAME"
echo "  User: $DB_USER"

# Try to connect to database
if command -v psql &> /dev/null; then
    if PGPASSWORD="$(grep '^DB_PASSWORD=' "$DEPLOY_PATH/.env.local" | cut -d= -f2)" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -c "SELECT version();" 2>/dev/null | grep -q "PostgreSQL"; then
        echo -e "${GREEN}✓${NC} Database connection successful"
        ((CHECKS_PASSED++))
    else
        echo -e "${YELLOW}⚠${NC} Database connection test failed (psql may not be configured)"
        ((CHECKS_WARNING++))
    fi
else
    echo -e "${YELLOW}⚠${NC} psql not installed (cannot test database connection)"
    ((CHECKS_WARNING++))
fi

echo ""

# =====================================================================
# Step 6: Check SSL Configuration
# =====================================================================
echo -e "${CYAN}[STEP 6/7] Checking SSL Configuration${NC}"
echo ""

SSL_CERT_PATH=$(grep "^SSL_CERT_PATH=" "$DEPLOY_PATH/.env.local" | cut -d= -f2)
SSL_KEY_PATH=$(grep "^SSL_KEY_PATH=" "$DEPLOY_PATH/.env.local" | cut -d= -f2)

if [ -f "$SSL_CERT_PATH" ]; then
    echo -e "${GREEN}✓${NC} SSL certificate found: $SSL_CERT_PATH"
    ((CHECKS_PASSED++))
else
    echo -e "${YELLOW}⚠${NC} SSL certificate not found: $SSL_CERT_PATH"
    ((CHECKS_WARNING++))
fi

if [ -f "$SSL_KEY_PATH" ]; then
    echo -e "${GREEN}✓${NC} SSL key found: $SSL_KEY_PATH"
    ((CHECKS_PASSED++))
else
    echo -e "${YELLOW}⚠${NC} SSL key not found: $SSL_KEY_PATH"
    ((CHECKS_WARNING++))
fi

echo ""

# =====================================================================
# Step 7: Check Port Availability
# =====================================================================
echo -e "${CYAN}[STEP 7/7] Checking Port Availability${NC}"
echo ""

KNOWLEDGE_PORT=$(grep "^KNOWLEDGE_API_PORT=" "$DEPLOY_PATH/.env.local" | cut -d= -f2)
DROID_PORT=$(grep "^DROID_API_PORT=" "$DEPLOY_PATH/.env.local" | cut -d= -f2)

if netstat -tuln 2>/dev/null | grep -q ":$KNOWLEDGE_PORT "; then
    echo -e "${YELLOW}⚠${NC} Knowledge API port already in use: $KNOWLEDGE_PORT"
    ((CHECKS_WARNING++))
else
    echo -e "${GREEN}✓${NC} Knowledge API port available: $KNOWLEDGE_PORT"
    ((CHECKS_PASSED++))
fi

if netstat -tuln 2>/dev/null | grep -q ":$DROID_PORT "; then
    echo -e "${YELLOW}⚠${NC} Droid API port already in use: $DROID_PORT"
    ((CHECKS_WARNING++))
else
    echo -e "${GREEN}✓${NC} Droid API port available: $DROID_PORT"
    ((CHECKS_PASSED++))
fi

echo ""

# =====================================================================
# Summary
# =====================================================================
echo "========================================================"
echo "📊 Validation Summary"
echo "========================================================"
echo ""
echo -e "${GREEN}✓ Passed: $CHECKS_PASSED${NC}"
echo -e "${YELLOW}⚠ Warnings: $CHECKS_WARNING${NC}"
echo -e "${RED}✗ Failed: $CHECKS_FAILED${NC}"

echo ""

if [ $CHECKS_FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ Production deployment validation SUCCESSFUL${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. Configure systemd service files"
    echo "  2. Install dependencies: pip install -r requirements.txt"
    echo "  3. Start services: systemctl start r3aler-knowledge-api r3aler-droid-api"
    echo "  4. Verify: curl http://localhost:$KNOWLEDGE_PORT/health"
    exit 0
else
    echo -e "${RED}❌ Production deployment validation FAILED${NC}"
    echo ""
    echo "Please fix the above issues before deploying to production."
    exit 1
fi
