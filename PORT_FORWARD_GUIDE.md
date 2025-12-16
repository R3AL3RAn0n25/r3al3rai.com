# Port Forwarding Guide for R3ÆLƎR AI

## Your Network Info
- **Public IP:** 47.215.15.217
- **Router Gateway:** 192.168.1.1 (usually)

## Ports to Forward
- **Port 80** → Your PC (HTTP)
- **Port 443** → Your PC (HTTPS)
- **Port 3000** → Your PC (Backend API)

## Steps to Port Forward

### 1. Find Your Local IP
```powershell
ipconfig | findstr IPv4
```
Look for something like: `192.168.1.XXX`

### 2. Access Your Router
Open browser and go to:
- http://192.168.1.1
- OR http://192.168.0.1
- OR http://10.0.0.1

**Login:** Usually admin/admin or admin/password (check router label)

### 3. Find Port Forwarding Section
Look for:
- "Port Forwarding"
- "Virtual Server"
- "NAT Forwarding"
- "Applications & Gaming"

### 4. Add These Rules

**Rule 1: HTTP**
- Service Name: R3ALER-HTTP
- External Port: 80
- Internal Port: 80
- Internal IP: [Your PC IP from step 1]
- Protocol: TCP

**Rule 2: HTTPS**
- Service Name: R3ALER-HTTPS
- External Port: 443
- Internal Port: 443
- Internal IP: [Your PC IP from step 1]
- Protocol: TCP

**Rule 3: Backend**
- Service Name: R3ALER-API
- External Port: 3000
- Internal Port: 3000
- Internal IP: [Your PC IP from step 1]
- Protocol: TCP

### 5. Save and Reboot Router

## Test Port Forwarding

After setup, test from external site:
- https://www.yougetsignal.com/tools/open-ports/
- Enter: 47.215.15.217
- Test ports: 80, 443, 3000

## Windows Firewall Rules

```powershell
# Allow ports through Windows Firewall
netsh advfirewall firewall add rule name="R3ALER HTTP" dir=in action=allow protocol=TCP localport=80
netsh advfirewall firewall add rule name="R3ALER HTTPS" dir=in action=allow protocol=TCP localport=443
netsh advfirewall firewall add rule name="R3ALER API" dir=in action=allow protocol=TCP localport=3000
```

## Common Router Brands

**Netgear:** Advanced > Advanced Setup > Port Forwarding
**TP-Link:** Forwarding > Virtual Servers
**Linksys:** Security > Apps and Gaming > Port Range Forward
**ASUS:** WAN > Virtual Server / Port Forwarding
**D-Link:** Advanced > Port Forwarding

## Alternative: Use ngrok (Quick Test)

If port forwarding is difficult:
```powershell
# Download ngrok from ngrok.com
ngrok http 3000
```
This gives you a public URL instantly (but temporary).

## Verify Setup

Once port forwarding is done:
```powershell
# Test from another network or phone (not on same WiFi)
curl http://47.215.15.217:3000/api/health
```

Should return: `{"ok":true,...}`
