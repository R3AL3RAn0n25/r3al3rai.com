# Cloudflare Tunnel Setup (No Router Access Needed!)

## Why Cloudflare Tunnel?
- ✓ No port forwarding needed
- ✓ No router access needed
- ✓ Free SSL certificate
- ✓ DDoS protection
- ✓ Works behind any firewall

## Setup Steps

### 1. Install Cloudflared
```powershell
# Download from: https://github.com/cloudflare/cloudflared/releases
# Or use winget:
winget install --id Cloudflare.cloudflared
```

### 2. Login to Cloudflare
```powershell
cloudflared tunnel login
```
This opens browser - login with your Cloudflare account (free)

### 3. Create Tunnel
```powershell
cloudflared tunnel create r3aler-ai
```
Save the tunnel ID shown

### 4. Create Config File
Create: `C:\Users\work8\.cloudflared\config.yml`
```yaml
tunnel: r3aler-ai
credentials-file: C:\Users\work8\.cloudflared\<TUNNEL-ID>.json

ingress:
  - hostname: www.r3al3rai.com
    service: http://localhost:3000
  - hostname: r3al3rai.com
    service: http://localhost:3000
  - service: http_status:404
```

### 5. Route DNS
```powershell
cloudflared tunnel route dns r3aler-ai www.r3al3rai.com
cloudflared tunnel route dns r3aler-ai r3al3rai.com
```

### 6. Run Tunnel
```powershell
cloudflared tunnel run r3aler-ai
```

### 7. Install as Windows Service (Optional)
```powershell
cloudflared service install
```

## Done!
Your site is now live at:
- https://www.r3al3rai.com
- https://r3al3rai.com

No port forwarding, no router access needed!

## Verify
```powershell
curl https://www.r3al3rai.com/api/health
```
