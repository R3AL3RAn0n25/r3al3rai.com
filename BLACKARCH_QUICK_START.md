# BlackArch Tools - Quick Start Guide

## 🚀 How to Use BlackArch Tools in R3AL3R AI

### Access the Terminal
1. Navigate to the **Terminal** page in R3AL3R AI
2. Look for the **BlackArch Tools Console** section
3. Click "Open Console" or use the quick-access buttons

---

## 📋 Available Tools (55 Total)

### Currently Installed (Ready to Use)
- **nmap** - Network scanning and security auditing
- **wireshark** - Network protocol analyzer  
- **aircrack-ng** - WiFi security testing suite

### Quick Install Commands
Install popular tools via terminal or system:
```bash
sudo apt-get install sqlmap nikto hydra john hashcat gobuster masscan
```

---

## 💻 Usage Examples

### Network Scanning (nmap)
```bash
# Basic scan
nmap 192.168.1.1

# Service version detection
nmap -sV 192.168.1.1

# Vulnerability scan
nmap --script vuln target.com

# Fast scan top 100 ports
nmap -F 192.168.1.0/24
```

### WiFi Security (aircrack-ng)
```bash
# Show help
aircrack-ng --help

# Crack WPA/WPA2 (requires capture file)
aircrack-ng -w wordlist.txt capture.cap
```

### Web Application Testing (sqlmap) *
```bash
# Test for SQL injection
sqlmap -u "http://target.com?id=1" --dbs

# Dump database tables
sqlmap -u "http://target.com?id=1" -D database_name --tables

# Extract data
sqlmap -u "http://target.com?id=1" -D db -T users --dump
```

### Web Server Scanning (nikto) *
```bash
# Basic web server scan
nikto -h http://target.com

# Scan with specific port
nikto -h http://target.com:8080

# Save output to file
nikto -h http://target.com -o results.html
```

### Password Cracking (john) *
```bash
# Crack password hashes
john --wordlist=/usr/share/wordlists/rockyou.txt hashes.txt

# Show cracked passwords
john --show hashes.txt

# Brute force mode
john --incremental hashes.txt
```

### Login Brute Force (hydra) *
```bash
# SSH brute force
hydra -L users.txt -P passwords.txt ssh://192.168.1.1

# HTTP form attack
hydra -l admin -P passwords.txt 192.168.1.1 http-post-form "/login:user=^USER^&pass=^PASS^:F=incorrect"

# FTP brute force
hydra -L users.txt -P passwords.txt ftp://192.168.1.1
```

*Install first with: `sudo apt-get install <tool-name>`

---

## 🔧 Tool Management

### Check Tool Status
```bash
# Via API
curl http://localhost:8081/api/tools/nmap

# Will show: installed status, path, version, description
```

### Install New Tool
**Method 1: Frontend**
- Go to Terminal → BlackArch Console
- Find tool in list
- Click "Install" button

**Method 2: System Command**
```bash
sudo apt-get install <tool-name>
# Then refresh the tool list
```

**Method 3: API**
```bash
curl -X POST http://localhost:8081/api/install/sqlmap
```

---

## 🎯 Common Workflows

### 1. Web Application Security Audit
```bash
# Step 1: Discover web servers
nmap -p 80,443,8080,8443 192.168.1.0/24

# Step 2: Scan for vulnerabilities
nikto -h http://target.com

# Step 3: Test for SQL injection
sqlmap -u "http://target.com?id=1" --batch

# Step 4: Directory bruteforce
gobuster dir -u http://target.com -w /usr/share/wordlists/dirb/common.txt
```

### 2. Network Reconnaissance
```bash
# Step 1: Ping sweep
nmap -sn 192.168.1.0/24

# Step 2: Port scan live hosts
nmap -sS -p- 192.168.1.1-254

# Step 3: Service detection
nmap -sV -sC -O 192.168.1.10

# Step 4: Vulnerability scan
nmap --script vuln 192.168.1.10
```

