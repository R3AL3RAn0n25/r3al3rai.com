#!/bin/bash
# Complete WSL2 Supervisor deployment
# Run this script in WSL2: bash complete-wsl-deployment.sh

set -e  # Exit on error

echo "==================================="
echo "WSL2 R3AL3R AI Deployment Completion"
echo "==================================="
echo ""

# Step 1: Create log directory
echo "[1/6] Creating log directory..."
sudo mkdir -p /var/log/r3aler
sudo chown -R r3aler:r3aler /var/log/r3aler
sudo chmod 755 /var/log/r3aler
echo "✓ Log directory created: /var/log/r3aler"
echo ""

# Step 2: Verify run scripts exist
echo "[2/6] Checking run scripts..."
if sudo ls /opt/r3aler-ai/AI_Core_Worker/run_*.py > /dev/null 2>&1; then
    echo "✓ Run scripts found:"
    sudo ls -lh /opt/r3aler-ai/AI_Core_Worker/run_*.py
else
    echo "⚠ Warning: Run scripts not found"
    echo "Checking what files exist in AI_Core_Worker:"
    sudo ls -lh /opt/r3aler-ai/AI_Core_Worker/*.py | head -20
fi
echo ""

# Step 3: Create Supervisor configuration (if needed)
echo "[3/6] Setting up Supervisor configuration..."
if [ -f /etc/supervisor/conf.d/r3aler-ai.conf ]; then
    echo "✓ Supervisor config already exists"
else
    echo "Creating Supervisor configuration..."
    sudo tee /etc/supervisor/conf.d/r3aler-ai.conf > /dev/null <<'EOF'
[group:r3aler]
programs=backend,intelligence,knowledge,storage

[program:backend]
command=/opt/r3aler-ai/.venv/bin/python /opt/r3aler-ai/AI_Core_Worker/run_backend.py
directory=/opt/r3aler-ai
user=r3aler
autostart=true
autorestart=true
stderr_logfile=/var/log/r3aler/backend.log
stdout_logfile=/var/log/r3aler/backend.log

[program:intelligence]
command=/opt/r3aler-ai/.venv/bin/python /opt/r3aler-ai/AI_Core_Worker/run_intelligence.py
directory=/opt/r3aler-ai
user=r3aler
autostart=true
autorestart=true
stderr_logfile=/var/log/r3aler/intelligence.log
stdout_logfile=/var/log/r3aler/intelligence.log

[program:knowledge]
command=/opt/r3aler-ai/.venv/bin/python /opt/r3aler-ai/AI_Core_Worker/run_knowledge.py
directory=/opt/r3aler-ai
user=r3aler
autostart=true
autorestart=true
stderr_logfile=/var/log/r3aler/knowledge.log
stdout_logfile=/var/log/r3aler/knowledge.log

[program:storage]
command=/opt/r3aler-ai/.venv/bin/python /opt/r3aler-ai/AI_Core_Worker/run_storage.py
directory=/opt/r3aler-ai
user=r3aler
autostart=true
autorestart=true
stderr_logfile=/var/log/r3aler/storage.log
stdout_logfile=/var/log/r3aler/storage.log
EOF
    echo "✓ Supervisor config created"
fi
echo ""

# Step 4: Reload Supervisor configuration
echo "[4/6] Reloading Supervisor configuration..."
sudo supervisorctl reread
sudo supervisorctl update
echo "✓ Supervisor configuration reloaded"
echo ""

# Step 5: Start all services
echo "[5/6] Starting R3AL3R AI services..."
sudo supervisorctl start r3aler:*
sleep 2  # Give services time to start
echo "✓ Services started"
echo ""

# Step 6: Check service status
echo "[6/6] Service Status:"
echo "===================="
sudo supervisorctl status
echo ""

# Check logs for errors
echo "Recent logs (last 10 lines each):"
echo "=================================="
for service in backend intelligence knowledge storage; do
    if [ -f /var/log/r3aler/${service}.log ]; then
        echo ""
        echo "--- ${service}.log ---"
        sudo tail -5 /var/log/r3aler/${service}.log 2>/dev/null || echo "(no logs yet)"
    fi
done
echo ""

echo "==================================="
echo "Deployment Complete!"
echo "==================================="
echo ""
echo "Services should be running on:"
echo "  - Backend:      localhost:3002"
echo "  - Storage:      localhost:3003"
echo "  - Knowledge:    localhost:5004"
echo "  - Intelligence: localhost:5010"
echo ""
echo "View logs: sudo tail -f /var/log/r3aler/*.log"
echo "Control services: sudo supervisorctl status|start|stop|restart r3aler:*"
echo ""
