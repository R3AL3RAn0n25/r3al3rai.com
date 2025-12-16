# R3AL3R AI - BitXtractor Service Launcher
# Starts the BitXtractor backend API on port 3002

param(
    [string]$Port = "3002",
    [switch]$WSL = $false
)

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "R3AL3R AI - BitXtractor Service Launcher" -ForegroundColor Cyan
Write-Host ""

$RepoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$BackendDir = Join-Path $RepoRoot "application\Backend"
$VenvPython = Join-Path $RepoRoot ".venv\Scripts\python.exe"

if ($WSL) {
    Write-Host "Starting in WSL Mode..." -ForegroundColor Yellow
    
    # Check WSL
    $wslCheck = wsl --status 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "WSL not available. Install with: wsl --install" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "Checking bsddb3 in WSL..." -ForegroundColor Blue
    $bsddb3Check = wsl -d Ubuntu -- bash -lc "python3 -m pip show bsddb3 2>/dev/null"
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Installing bsddb3 in WSL..." -ForegroundColor Yellow
        wsl -d Ubuntu -- bash -lc 'sudo apt update; sudo apt install -y python3 python3-pip libdb-dev; pip3 install bsddb3 base58 cryptography flask flask-cors'
    }
    
    $WslRepoPath = $RepoRoot -replace '\\', '/' -replace 'C:', '/mnt/c'
    $WslBackendPath = "$WslRepoPath/application/Backend"
    
    Write-Host "Starting BitXtractor in WSL..." -ForegroundColor Blue
    Start-Process wsl -ArgumentList "-d", "Ubuntu", "--", "bash", "-lc", "cd '$WslBackendPath'; export FLASK_RUN_PORT=$Port; python3 app.py"
    
} else {
    Write-Host "Starting in Windows Mode..." -ForegroundColor Yellow
    
    if (-not (Test-Path $VenvPython)) {
        Write-Host "Virtual environment not found. Run: python -m venv .venv" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "Checking dependencies..." -ForegroundColor Blue
    & $VenvPython -m pip install --quiet flask flask-cors base58 cryptography 2>&1 | Out-Null
    
    Write-Host "Note: bsddb3 not available on Windows. Use -WSL for full support." -ForegroundColor Yellow
    
    $env:FLASK_RUN_PORT = $Port
    Write-Host "Starting BitXtractor on port $Port..." -ForegroundColor Blue
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$BackendDir'; & '$VenvPython' app.py"
}

Start-Sleep -Seconds 2

Write-Host ""
Write-Host "BitXtractor Service Started!" -ForegroundColor Green
Write-Host ""
Write-Host "Endpoints:" -ForegroundColor Cyan
Write-Host "  POST http://localhost:$Port/api/bitxtractor/start" -ForegroundColor White
Write-Host "  GET  http://localhost:$Port/api/bitxtractor/status/<job_id>" -ForegroundColor White
Write-Host ""
Write-Host "Test: python test_bitxtractor_integration.py" -ForegroundColor Yellow
Write-Host ""
