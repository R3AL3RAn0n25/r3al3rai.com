# R3AL3R AI - HTTPS Production Deployment Guide

## Current Status
✅ SSL Certificates Located: `C:\Users\work8\OneDrive\Desktop\_.r3al3rai.com_ssl_certificate_INTERMEDIATE`
- r3al3rai.com_ssl_certificate.cer (2309 bytes)
- intermediate1.cer (2244 bytes)
- intermediate2.cer (2342 bytes)

⚠️ **MISSING: Private Key File** (required for HTTPS)

## Required Files for HTTPS

### 1. Certificate Files (✅ Have)
- `r3al3rai.com_ssl_certificate.cer` - Your domain certificate
- `intermediate1.cer` - Intermediate CA certificate  
- `intermediate2.cer` - Root CA certificate

### 2. Private Key File (❌ Need)
- Usually named: `r3al3rai.com.key` or `private.key`
- **WHERE TO FIND IT:**
  - Check your SSL provider's download page
  - Check email from SSL provider
  - If you generated CSR yourself, check where you saved the private key
  - Common locations: Downloads folder, Desktop, Documents

### 3. Combined Certificate Chain (We'll create)
```bash
cat r3al3rai.com_ssl_certificate.cer intermediate1.cer intermediate2.cer > fullchain.pem
```

## Deployment Options

### Option A: Nginx Reverse Proxy (RECOMMENDED)

**Architecture:**
```
Internet → r3al3rai.com:443 (HTTPS/Nginx)
    ↓ SSL Termination
    ↓
Internal Services (HTTP localhost)
    - Frontend: localhost:3000
    - Backend: localhost:3002
    - Knowledge API: localhost:5004
    - etc.
```

**Nginx Configuration:**
```nginx
server {
    listen 443 ssl http2;
    server_name r3al3rai.com www.r3al3rai.com;

    # SSL Certificates
    ssl_certificate /path/to/fullchain.pem;
    ssl_certificate_key /path/to/r3al3rai.com.key;
    
    # SSL Settings
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # Proxy to R3AL3R AI Frontend
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # API endpoints
    location /api/ {
        proxy_pass http://localhost:3002;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# HTTP to HTTPS redirect
server {
    listen 80;
    server_name r3al3rai.com www.r3al3rai.com;
    return 301 https://$server_name$request_uri;
}
```

### Option B: Python HTTPS Server (Alternative)

Update each Flask app to support HTTPS directly:

```python
# Knowledge API with SSL
from flask import Flask
import ssl

app = Flask(__name__)

if __name__ == '__main__':
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(
        'C:/path/to/fullchain.pem',
        'C:/path/to/r3al3rai.com.key'
    )
    
    app.run(
        host='0.0.0.0',
        port=5004,
        ssl_context=context
    )
```

## Deployment Steps

### Step 1: Locate Private Key
1. Check SSL provider dashboard
2. Check email from SSL provider
3. Search computer: `Get-ChildItem -Path C:\ -Filter "*r3al3rai*.key" -Recurse -ErrorAction SilentlyContinue`

### Step 2: Copy Certificates to Project
```powershell
# Create certs directory
New-Item -ItemType Directory -Path ".\certs" -Force

# Copy certificates
Copy-Item "C:\Users\work8\OneDrive\Desktop\_.r3al3rai.com_ssl_certificate_INTERMEDIATE\*" -Destination ".\certs\"

# Copy private key (once found)
Copy-Item "C:\path\to\private.key" -Destination ".\certs\r3al3rai.com.key"
```

### Step 3: Create Certificate Chain
```powershell
# Combine certificates
Get-Content .\certs\r3al3rai.com_ssl_certificate.cer, .\certs\intermediate1.cer, .\certs\intermediate2.cer | Set-Content .\certs\fullchain.pem
```

### Step 4: Install Nginx (Windows)
```powershell
# Download Nginx for Windows
Invoke-WebRequest -Uri "http://nginx.org/download/nginx-1.24.0.zip" -OutFile "nginx.zip"
Expand-Archive nginx.zip -DestinationPath "C:\nginx"

# Copy config
Copy-Item .\nginx.conf -Destination "C:\nginx\conf\nginx.conf"

# Start Nginx
cd C:\nginx
.\nginx.exe
```

### Step 5: Update DNS
Point r3al3rai.com to your server IP:
```
A Record: r3al3rai.com → YOUR_PUBLIC_IP
A Record: www.r3al3rai.com → YOUR_PUBLIC_IP
```

### Step 6: Update Service URLs
Update all services to use domain instead of localhost:
- Frontend: https://r3al3rai.com
- API endpoints: https://r3al3rai.com/api/*

## Security Checklist

- [ ] Private key file secured (chmod 600 on Linux, restricted NTFS permissions on Windows)
- [ ] Certificates valid and not expired
- [ ] Firewall configured (allow port 443)
- [ ] HTTP redirects to HTTPS
- [ ] HSTS header enabled
- [ ] CORS configured for r3al3rai.com
- [ ] API keys/secrets in environment variables
- [ ] PostgreSQL not exposed to internet

## Production Service Configuration

Update `start-production.ps1` to bind to 127.0.0.1 (internal only):

```powershell
# Services should only listen on localhost
# Nginx will handle external HTTPS traffic
serve(app, host='127.0.0.1', port=5004)  # Not 0.0.0.0
```

## Testing HTTPS

1. **Local Testing (hosts file):**
   ```
   C:\Windows\System32\drivers\etc\hosts
   127.0.0.1 r3al3rai.com
   ```

2. **Test SSL:**
   ```powershell
   curl https://r3al3rai.com -k
   ```

3. **Check Certificate:**
   ```powershell
   openssl s_client -connect r3al3rai.com:443 -servername r3al3rai.com
   ```

## Alternative: Cloudflare Tunnel (Zero Config)

If you don't want to expose your IP or configure DNS:

```bash
# Install Cloudflare Tunnel
cloudflared tunnel create r3aler-ai
cloudflared tunnel route dns r3aler-ai r3al3rai.com
cloudflared tunnel run r3aler-ai
```

Cloudflare handles HTTPS automatically!

## Next Steps

1. **URGENT**: Locate private key file
2. Install Nginx or configure Cloudflare Tunnel
3. Update service configurations
4. Test HTTPS locally
5. Deploy to production

## Support

If private key is lost:
- Generate new CSR and reissue certificate from SSL provider
- Use Let's Encrypt for free certificates (with auto-renewal)

---

**Status**: Waiting for private key file to complete HTTPS setup
**Priority**: HIGH - Required for production deployment
