# Deploy from Windows to Ubuntu VM (172.17.48.5)

$VM_IP = "172.17.48.5"
$VM_USER = "ubuntu"  # Change if different

Write-Host "=== Deploying to Ubuntu VM ===" -ForegroundColor Cyan

# Build frontend
Write-Host "[1/4] Building frontend..." -ForegroundColor Green
cd application\Frontend
npm run build
cd ..\..

# Copy files to VM
Write-Host "[2/4] Copying files to VM..." -ForegroundColor Green
scp -r application\Backend\build\* ${VM_USER}@${VM_IP}:/var/www/r3aler/html/
scp application\Backend\backendserver.js ${VM_USER}@${VM_IP}:/var/www/r3aler/backend/
scp application\Backend\db.js ${VM_USER}@${VM_IP}:/var/www/r3aler/backend/
scp application\Backend\modeManager.js ${VM_USER}@${VM_IP}:/var/www/r3aler/backend/
scp application\Backend\stripe_routes.js ${VM_USER}@${VM_IP}:/var/www/r3aler/backend/
scp application\Backend\package.json ${VM_USER}@${VM_IP}:/var/www/r3aler/backend/
scp application\Backend\.env ${VM_USER}@${VM_IP}:/var/www/r3aler/backend/
scp -r application\Backend\middleware ${VM_USER}@${VM_IP}:/var/www/r3aler/backend/

# Install and start backend
Write-Host "[3/4] Starting backend on VM..." -ForegroundColor Green
ssh ${VM_USER}@${VM_IP} "cd /var/www/r3aler/backend && npm install && pm2 start backendserver.js --name r3aler-backend && pm2 save"

# Test
Write-Host "[4/4] Testing..." -ForegroundColor Green
curl http://${VM_IP}/api/health

Write-Host "`nDeployment complete!" -ForegroundColor Green
Write-Host "VM accessible at: http://${VM_IP}" -ForegroundColor Cyan
Write-Host "`nNext: Port forward router to ${VM_IP}" -ForegroundColor Yellow
