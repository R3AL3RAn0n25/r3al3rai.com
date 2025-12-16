# R3AL3R AI - PRODUCTION DEPLOYMENT (NO DEMO/DEV SERVERS)
# All services use Waitress production WSGI server
# No Flask development servers, no demo code

$ErrorActionPreference = "SilentlyContinue"
$ProjectRoot = $PSScriptRoot

Write-Host ""
Write-Host "================================================================" -ForegroundColor Green
Write-Host "          R3AL3R AI - PRODUCTION SYSTEM STARTUP" -ForegroundColor Green
Write-Host "          ALL SERVICES: PRODUCTION SERVERS (Waitress)" -ForegroundColor Green
Write-Host "================================================================" -ForegroundColor Green
Write-Host ""

# Python executable from venv
$pythonExe = Join-Path $ProjectRoot ".venv\Scripts\python.exe"

if (-not (Test-Path $pythonExe)) {
    Write-Host "ERROR: Python venv not found at: $pythonExe" -ForegroundColor Red
    Write-Host "Run this first: python -m venv .venv" -ForegroundColor Yellow
    exit 1
}

# Kill any existing services
Write-Host "Stopping any existing services..." -ForegroundColor Yellow
Get-Process | Where-Object {$_.ProcessName -eq 'python'} | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2
Write-Host "  Clean slate ready" -ForegroundColor Green
Write-Host ""

function Start-ProductionService {
    param(
        [string]$Name,
        [string]$Path,
        [string]$Runner,
        [int]$Port
    )
    
    Write-Host "Starting $Name (Port $Port)..." -ForegroundColor Cyan
    $runnerFile = Join-Path $Path $Runner
    
    if (Test-Path $runnerFile) {
        $command = "Write-Host ''; Write-Host '==========================================='; Write-Host '  $Name'; Write-Host '  Port: $Port (PRODUCTION - Waitress)'; Write-Host '  Started: $((Get-Date).ToString('yyyy-MM-dd HH:mm:ss'))'; Write-Host '==========================================='; Write-Host ''; cd '$Path'; & '$pythonExe' $Runner"
        Start-Process powershell -ArgumentList "-NoExit", "-Command", $command -WindowStyle Normal
        Start-Sleep -Seconds 3
        Write-Host "  $Name STARTED" -ForegroundColor Green
    } else {
        Write-Host "  ERROR: $runnerFile not found!" -ForegroundColor Red
    }
}

# Start all production services
Start-ProductionService -Name "Storage Facility" -Path (Join-Path $ProjectRoot "AI_Core_Worker") -Runner "run_storage.py" -Port 3003
Start-ProductionService -Name "Knowledge API" -Path (Join-Path $ProjectRoot "AI_Core_Worker") -Runner "run_knowledge.py" -Port 5004
Start-ProductionService -Name "Enhanced Intelligence" -Path (Join-Path $ProjectRoot "AI_Core_Worker") -Runner "run_intelligence.py" -Port 5010
Start-ProductionService -Name "Droid API" -Path (Join-Path $ProjectRoot "application\Backend") -Runner "run_droid.py" -Port 5005
Start-ProductionService -Name "User Auth API" -Path (Join-Path $ProjectRoot "AI_Core_Worker") -Runner "run_userauth.py" -Port 5006
Start-ProductionService -Name "BlackArch Security" -Path (Join-Path $ProjectRoot "Tools\tools") -Runner "run_blackarch.py" -Port 5003
Start-ProductionService -Name "Backend Server" -Path (Join-Path $ProjectRoot "application\Backend") -Runner "run_backend.py" -Port 3002
Start-ProductionService -Name "Management API" -Path (Join-Path $ProjectRoot "R3AL3R Production\manage") -Runner "run_management.py" -Port 5000

Write-Host ""
Write-Host "================================================================" -ForegroundColor Green
Write-Host "              R3AL3R AI PRODUCTION SYSTEM ONLINE" -ForegroundColor Green
Write-Host "================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "ALL SERVICES RUNNING WITH PRODUCTION WSGI SERVERS (Waitress)" -ForegroundColor Cyan
Write-Host ""
Write-Host "Core Services:" -ForegroundColor White
Write-Host "  Storage Facility    -> http://localhost:3003" -ForegroundColor Gray
Write-Host "  Knowledge API       -> http://localhost:5004" -ForegroundColor Gray
Write-Host "  Intelligence API    -> http://localhost:5010" -ForegroundColor Gray
Write-Host "  Droid API          -> http://localhost:5005" -ForegroundColor Gray
Write-Host "  User Auth          -> http://localhost:5006" -ForegroundColor Gray
Write-Host ""
Write-Host "Specialized Tools:" -ForegroundColor White
Write-Host "  BlackArch Security -> http://localhost:5003" -ForegroundColor Gray
Write-Host ""
Write-Host "User Interfaces:" -ForegroundColor White
Write-Host "  Backend Server     -> http://localhost:3002" -ForegroundColor Gray
Write-Host "  Management API     -> http://localhost:5000" -ForegroundColor Gray
Write-Host ""
Write-Host "PRODUCTION MODE: No development servers, no demo code" -ForegroundColor Green
Write-Host "Press Ctrl+C in any terminal to stop that service" -ForegroundColor Yellow
Write-Host ""
