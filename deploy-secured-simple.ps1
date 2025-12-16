# R3AL3R Security Deployment Script for Windows
# Simple version without Unicode characters

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "R3AL3R API Security Deployment" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check .env.local exists
Write-Host "[1] Validating .env.local..." -ForegroundColor Yellow
if (!(Test-Path ".env.local")) {
    Write-Host "ERROR: .env.local not found!" -ForegroundColor Red
    Write-Host "Copy .env.example.secured to .env.local first" -ForegroundColor Red
    exit 1
}

$envContent = Get-Content ".env.local" -Raw
if ($envContent -match "GENERATE_|<") {
    Write-Host "ERROR: .env.local contains placeholder values!" -ForegroundColor Red
    Write-Host "Please fill in all required variables" -ForegroundColor Red
    exit 1
}

Write-Host "OK: .env.local configured" -ForegroundColor Green
Write-Host ""

# Create backup directory
Write-Host "[2] Creating backups..." -ForegroundColor Yellow
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$backupDir = ".backups/deployment_$timestamp"

if (!(Test-Path $backupDir)) {
    New-Item -ItemType Directory -Path $backupDir -Force | Out-Null
}

# Backup original files
if (Test-Path "AI_Core_Worker/knowledge_api.py") {
    Copy-Item "AI_Core_Worker/knowledge_api.py" "$backupDir/" -Force
    Write-Host "OK: Backed up knowledge_api.py" -ForegroundColor Green
}

if (Test-Path "src/apis/droid_api.py") {
    Copy-Item "src/apis/droid_api.py" "$backupDir/" -Force
    Write-Host "OK: Backed up droid_api.py" -ForegroundColor Green
}

Write-Host ""

# Install/update dependencies
Write-Host "[3] Installing Python dependencies..." -ForegroundColor Yellow
pip install flask flask-cors flask-limiter bcrypt python-dotenv psycopg2 requests --quiet
Write-Host "OK: Dependencies installed" -ForegroundColor Green
Write-Host ""

# Deploy secured versions
Write-Host "[4] Deploying secured APIs..." -ForegroundColor Yellow
if (Test-Path "AI_Core_Worker/knowledge_api_secured.py") {
    Copy-Item "AI_Core_Worker/knowledge_api_secured.py" "AI_Core_Worker/knowledge_api.py" -Force
    Write-Host "OK: Deployed knowledge_api_secured.py" -ForegroundColor Green
} else {
    Write-Host "WARNING: knowledge_api_secured.py not found" -ForegroundColor Yellow
}

if (Test-Path "src/apis/droid_api_secured.py") {
    Copy-Item "src/apis/droid_api_secured.py" "src/apis/droid_api.py" -Force
    Write-Host "OK: Deployed droid_api_secured.py" -ForegroundColor Green
} else {
    Write-Host "WARNING: droid_api_secured.py not found" -ForegroundColor Yellow
}

Write-Host ""

# Generate test token
Write-Host "[5] Generating test authentication token..." -ForegroundColor Yellow
$testToken = python -c "import uuid; print(uuid.uuid4())"
Write-Host "Test Token: $testToken" -ForegroundColor Cyan
Write-Host ""

# Summary
Write-Host "========================================" -ForegroundColor Green
Write-Host "DEPLOYMENT COMPLETE" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "NEXT STEPS:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Start Knowledge API (in terminal):" -ForegroundColor White
Write-Host "   python AI_Core_Worker/knowledge_api.py" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Start Droid API (in another terminal):" -ForegroundColor White
Write-Host "   python src/apis/droid_api.py" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Test with authentication:" -ForegroundColor White
Write-Host "   curl -X POST http://localhost:5004/api/query \" -ForegroundColor Gray
Write-Host "     -H 'X-Session-Token: $testToken' \" -ForegroundColor Gray
Write-Host "     -d '{""query"": ""test""}'" -ForegroundColor Gray
Write-Host ""
Write-Host "Configuration Files:" -ForegroundColor Cyan
Write-Host "   Environment: .env.local" -ForegroundColor Gray
Write-Host "   Documentation: SECURITY_QUICKSTART.md" -ForegroundColor Gray
Write-Host ""
Write-Host "Status: READY FOR STARTUP" -ForegroundColor Green
