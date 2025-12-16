# R3ÆLƎR API Security Deployment Script (PowerShell)
# Deploys security-hardened APIs to 72.17.63.255
#
# Usage: .\deploy-secured-apis.ps1

$ErrorActionPreference = "Stop"

Write-Host "===============================================" -ForegroundColor Green
Write-Host "🔐 R3ÆLƎR API Security Deployment (Windows)" -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Green
Write-Host ""

# Configuration
$DEPLOYMENT_IP = "72.17.63.255"
$KNOWLEDGE_API_PORT = 5004
$DROID_API_PORT = 5005
$APP_DIR = "C:\r3al3rai\apis"

# Check if .env.local exists
if (-not (Test-Path ".env.local")) {
    Write-Host "✗ ERROR: .env.local not found" -ForegroundColor Red
    Write-Host "  1. Copy .env.example.secured to .env.local"
    Write-Host "  2. Fill in all required values:"
    Write-Host "     - DB_PASSWORD"
    Write-Host "     - FLASK_SECRET_KEY"
    Write-Host "     - STORAGE_FACILITY_URL"
    Write-Host "     - SSL certificate paths"
    exit 1
}

# Validate .env.local
Write-Host "→ Validating .env.local..." -ForegroundColor Yellow

$requiredVars = @("DB_HOST", "DB_PORT", "DB_NAME", "DB_USER", "DB_PASSWORD", "FLASK_SECRET_KEY", "STORAGE_FACILITY_URL")
$envContent = Get-Content ".env.local"

foreach ($var in $requiredVars) {
    if ($envContent -notmatch "^$var=") {
        Write-Host "✗ Missing variable: $var" -ForegroundColor Red
        exit 1
    }
}

Write-Host "✓ .env.local validation passed" -ForegroundColor Green
Write-Host ""

# Install dependencies
Write-Host "→ Installing Python dependencies..." -ForegroundColor Yellow
pip install -q flask flask-cors flask-limiter psycopg2-binary bcrypt python-dotenv requests
Write-Host "✓ Dependencies installed" -ForegroundColor Green
Write-Host ""

# Backup original files
Write-Host "→ Creating backups of original API files..." -ForegroundColor Yellow
$backupDir = "backups\$(Get-Date -Format 'yyyyMMdd_HHmmss')"
New-Item -ItemType Directory -Path $backupDir -Force | Out-Null

if (Test-Path "AI_Core_Worker\knowledge_api.py") {
    Copy-Item "AI_Core_Worker\knowledge_api.py" "$backupDir\knowledge_api.py.backup"
}

if (Test-Path "src\apis\droid_api.py") {
    Copy-Item "src\apis\droid_api.py" "$backupDir\droid_api.py.backup"
}

Write-Host "✓ Backups created in $backupDir" -ForegroundColor Green
Write-Host ""

# Deploy secured versions
Write-Host "→ Deploying security-hardened API versions..." -ForegroundColor Yellow

if (Test-Path "knowledge_api_secured.py") {
    Copy-Item "knowledge_api_secured.py" "AI_Core_Worker\knowledge_api.py" -Force
    Write-Host "✓ Deployed knowledge_api.py (secured)" -ForegroundColor Green
} else {
    Write-Host "✗ knowledge_api_secured.py not found" -ForegroundColor Red
    exit 1
}

