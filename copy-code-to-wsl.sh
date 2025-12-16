#!/bin/bash
# Copy AI_Core_Worker code to WSL2 deployment

set -e

echo "Copying AI_Core_Worker code to WSL2..."
echo ""

# Copy code from Windows to WSL2
sudo cp -r /mnt/c/Users/work8/OneDrive/Desktop/r3al3rai/New\ Folder\ 1/R3al3r-AI\ Main\ Working/R3aler-ai/R3aler-ai/AI_Core_Worker/* /opt/r3aler-ai/AI_Core_Worker/

# Fix ownership
sudo chown -R r3aler:r3aler /opt/r3aler-ai/AI_Core_Worker

# Verify
echo ""
echo "Files copied:"
sudo ls -lh /opt/r3aler-ai/AI_Core_Worker/*.py | head -20

echo ""
echo "✓ Code copied successfully!"
echo ""
echo "Now run: wsl bash complete-wsl-deployment.sh"
