# 🐧 R3ALER AI - Complete WSL Ubuntu Installation Guide

## 📋 Prerequisites

### 1. Install WSL2 with Ubuntu (if not already installed)

```powershell
# In Windows PowerShell (as Administrator):
wsl --install -d Ubuntu-22.04

# Or if WSL is already installed:
wsl --install Ubuntu-22.04
```

### 2. Update WSL to latest version
```powershell
wsl --update
wsl --shutdown
```

## 🚀 Step-by-Step Installation

### Step 1: Access WSL Ubuntu
```powershell
# From Windows PowerShell, navigate to your project directory
# NOTE: Update this path if your R3ALER AI project is in a different location
cd "C:\Users\work8\OneDrive\Desktop\r3al3rai\New Folder 1\R3al3r-AI Main Working\R3aler-ai\R3aler-ai"

# Enter WSL Ubuntu
wsl
```

### Step 2: Update Ubuntu System
```bash
# Update package lists and upgrade system
sudo apt update && sudo apt upgrade -y

# Install essential build tools
sudo apt install -y build-essential curl wget git
```

### Step 3: Install Python and Dependencies
```bash
# Install Python 3.11+ and pip
sudo apt install -y python3 python3-pip python3-venv python3-dev

# Install additional Python development tools
sudo apt install -y python3-setuptools python3-wheel

# Verify Python installation
python3 --version
pip3 --version
```

### Step 4: Install Node.js and npm
```bash
# Remove any existing Node.js installations that might cause conflicts
sudo apt remove -y nodejs npm

# Clean up any leftover packages
sudo apt autoremove -y
sudo apt autoclean

# Method 1: Install Node.js via NodeSource (Recommended)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Verify installation
node --version
npm --version

# If you still get conflicts, use Method 2 instead:
# Method 2: Install via Snap (Alternative)
# sudo snap install node --classic
```

### Step 5: Install Bitcoin Core Dependencies (Optional but Recommended)
```bash
# For Berkeley DB support (wallet.dat files)
sudo apt install -y libdb-dev libdb++-dev

# Additional crypto libraries
sudo apt install -y libssl-dev libffi-dev

# For Berkeley DB Python bindings
sudo apt install -y python3-bsddb3 || echo "bsddb3 not available in repos, will install via pip"
```

### Step 6: Set Up R3ALER AI Environment
```bash
# Navigate to the R3ALER AI project directory
# Note: Adjust the path based on where you cloned/downloaded the project
cd /mnt/c/Users/work8/OneDrive/Desktop/r3al3rai/New\ Folder\ 1/R3al3r-AI\ Main\ Working/R3aler-ai/R3aler-ai

# Create Python virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Upgrade pip in virtual environment
pip install --upgrade pip

# Install R3ALER AI Python dependencies
# 1. Install Knowledge Base API dependencies
cd AI_Core_Worker
pip install -r requirements-kb-api.txt
cd ..

# 2. Install Backend Python dependencies (Droid API, etc.)
cd application/Backend
pip install -r requirements.txt
cd ../..

# 3. Install wallet extractor dependencies
cd Tools/tools
pip install -r requirements.txt
cd ../..

# 4. Install server dependencies (OPTIONAL - only if using FastAPI server module)
# Note: Skip this step if you only need the main R3ALER AI functionality
cd server
pip install -r requirements.txt
cd ..
```

### Step 7: Install Node.js Dependencies
```bash
# Install backend Node.js dependencies
cd application/Backend
npm install
cd ../..
```

### Step 8: Test Installation
```bash
# Ensure you're in the project root directory
pwd  # Should show the R3aler-ai project path

# Make sure virtual environment is activated
source .venv/bin/activate

# Test Python environment
python3 --version
pip list | grep -E "(Flask|cryptography|base58)"

# Test Node.js environment
node --version
npm --version

# Test that required Python packages are installed
python3 -c "import flask, cryptography, base58, requests; print('Core Python packages OK')"

# Test wallet extractor (optional)
cd Tools/tools
python3 -c "import wallet_extractor; print('Wallet extractor module OK')" || echo "Wallet extractor test skipped"
cd ../..

# Verify directory structure
ls -la AI_Core_Worker/
ls -la application/Backend/
ls -la Tools/tools/
```

## 🚀 Starting R3ALER AI in WSL Ubuntu

### Method 1: Using Our WSL Scripts (Recommended)
```bash
# Make scripts executable
chmod +x scripts/wsl/*.sh

# Start the system
chmod +x scripts/wsl/*.sh
```

