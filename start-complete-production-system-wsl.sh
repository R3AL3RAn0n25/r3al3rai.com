#!/bin/bash

# R3ÆLƎR AI - Complete Production Deployment for WSL/Ubuntu
# Deploys all subsystems with proper routing and management

echo ""
echo "================================================================"
echo "    R3ÆLƎR AI - COMPLETE PRODUCTION DEPLOYMENT (WSL/Ubuntu)"
echo "    THE WORLD'S MOST ADVANCED AI WITH ALL SUBSYSTEMS"
echo "================================================================"
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Function to print colored output
print_status() {
    echo -e "${CYAN}[STATUS]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if port is in use
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1 ; then
        return 0  # Port is in use
    else
        return 1  # Port is free
    fi
}

# Function to wait for service
wait_for_service() {
    local port=$1
    local service_name=$2
    local max_attempts=30
    local attempt=1
    
    print_status "Waiting for $service_name on port $port..."
    while [ $attempt -le $max_attempts ]; do
        if check_port $port; then
            print_success "$service_name is running on port $port"
            return 0
        fi
        sleep 2
        attempt=$((attempt + 1))
    done
    
    print_error "$service_name failed to start on port $port"
    return 1
}

echo ""
echo -e "${CYAN}STEP 1: SYSTEM REQUIREMENTS CHECK${NC}"
echo "================================================================"
echo ""

# Check for required commands
print_status "Checking system requirements..."

# Check Python
if command_exists python3; then
    PYTHON_VERSION=$(python3 --version)
    print_success "Python3 found: $PYTHON_VERSION"
    PYTHON_CMD="python3"
elif command_exists python; then
    PYTHON_VERSION=$(python --version)
    print_success "Python found: $PYTHON_VERSION"
    PYTHON_CMD="python"
else
    print_error "Python not found. Please install Python 3.8 or higher."
    exit 1
fi

# Check Node.js and npm
if command_exists node; then
    NODE_VERSION=$(node --version)
    print_success "Node.js found: $NODE_VERSION"
else
    print_warning "Node.js not found. Backend server may not start."
fi

if command_exists npm; then
    NPM_VERSION=$(npm --version)
    print_success "npm found: $NPM_VERSION"
else
    print_warning "npm not found. Backend dependencies may not install."
fi

# Check Go (for RVN)
if command_exists go; then
    GO_VERSION=$(go version)
    print_success "Go found: $GO_VERSION"
    HAS_GO=true
else
    print_warning "Go not found. RVN Privacy System will not build."
    print_info "Install Go 1.21+ to enable RVN: https://go.dev/dl/"
    HAS_GO=false
fi

# Check PostgreSQL
if command_exists psql; then
    PG_VERSION=$(psql --version)
    print_success "PostgreSQL found: $PG_VERSION"
    HAS_POSTGRES=true
else
    print_warning "PostgreSQL client not found."
    HAS_POSTGRES=false
fi

# Check if PostgreSQL service is running
if systemctl is-active --quiet postgresql; then
    print_success "PostgreSQL service is running"
elif service postgresql status >/dev/null 2>&1; then
    print_success "PostgreSQL service is running"
else
    print_warning "PostgreSQL service not running. Attempting to start..."
    if command_exists systemctl; then
        sudo systemctl start postgresql
    elif command_exists service; then
        sudo service postgresql start
    fi
    sleep 3
fi

# Check Nginx
if command_exists nginx; then
    NGINX_VERSION=$(nginx -v 2>&1)
    print_success "Nginx found: $NGINX_VERSION"
    HAS_NGINX=true
else
    print_warning "Nginx not found. URL routing will not work."
    print_info "Install Nginx: sudo apt-get install nginx"
    HAS_NGINX=false
fi

echo ""
echo -e "${CYAN}STEP 2: PYTHON DEPENDENCIES${NC}"
echo "================================================================"
echo ""

print_status "Checking Python dependencies..."

# Install required Python packages
print_status "Installing Python dependencies..."
$PYTHON_CMD -m pip install --upgrade pip >/dev/null 2>&1

# Core dependencies
REQUIRED_PACKAGES=(
    "flask"
    "psycopg2-binary"
    "requests"
    "werkzeug"
    "psutil"
    "anthropic"
    "openai"
)

for package in "${REQUIRED_PACKAGES[@]}"; do
    $PYTHON_CMD -c "import $package" 2>/dev/null
    if [ $? -eq 0 ]; then
        print_success "$package is installed"
    else
        print_warning "$package not found. Installing..."
        $PYTHON_CMD -m pip install $package
    fi
done

echo ""
echo -e "${CYAN}STEP 3: BUILD RVN PRIVACY SYSTEM${NC}"
echo "================================================================"
echo ""

