# R3ALER AI SystemD Process Management

## Overview
Complete SystemD service management for reliable R3ALER AI operation with automatic restart capabilities, security hardening, and unified service control.

## Components Created

### SystemD Service Files
- **r3aler-backend.service** - Node.js backend server (port 3000)
- **r3aler-knowledge.service** - Python Knowledge API (port 5002)  
- **r3aler-droid.service** - Python Droid API (port 5001)
- **r3aler-ai.target** - Unified service group management

### Management Scripts
- **install-systemd.sh** - Install and enable all services
- **manage-services.sh** - Comprehensive service management
- **manage-services.ps1** - PowerShell wrapper for Windows

## Installation

### Step 1: Install SystemD Services
```bash
# Navigate to project directory
cd /mnt/c/Users/work8/OneDrive/Desktop/r3al3rai/New\ Folder\ 1/R3al3r-AI\ Main\ Working/R3aler-ai/R3aler-ai

# Make script executable
chmod +x scripts/wsl/install-systemd.sh

# Run installation
./scripts/wsl/install-systemd.sh
```

### Step 2: Start Services
```bash
# Start all services
sudo systemctl start r3aler-ai.target

# Check status
sudo systemctl status r3aler-backend
```

## Service Management

### Using Bash Script (WSL)
```bash
# Make management script executable
chmod +x scripts/wsl/manage-services.sh

# Available commands
./scripts/wsl/manage-services.sh start      # Start all services
./scripts/wsl/manage-services.sh stop       # Stop all services
./scripts/wsl/manage-services.sh restart    # Restart all services
./scripts/wsl/manage-services.sh status     # Show status
./scripts/wsl/manage-services.sh logs r3aler-backend  # View logs
./scripts/wsl/manage-services.sh test       # Test endpoints
```

### Using PowerShell (Windows)
```powershell
# Import management functions
. .\scripts\windows\manage-services.ps1

# Available commands
Install-R3alerServices                      # Install services
Start-R3alerServices                        # Start all services
Stop-R3alerServices                         # Stop all services
Restart-R3alerServices                      # Restart all services
Get-R3alerServiceStatus                     # Show status
Get-R3alerServiceLogs -ServiceName r3aler-backend  # View logs
Test-R3alerEndpoints                        # Test endpoints
```

## Service Details

### Backend Service (r3aler-backend.service)
- **Port**: 3000
- **User**: r3al3ran0n24
- **Working Directory**: `/home/r3al3ran0n24/R3aler-ai/application/Backend`
- **Command**: `node backendserver.js`
- **Auto-restart**: Yes (10 second delay)
- **Security**: NoNewPrivileges, PrivateTmp, ProtectSystem=strict

### Knowledge API Service (r3aler-knowledge.service)
- **Port**: 5002
- **User**: r3al3ran0n24
- **Working Directory**: `/home/r3al3ran0n24/R3aler-ai/AI_Core_Worker`
- **Command**: `python knowledge_api.py`
- **Auto-restart**: Yes (10 second delay)
- **Security**: NoNewPrivileges, PrivateTmp, ProtectSystem=strict

### Droid API Service (r3aler-droid.service)
- **Port**: 5001
- **User**: r3al3ran0n24
- **Working Directory**: `/home/r3al3ran0n24/R3aler-ai`
- **Environment**: Flask development mode
- **Auto-restart**: Yes (10 second delay)
- **Security**: NoNewPrivileges, PrivateTmp, ProtectSystem=strict

## Service Features

### Automatic Restart
- All services configured with `Restart=always`
- 10-second restart delay (`RestartSec=10`)
- Automatic recovery from crashes

### Security Hardening
- `NoNewPrivileges=true` - Prevents privilege escalation
- `PrivateTmp=true` - Isolated temporary directories
- `ProtectSystem=strict` - Read-only filesystem protection

### Logging
- All output captured in SystemD journal
- View logs: `sudo journalctl -u <service-name> -f`
- Persistent logging across reboots

### Service Dependencies
- Services start in proper order
- Target file manages all services as group
- Graceful shutdown sequence

## Troubleshooting

### Check Service Status
```bash
sudo systemctl status r3aler-backend
sudo systemctl status r3aler-knowledge
sudo systemctl status r3aler-droid
```

### View Service Logs
```bash
# Follow logs in real-time
sudo journalctl -u r3aler-backend -f

# View recent logs
sudo journalctl -u r3aler-backend -n 50

# View logs since last boot
sudo journalctl -u r3aler-backend -b
```

### Restart Individual Service
```bash
sudo systemctl restart r3aler-backend
```

### Test Endpoints
```bash
# Test backend
curl http://localhost:3000

# Test Knowledge API
curl http://localhost:5002

# Test Droid API
curl http://localhost:5001
```

## Access URLs

After services are running:
- **Frontend**: http://localhost:3000
- **Knowledge API**: http://localhost:5002
- **Droid API**: http://localhost:5001

## Environment Variables

Services use environment variables from:
- Backend: `.env` file in Backend directory
- Knowledge API: System environment
- Droid API: Flask development environment

## Auto-Start Configuration

Services are enabled for automatic start on system boot:
```bash
# Enable auto-start
sudo systemctl enable r3aler-ai.target

# Disable auto-start
sudo systemctl disable r3aler-ai.target
```

## Benefits

### Reliability
- Automatic service recovery
- Process monitoring
- Graceful error handling

### Performance
- Optimized resource usage
- Proper service isolation
- Efficient restart policies

### Management
- Unified service control
- Comprehensive logging
- Easy troubleshooting

### Security
- Process isolation
- Privilege restrictions
- Secure defaults

## Next Steps

1. **Install Services**: Run `install-systemd.sh`
2. **Start System**: `sudo systemctl start r3aler-ai.target`
3. **Verify Operation**: Check status and test endpoints
4. **Monitor Logs**: Use journalctl for troubleshooting
5. **Access Application**: Navigate to http://localhost:3000

This SystemD implementation resolves the backend server stability issues and provides a production-ready process management solution for R3ALER AI.