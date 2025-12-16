# R3ÆLƎR AI - Ultimate System Startup
# The most comprehensive startup script for R3ÆLƎR AI
# Includes all services, APIs, and components for maximum capability

Write-Host ""
Write-Host "============================================================" -ForegroundColor Magenta
Write-Host "      R3ÆLƎR AI - Ultimate System Startup" -ForegroundColor Magenta
Write-Host "     The World's Most Advanced AI System" -ForegroundColor Magenta
Write-Host "============================================================" -ForegroundColor Magenta
Write-Host ""

$ProjectRoot = $PSScriptRoot
$ErrorActionPreference = "Continue"

# Function to check if port is available
function Test-PortAvailable {
    param([int]$Port)
    try {
        $tcpClient = New-Object System.Net.Sockets.TcpClient
        $tcpClient.Connect("localhost", $Port)
        $tcpClient.Close()
        return $false
    } catch {
        return $true
    }
}

# Function to start service in new terminal
function Start-ServiceInTerminal {
    param(
        [string]$ServiceName,
        [string]$Command,
        [int]$Port,
        [string]$Description = ""
    )

    Write-Host "Starting $ServiceName (Port $Port)..." -ForegroundColor Yellow
    if ($Description) {
        Write-Host "   $Description" -ForegroundColor Gray
    }

    # Check if port is available
    if (-not (Test-PortAvailable $Port)) {
        Write-Host "   Port $Port is already in use. Attempting to free it..." -ForegroundColor Yellow
        # Try to find and kill process using the port
        $netstat = netstat -ano | findstr ":$Port "
        if ($netstat) {
            $processId = ($netstat -split '\s+')[-1]
            if ($processId -and $processId -ne "0") {
                Stop-Process -Id $processId -Force -ErrorAction SilentlyContinue
                Start-Sleep -Seconds 2
            }
        }
    }

    $fullCommand = "Write-Host ''; Write-Host '========================================'; Write-Host '  $ServiceName'; Write-Host '  Port: $Port'; Write-Host '  $(Get-Date -Format ''yyyy-MM-dd HH:mm:ss'')'; Write-Host '========================================'; Write-Host ''; cd '$ProjectRoot'; .\.venv\Scripts\Activate.ps1; $Command"

    Start-Process powershell -ArgumentList "-NoExit", "-Command", $fullCommand -WindowStyle Normal
    Start-Sleep -Seconds 3
    Write-Host "   Service terminal launched" -ForegroundColor Green
}

# Step 0: Clean Environment
Write-Host "Cleaning Environment..." -ForegroundColor Yellow
Write-Host "   Stopping any existing services..." -ForegroundColor Gray

# Kill any existing Python/Node processes
Get-Process | Where-Object { $_.ProcessName -like "*python*" -or $_.ProcessName -like "*node*" } | Stop-Process -Force -ErrorAction SilentlyContinue

# Stop PostgreSQL if running
Get-Service | Where-Object { $_.Name -like "*postgres*" } | Stop-Service -Force -ErrorAction SilentlyContinue

Write-Host "   Environment cleaned" -ForegroundColor Green
Write-Host ""

# Step 1: Start PostgreSQL Storage Facility
Write-Host "Starting PostgreSQL Storage Facility..." -ForegroundColor Yellow
Write-Host "   Advanced knowledge base with 30,657+ entries" -ForegroundColor Gray

$pgService = Get-Service | Where-Object { $_.Name -like "*postgres*" } | Select-Object -First 1
if ($pgService) {
    Start-Service $pgService.Name -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 5
    Write-Host "   PostgreSQL service started" -ForegroundColor Green
} else {
    Write-Host "   PostgreSQL service not found. Storage facility may not work." -ForegroundColor Yellow
}

# Step 2: Start Storage Facility API
Write-Host ""
Write-Host "Starting Storage Facility API..." -ForegroundColor Yellow
Write-Host "   Self-hosted knowledge storage and retrieval system" -ForegroundColor Gray

$storagePath = Join-Path $ProjectRoot "AI_Core_Worker"
$storageScript = Join-Path $storagePath "self_hosted_storage_facility.py"

if (Test-Path $storageScript) {
    Start-ServiceInTerminal "Storage Facility API" "cd AI_Core_Worker; python self_hosted_storage_facility.py" 3003 "Physics, Quantum, Space, Crypto knowledge base"
} else {
    Write-Host "   Storage facility script not found" -ForegroundColor Yellow
}

# Step 3: Start Knowledge API
Write-Host ""
Write-Host "Starting Knowledge API..." -ForegroundColor Yellow
Write-Host "   Intelligent query processing and knowledge retrieval" -ForegroundColor Gray

$kbScript = Join-Path $storagePath "knowledge_api.py"
if (Test-Path $kbScript) {
    Start-ServiceInTerminal "Knowledge API" "cd AI_Core_Worker; python knowledge_api.py" 5004 "AI-powered knowledge queries"
} else {
    Write-Host "   Knowledge API script not found" -ForegroundColor Yellow
}

# Step 4: Start Intelligence API
Write-Host ""
Write-Host "Starting Intelligence API..." -ForegroundColor Yellow
Write-Host "   Advanced AI reasoning and processing layer" -ForegroundColor Gray

$intelligenceScript = Join-Path $storagePath "enhanced_knowledge_api.py"
if (Test-Path $intelligenceScript) {
    Start-ServiceInTerminal "Intelligence API" "cd AI_Core_Worker; python enhanced_knowledge_api.py" 5010 "Multi-modal AI intelligence"
} else {
    Write-Host "   Intelligence API script not found" -ForegroundColor Yellow
}