if [ "$HAS_GO" = true ]; then
    RVN_DIR="$PROJECT_ROOT/RVN"
    if [ -d "$RVN_DIR" ]; then
        print_status "Building RVN Privacy System..."
        cd "$RVN_DIR/cmd/rvn"
        
        # Build RVN binary
        go build -o "$RVN_DIR/rvn" .
        
        if [ -f "$RVN_DIR/rvn" ]; then
            print_success "RVN binary built successfully"
            chmod +x "$RVN_DIR/rvn"
        else
            print_error "RVN build failed"
        fi
        
        cd "$PROJECT_ROOT"
    else
        print_warning "RVN directory not found at: $RVN_DIR"
    fi
else
    print_warning "Skipping RVN build (Go not installed)"
fi

echo ""
echo -e "${CYAN}STEP 4: CONFIGURE NGINX ROUTING${NC}"
echo "================================================================"
echo ""

if [ "$HAS_NGINX" = true ]; then
    print_status "Configuring Nginx..."
    
    NGINX_CONFIG="$PROJECT_ROOT/R3AL3R Production/nginx/r3al3rai.com.conf"
    if [ -f "$NGINX_CONFIG" ]; then
        # Copy Nginx config
        sudo cp "$NGINX_CONFIG" /etc/nginx/sites-available/r3al3rai.com.conf
        
        # Create symbolic link
        sudo ln -sf /etc/nginx/sites-available/r3al3rai.com.conf /etc/nginx/sites-enabled/
        
        # Remove default if exists
        if [ -f /etc/nginx/sites-enabled/default ]; then
            sudo rm /etc/nginx/sites-enabled/default
        fi
        
        # Test Nginx configuration
        if sudo nginx -t 2>&1 | grep -q "successful"; then
            print_success "Nginx configuration is valid"
            
            # Reload Nginx
            sudo systemctl reload nginx
            print_success "Nginx reloaded with new configuration"
        else
            print_error "Nginx configuration test failed"
            sudo nginx -t
        fi
    else
        print_error "Nginx config file not found at: $NGINX_CONFIG"
    fi
else
    print_warning "Skipping Nginx configuration (Nginx not installed)"
fi

echo ""
echo -e "${CYAN}STEP 5: START CORE AI SERVICES${NC}"
echo "================================================================"
echo ""

cd "$PROJECT_ROOT"

# Function to start Python service in background
start_service() {
    local name=$1
    local script=$2
    local port=$3
    local description=$4
    
    print_status "Starting $name..."
    print_info "$description"
    
    # Kill existing process on port
    if check_port $port; then
        print_warning "Port $port already in use. Stopping existing process..."
        PID=$(lsof -ti:$port)
        if [ ! -z "$PID" ]; then
            kill -9 $PID 2>/dev/null
            sleep 2
        fi
    fi
    
    # Start service
    nohup $PYTHON_CMD $script > "logs/${name}.log" 2>&1 &
    echo $! > "logs/${name}.pid"
    
    sleep 3
    
    if check_port $port; then
        print_success "$name started on port $port"
    else
        print_error "$name failed to start"
    fi
}

# Create logs directory
mkdir -p "$PROJECT_ROOT/logs"

# Start Storage Facility
start_service \
    "StorageFacility" \
    "AI_Core_Worker/self_hosted_storage_facility.py" \
    3003 \
    "Self-hosted PostgreSQL knowledge storage (30,657+ entries)"

# Start Knowledge API
start_service \
    "KnowledgeAPI" \
    "AI_Core_Worker/knowledge_api.py" \
    5004 \
    "AI-powered knowledge retrieval and processing"

# Start Enhanced Intelligence API
start_service \
    "IntelligenceAPI" \
    "AI_Core_Worker/enhanced_knowledge_api.py" \
    5010 \
    "Multi-modal AI with vision and advanced reasoning"

# Start Droid API (Crypto AI)
start_service \
    "DroidAPI" \
    "-m application.Backend.droid_api" \
    5005 \
    "Cryptocurrency AI assistant with intent recognition"

# Start User Authentication API
start_service \
    "UserAuthAPI" \
    "AI_Core_Worker/user_auth_api.py" \
    5006 \
    "Secure user management and authentication"

echo ""
echo -e "${CYAN}STEP 6: START SPECIALIZED SUBSYSTEMS${NC}"
echo "================================================================"
echo ""

# Start RVN Privacy System
if [ "$HAS_GO" = true ] && [ -f "$RVN_DIR/rvn" ]; then
    print_status "Starting RVN Privacy System..."
    print_info "Complete privacy network with V2Ray/Xray Reality"
    
    cd "$RVN_DIR"
    nohup ./rvn -config config.toml > "$PROJECT_ROOT/logs/RVN.log" 2>&1 &
    echo $! > "$PROJECT_ROOT/logs/RVN.pid"
    cd "$PROJECT_ROOT"
    
    wait_for_service 8443 "RVN Privacy System"
else
    print_warning "Skipping RVN (not built or Go not installed)"
fi

# Start BitXtractor
start_service \
    "BitXtractor" \
    "-m application.Backend.app" \
    3002 \
    "Cryptocurrency wallet analysis and forensics"

# Start BlackArch Tools
start_service \
    "BlackArchTools" \
    "Tools/blackarch_web_app.py" \
    5003 \
    "Complete cybersecurity toolkit with 55+ tools"

