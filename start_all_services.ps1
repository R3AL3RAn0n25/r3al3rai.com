# R3ÆLƎR AI - Complete System Startup
# Starts all services in the correct order

param(
    [switch]$NoWait = $false,
    [switch]$Verbose = $false
)

$ErrorActionPreference = "Continue"

function Write-Status {
    param([string]$Message, [string]$Status = "INFO")
    $colors = @{
        "INFO" = "Cyan"
        "SUCCESS" = "Green"
        "ERROR" = "Red"
        "WARNING" = "Yellow"
    }
    Write-Host "[$Status] $Message" -ForegroundColor $colors[$Status]
}

Write-Host "`n" -ForegroundColor Cyan
Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║      R3ÆLƎR AI - COMPLETE SYSTEM STARTUP                  ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Check if services are already running
Write-Status "Checking for running services..." "INFO"

$ports = @{
    "PostgreSQL" = 5432
    "Backend" = 3000
    "Frontend" = 5173
    "Knowledge API" = 5004
    "Storage Facility" = 3003
}

$running = @()
foreach ($service in $ports.Keys) {
    try {
        $connection = New-Object System.Net.Sockets.TcpClient
        $connection.Connect("localhost", $ports[$service])
        $connection.Close()
        $running += $service
        Write-Status "$service already running on port $($ports[$service])" "WARNING"
    }
    catch {
        # Service not running
    }
}

Write-Host ""

# 1. Start PostgreSQL (if not running)
if ($running -notcontains "PostgreSQL") {
    Write-Status "Starting PostgreSQL..." "INFO"
    try {
        # Check if PostgreSQL service exists
        $pgService = Get-Service -Name "postgresql-x64-*" -ErrorAction SilentlyContinue | Select-Object -First 1
        if ($pgService) {
            Start-Service -Name $pgService.Name -ErrorAction SilentlyContinue
            Write-Status "PostgreSQL service started" "SUCCESS"
        }
        else {
            Write-Status "PostgreSQL service not found. Ensure it's installed." "ERROR"
        }
    }
    catch {
        Write-Status "Could not start PostgreSQL: $_" "ERROR"
    }
    Start-Sleep -Seconds 3
}

# 2. Start Backend (Node.js)
if ($running -notcontains "Backend") {
    Write-Status "Starting Backend Server..." "INFO"
    try {
        $backendPath = Join-Path $PSScriptRoot "application\Backend"
        if (Test-Path $backendPath) {
            Push-Location $backendPath
            
            # Check if node_modules exists
            if (-not (Test-Path "node_modules")) {
                Write-Status "Installing dependencies..." "INFO"
                npm install
            }
            
            # Start backend in new window
            Start-Process -FilePath "cmd.exe" -ArgumentList "/c npm start" -WindowStyle Normal
            Write-Status "Backend started in new window" "SUCCESS"
            Pop-Location
        }
        else {
            Write-Status "Backend directory not found at $backendPath" "ERROR"
        }
    }
    catch {
        Write-Status "Could not start Backend: $_" "ERROR"
    }
    Start-Sleep -Seconds 5
}

# 3. Start Frontend (Vite)
if ($running -notcontains "Frontend") {
    Write-Status "Starting Frontend Dev Server..." "INFO"
    try {
        $frontendPath = Join-Path $PSScriptRoot "application\Frontend"
        if (Test-Path $frontendPath) {
            Push-Location $frontendPath
            
            # Check if node_modules exists
            if (-not (Test-Path "node_modules")) {
                Write-Status "Installing dependencies..." "INFO"
                npm install
            }
            
            # Start frontend in new window
            Start-Process -FilePath "cmd.exe" -ArgumentList "/c npm run dev" -WindowStyle Normal
            Write-Status "Frontend started in new window" "SUCCESS"
            Pop-Location
        }
        else {
            Write-Status "Frontend directory not found at $frontendPath" "ERROR"
        }
    }
    catch {
        Write-Status "Could not start Frontend: $_" "ERROR"
    }
    Start-Sleep -Seconds 3
}

# 4. Start Storage Facility (Python)
if ($running -notcontains "Storage Facility") {
    Write-Status "Starting Storage Facility..." "INFO"
    try {
        $storagePath = Join-Path $PSScriptRoot "AI_Core_Worker\self_hosted_storage_facility_windows.py"
        if (Test-Path $storagePath) {
            Start-Process -FilePath "python" -ArgumentList $storagePath -WindowStyle Normal
            Write-Status "Storage Facility started in new window" "SUCCESS"
        }
        else {
            Write-Status "Storage Facility script not found" "ERROR"
        }
    }
    catch {
        Write-Status "Could not start Storage Facility: $_" "ERROR"
    }
    Start-Sleep -Seconds 3
}

# 5. Start Knowledge API (Python)
if ($running -notcontains "Knowledge API") {
    Write-Status "Starting Knowledge API..." "INFO"
    try {
        $knowledgePath = Join-Path $PSScriptRoot "AI_Core_Worker\knowledge_api.py"
        if (Test-Path $knowledgePath) {
            Start-Process -FilePath "python" -ArgumentList $knowledgePath -WindowStyle Normal
            Write-Status "Knowledge API started in new window" "SUCCESS"
        }
        else {
            Write-Status "Knowledge API script not found" "ERROR"
        }
    }
    catch {
        Write-Status "Could not start Knowledge API: $_" "ERROR"
    }
    Start-Sleep -Seconds 2
}

Write-Host ""
Write-Status "Waiting for services to initialize..." "INFO"
Start-Sleep -Seconds 5

# Verify all services
Write-Host ""
Write-Status "Verifying services..." "INFO"
Write-Host ""

$allRunning = $true
foreach ($service in $ports.Keys) {
    try {
        $connection = New-Object System.Net.Sockets.TcpClient
        $connection.Connect("localhost", $ports[$service])
        $connection.Close()
        Write-Status "$service is running on port $($ports[$service])" "SUCCESS"
    }
    catch {
        Write-Status "$service is NOT running on port $($ports[$service])" "ERROR"
        $allRunning = $false
    }
}

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan

if ($allRunning) {
    Write-Host ""
    Write-Status "✓ All systems operational!" "SUCCESS"
    Write-Host ""
    Write-Host "Access the application:" -ForegroundColor Cyan
    Write-Host "  Frontend:  http://localhost:5173" -ForegroundColor Yellow
    Write-Host "  Backend:   http://localhost:3000" -ForegroundColor Yellow
    Write-Host "  Knowledge: http://localhost:5004" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Default credentials:" -ForegroundColor Cyan
    Write-Host "  Username: admin" -ForegroundColor Yellow
    Write-Host "  Password: (check .env file)" -ForegroundColor Yellow
}
else {
    Write-Host ""
    Write-Status "Some services failed to start. Check the windows above for errors." "ERROR"
}

Write-Host ""

if (-not $NoWait) {
    Write-Host "Press any key to continue..." -ForegroundColor Cyan
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}
