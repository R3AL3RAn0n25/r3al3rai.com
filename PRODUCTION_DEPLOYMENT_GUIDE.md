# Production Deployment Guide - 216.198.79.65

## Quick Deploy

### Windows (PowerShell)
```powershell
.\DEPLOY_TO_PRODUCTION.ps1
```

### Linux/Mac (Bash)
```bash
bash DEPLOY_TO_PRODUCTION.sh
```

---

## Manual Deployment Steps

### 1. Build Frontend
```bash
cd application/Frontend
npm run build
```
This creates `application/Backend/build/` with production files.

### 2. Connect to Server
```bash
ssh root@216.198.79.65
```

### 3. Upload Build Files
```bash
# From local machine
scp -r application/Backend/build/* root@216.198.79.65:/var/www/r3al3rai.com/html/
```

### 4. Upload Backend Files
```bash
scp -r application/Backend/*.js root@216.198.79.65:/var/www/r3al3rai.com/backend/
scp application/Backend/package.json root@216.198.79.65:/var/www/r3al3rai.com/backend/
scp application/Backend/.env root@216.198.79.65:/var/www/r3al3rai.com/backend/
scp -r application/Backend/middleware root@216.198.79.65:/var/www/r3al3rai.com/backend/
scp application/Backend/db.js root@216.198.79.65:/var/www/r3al3rai.com/backend/
scp application/Backend/modeManager.js root@216.198.79.65:/var/www/r3al3rai.com/backend/
scp application/Backend/stripe_routes.js root@216.198.79.65:/var/www/r3al3rai.com/backend/
```

### 5. Install Dependencies on Server
```bash
ssh root@216.198.79.65
cd /var/www/r3al3rai.com/backend
npm install
```

### 6. Restart Backend
```bash
# Using PM2
pm2 restart r3aler-backend

# Or start if not running
pm2 start backendserver.js --name r3aler-backend

# Or using systemd
systemctl restart r3aler-backend
```

### 7. Reload Nginx
```bash
systemctl reload nginx
```

---

## Verify Deployment

### Check Files
```bash
ssh root@216.198.79.65
ls -la /var/www/r3al3rai.com/html/
ls -la /var/www/r3al3rai.com/backend/
```

### Check Backend
```bash
curl http://localhost:3000/api/health
```

### Check Site
```bash
curl https://www.r3al3rai.com
```

---

## Troubleshooting

### Backend Not Starting
```bash
ssh root@216.198.79.65
cd /var/www/r3al3rai.com/backend
pm2 logs r3aler-backend
```

### Nginx Errors
```bash
ssh root@216.198.79.65
tail -f /var/log/nginx/error.log
```

### Database Connection
```bash
ssh root@216.198.79.65
psql -h localhost -U r3aler_user_2025 -d r3aler_ai -c "SELECT 1"
```

---

## Server Info

**IP:** 216.198.79.65  
**Domain:** www.r3al3rai.com  
**Frontend Path:** /var/www/r3al3rai.com/html/  
**Backend Path:** /var/www/r3al3rai.com/backend/  
**Nginx Config:** /etc/nginx/sites-available/r3al3rai.com.conf  

---

## Required Files on Server

### Frontend (in /var/www/r3al3rai.com/html/)
- index.html
- assets/index-*.js
- assets/index-*.css

### Backend (in /var/www/r3al3rai.com/backend/)
- backendserver.js
- db.js
- modeManager.js
- stripe_routes.js
- package.json
- .env
- middleware/security.js
- middleware/subscription.js

---

## Post-Deployment Checklist

- [ ] Frontend files uploaded
- [ ] Backend files uploaded
- [ ] Dependencies installed (npm install)
- [ ] .env file configured
- [ ] Database accessible
- [ ] Backend running (pm2 list)
- [ ] Nginx reloaded
- [ ] Site accessible at www.r3al3rai.com
- [ ] Login working
- [ ] API endpoints responding
