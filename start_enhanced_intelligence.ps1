# R3ÆLƎR AI - Enhanced Intelligence Layer Startup (PowerShell)
# This script starts the Enhanced Knowledge API with all safety checks

$ErrorActionPreference = "Stop"

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "R3ÆLƎR AI - Enhanced Intelligence Layer Startup" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Change to workspace directory
$WorkspaceDir = "c:\Users\work8\OneDrive\Desktop\r3al3rai\New Folder 1\R3al3r-AI Main Working\R3aler-ai\R3aler-ai"
Set-Location $WorkspaceDir

# ========== CHECK 1: Storage Facility ==========
Write-Host "[1/5] Checking Storage Facility (port 5003)..." -ForegroundColor Yellow -NoNewline

try {
    $response = Invoke-WebRequest -Uri "http://localhost:5003/api/facility/health" -TimeoutSec 2 -UseBasicParsing -ErrorAction Stop
    $health = $response.Content | ConvertFrom-Json
    Write-Host " OK" -ForegroundColor Green
    Write-Host "      Total entries: $($health.total_entries)" -ForegroundColor Gray
} catch {
    Write-Host " FAILED" -ForegroundColor Red
    Write-Host ""
    Write-Host "ERROR: Storage Facility not running on port 5003" -ForegroundColor Red
    Write-Host "Please start it first:" -ForegroundColor Yellow
    Write-Host "  python AI_Core_Worker\storage_facility.py" -ForegroundColor White
    Write-Host ""
    pause
    exit 1
}

# ========== CHECK 2: Knowledge API (Optional) ==========
Write-Host "[2/5] Checking Knowledge API (port 5001)..." -ForegroundColor Yellow -NoNewline
start powershell.exe "-WindowStyle Normal -NoProfile -ExecutionPolicy Bypass -File 'scrip








tname.ps1'"try {
    $response = Invoke-WebRequest -Uri "http://localhost:5001/api/kb/health" -TimeoutSec 2 -UseBasicParsing -ErrorAction Stop
    Write-Host " OK" -ForegroundColor Green
} catch {
    Write-Host " WARNING" -ForegroundColor DarkYellow
    Write-Host "      Knowledge API not running (optional but recommended)" -ForegroundColor Gray
}

# ========== CHECK 3: PostgreSQL ==========
Write-Host "[3/5] Checking PostgreSQL database..." -ForegroundColor Yellow -NoNewline

try {
    # Check if postgres process is running
    $pgProcess = Get-Process -Name "postgres" -ErrorAction SilentlyContinue
    if ($pgProcess) {
        Write-Host " OK" -ForegroundColor Green
    } else {
        Write-Host " WARNING" -ForegroundColor DarkYellow
        Write-Host "      PostgreSQL process not detected (might be OK if using WSL)" -ForegroundColor Gray
    }
} catch {
    Write-Host " SKIPPED" -ForegroundColor DarkYellow
}

# ========== CHECK 4: Dependencies ==========
Write-Host "[4/5] Checking Python dependencies..." -ForegroundColor Yellow -NoNewline

try {
    python -c "import requests, flask, flask_cors" 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host " OK" -ForegroundColor Green
    } else {
        Write-Host " MISSING" -ForegroundColor Red
        Write-Host ""
        Write-Host "Installing dependencies..." -ForegroundColor Yellow
        pip install requests flask flask-cors
        if ($LASTEXITCODE -ne 0) {
            Write-Host "ERROR: Failed to install dependencies" -ForegroundColor Red
            pause
            exit 1
        }
        Write-Host "Dependencies installed successfully" -ForegroundColor Green
    }
} catch {
    Write-Host " ERROR" -ForegroundColor Red
    Write-Host "ERROR: Could not check dependencies" -ForegroundColor Red
    pause
    exit 1
}

# ========== CHECK 5: Port Availability ==========
Write-Host "[5/5] Checking port 5010 availability..." -ForegroundColor Yellow -NoNewline

$port = 5010
$tcpConnection = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue

if ($tcpConnection) {
    Write-Host " OCCUPIED" -ForegroundColor Red
    Write-Host ""
    Write-Host "ERROR: Port $port is already in use" -ForegroundColor Red
    Write-Host "Process using port: $($tcpConnection.OwningProcess)" -ForegroundColor Gray
    Write-Host "Please free port $port and try again" -ForegroundColor Yellow
    pause
    exit 1
} else {
    Write-Host " OK" -ForegroundColor Green
}

# ========== ALL CHECKS PASSED ==========
Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "READY TO LAUNCH" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Features enabled:" -ForegroundColor White
Write-Host "  ✓ Intent Classification (7 types)" -ForegroundColor Gray
Write-Host "  ✓ Live External Data (CoinGecko, NIST NVD, Wikipedia)" -ForegroundColor Gray
Write-Host "  ✓ Circuit Breakers (reliability)" -ForegroundColor Gray
Write-Host "  ✓ Security Validation (SQL injection, XSS, rate limiting)" -ForegroundColor Gray
Write-Host "  ✓ Performance Monitoring (metrics, uptime)" -ForegroundColor Gray
Write-Host "  ✓ Emergency Kill Switch" -ForegroundColor Gray
Write-Host ""
Write-Host "Database Status: " -ForegroundColor White -NoNewline
Write-Host "PRESERVED (no modifications)" -ForegroundColor Green
Write-Host ""
Write-Host "Starting Enhanced Knowledge API on port 5010..." -ForegroundColor Yellow
Write-Host ""

# ========== START API ==========
try {
    Set-Location "AI_Core_Worker"
    python enhanced_knowledge_api.py
} catch {
    Write-Host ""
    Write-Host "ERROR: Enhanced API stopped unexpectedly" -ForegroundColor Red
    Write-Host "Error: $_" -ForegroundColor Gray
    pause
    exit 1
}
