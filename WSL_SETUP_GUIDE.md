# R3ÆLƎR AI - WSL Setup and Usage Guide

## 🐧 Running R3ÆLƎR AI in WSL

This guide helps you run the complete R3ÆLƎR AI system in Windows Subsystem for Linux (WSL) for better Python compatibility and Linux-native tools.

### 📋 Prerequisites

1. **WSL2 installed** with Ubuntu 20.04+ or Debian
2. **Access to your Windows files** from WSL (typically `/mnt/c/Users/...`)

### 🚀 Quick Start

```bash
# Navigate to your project in WSL
cd "/mnt/c/Users/work8/OneDrive/Desktop/r3al3rai/New Folder 1/R3al3r-AI Main Working/R3aler-ai/R3aler-ai"

# Make scripts executable
chmod +x *.sh

# Start the complete system
./start-wsl-system.sh
```

### 🔧 WSL Scripts Overview

#### 1. **start-wsl-system.sh** - Main startup script
- ✅ Auto-installs missing dependencies (Python, Node.js, etc.)
- ✅ Creates Python virtual environment
- ✅ Installs all required packages
- ✅ Starts all services in background
- ✅ Provides status feedback

#### 2. **stop-wsl-system.sh** - Clean shutdown
- 🛑 Stops all R3ÆLƎR AI services gracefully
- 🛑 Cleans up PID files
- 🛑 Force-kills stuck processes

#### 3. **check-wsl-status.sh** - System monitoring
- 📊 Shows service status (running/stopped)
- 📊 Checks port accessibility
- 📊 Displays system resources
- 📊 Shows recent log entries

### 🌐 Service Endpoints

Once started, access these URLs from your Windows browser:

- **Frontend/Backend**: http://localhost:3000
- **Knowledge API**: http://localhost:5001  
- **Droid API**: http://localhost:5002

### 🔍 Wallet Extractor in WSL

```bash
# Navigate to wallet extractor
cd Tools/tools

# Check dependencies
python wallet_extractor.py --check-deps --json

# Show help
python wallet_extractor.py --help

# Example usage (dry run)
python wallet_extractor.py --wallet /path/to/wallet.dat --dry-run --json
```

### 🛠️ Troubleshooting

#### Permission Issues
```bash
# If scripts aren't executable
chmod +x start-wsl-system.sh stop-wsl-system.sh check-wsl-status.sh
```

#### Python Issues
```bash
# If virtual environment has issues
rm -rf .venv
./start-wsl-system.sh  # Will recreate venv
```

#### Port Conflicts
```bash
# Check what's using ports
./check-wsl-status.sh

# Force stop everything
./stop-wsl-system.sh
```

#### Node.js Issues
```bash
# Update Node.js if too old
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

### 📦 Manual Dependency Installation

If auto-installation fails:

```bash
# Essential packages
sudo apt update
sudo apt install -y python3 python3-pip python3-venv nodejs npm git curl

# For Bitcoin Core development (optional)
sudo apt install -y build-essential autoconf libtool pkg-config libdb-dev libdb++-dev
```

### 🔄 Advanced Usage

#### Background Services Management
```bash
# Start system
./start-wsl-system.sh

# Check status
./check-wsl-status.sh

# View live logs
tail -f knowledge-api_output.log
tail -f droid-api_output.log  
tail -f backend-server_output.log

# Stop system
./stop-wsl-system.sh
```

#### Development Mode
```bash
# For development, you might want to run services individually:

# Terminal 1: Knowledge API
cd AI_Core_Worker
source ../.venv/bin/activate
python knowledge_api.py

# Terminal 2: Droid API
cd application/Backend
source ../../.venv/bin/activate
python droid_api.py

# Terminal 3: Backend Server
cd application/Backend
npm start
```

### 🚨 Important Notes

1. **File Paths**: WSL can access Windows files at `/mnt/c/...`
2. **Performance**: WSL2 provides near-native Linux performance
3. **Networking**: localhost works from both WSL and Windows
4. **Bitcoin Core**: Install Bitcoin Core in WSL for best wallet.dat compatibility
5. **Permissions**: Some operations may require `sudo` in WSL

### 🔐 Security Considerations

- WSL runs with your Windows user privileges
- Be cautious with `sudo` commands
- wallet.dat files should be testnet only
- Consider firewall rules for exposed ports

### 💡 Pro Tips

1. **WSL Integration**: Install Windows Terminal for better WSL experience
2. **VS Code**: Use WSL extension for seamless development
3. **Bitcoin Core**: Install in WSL for native Berkeley DB support
4. **Aliases**: Add helpful aliases to `~/.bashrc`:

```bash
# Add to ~/.bashrc
alias r3start='cd "/mnt/c/path/to/r3aler-ai" && ./start-wsl-system.sh'
alias r3stop='cd "/mnt/c/path/to/r3aler-ai" && ./stop-wsl-system.sh'  
alias r3status='cd "/mnt/c/path/to/r3aler-ai" && ./check-wsl-status.sh'
```

### 🎯 Next Steps

1. Start the system: `./start-wsl-system.sh`
2. Check status: `./check-wsl-status.sh`
3. Test wallet extractor in `Tools/tools/`
4. Access web interface at http://localhost:3000
5. Stop when done: `./stop-wsl-system.sh`

The WSL environment provides the best compatibility for Python dependencies, Berkeley DB support, and native Linux tools while maintaining easy access to your Windows files.