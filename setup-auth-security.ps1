# R3ÆLƎR AI - Security Setup Script (PowerShell)
# Applies security hardening to user_auth_api.py

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "R3ÆLƎR AI - Security Setup" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# Check if .env.local exists
if (-Not (Test-Path ".env.local")) {
    Write-Host "⚠️  .env.local not found!" -ForegroundColor Yellow
    Write-Host "Creating .env.local from .env.example..." -ForegroundColor Yellow
    
    if (Test-Path ".env.example") {
        Copy-Item ".env.example" ".env.local"
        Write-Host "✅ Created .env.local" -ForegroundColor Green
    } else {
        Write-Host "❌ .env.example not found!" -ForegroundColor Red
        exit 1
    }
    
    Write-Host ""
    Write-Host "⚠️  Please edit .env.local with your database credentials:" -ForegroundColor Yellow
    Write-Host "   Notepad .env.local" -ForegroundColor Yellow
    exit 1
}

# Load environment variables
$env_content = Get-Content ".env.local" | ForEach-Object {
    if ($_ -match '^([^=]+)=(.*)$') {
        [Environment]::SetEnvironmentVariable($matches[1], $matches[2])
    }
}

# Install required packages
Write-Host ""
Write-Host "📦 Installing required dependencies..." -ForegroundColor Cyan
python -m pip install python-dotenv flask-limiter --quiet | Out-Null
if ($?) {
    Write-Host "✅ Dependencies installed" -ForegroundColor Green
} else {
    Write-Host "⚠️  Failed to install dependencies" -ForegroundColor Yellow
    Write-Host "   Run manually: pip install python-dotenv flask-limiter" -ForegroundColor Gray
}

# Check database configuration
Write-Host ""
Write-Host "🔍 Checking database configuration in .env.local..." -ForegroundColor Cyan

$dbHost = (Select-String -Path ".env.local" -Pattern "^DB_HOST=" | ForEach-Object { $_.Line -replace "DB_HOST=", "" })
$dbUser = (Select-String -Path ".env.local" -Pattern "^DB_USER=" | ForEach-Object { $_.Line -replace "DB_USER=", "" })
$dbName = (Select-String -Path ".env.local" -Pattern "^DB_NAME=" | ForEach-Object { $_.Line -replace "DB_NAME=", "" })

if ([string]::IsNullOrEmpty($dbHost) -or [string]::IsNullOrEmpty($dbUser)) {
    Write-Host "❌ Missing database credentials in .env.local" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Configuration looks good" -ForegroundColor Green
Write-Host "   Host: $dbHost" -ForegroundColor Gray
Write-Host "   User: $dbUser" -ForegroundColor Gray
Write-Host "   Database: $dbName" -ForegroundColor Gray

# Show migration reminder
Write-Host ""
Write-Host "==================================" -ForegroundColor Cyan
Write-Host "⚠️  DATABASE MIGRATION REQUIRED" -ForegroundColor Yellow
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Run this SQL migration on your PostgreSQL database:" -ForegroundColor Cyan
Write-Host ""
Write-Host "  psql -U $dbUser -d $dbName < SECURITY_MIGRATION.sql" -ForegroundColor Gray
Write-Host ""
Write-Host "Or manually run these SQL commands:" -ForegroundColor Cyan
Write-Host ""
Write-Host "  ALTER TABLE user_unit.profiles ADD COLUMN api_key_hash VARCHAR(64);" -ForegroundColor Gray
Write-Host "  CREATE INDEX idx_profiles_api_key_hash ON user_unit.profiles(api_key_hash);" -ForegroundColor Gray
Write-Host "  ALTER TABLE user_unit.sessions ADD COLUMN ip_address INET;" -ForegroundColor Gray
Write-Host "  ALTER TABLE user_unit.sessions ADD COLUMN user_agent VARCHAR(500);" -ForegroundColor Gray
Write-Host ""

# Verify files
Write-Host "==================================" -ForegroundColor Cyan
Write-Host "📋 Verification" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

$authApiPath = "src\apis\user_auth_api.py"
if (Test-Path $authApiPath) {
    Write-Host "✅ user_auth_api.py found" -ForegroundColor Green
} else {
    Write-Host "❌ user_auth_api.py not found at $authApiPath" -ForegroundColor Red
    exit 1
}

if (Test-Path ".env.local") {
    Write-Host "✅ .env.local configured" -ForegroundColor Green
} else {
    Write-Host "❌ .env.local not found" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "==================================" -ForegroundColor Cyan
Write-Host "✅ SETUP COMPLETE!" -ForegroundColor Green
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Run database migrations" -ForegroundColor White
Write-Host "2. Start the API:" -ForegroundColor White
Write-Host "   python src\apis\user_auth_api.py" -ForegroundColor Gray
Write-Host ""
Write-Host "Test with:" -ForegroundColor Cyan
Write-Host "   curl http://localhost:5004/health" -ForegroundColor Gray
Write-Host ""
