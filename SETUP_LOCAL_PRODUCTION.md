# Setup Local Production Server

## Make Your Local Machine the Production Server

### Step 1: Get Your Public IP
```powershell
curl ifconfig.me
```

### Step 2: Update DNS
Go to your domain registrar (where you bought r3al3rai.com) and update:
- **A Record**: r3al3rai.com → YOUR_PUBLIC_IP
- **A Record**: www.r3al3rai.com → YOUR_PUBLIC_IP

### Step 3: Port Forwarding on Router
Forward these ports to your local machine:
- Port 80 (HTTP)
- Port 443 (HTTPS)
- Port 3000 (Backend)

### Step 4: Update Backend .env
```
FRONTEND_URL=https://www.r3al3rai.com
CORS_ORIGIN=https://r3al3rai.com,https://www.r3al3rai.com
NODE_ENV=production
HOST=0.0.0.0
PORT=3000
```

### Step 5: Install Nginx (Windows)
Download from: http://nginx.org/en/download.html

**nginx.conf:**
```nginx
server {
    listen 80;
    server_name r3al3rai.com www.r3al3rai.com;
    
    location /api/ {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
    }
    
    location / {
        root C:/path/to/R3aler-ai/application/Backend/build;
        try_files $uri /index.html;
    }
}
```

### Step 6: Start Services
```powershell
# Start backend
cd application\Backend
npm start

# Start nginx
nginx.exe
```

### Step 7: Get SSL Certificate
Use Cloudflare (free) or Let's Encrypt

## OR Use Cloudflare Tunnel (Easier)

### Install Cloudflare Tunnel
```powershell
# Download cloudflared
# Run:
cloudflared tunnel login
cloudflared tunnel create r3aler
cloudflared tunnel route dns r3aler r3al3rai.com
cloudflared tunnel run r3aler
```

This creates a secure tunnel without port forwarding!

## Current Status
- ✓ System running on localhost:3000
- ⏳ Need to expose to internet
- ⏳ Need to update DNS
