# 🐧 R3ÆLƎR AI - WSL Quick Start Guide

## 🚀 How to Run R3ÆLƎR AI in WSL

### Option 1: Simple Start (Recommended)

```bash
# From PowerShell in your project directory:
wsl ./start-wsl-simple.sh
```

This will:
- ✅ Install all dependencies automatically
- ✅ Start all services (Knowledge API, Droid API, Backend)
- ✅ Use system Python (avoids virtual environment issues)

### Option 2: Advanced Start (Full Features)

```bash
# From PowerShell:
wsl ./start-wsl-system.sh
```

This includes virtual environment management and more features.

### 🔧 Management Commands

```bash
# Check if services are running
wsl ./check-wsl-status.sh

# Stop all services
wsl ./stop-wsl-system.sh

# Manual start if needed
wsl ./start-wsl-simple.sh
```

### 🌐 Access Points

Once started, open these in your Windows browser:

- **Main Application**: http://localhost:3000
- **Knowledge API**: http://localhost:5001
- **Droid API**: http://localhost:5002

### 🔍 Wallet Extractor in WSL

```bash
# From PowerShell:
wsl bash -c "cd Tools/tools && python3 wallet_extractor.py --help"

# Check dependencies
wsl bash -c "cd Tools/tools && python3 wallet_extractor.py --check-deps --json"

# Test with a wallet file
wsl bash -c "cd Tools/tools && python3 wallet_extractor.py --wallet /path/to/wallet.dat --dry-run"
```

### 🛠️ Troubleshooting

#### If services don't start:
```bash
# Stop everything first
wsl ./stop-wsl-system.sh

# Try simple start
wsl ./start-wsl-simple.sh
```

#### If you get permission errors:
```bash
# Make scripts executable
wsl chmod +x *.sh
```

#### If you need to install Bitcoin Core in WSL:
```bash
wsl sudo apt update
wsl sudo apt install software-properties-common
wsl sudo add-apt-repository ppa:bitcoin/bitcoin
wsl sudo apt update
wsl sudo apt install bitcoind
```

### 💡 Pro Tips

1. **Keep PowerShell open** - You can run WSL commands directly from PowerShell
2. **File access** - Your Windows files are at `/mnt/c/Users/...` in WSL
3. **Multiple terminals** - Open new PowerShell windows for different WSL sessions
4. **VS Code integration** - Use the WSL extension for seamless development

### 🎯 Complete Workflow

```bash
# 1. Start the system
wsl ./start-wsl-simple.sh

# 2. Check it's running (in another PowerShell window)
wsl ./check-wsl-status.sh

# 3. Use wallet extractor
wsl bash -c "cd Tools/tools && python3 wallet_extractor.py --check-deps"

# 4. Access web interface
# Open http://localhost:3000 in your browser

# 5. Stop when done
wsl ./stop-wsl-system.sh
```

The WSL approach gives you:
- ✅ Better Python package compatibility
- ✅ Native Linux tools
- ✅ Better Berkeley DB support for wallet files
- ✅ Easy access from Windows
- ✅ No virtual environment conflicts