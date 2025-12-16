# R3ÆLƎR AI - GO LIVE CHECKLIST

## Current Situation
- Local system: FULLY OPERATIONAL on localhost:3000
- Production server: 216.198.79.65 (needs deployment)
- Domain: www.r3al3rai.com (currently points to 216.198.79.65)

## Steps to Go Live

### 1. Access Production Server
You need SSH/FTP access to 216.198.79.65

**Test access:**
```bash
ssh root@216.198.79.65
# OR
ssh admin@216.198.79.65
# OR use FTP/SFTP client
```

**If you don't have access:**
- Contact hosting provider
- Get SSH credentials
- Or get FTP/cPanel access

### 2. Upload Files to Server

**Files to upload:**
```
application/Backend/build/          → /var/www/r3al3rai.com/html/
application/Backend/backendserver.js → /var/www/r3al3rai.com/backend/
application/Backend/db.js           → /var/www/r3al3rai.com/backend/
application/Backend/package.json    → /var/www/r3al3rai.com/backend/
application/Backend/.env            → /var/www/r3al3rai.com/backend/
application/Backend/middleware/     → /var/www/r3al3rai.com/backend/
application/Backend/modeManager.js  → /var/www/r3al3rai.com/backend/
application/Backend/stripe_routes.js → /var/www/r3al3rai.com/backend/
```

### 3. Configure Server

**On the server (216.198.79.65):**
```bash
# Install dependencies
cd /var/www/r3al3rai.com/backend
npm install

# Setup database
psql -U postgres
CREATE DATABASE r3aler_ai;
CREATE USER r3aler_user_2025 WITH PASSWORD 'password123';
GRANT ALL PRIVILEGES ON DATABASE r3aler_ai TO r3aler_user_2025;
\q

# Import schema
psql -U r3aler_user_2025 -d r3aler_ai < schema.sql

# Start backend with PM2
pm2 start backendserver.js --name r3aler-backend
pm2 save
pm2 startup

# Configure Nginx (already done based on config file)
systemctl reload nginx
```

### 4. Update .env for Production

**On server, edit /var/www/r3al3rai.com/backend/.env:**
```
DB_HOST=localhost
DB_PORT=5432
DB_USER=r3aler_user_2025
DB_PASSWORD=password123
DB_NAME=r3aler_ai
JWT_SECRET=35enIZkEkIsuUopiso83mhDu2oo3N1JnhY9QX5H6faA=
PORT=3000
HOST=0.0.0.0
FRONTEND_URL=https://www.r3al3rai.com
NODE_ENV=production
CORS_ORIGIN=https://r3al3rai.com,https://www.r3al3rai.com
```

### 5. Verify DNS

**Check DNS points to 216.198.79.65:**
```bash
nslookup www.r3al3rai.com
# Should show: 216.198.79.65
```

**If not, update DNS at your registrar:**
- A Record: r3al3rai.com → 216.198.79.65
- A Record: www.r3al3rai.com → 216.198.79.65

### 6. SSL Certificate

**Install Let's Encrypt SSL:**
```bash
certbot --nginx -d r3al3rai.com -d www.r3al3rai.com
```

### 7. Test Production

```bash
# Test backend
curl http://216.198.79.65:3000/api/health

# Test frontend
curl https://www.r3al3rai.com

# Test login
curl -X POST https://www.r3al3rai.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"test"}'
```

## Alternative: Use FileZilla/WinSCP

**If SSH doesn't work:**

1. Download WinSCP or FileZilla
2. Connect to 216.198.79.65 with SFTP
3. Upload files manually:
   - Upload `application/Backend/build/*` to `/var/www/r3al3rai.com/html/`
   - Upload backend files to `/var/www/r3al3rai.com/backend/`

## What You Need

- [ ] SSH/FTP credentials for 216.198.79.65
- [ ] Root or sudo access on server
- [ ] PostgreSQL installed on server
- [ ] Node.js installed on server
- [ ] Nginx installed and configured
- [ ] PM2 installed (npm install -g pm2)
- [ ] SSL certificate (Let's Encrypt)

## Contact Hosting Provider

If you don't have access, contact your hosting provider and ask for:
1. SSH access to 216.198.79.65
2. Root or sudo privileges
3. PostgreSQL database access
4. Nginx configuration access

## Quick Deploy (Once You Have Access)

```bash
# Build locally
cd application/Frontend
npm run build

# Upload (replace USER with your username)
scp -r ../Backend/build/* USER@216.198.79.65:/var/www/r3al3rai.com/html/
scp -r ../Backend/*.js USER@216.198.79.65:/var/www/r3al3rai.com/backend/
scp ../Backend/package.json USER@216.198.79.65:/var/www/r3al3rai.com/backend/

# SSH and restart
ssh USER@216.198.79.65
cd /var/www/r3al3rai.com/backend
npm install
pm2 restart r3aler-backend
systemctl reload nginx
```

## Status

- ✓ Local system fully operational
- ✓ Frontend built and ready
- ✓ Backend configured
- ✓ Database schema ready
- ⏳ Need server access to deploy
- ⏳ Need to upload files
- ⏳ Need to configure server

**Next Step: Get SSH/FTP access to 216.198.79.65**