### Method 2: Manual Startup (For Troubleshooting)
```bash
# Ensure you're in the project root directory
cd /mnt/c/Users/work8/OneDrive/Desktop/r3al3rai/New\ Folder\ 1/R3al3r-AI\ Main\ Working/R3aler-ai/R3aler-ai

# Activate virtual environment
source .venv/bin/activate

# Option A: Start all services in foreground (for debugging)
# Terminal 1: Start Knowledge API
cd AI_Core_Worker
python3 knowledge_api.py
# This will block - open new terminal for next service

# In new terminal - Terminal 2: Start Droid API
cd /mnt/c/Users/work8/OneDrive/Desktop/r3al3rai/New\ Folder\ 1/R3al3r-AI\ Main\ Working/R3aler-ai/R3aler-ai
source .venv/bin/activate
cd application/Backend
python3 droid_api.py
# This will block - open new terminal for next service

# In new terminal - Terminal 3: Start Backend Server
cd /mnt/c/Users/work8/OneDrive/Desktop/r3al3rai/New\ Folder\ 1/R3al3r-AI\ Main\ Working/R3aler-ai/R3aler-ai
cd application/Backend
npm start

# Option B: Start all services in background (single terminal)
# Knowledge API
cd AI_Core_Worker
python3 knowledge_api.py &
cd ..

# Droid API
cd application/Backend
python3 droid_api.py &

# Backend Server
npm start &
cd ../..
```

### Method 3: Background Services with nohup
```bash
# Ensure you're in the project root directory
cd /mnt/c/Users/work8/OneDrive/Desktop/r3al3rai/New\ Folder\ 1/R3al3r-AI\ Main\ Working/R3aler-ai/R3aler-ai

# Start all services in background
source .venv/bin/activate

# Knowledge API
cd AI_Core_Worker
nohup python3 knowledge_api.py > ../knowledge-api.log 2>&1 &
echo $! > ../knowledge-api.pid
cd ..

# Droid API
cd application/Backend
nohup python3 droid_api.py > ../../droid-api.log 2>&1 &
echo $! > ../../droid-api.pid

# Backend Server (Node.js)
nohup npm start > ../../backend-server.log 2>&1 &
echo $! > ../../backend-server.pid
cd ../..
```

## 🔧 Management Commands

### Check Service Status
```bash
# Check if services are running
ps aux | grep -E "(python3|node)" | grep -v grep

# Check ports
ss -tuln | grep -E "(3000|5001|5002)"

# Check logs
tail -f knowledge-api.log
tail -f droid-api.log
tail -f backend-server.log
```

### Stop Services
```bash
# Kill services by PID files
if [ -f knowledge-api.pid ]; then kill $(cat knowledge-api.pid) && rm knowledge-api.pid; fi
if [ -f droid-api.pid ]; then kill $(cat droid-api.pid) && rm droid-api.pid; fi
if [ -f backend-server.pid ]; then kill $(cat backend-server.pid) && rm backend-server.pid; fi

# Or use our stop script
./scripts/wsl/stop-wsl-system.sh
```

## 🌐 Access from Windows

Once services are running in WSL, access from Windows browser:

- **Main Application**: http://localhost:3000
- **Knowledge API**: http://localhost:5001
- **Droid API**: http://localhost:5002

## 🛠️ Troubleshooting

### Permission Issues
```bash
# Fix file permissions
sudo chown -R $USER:$USER /mnt/c/Users/work8/OneDrive/Desktop/r3al3rai/
chmod +x scripts/wsl/*.sh
```

### Python Package Issues
```bash
# Recreate virtual environment
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip

# Install packages one by one
pip install Flask==3.0.0
pip install flask-cors==4.0.0
pip install requests==2.31.0
pip install openai==1.3.0
pip install cryptography
pip install base58
```

### Berkeley DB Issues
```bash
# Install Berkeley DB from source (if needed)
wget http://download.oracle.com/berkeley-db/db-5.3.28.tar.gz
tar -xzf db-5.3.28.tar.gz
cd db-5.3.28/build_unix
../dist/configure --prefix=/usr/local --enable-cxx
make && sudo make install

# Then install bsddb3
pip install bsddb3
```

### Node.js Issues
```bash
# If you get dependency conflicts, completely remove Node.js and reinstall
sudo apt remove -y nodejs npm
sudo apt autoremove -y
sudo apt autoclean

# Method 1: Clean install via NodeSource
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt update
sudo apt install -y nodejs

# Method 2: If NodeSource fails, use Snap
sudo snap install node --classic

# Method 3: Use Node Version Manager (NVM) - Most reliable
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
source ~/.bashrc
nvm install 18
nvm use 18
nvm alias default 18

# Verify installation
node --version
npm --version

# Clear npm cache and reinstall dependencies
cd application/Backend
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
cd ../..
```

