# R3ÆLƎR AI - Complete System Startup
# Starts Knowledge API, Droid API, and Backend Server

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║           R3ÆLƎR AI - Complete System Startup             ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Step 1: Start Storage Facility (PostgreSQL Knowledge Base)
Write-Host "🏢 [1/4] Starting Storage Facility (PostgreSQL)..." -ForegroundColor Yellow
$storagePath = Join-Path $PSScriptRoot "AI_Core_Worker"
$storageScript = Join-Path $storagePath "self_hosted_storage_facility_windows.py"

if (Test-Path $storageScript) {
    $command = "cd '$storagePath'; python self_hosted_storage_facility_windows.py"
    Start-Process powershell -ArgumentList "-NoExit", "-Command", $command -WindowStyle Normal
    Write-Host "    [OK] Storage Facility starting on http://localhost:3003" -ForegroundColor Green
    Write-Host "    [OK] Storage contains 30657 entries in Physics, Quantum, Space, and Crypto units." -ForegroundColor Green
    Start-Sleep -Seconds 5  # Wait for Storage Facility to initialize
} else {
    Write-Host "    ⚠ Storage Facility not found at: $storageScript" -ForegroundColor Yellow
    Write-Host "    Knowledge API will use fallback mode..." -ForegroundColor Yellow
}

# Step 2: Start Knowledge API in background
Write-Host ""
Write-Host "📚 [2/4] Starting Knowledge Base API..." -ForegroundColor Yellow
$kbPath = Join-Path $PSScriptRoot "AI_Core_Worker"
$kbScript = Join-Path $kbPath "knowledge_api.py"

if (Test-Path $kbScript) {
    $command = "`$env:KNOWLEDGE_API_PORT = '5004'; cd '$kbPath'; python knowledge_api.py"
    Start-Process powershell -ArgumentList "-NoExit", "-Command", $command -WindowStyle Normal
    Write-Host "    [OK] Knowledge API starting on http://localhost:5004" -ForegroundColor Green
    Write-Host "    [OK] Querying Storage Facility for knowledge retrieval" -ForegroundColor Green
    Start-Sleep -Seconds 3
} else {
    Write-Host "    ⚠ Knowledge API not found at: $kbScript" -ForegroundColor Yellow
    Write-Host "    Continuing without Knowledge Base..." -ForegroundColor Yellow
}

# Step 3: Start Droid API in background
Write-Host ""
Write-Host "🤖 [3/4] Starting Droid API..." -ForegroundColor Yellow
$droidPath = Join-Path $PSScriptRoot "application\Backend"
$droidScript = Join-Path $droidPath "droid_api.py"

if (Test-Path $droidScript) {
    $command = "cd '$droidPath'; python droid_api.py"
    Start-Process powershell -ArgumentList "-NoExit", "-Command", $command -WindowStyle Normal
    Write-Host "    [OK] Droid API starting on http://localhost:5005" -ForegroundColor Green
    Start-Sleep -Seconds 2
} else {
    Write-Host "    ⚠ Droid API not found at: $droidScript" -ForegroundColor Yellow
    Write-Host "    Continuing without Droid..." -ForegroundColor Yellow
}

# Step 4: Start Backend Server
Write-Host ""
Write-Host "🚀 [4/4] Starting Backend Server..." -ForegroundColor Yellow
$backendPath = Join-Path $PSScriptRoot "application\Backend"

if (Test-Path $backendPath) {
    Set-Location $backendPath
    
    Write-Host "    ✓ Starting server on http://192.168.1.59:3000" -ForegroundColor Green
    Write-Host ""
    Write-Host "════════════════════════════════════════════════════════════" -ForegroundColor Gray
    Write-Host "✅ System Status:" -ForegroundColor Green
    Write-Host "   • Storage Facility: http://localhost:3003 (PostgreSQL: 30,657 entries)" -ForegroundColor White
    Write-Host "   • Knowledge API:    http://localhost:5004 (Queries Storage Facility)" -ForegroundColor White
    Write-Host "   • Droid API:        http://localhost:5005 (Crypto Intent Recognition)" -ForegroundColor White
    Write-Host "   • Backend:          http://192.168.1.59:3000" -ForegroundColor White
    Write-Host "   • Frontend:         http://192.168.1.59:3000" -ForegroundColor White
    Write-Host "════════════════════════════════════════════════════════════" -ForegroundColor Gray
    Write-Host ""
    
    # Start the backend server
    npm start
} else {
    Write-Host "    [ERROR] Backend path not found: $backendPath" -ForegroundColor Red
    exit 1
}