# Deploy R3ÆLƎR AI to production server 216.198.79.65

$SERVER = "216.198.79.65"
$USER = "root"  # Change if different
$REMOTE_PATH = "/var/www/r3al3rai.com/html"
$LOCAL_BUILD = "application\Backend\build"

Write-Host "Deploying to production server: $SERVER" -ForegroundColor Cyan

# Build frontend
Write-Host "Building frontend..." -ForegroundColor Yellow
Push-Location application\Frontend
npm run build
Pop-Location

# Use SCP to copy files (requires SSH client)
Write-Host "Copying files to $SERVER..." -ForegroundColor Yellow

# Copy build directory
scp -r "$LOCAL_BUILD\*" "${USER}@${SERVER}:${REMOTE_PATH}/"

# Copy backend files
Write-Host "Copying backend..." -ForegroundColor Yellow
ssh "${USER}@${SERVER}" "mkdir -p /var/www/r3al3rai.com/backend"
scp -r "application\Backend\*.js" "${USER}@${SERVER}:/var/www/r3al3rai.com/backend/"
scp "application\Backend\package.json" "${USER}@${SERVER}:/var/www/r3al3rai.com/backend/"
scp "application\Backend\.env" "${USER}@${SERVER}:/var/www/r3al3rai.com/backend/"
scp -r "application\Backend\middleware" "${USER}@${SERVER}:/var/www/r3al3rai.com/backend/"

# Restart services
Write-Host "Restarting services..." -ForegroundColor Yellow
ssh "${USER}@${SERVER}" "cd /var/www/r3al3rai.com/backend && npm install && pm2 restart r3aler-backend || pm2 start backendserver.js --name r3aler-backend"
ssh "${USER}@${SERVER}" "systemctl reload nginx"

Write-Host "Deployment complete!" -ForegroundColor Green
Write-Host "Site: https://www.r3al3rai.com" -ForegroundColor Cyan