### Port Access Issues
```bash
# Check if ports are bound correctly
netstat -tlnp | grep -E "(3000|5001|5002)"

# Test port connectivity
curl http://localhost:3000
curl http://localhost:5001
curl http://localhost:5002
```

### WSL Networking Issues
```bash
# Get WSL IP address
ip addr show eth0

# If localhost doesn't work, try WSL IP from Windows
# From Windows PowerShell:
wsl hostname -I
```

## 📊 System Monitoring

### Create Monitoring Script
```bash
# Create monitor.sh
cat << 'EOF' > monitor.sh
#!/bin/bash
echo "=== R3ALER AI System Status ==="
echo "Date: $(date)"
echo ""

echo "Services:"
ps aux | grep -E "(python3.*knowledge_api|python3.*droid_api|npm.*start)" | grep -v grep || echo "No services running"

echo ""
echo "Ports:"
ss -tuln | grep -E "(3000|5001|5002)" || echo "No ports listening"

echo ""
echo "Memory Usage:"
free -h

echo ""
echo "Disk Usage:"
df -h /

echo ""
echo "Recent Logs:"
if [ -f knowledge-api.log ]; then
    echo "Knowledge API (last 3 lines):"
    tail -3 knowledge-api.log
fi
if [ -f droid-api.log ]; then
    echo "Droid API (last 3 lines):"
    tail -3 droid-api.log
fi
if [ -f backend-server.log ]; then
    echo "Backend Server (last 3 lines):"
    tail -3 backend-server.log
fi
EOF

chmod +x monitor.sh
```

### Use the Monitor
```bash
# Run system monitor
./monitor.sh

# Watch continuously (updates every 5 seconds)
watch -n 5 ./monitor.sh
```

## 🎯 Quick Start Summary

```bash
# One-time setup (run once)
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv build-essential

# Install Node.js (clean method to avoid conflicts)
sudo apt remove -y nodejs npm 2>/dev/null || true
sudo apt autoremove -y
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Project setup (run once per project)
# Navigate to project directory
cd /mnt/c/Users/work8/OneDrive/Desktop/r3al3rai/New\ Folder\ 1/R3al3r-AI\ Main\ Working/R3aler-ai/R3aler-ai

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install Python dependencies
pip install -r AI_Core_Worker/requirements-kb-api.txt
pip install -r application/Backend/requirements.txt
pip install -r Tools/tools/requirements.txt
# Optional: pip install -r server/requirements.txt  # Only if using FastAPI server

# Install Node.js dependencies
cd application/Backend && npm install && cd ../..

# Daily usage
source .venv/bin/activate
./scripts/wsl/start-wsl-simple.sh
# Access: http://localhost:3000

# Stop services
./scripts/wsl/stop-wsl-system.sh
```

## 💡 Pro Tips

1. **Performance**: WSL2 provides near-native Linux performance
2. **File Access**: Your Windows files are at `/mnt/c/...`
3. **VS Code**: Use the WSL extension for seamless development
4. **Aliases**: Add to `~/.bashrc`:
   ```bash
   # R3ALER AI aliases for quick access
   alias r3start='cd /mnt/c/Users/work8/OneDrive/Desktop/r3al3rai/New\ Folder\ 1/R3al3r-AI\ Main\ Working/R3aler-ai/R3aler-ai && source .venv/bin/activate && ./scripts/wsl/start-wsl-simple.sh'
   alias r3stop='cd /mnt/c/Users/work8/OneDrive/Desktop/r3al3rai/New\ Folder\ 1/R3al3r-AI\ Main\ Working/R3aler-ai/R3aler-ai && ./scripts/wsl/stop-wsl-system.sh'
   alias r3status='cd /mnt/c/Users/work8/OneDrive/Desktop/r3al3rai/New\ Folder\ 1/R3al3r-AI\ Main\ Working/R3aler-ai/R3aler-ai && ./scripts/wsl/check-wsl-status.sh'
   alias r3cd='cd /mnt/c/Users/work8/OneDrive/Desktop/r3al3rai/New\ Folder\ 1/R3al3r-AI\ Main\ Working/R3aler-ai/R3aler-ai'
   ```

This guide provides complete WSL Ubuntu setup for optimal R3ALER AI performance with native Linux compatibility!