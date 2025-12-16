#!/bin/bash

# R3ÆLƎR AI - Stop All Services
# Gracefully stops all running services

echo ""
echo "================================================================"
echo "    R3ÆLƎR AI - STOPPING ALL SERVICES"
echo "================================================================"
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOGS_DIR="$PROJECT_ROOT/logs"

print_status() {
    echo -e "${CYAN}[STATUS]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to stop service by PID file
stop_service() {
    local name=$1
    local pid_file="$LOGS_DIR/${name}.pid"
    
    if [ -f "$pid_file" ]; then
        PID=$(cat "$pid_file")
        if kill -0 $PID 2>/dev/null; then
            print_status "Stopping $name (PID: $PID)..."
            kill -TERM $PID 2>/dev/null
            sleep 2
            
            # Force kill if still running
            if kill -0 $PID 2>/dev/null; then
                kill -9 $PID 2>/dev/null
            fi
            
            rm "$pid_file"
            print_success "$name stopped"
        else
            print_error "$name not running (stale PID file)"
            rm "$pid_file"
        fi
    else
        print_status "$name PID file not found"
    fi
}

# Function to stop service by port
stop_port() {
    local port=$1
    local name=$2
    
    PID=$(lsof -ti:$port 2>/dev/null)
    if [ ! -z "$PID" ]; then
        print_status "Stopping $name on port $port (PID: $PID)..."
        kill -TERM $PID 2>/dev/null
        sleep 2
        
        # Force kill if still running
        PID=$(lsof -ti:$port 2>/dev/null)
        if [ ! -z "$PID" ]; then
            kill -9 $PID 2>/dev/null
        fi
        
        print_success "$name stopped"
    fi
}

# Stop services by PID files
echo -e "${CYAN}Stopping services by PID files...${NC}"
echo ""

stop_service "StorageFacility"
stop_service "KnowledgeAPI"
stop_service "IntelligenceAPI"
stop_service "DroidAPI"
stop_service "UserAuthAPI"
stop_service "BitXtractor"
stop_service "BlackArchTools"
stop_service "ManagementSystem"
stop_service "RVN"
stop_service "R3AL3R_AI"
stop_service "Backend"

echo ""
echo -e "${CYAN}Stopping any remaining services by port...${NC}"
echo ""

# Stop services by port (in case PID files are missing)
stop_port 3003 "Storage Facility"
stop_port 5004 "Knowledge API"
stop_port 5010 "Intelligence API"
stop_port 5005 "Droid API"
stop_port 5006 "User Auth API"
stop_port 8443 "RVN Privacy System"
stop_port 3002 "BitXtractor"
stop_port 5003 "BlackArch Tools"
stop_port 5000 "Management System"
stop_port 3000 "Backend Server"

echo ""
echo "================================================================"
echo -e "${GREEN}   ALL R3AL3R AI SERVICES STOPPED${NC}"
echo "================================================================"
echo ""
print_success "All services have been stopped"
echo ""
