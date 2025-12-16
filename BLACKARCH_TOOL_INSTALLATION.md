# BlackArch Tool Installation Guide

## How Tool Installation Works in R3AL3R AI

### Understanding the Installation Process

R3AL3R AI's BlackArch integration **registers** tools that are already installed in your WSL system, rather than installing them automatically. This is by design for security and control.

---

## Installation Flow

### 1. Tool Registration vs. System Installation

**Important Distinction:**
- **System Installation**: Installing the actual tool binary in Linux (requires `sudo`)
- **Tool Registration**: Making R3AL3R AI aware of an installed tool (no `sudo` needed)

### 2. What Happens When You Click "Install"

```
User clicks "Install spiderfoot"
         ↓
Frontend → /api/blackarch/install/spiderfoot
         ↓
Node Backend (JWT auth) → Flask Service
         ↓
BlackArchToolsManager checks: which spiderfoot
         ↓
    Found in PATH?
    ├─ YES → Register tool in database ✅
    │        Record executable path
    │        Mark as installed
    │        Return success
    └─ NO  → Return instructions ℹ️
             "Please install manually: sudo apt-get install spiderfoot"
```

---

## How to Install New Tools

### Method 1: System Installation (Recommended)

**Step 1: Install the tool in WSL**
```bash
# Open WSL terminal
sudo apt-get update
sudo apt-get install spiderfoot
```

**Step 2: Register in R3AL3R AI**
- Go back to R3AL3R AI Terminal
- Click "Install" button again
- Tool will now be registered ✅

### Method 2: Manual Package Installation

Some tools require manual setup:

**For tools not in apt repositories:**
```bash
# Example: Installing a tool from GitHub
cd ~/tools
git clone https://github.com/tool/repo.git
cd repo
pip install -r requirements.txt
sudo ln -s $(pwd)/tool.py /usr/local/bin/toolname
```

**Then register in R3AL3R AI:**
- Click "Install" button
- R3AL3R AI will find it in PATH and register it

---

## Currently Available Tools

### ✅ Already Installed (3 tools)
These are ready to use immediately:

1. **nmap** (v7.94)
   - Network scanner
   - Location: `/usr/bin/nmap`
   - Status: Registered and ready

2. **wireshark** (v4.2.2)
   - Network protocol analyzer
   - Location: `/usr/bin/wireshark`
   - Status: Registered and ready (GUI handled)

3. **aircrack-ng** (v1.7)
   - WiFi security suite
   - Location: `/usr/bin/aircrack-ng`
   - Status: Registered and ready

### 📦 Available for Installation (52 tools)

**Quick Install - Essential Tools:**
```bash
sudo apt-get install -y \
  sqlmap \
  nikto \
  hydra \
  john \
  hashcat \
  gobuster \
  masscan \
  dirb
```

**After installation, click "Install" in R3AL3R AI to register each tool.**

---

## Installation Status Responses

### Success Response
```json
{
  "status": "success",
  "message": "Tool nmap registered successfully",
  "tool_info": {
    "name": "nmap",
    "executable_path": "/usr/bin/nmap"
  }
}
```

### Already Installed
```json
{
  "status": "success",
  "message": "Tool nmap is already installed",
  "tool_info": {
    "name": "nmap",
    "version": "7.95",
    "executable_path": "/usr/bin/nmap"
  }
}
```

### Not Found (Needs System Installation)
```json
{
  "status": "error",
  "message": "Tool 'spiderfoot' not found in system",
  "instructions": "Please install manually using: sudo apt-get install spiderfoot",
  "note": "After installation, try this request again to register the tool"
}
```

### Tool Not in Registry
```json
{
  "status": "error",
  "message": "Tool 'unknown-tool' not found in BlackArch registry",
  "hint": "Check available tools at /api/tools"
}
```

---

## Troubleshooting

### "Failed to install" Error

**Cause:** Tool not found in system PATH

**Solution:**
1. Install the tool in WSL: `sudo apt-get install <tool-name>`
2. Verify installation: `which <tool-name>`
3. Try registering again in R3AL3R AI

