#!/bin/bash

# R3AL3R AI - Deploy Code to Ubuntu Server
# Run this FROM YOUR WINDOWS MACHINE to upload code to Ubuntu server

set -e

echo "================================================================"
echo "     R3AL3R AI - UPLOAD TO UBUNTU SERVER"
echo "================================================================"
echo ""

# Configuration
read -p "Enter server IP address: " SERVER_IP
read -p "Enter SSH username (default: root): " SSH_USER
SSH_USER=${SSH_USER:-root}

PROJECT_DIR="/opt/r3aler-ai"
LOCAL_DIR="."

echo ""
echo "Uploading R3AL3R AI to $SSH_USER@$SERVER_IP:$PROJECT_DIR..."
echo ""

# Exclude patterns
EXCLUDE=(
    ".git"
    ".venv"
    "__pycache__"
    "*.pyc"
    "*.pyo"
    "*.log"
    "node_modules"
    ".backups"
    "unused_candidates"
    "build"
    "dist"
    "*.egg-info"
)

# Build rsync exclude arguments
EXCLUDE_ARGS=""
for pattern in "${EXCLUDE[@]}"; do
    EXCLUDE_ARGS="$EXCLUDE_ARGS --exclude=$pattern"
done

# Upload using rsync (requires rsync on both systems)
if command -v rsync &> /dev/null; then
    rsync -avz --progress $EXCLUDE_ARGS \
        "$LOCAL_DIR/" "$SSH_USER@$SERVER_IP:$PROJECT_DIR/"
    echo "✓ Code uploaded successfully via rsync"
else
    echo "⚠️  rsync not found. Install rsync or use SCP manually:"
    echo "   scp -r . $SSH_USER@$SERVER_IP:$PROJECT_DIR/"
    exit 1
fi

echo ""
echo "================================================================"
echo "                 UPLOAD COMPLETE!"
echo "================================================================"
echo ""
echo "Now SSH into your server and:"
echo "1. SSH: ssh $SSH_USER@$SERVER_IP"
echo "2. Set permissions: sudo chown -R r3aler:r3aler /opt/r3aler-ai"
echo "3. Start services: sudo supervisorctl start r3aler:*"
echo "4. Check status: sudo supervisorctl status"
echo ""
echo "================================================================"