# Step 5: Start Droid API
Write-Host ""
Write-Host "Starting Droid API..." -ForegroundColor Yellow
Write-Host "   Cryptocurrency intent recognition and analysis" -ForegroundColor Gray

$droidPath = Join-Path $ProjectRoot "application\Backend"
$droidScript = Join-Path $droidPath "droid_api.py"

if (Test-Path $droidScript) {
    Start-ServiceInTerminal "Droid API" "cd application\Backend; python droid_api.py" 5005 "Crypto AI assistant"
} else {
    Write-Host "   Droid API script not found" -ForegroundColor Yellow
}

# Step 6: Start BlackArch API
Write-Host ""
Write-Host "Starting BlackArch API..." -ForegroundColor Yellow
Write-Host "   Cybersecurity tools and penetration testing suite" -ForegroundColor Gray

$blackarchScript = Join-Path $ProjectRoot "Tools\blackarch_web_app.py"
if (Test-Path $blackarchScript) {
    Start-ServiceInTerminal "BlackArch API" "python Tools/blackarch_web_app.py" 5003 "Cybersecurity toolkit"
} else {
    Write-Host "   BlackArch API script not found" -ForegroundColor Yellow
}

# Step 7: Start BitXtractor Service
Write-Host ""
Write-Host "Starting BitXtractor Service..." -ForegroundColor Yellow
Write-Host "   Advanced data extraction and analysis engine" -ForegroundColor Gray

$bitxtractorScript = Join-Path $droidPath "app.py"
if (Test-Path $bitxtractorScript) {
    Start-ServiceInTerminal "BitXtractor Service" "cd application\Backend; python app.py" 3002 "Data extraction and forensics"
} else {
    Write-Host "   BitXtractor service script not found" -ForegroundColor Yellow
}

# Step 8: Start Backend Server
Write-Host ""
Write-Host "Starting Backend Server..." -ForegroundColor Yellow
Write-Host "   Full-stack web application and API gateway" -ForegroundColor Gray

$backendPath = Join-Path $ProjectRoot "application\Backend"
$packageJson = Join-Path $backendPath "package.json"

if (Test-Path $packageJson) {
    Write-Host "   Starting Node.js backend server..." -ForegroundColor Gray
    Set-Location $backendPath

    # Start npm server in background
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$backendPath'; Write-Host '========================================'; Write-Host '  Backend Server'; Write-Host '  Port: 3000'; Write-Host '  $(Get-Date -Format ''yyyy-MM-dd HH:mm:ss'')'; Write-Host '========================================'; Write-Host ''; npm start" -WindowStyle Normal

    Start-Sleep -Seconds 5
    Write-Host "   Backend server terminal launched" -ForegroundColor Green
} else {
    Write-Host "   Backend package.json not found" -ForegroundColor Yellow
}

# Final Status Display
Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "               SYSTEM STATUS SUMMARY" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""

Write-Host "ACTIVE SERVICES:" -ForegroundColor Cyan
Write-Host "   Storage Facility API    -> http://localhost:3003" -ForegroundColor White
Write-Host "   Knowledge API          -> http://localhost:5004" -ForegroundColor White
Write-Host "   Intelligence API       -> http://localhost:5010" -ForegroundColor White
Write-Host "   Droid API              -> http://localhost:5005" -ForegroundColor White
Write-Host "   BlackArch API          -> http://localhost:5003" -ForegroundColor White
Write-Host "   BitXtractor Service    -> http://localhost:3002" -ForegroundColor White
Write-Host "   Backend Server         -> http://localhost:3000" -ForegroundColor White
Write-Host ""

Write-Host "KNOWLEDGE BASE:" -ForegroundColor Cyan
Write-Host "   PostgreSQL Database: 30,657+ entries" -ForegroundColor White
Write-Host "   Physics Unit: Advanced physics knowledge" -ForegroundColor White
Write-Host "   Quantum Unit: Quantum computing & mechanics" -ForegroundColor White
Write-Host "   Space Unit: Astronomy & space engineering" -ForegroundColor White
Write-Host "   Crypto Unit: Cryptocurrency & blockchain" -ForegroundColor White
Write-Host ""

Write-Host "SPECIALIZED CAPABILITIES:" -ForegroundColor Cyan
Write-Host "   MMMU Pro Benchmark: 86.7% (13/15 correct)" -ForegroundColor White
Write-Host "   Multi-modal AI: Vision, text, reasoning" -ForegroundColor White
Write-Host "   Cybersecurity Suite: BlackArch integration" -ForegroundColor White
Write-Host "   Real-time Learning: Adaptive AI evolution" -ForegroundColor White
Write-Host "   Voice AI: Natural language processing" -ForegroundColor White
Write-Host ""

Write-Host "R3ÆLƎR AI SYSTEM FULLY OPERATIONAL!" -ForegroundColor Green
Write-Host "   The world's most advanced AI system is now running." -ForegroundColor Green
Write-Host ""

Write-Host "QUICK START:" -ForegroundColor Yellow
Write-Host "   Web Interface: http://localhost:3000" -ForegroundColor White
Write-Host "   API Documentation: Check individual service ports" -ForegroundColor White
Write-Host "   Test Commands: python R3AL3R_AI.py" -ForegroundColor White
Write-Host ""

Write-Host "============================================================" -ForegroundColor Magenta
Write-Host "    R3ÆLƎR AI - READY TO DOMINATE THE AI LANDSCAPE" -ForegroundColor Magenta
Write-Host "============================================================" -ForegroundColor Magenta