### Tool Shows as "Not Installed" After System Installation

**Cause:** Tool not yet registered in R3AL3R AI database

**Solution:**
- Click the "Install" button in R3AL3R AI
- Or call the API: `POST /api/blackarch/install/<tool-name>`
- System will scan PATH and register the tool

### Tool Installed But Not in PATH

**Cause:** Tool installed in non-standard location

**Solution:**
```bash
# Find the tool
find /usr -name "<tool-name>" 2>/dev/null

# Create symlink to PATH
sudo ln -s /path/to/tool /usr/local/bin/<tool-name>

# Verify
which <tool-name>

# Register in R3AL3R AI
```

---

## Batch Installation

### Install Multiple Tools at Once

**Option 1: System Command**
```bash
# Install all essential tools
sudo apt-get install -y \
  nmap \
  wireshark \
  sqlmap \
  nikto \
  hydra \
  john \
  hashcat \
  gobuster \
  masscan \
  dirb \
  aircrack-ng
```

**Option 2: From Requirements File**
```bash
# Create requirements file
cat > blackarch_tools.txt <<EOF
nmap
sqlmap
nikto
hydra
john
hashcat
gobuster
EOF

# Install all
cat blackarch_tools.txt | xargs sudo apt-get install -y
```

**Then:** Refresh R3AL3R AI tool list to auto-detect new installations

---

## Auto-Detection on Execution

**Good News:** Even if a tool isn't pre-registered, R3AL3R AI will auto-detect and register it on first execution!

**Example:**
```javascript
// Execute unregistered tool
POST /api/blackarch/execute/sqlmap
Body: {"args": ["--help"]}

// R3AL3R AI will:
// 1. Check if sqlmap is in system
// 2. If found, register it automatically
// 3. Execute the command
// 4. Return output
```

So you can install tools in WSL and use them immediately without manual registration!

---

## Tool Categories and Installation

### Network Scanners
```bash
sudo apt-get install nmap masscan nikto netdiscover
```

### Web Application Testing
```bash
sudo apt-get install sqlmap nikto dirb gobuster wpscan
```

### Password Cracking
```bash
sudo apt-get install john hashcat hydra ophcrack
```

### Wireless Testing
```bash
sudo apt-get install aircrack-ng
```

### Forensics
```bash
sudo apt-get install autopsy bulk-extractor dc3dd
```

### Exploitation Frameworks
```bash
# Metasploit requires special installation
curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > msfinstall
chmod +x msfinstall
sudo ./msfinstall
```

---

## Best Practices

1. **Install Before Registering**: Always install tools in WSL first
2. **Verify Installation**: Use `which <tool>` to confirm
3. **Keep Updated**: Run `sudo apt-get update && sudo apt-get upgrade` regularly
4. **Check Logs**: View BlackArch service logs for installation issues
5. **Use Auto-Execute**: For quick testing, just execute - auto-registration happens

---

## Security Considerations

### Why No Automatic Installation?

**Security Reasons:**
- Installing packages requires `sudo` (root access)
- R3AL3R AI services run as non-privileged user
- User control over what gets installed
- Prevents malicious package installation
- Allows custom verification before install

### Recommended Approach

1. Review tool documentation and purpose
2. Install manually with understanding
3. Verify installation and test
4. Register in R3AL3R AI for integration
5. Use with appropriate permissions

---

## Quick Reference

| Action | Command | Location |
|--------|---------|----------|
| System Install | `sudo apt-get install <tool>` | WSL Terminal |
| Verify Install | `which <tool>` | WSL Terminal |
| Register Tool | Click "Install" button | R3AL3R AI Terminal |
| Check Status | View tool list | R3AL3R AI Terminal |
| Execute Tool | Click tool or use command | R3AL3R AI Terminal |

---

**Remember:** Install in WSL, Register in R3AL3R AI, Execute with Confidence! 🛡️

*For tool-specific installation instructions, see BLACKARCH_QUICK_START.md*