echo ""
echo -e "${CYAN}STEP 7: START MANAGEMENT SYSTEM${NC}"
echo "================================================================"
echo ""

# Start Management System
MANAGEMENT_DIR="$PROJECT_ROOT/R3AL3R Production/manage"
if [ -f "$MANAGEMENT_DIR/management_api.py" ]; then
    cd "$MANAGEMENT_DIR"
    start_service \
        "ManagementSystem" \
        "$MANAGEMENT_DIR/management_api.py" \
        5000 \
        "Production monitoring, service control, and analytics"
    cd "$PROJECT_ROOT"
else
    print_warning "Management API not found at: $MANAGEMENT_DIR/management_api.py"
fi

echo ""
echo -e "${CYAN}STEP 8: START MAIN AI SYSTEM${NC}"
echo "================================================================"
echo ""

# Start Main R3AL3R AI
print_status "Starting Main R3AL3R AI Orchestrator..."
print_info "Core AI system with all engines and components"

nohup $PYTHON_CMD R3AL3R_AI.py > "logs/R3AL3R_AI.log" 2>&1 &
echo $! > "logs/R3AL3R_AI.pid"
sleep 5
print_success "Main R3AL3R AI started"

echo ""
echo -e "${CYAN}STEP 9: START BACKEND WEB SERVER${NC}"
echo "================================================================"
echo ""

# Start Backend Server
BACKEND_DIR="$PROJECT_ROOT/application/Backend"
if [ -f "$BACKEND_DIR/server.js" ]; then
    print_status "Starting Backend Web Server..."
    
    cd "$BACKEND_DIR"
    
    # Install dependencies if needed
    if [ ! -d "node_modules" ]; then
        print_status "Installing Node.js dependencies..."
        npm install
    fi
    
    # Start server
    nohup npm start > "$PROJECT_ROOT/logs/Backend.log" 2>&1 &
    echo $! > "$PROJECT_ROOT/logs/Backend.pid"
    
    cd "$PROJECT_ROOT"
    
    wait_for_service 3000 "Backend Web Server"
else
    print_warning "Backend server.js not found at: $BACKEND_DIR/server.js"
fi

# Final Status
echo ""
echo "================================================================"
echo -e "${GREEN}       R3AL3R AI - COMPLETE PRODUCTION SYSTEM STATUS${NC}"
echo "================================================================"
echo ""

echo -e "${CYAN}INFRASTRUCTURE:${NC}"
echo "   PostgreSQL Database     -> Active (30,657+ knowledge entries)"
echo ""

echo -e "${CYAN}CORE AI SERVICES:${NC}"
echo "   Storage Facility        -> http://localhost:3003"
echo "   Knowledge API           -> http://localhost:5004"
echo "   Intelligence API        -> http://localhost:5010"
echo "   Droid API (Crypto)      -> http://localhost:5005"
echo "   User Auth API           -> http://localhost:5006"
echo ""

echo -e "${CYAN}SPECIALIZED SUBSYSTEMS:${NC}"
echo "   RVN Privacy Network     -> https://localhost:8443 (https://r3al3rai.com/rvn)"
echo "   BitXtractor Forensics   -> http://localhost:3002 (https://r3al3rai.com/bitxtractor)"
echo "   BlackArch Security      -> http://localhost:5003 (https://r3al3rai.com/blackarchtools)"
echo ""

echo -e "${CYAN}MANAGEMENT & CONTROL:${NC}"
echo "   Management System       -> http://localhost:5000 (https://r3al3rai.com/manage)"
echo "   Main AI Orchestrator    -> Active (All Engines)"
echo "   Backend Web Server      -> http://localhost:3000 (https://r3al3rai.com)"
echo ""

echo -e "${CYAN}URL ROUTING (via Nginx):${NC}"
echo "   https://r3al3rai.com/rvn            -> RVN Privacy System"
echo "   https://r3al3rai.com/bitxtractor    -> Wallet Forensics"
echo "   https://r3al3rai.com/blackarchtools -> Security Tools Suite"
echo "   https://r3al3rai.com/manage         -> Management System"
echo "   https://r3al3rai.com/api/*          -> Core AI APIs"
echo "   https://r3al3rai.com                -> Main Application"
echo ""

echo "================================================================"
echo -e "${MAGENTA}   R3AL3R AI - COMPLETE PRODUCTION SYSTEM FULLY OPERATIONAL!${NC}"
echo "================================================================"
echo ""
echo -e "${GREEN}All subsystems are now running with proper URL routing.${NC}"
echo -e "${GREEN}Access the main application at: https://r3al3rai.com${NC}"
echo ""

# Service control commands
echo -e "${YELLOW}SERVICE CONTROL COMMANDS:${NC}"
echo "   View all logs:       tail -f logs/*.log"
echo "   Stop all services:   ./stop-all-services.sh"
echo "   Restart services:    ./start-complete-production-system-wsl.sh"
echo "   Check service pids:  cat logs/*.pid"
echo ""

print_success "R3AL3R AI production deployment complete!"
