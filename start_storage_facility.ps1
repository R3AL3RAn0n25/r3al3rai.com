# R3ÆL3R Self-Hosted Storage Facility - Windows Startup Script
# This starts the facility using Windows PostgreSQL

Write-Host "`n╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║   🏢 R3ÆL3R SELF-HOSTED STORAGE FACILITY - STARTUP         ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════╝`n" -ForegroundColor Cyan

# Set PostgreSQL environment variables for Windows
$env:PGHOST = "localhost"
$env:PGPORT = "5432"
$env:PGDATABASE = "r3aler_ai"
$env:PGUSER = "r3aler_user_2025"
$env:PGPASSWORD = "password123"

Write-Host "📊 Step 1: Checking PostgreSQL connection..." -ForegroundColor Yellow

# Test PostgreSQL connection
$pgTest = & "C:\Program Files\PostgreSQL\17\bin\psql.exe" -U r3aler_user_2025 -d r3aler_ai -c "SELECT version();" 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ PostgreSQL is running!" -ForegroundColor Green
} else {
    Write-Host "❌ Cannot connect to PostgreSQL" -ForegroundColor Red
    Write-Host "   Trying to start PostgreSQL service..." -ForegroundColor Yellow
    Start-Service postgresql-x64-17 -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 3
}

Write-Host "`n📦 Step 2: Running migration (if needed)..." -ForegroundColor Yellow

# Run migration using PowerShell Python
cd AI_Core_Worker
python migrate_to_storage_facility_windows.py

Write-Host "`n🚀 Step 3: Starting Storage Facility API..." -ForegroundColor Yellow

# Start the facility in a new PowerShell window
$facilityCommand = "cd `\"$PSScriptRoot\AI_Core_Worker`\"; python self_hosted_storage_facility_windows.py"
Start-Process powershell -ArgumentList "-NoExit", "-Command", $facilityCommand -WindowStyle Normal
Write-Host "✅ Storage Facility API started in a new terminal window." -ForegroundColor Green