if (Test-Path "droid_api_secured.py") {
    Copy-Item "droid_api_secured.py" "src\apis\droid_api.py" -Force
    Write-Host "✓ Deployed droid_api.py (secured)" -ForegroundColor Green
} else {
    Write-Host "✗ droid_api_secured.py not found" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Verify SSL certificates
Write-Host "→ Verifying SSL certificate configuration..." -ForegroundColor Yellow

$sslCert = (Select-String -Path ".env.local" -Pattern "^SSL_CERT_PATH=" | ForEach-Object { $_.Line -replace 'SSL_CERT_PATH=' }).Trim()

if ([string]::IsNullOrEmpty($sslCert)) {
    Write-Host "⚠ SSL_CERT_PATH not configured" -ForegroundColor Yellow
    Write-Host "  Add to .env.local: SSL_CERT_PATH=C:\path\to\r3al3rai.com_ssl_certificate.cer"
} else {
    if (Test-Path $sslCert) {
        Write-Host "✓ SSL certificate found: $sslCert" -ForegroundColor Green
    } else {
        Write-Host "⚠ SSL certificate not found at: $sslCert" -ForegroundColor Yellow
    }
}

Write-Host ""

# Test database connectivity
Write-Host "→ Testing database connectivity..." -ForegroundColor Yellow

$pythonTest = @"
import os
from dotenv import load_dotenv
import psycopg2

load_dotenv('.env.local')

try:
    db_config = {
        'host': os.getenv('DB_HOST'),
        'port': int(os.getenv('DB_PORT', 5432)),
        'database': os.getenv('DB_NAME'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'sslmode': os.getenv('DB_SSLMODE', 'require'),
        'connect_timeout': 5
    }
    
    conn = psycopg2.connect(**db_config)
    print(f"Database connection successful (SSL/TLS: {db_config['sslmode']})")
    conn.close()
except Exception as e:
    print(f"Database connection failed: {e}")
    exit(1)
"@

$pythonTest | python.exe
if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Database connectivity test failed" -ForegroundColor Red
    exit 1
}

Write-Host "✓ Database connection successful (SSL/TLS: require)" -ForegroundColor Green
Write-Host ""

# Generate test authentication token
Write-Host "→ Generating test authentication token..." -ForegroundColor Yellow

$testToken = python.exe -c "import uuid; print(uuid.uuid4())"
Write-Host "✓ Test token: $testToken" -ForegroundColor Green
Write-Host ""

# Show deployment summary
Write-Host "===============================================" -ForegroundColor Green
Write-Host "✓ SECURITY DEPLOYMENT COMPLETE" -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Deployment Summary:" -ForegroundColor Cyan
Write-Host "  - Deployment IP: $DEPLOYMENT_IP"
Write-Host "  - Knowledge API Port: $KNOWLEDGE_API_PORT"
Write-Host "  - Droid API Port: $DROID_API_PORT"
Write-Host ""
Write-Host "🔐 Security Features Enabled:" -ForegroundColor Cyan
Write-Host "  ✓ SSL/TLS for all database connections"
Write-Host "  ✓ Authentication required (X-Session-Token or X-API-Key)"
Write-Host "  ✓ Rate limiting enabled (Query: 20/hr, Search: 30/hr, Chat: 5/hr)"
Write-Host "  ✓ CORS whitelisting"
Write-Host "  ✓ Input validation and sanitization"
Write-Host "  ✓ IP whitelisting (72.17.63.255)"
Write-Host "  ✓ Comprehensive security logging"
Write-Host ""
Write-Host "📝 Next Steps:" -ForegroundColor Cyan
Write-Host "  1. Copy SSL certificates to secure location:"
Write-Host "     - r3al3rai.com_ssl_certificate.cer"
Write-Host "     - r3al3rai.com_private.key"
Write-Host "     - r3al3rai.com_intermediate.pem"
Write-Host ""
Write-Host "  2. Update certificate paths in .env.local"
Write-Host ""
Write-Host "  3. Start the APIs (in separate terminals):"
Write-Host "     Terminal 1: python AI_Core_Worker\knowledge_api.py"
Write-Host "     Terminal 2: python src\apis\droid_api.py"
Write-Host ""
Write-Host "  4. Test endpoint with authentication:"
Write-Host "     curl -X POST http://localhost:5004/api/query " -ForegroundColor Gray
Write-Host "       -H X-Session-Token: $testToken " -ForegroundColor Gray
Write-Host "       -H Content-Type: application/json " -ForegroundColor Gray
Write-Host "       -d {`"query`": `"test query`"}" -ForegroundColor Gray
Write-Host ""
Write-Host "  5. Monitor logs for security events"
Write-Host ""
Write-Host "📊 Configuration Files:" -ForegroundColor Cyan
Write-Host "  - API Config: .env.local"
Write-Host "  - Example Config: .env.example.secured"
Write-Host "  - Documentation: SECURITY_IMPLEMENTATION_COMPLETE.md"
Write-Host ""
Write-Host "===============================================" -ForegroundColor Green
Write-Host ""