### 3. Password Security Testing
```bash
# Step 1: Generate wordlist
crunch 8 8 -t @@@@%%%% -o passwords.txt

# Step 2: Crack hashes
john --wordlist=passwords.txt hashes.txt

# Step 3: Brute force service
hydra -L users.txt -P passwords.txt ssh://target.com
```

---

## 📚 Tool Categories

### Network Scanners (13 tools)
nmap, masscan, nikto, netdiscover, gobuster, dirb, etc.

### Web Application (9 tools)
sqlmap, nikto, burpsuite, dirb, gobuster, arjun, arachni, beef, recon-ng

### Password Tools (8 tools)
john, hashcat, hydra, ophcrack, crunch, acccheck

### Exploitation (6 tools)
metasploit, empire, armitage, koadic, pupy, beef

### Forensics (6 tools)
autopsy, bulk-extractor, afflib, dc3dd, dcfldd, hashcat

### Wireless (4 tools)
aircrack-ng, airgeddon, fern-wifi-cracker, netdiscover

---

## ⚠️ Important Notes

### Security & Ethics
- **Only test systems you own or have permission to test**
- Unauthorized scanning/testing is illegal
- R3AL3R AI is for ethical security testing only
- Keep all credentials secure

### WSL Limitations
- GUI tools require `--version` or CLI modes
- Some tools may need additional setup
- Wireless tools require USB adapter pass-through
- X11 forwarding needed for full GUI support

### Best Practices
1. Always start with `-h` or `--help` to learn tool options
2. Use dry-run modes when available
3. Save results to files for documentation
4. Verify targets before executing scans
5. Monitor resource usage on large scans

---

## 🔍 Troubleshooting

### Tool Not Found
```bash
# Check if installed:
which <tool-name>

# Install if missing:
sudo apt-get install <tool-name>

# Refresh R3AL3R AI tool list
curl http://localhost:8081/api/tools
```

### Permission Denied
```bash
# Some tools need sudo:
sudo nmap -sS 192.168.1.1

# Or give capabilities:
sudo setcap cap_net_raw+ep /usr/bin/nmap
```

### GUI Tool Errors
```bash
# Use CLI flags:
wireshark --version  # Instead of GUI
tshark -i eth0       # CLI alternative

# Or setup X11:
export DISPLAY=:0
```

---

## 📖 Learn More

### Official Documentation
- nmap: https://nmap.org/docs.html
- Metasploit: https://docs.metasploit.com/
- aircrack-ng: https://www.aircrack-ng.org/documentation.html
- sqlmap: https://github.com/sqlmapproject/sqlmap/wiki

### Training Resources
- OSCP: Offensive Security Certified Professional
- CEH: Certified Ethical Hacker
- HackTheBox: Hands-on penetration testing platform
- TryHackMe: Guided cybersecurity training

---

## 🎯 Quick Reference Commands

```bash
# Help/Version
<tool> --help
<tool> --version
<tool> -h

# Network Scanning
nmap -sV <target>
masscan -p1-65535 <target>

# Web Testing
nikto -h <url>
sqlmap -u "<url>?id=1"

# Password
john <hash_file>
hydra -L users -P pass <service://target>

# Wireless
aircrack-ng -w <wordlist> <cap_file>
```

---

## 🌟 Pro Tips

1. **Use screen/tmux** for long-running scans
2. **Save output** with `-o` or `>` redirection
3. **Start with non-intrusive scans** before aggressive testing
4. **Read documentation** before using new tools
5. **Keep tools updated** with `apt-get update && apt-get upgrade`

---

**Need Help?**
- Check tool documentation: `<tool> --help`
- View available tools: Visit BlackArch Console
- Test connectivity: `curl http://localhost:8081/api/status`
- Report issues: Check logs in `/var/log/` or Terminal output

**Happy Ethical Hacking! 🛡️**
