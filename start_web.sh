#!/bin/bash

# BlackArch Web Interface Launcher Script
echo "🛡️ Starting R3AL3R-AI BlackArch Web Interface..."

# Change to the correct directory
cd '/mnt/c/Users/work8/OneDrive/Desktop/r3al3rai/New Folder 1/R3al3r-AI Main Working/R3aler-ai/R3aler-ai'

# Activate virtual environment
source blackarch_venv/bin/activate

# Start the web interface
python3 Tools/launch_web_interface.py