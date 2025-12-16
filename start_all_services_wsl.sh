#!/bin/bash

# R3AL3R AI - Start All Services in WSL
source .venv_wsl/bin/activate

# Start services in background
echo "🚀 Starting R3AL3R AI Services..."

# Start PostgreSQL
sudo service postgresql start

# Storage Facility (Port 3003)
echo "Starting Storage Facility (Port 3003)..."
python3 AI_Core_Worker/self_hosted_storage_facility_windows.py > logs/storage.log 2>&1 &
STORAGE_PID=$!
echo "  PID: $STORAGE_PID"

sleep 2

# Knowledge API (Port 5004)
echo "Starting Knowledge API (Port 5004)..."
python3 src/apis/knowledge_api.py > logs/knowledge.log 2>&1 &
KNOWLEDGE_PID=$!
echo "  PID: $KNOWLEDGE_PID"

sleep 2

# Enhanced Knowledge/Intelligence API (Port 5010)
echo "Starting Enhanced Intelligence API (Port 5010)..."
python3 src/apis/enhanced_knowledge_api.py > logs/intelligence.log 2>&1 &
INTELLIGENCE_PID=$!
echo "  PID: $INTELLIGENCE_PID"

sleep 2

# Droid API (Port 5005)
echo "Starting Droid API (Port 5005)..."
python3 src/apis/droid_api.py > logs/droid.log 2>&1 &
DROID_PID=$!
echo "  PID: $DROID_PID"

sleep 2

export AUTH_API_PORT=5006

# User Auth API (Port 5006)
echo "Starting User Auth API (Port 5006)..."
python3 src/apis/user_auth_api.py > logs/user_auth.log 2>&1 &
USER_AUTH_PID=$!
echo "  PID: $USER_AUTH_PID"

sleep 2

# Backend Server (Port 3000)
echo "Starting Backend Server (Port 3000)..."
python3 application/Backend/app.py > logs/backend.log 2>&1 &
BACKEND_PID=$!
echo "  PID: $BACKEND_PID"

sleep 2

# Management API (Port 5000)
echo "Starting Management API (Port 5000)..."
cd "R3AL3R Production/manage"
python3 management_api.py > ../../logs/management.log 2>&1 &
MANAGEMENT_PID=$!
cd ../..
echo "  PID: $MANAGEMENT_PID"

echo ""
echo "✅ All services started!"
echo ""
echo "Service URLs:"
echo "  Backend:      http://localhost:3000"
echo "  Storage:      http://localhost:3003"
echo "  Knowledge:    http://localhost:5004"
echo "  Intelligence: http://localhost:5010"
echo "  Droid:        http://localhost:5005"
echo "  User Auth:    http://localhost:5006"
echo "  Management:   http://localhost:5000"
echo ""
echo "Process IDs saved. Use './stop_all_services_wsl.sh' to stop"

# Save PIDs to file
cat > .service_pids << PIDS
STORAGE_PID=$STORAGE_PID
KNOWLEDGE_PID=$KNOWLEDGE_PID
INTELLIGENCE_PID=$INTELLIGENCE_PID
DROID_PID=$DROID_PID
USER_AUTH_PID=$USER_AUTH_PID
BACKEND_PID=$BACKEND_PID
MANAGEMENT_PID=$MANAGEMENT_PID
PIDS

