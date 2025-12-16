# Quick Deploy to 216.198.79.65
# Run this to fix www.r3al3rai.com

$SERVER = "216.198.79.65"

Write-Host "`n=== R3ÆLƎR AI - Quick Production Deploy ===" -ForegroundColor Cyan
Write-Host "Target: $SERVER`n" -ForegroundColor Yellow

# Step 1: Build
Write-Host "[1/4] Building frontend..." -ForegroundColor Green
cd application\Frontend
npm run build
cd ..\..

# Step 2: Upload frontend
Write-Host "[2/4] Uploading frontend files..." -ForegroundColor Green
scp -r application\Backend\build\* root@${SERVER}:/var/www/r3al3rai.com/html/

# Step 3: Upload backend
Write-Host "[3/4] Uploading backend files..." -ForegroundColor Green
scp application\Backend\backendserver.js root@${SERVER}:/var/www/r3al3rai.com/backend/
scp application\Backend\db.js root@${SERVER}:/var/www/r3al3rai.com/backend/
scp application\Backend\modeManager.js root@${SERVER}:/var/www/r3al3rai.com/backend/
scp application\Backend\stripe_routes.js root@${SERVER}:/var/www/r3al3rai.com/backend/
scp -r application\Backend\middleware root@${SERVER}:/var/www/r3al3rai.com/backend/

# Step 4: Restart
Write-Host "[4/4] Restarting services..." -ForegroundColor Green
ssh root@${SERVER} "pm2 restart r3aler-backend && systemctl reload nginx"

Write-Host "`n✓ Deployment complete!" -ForegroundColor Green
Write-Host "Check: https://www.r3al3rai.com`n" -ForegroundColor Cyan
