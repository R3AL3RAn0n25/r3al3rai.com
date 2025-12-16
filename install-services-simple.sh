#!/bin/bash
# Simple SystemD service installer for R3ALER AI

echo "Installing R3ALER AI SystemD Services..."

# Copy service files
sudo cp /home/r3al3ran0n24/R3aler-ai/systemd/r3aler-backend.service /etc/systemd/system/
sudo cp /home/r3al3ran0n24/R3aler-ai/systemd/r3aler-knowledge.service /etc/systemd/system/
sudo cp /home/r3al3ran0n24/R3aler-ai/systemd/r3aler-droid.service /etc/systemd/system/
sudo cp /home/r3al3ran0n24/R3aler-ai/systemd/r3aler-ai.target /etc/systemd/system/

# Set permissions
sudo chmod 644 /etc/systemd/system/r3aler-*.service
sudo chmod 644 /etc/systemd/system/r3aler-ai.target

# Reload systemd
sudo systemctl daemon-reload

# Enable services
sudo systemctl enable r3aler-backend.service
sudo systemctl enable r3aler-knowledge.service
sudo systemctl enable r3aler-droid.service
sudo systemctl enable r3aler-ai.target

echo "✓ Services installed and enabled"
echo "Start with: sudo systemctl start r3aler-ai.target"