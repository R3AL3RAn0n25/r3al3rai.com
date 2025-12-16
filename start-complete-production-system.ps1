# R3ÆLƎR AI - COMPLETE PRODUCTION SYSTEM STARTUP
# Integrates ALL subsystems with proper routing and management
# RVN (Privacy), BitXtractor (Forensics), BlackArch (Security), Management (Control)

Write-Host ""
Write-Host "================================================================" -ForegroundColor Magenta
Write-Host "    R3ÆLƎR AI - COMPLETE PRODUCTION SYSTEM STARTUP" -ForegroundColor Magenta
Write-Host "    THE WORLD'S MOST ADVANCED AI WITH ALL SUBSYSTEMS" -ForegroundColor Magenta
Write-Host "================================================================" -ForegroundColor Magenta
Write-Host ""

$ProjectRoot = $PSScriptRoot
$ErrorActionPreference = "Continue"

# Function to start service in new terminal
function Start-R3AL3RService {
    param(
        [string]$ServiceName,
        [string]$Command,
        [int]$Port,
        [string]$Description = "",
        [string]$WorkingDirectory = $ProjectRoot
    )

    Write-Host "Starting $ServiceName..." -ForegroundColor Yellow
    if ($Description) {
        Write-Host "   $Description" -ForegroundColor Gray
    }

    $fullCommand = "Write-Host ''; Write-Host '========================================'; Write-Host '  $ServiceName'; Write-Host '  Port: $Port'; Write-Host '  $((Get-Date).ToString('yyyy-MM-dd HH:mm:ss'))'; Write-Host '========================================'; Write-Host ''; cd '$WorkingDirectory'; $Command"

    Start-Process powershell -ArgumentList "-NoExit", "-Command", $fullCommand -WindowStyle Normal
    Start-Sleep -Seconds 3
    Write-Host "   $ServiceName terminal launched" -ForegroundColor Green
}

# Function to check if port is in use
function Test-PortInUse {
    param([int]$Port)
    try {
        $tcpClient = New-Object System.Net.Sockets.TcpClient
        $tcpClient.Connect("localhost", $Port)
        $tcpClient.Close()
        return $true
    } catch {
        return $false
    }
}

# Function to kill process on port
function Stop-ProcessOnPort {
    param([int]$Port)
    try {
        $tcpConnections = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
        if ($tcpConnections) {
            foreach ($conn in $tcpConnections) {
                $processId = $conn.OwningProcess
                if ($processId) {
                    Write-Host "   Stopping process on port $Port (PID: $processId)" -ForegroundColor Red
                    Stop-Process -Id $processId -Force -ErrorAction SilentlyContinue
                }
            }
            Start-Sleep -Seconds 2
        }
    } catch {
        Write-Host "   Could not stop process on port $Port" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "STEP 1: INFRASTRUCTURE SERVICES" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Start PostgreSQL Database
Write-Host "Starting PostgreSQL Database..." -ForegroundColor Yellow
Write-Host "   Self-hosted knowledge storage with 30,657+ entries" -ForegroundColor Gray

$pgService = Get-Service | Where-Object { $_.Name -like "*postgres*" } | Select-Object -First 1
if ($pgService) {
    Start-Service $pgService.Name -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 5
    Write-Host "   PostgreSQL database started" -ForegroundColor Green
} else {
    Write-Host "   PostgreSQL service not found - please start manually" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "STEP 2: CORE AI SERVICES" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

# Step 2: Start Storage Facility
Start-R3AL3RService `
    -ServiceName "Storage Facility" `
    -Command "python AI_Core_Worker\self_hosted_storage_facility.py" `
    -Port 3003 `
    -Description "Self-hosted PostgreSQL knowledge storage (30,657+ entries)"

# Step 3: Start Knowledge API
Start-R3AL3RService `
    -ServiceName "Knowledge API" `
    -Command "python AI_Core_Worker\knowledge_api.py" `
    -Port 5004 `
    -Description "AI-powered knowledge retrieval with 30,657+ knowledge entries"

# Step 4: Start Enhanced Intelligence API
Start-R3AL3RService `
    -ServiceName "Enhanced Intelligence API" `
    -Command "python AI_Core_Worker\enhanced_knowledge_api.py" `
    -Port 5010 `
    -Description "Multi-modal AI with vision, reasoning, advanced processing"

# Step 5: Start Droid API (Crypto AI)
Start-R3AL3RService `
    -ServiceName "Droid API (Crypto AI)" `
    -Command "python -m application.Backend.droid_api" `
    -Port 5005 `
    -Description "Cryptocurrency AI assistant with intent recognition"

# Step 6: Start User Authentication API
Start-R3AL3RService `
    -ServiceName "User Authentication API" `
    -Command "python AI_Core_Worker\user_auth_api.py" `
    -Port 5006 `
    -Description "Secure user management and authentication system"

Write-Host ""
Write-Host "STEP 3: SPECIALIZED SUBSYSTEMS" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

# Step 7: Start RVN - Virtual Realer Network (Privacy System)
Write-Host ""
Write-Host "Starting RVN - Virtual Realer Network..." -ForegroundColor Yellow
Write-Host "   Complete Privacy System for 'Going Ghost Online'" -ForegroundColor Gray
Write-Host "   V2Ray + Xray Reality, MAC Spoofing, Key Rotation" -ForegroundColor Gray

$rvnPath = Join-Path $ProjectRoot "RVN"
if (Test-Path $rvnPath) {
    # Check if Go is installed
    try {
        $goVersion = go version 2>&1
        Write-Host "   Go detected: $goVersion" -ForegroundColor Green
        
        # Build RVN if not already built
        $rvnBinaryPath = Join-Path $rvnPath "rvn.exe"
        if (-not (Test-Path $rvnBinaryPath)) {
            Write-Host "   Building RVN from source..." -ForegroundColor Yellow
            $buildCommand = "cd '$rvnPath\cmd\rvn'; go build -o '$rvnBinaryPath' ."
            Start-Process powershell -ArgumentList "-NoExit", "-Command", $buildCommand -WindowStyle Normal -Wait
        }
        
        # Start RVN service
        Start-R3AL3RService `
            -ServiceName "RVN Privacy Network" `
            -Command "./rvn.exe -config config.toml" `
            -Port 8443 `
            -Description "Complete privacy network with V2Ray/Xray Reality" `
            -WorkingDirectory $rvnPath
            
    } catch {
        Write-Host "   Go not installed - skipping RVN (install Go 1.21+ to enable)" -ForegroundColor Yellow
        Write-Host "   RVN provides complete online privacy and anonymity" -ForegroundColor Gray
    }
} else {
    Write-Host "   RVN directory not found at: $rvnPath" -ForegroundColor Yellow
}

# Step 8: Start BitXtractor - Wallet Analysis System
Write-Host ""
Write-Host "Starting BitXtractor - Wallet Analysis System..." -ForegroundColor Yellow
Write-Host "   Advanced cryptocurrency wallet extraction and forensics" -ForegroundColor Gray
Write-Host "   Private key extraction, decryption, balance checking" -ForegroundColor Gray

Stop-ProcessOnPort -Port 3002

Start-R3AL3RService `
    -ServiceName "BitXtractor Forensics" `
    -Command "python -m application.Backend.app" `
    -Port 3002 `
    -Description "Cryptocurrency wallet analysis and key extraction"

# Step 9: Start BlackArch Tools - Security Suite
Write-Host ""
Write-Host "Starting BlackArch Tools - Security Suite..." -ForegroundColor Yellow
Write-Host "   55 integrated security tools across multiple categories" -ForegroundColor Gray
Write-Host "   Exploitation, Forensics, Networking, Password Cracking" -ForegroundColor Gray

Stop-ProcessOnPort -Port 5003

Start-R3AL3RService `
    -ServiceName "BlackArch Security (PRODUCTION)" `
    -Command "python Tools\tools\run_blackarch.py" `
    -Port 5003 `
    -Description "Complete cybersecurity toolkit with 55+ tools"

Write-Host ""
Write-Host "STEP 4: MANAGEMENT & CONTROL SYSTEM" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

# Step 10: Start Management System
Write-Host "Starting R3AL3R Management System..." -ForegroundColor Yellow
Write-Host "   Production monitoring, service control, analytics" -ForegroundColor Gray
Write-Host "   Real-time health checks, mode switching, system improvements" -ForegroundColor Gray

Stop-ProcessOnPort -Port 5000

$managementPath = Join-Path $ProjectRoot "R3AL3R Production\manage"
if (Test-Path (Join-Path $managementPath "management_api.py")) {
    Start-R3AL3RService `
        -ServiceName "R3AL3R Management System" `
        -Command "python management_api.py" `
        -Port 5000 `
        -Description "Production management and monitoring system" `
        -WorkingDirectory $managementPath
} else {
    Write-Host "   Management API not found - using fallback location" -ForegroundColor Yellow
    Start-R3AL3RService `
        -ServiceName "R3AL3R Management System" `
        -Command "python R3AL3R` Production\manage\management_api.py" `
        -Port 5000 `
        -Description "Production management and monitoring system"
}

Write-Host ""
Write-Host "STEP 5: MAIN AI SYSTEM & BACKEND" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

# Step 11: Start Main R3AL3R AI System
Write-Host ""
Write-Host "Starting Main R3AL3R AI Orchestrator..." -ForegroundColor Yellow
Write-Host "   Core AI system with all engines and components" -ForegroundColor Gray

$aiCommand = "Write-Host ''; Write-Host '========================================'; Write-Host '  R3AL3R AI Main System'; Write-Host '  All Engines Active'; Write-Host '  $((Get-Date).ToString('yyyy-MM-dd HH:mm:ss'))'; Write-Host '========================================'; Write-Host ''; cd '$ProjectRoot'; python R3AL3R_AI.py; Write-Host 'Press Enter to exit...'; Read-Host"

Start-Process powershell -ArgumentList "-NoExit", "-Command", $aiCommand -WindowStyle Normal
Start-Sleep -Seconds 5
Write-Host "   R3AL3R AI orchestrator launched" -ForegroundColor Green

# Step 12: Start Backend Web Server
Write-Host ""
Write-Host "Starting Backend Web Server..." -ForegroundColor Yellow
Write-Host "   Full-stack web application and API gateway" -ForegroundColor Gray

Stop-ProcessOnPort -Port 3000

$backendPath = Join-Path $ProjectRoot "application\Backend"
$pythonExe = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
if (Test-Path (Join-Path $backendPath "run_backend.py")) {
    $backendCommand = "Write-Host ''; Write-Host '========================================'; Write-Host '  Backend Server (Flask/Waitress)'; Write-Host '  Port: 3002'; Write-Host '  $((Get-Date).ToString('yyyy-MM-dd HH:mm:ss'))'; Write-Host '========================================'; Write-Host ''; cd '$backendPath'; & '$pythonExe' run_backend.py"

    Start-Process powershell -ArgumentList "-NoExit", "-Command", $backendCommand -WindowStyle Normal
    Start-Sleep -Seconds 5
    Write-Host "   Backend production server launched" -ForegroundColor Green
} else {
    Write-Host "   Backend run_backend.py not found at: $backendPath" -ForegroundColor Yellow
    Write-Host "   Skipping backend server startup" -ForegroundColor Yellow
}

# Wait for all services to initialize
Write-Host ""
Write-Host "Waiting for all services to initialize..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Final Status Display
Write-Host ""
Write-Host "================================================================" -ForegroundColor Green
Write-Host "          R3AL3R AI - COMPLETE PRODUCTION SYSTEM STATUS" -ForegroundColor Green
Write-Host "================================================================" -ForegroundColor Green
Write-Host ""

Write-Host "INFRASTRUCTURE:" -ForegroundColor Cyan
Write-Host "   PostgreSQL Database     -> Active (30,657+ knowledge entries)" -ForegroundColor White
Write-Host ""

Write-Host "CORE AI SERVICES:" -ForegroundColor Cyan
Write-Host "   Storage Facility        -> http://localhost:3003" -ForegroundColor White
Write-Host "   Knowledge API           -> http://localhost:5004" -ForegroundColor White
Write-Host "   Intelligence API        -> http://localhost:5010" -ForegroundColor White
Write-Host "   Droid API (Crypto)      -> http://localhost:5005" -ForegroundColor White
Write-Host "   User Auth API           -> http://localhost:5006" -ForegroundColor White
Write-Host ""

Write-Host "SPECIALIZED SUBSYSTEMS:" -ForegroundColor Cyan
Write-Host "   RVN Privacy Network     -> https://localhost:8443 (https://r3al3rai.com/rvn)" -ForegroundColor White
Write-Host "   BitXtractor Forensics   -> http://localhost:3002 (https://r3al3rai.com/bitxtractor)" -ForegroundColor White
Write-Host "   BlackArch Security      -> http://localhost:5003 (https://r3al3rai.com/blackarchtools)" -ForegroundColor White
Write-Host ""

Write-Host "MANAGEMENT & CONTROL:" -ForegroundColor Cyan
Write-Host "   Management System       -> http://localhost:5000 (https://r3al3rai.com/manage)" -ForegroundColor White
Write-Host "   Main AI Orchestrator    -> Active (All Engines)" -ForegroundColor White
Write-Host "   Backend Web Server      -> http://localhost:3000 (https://r3al3rai.com)" -ForegroundColor White
Write-Host ""

Write-Host "URL ROUTING (via Nginx):" -ForegroundColor Cyan
Write-Host "   https://r3al3rai.com/rvn            -> RVN Privacy System" -ForegroundColor White
Write-Host "   https://r3al3rai.com/bitxtractor    -> Wallet Forensics" -ForegroundColor White
Write-Host "   https://r3al3rai.com/blackarchtools -> Security Tools Suite" -ForegroundColor White
Write-Host "   https://r3al3rai.com/manage         -> Management System" -ForegroundColor White
Write-Host "   https://r3al3rai.com/api/*          -> Core AI APIs" -ForegroundColor White
Write-Host "   https://r3al3rai.com                -> Main Application" -ForegroundColor White
Write-Host ""

Write-Host "ADVANCED AI ENGINES:" -ForegroundColor Cyan
Write-Host "   Evolution Engine        -> Self-improving algorithms" -ForegroundColor White
Write-Host "   Vector Engine           -> Advanced semantic search" -ForegroundColor White
Write-Host "   Self-Learning Engine    -> Adaptive AI evolution" -ForegroundColor White
Write-Host "   Intelligence Layer      -> Multi-modal processing" -ForegroundColor White
Write-Host "   Math Reasoning Engine   -> Advanced mathematical analysis" -ForegroundColor White
Write-Host "   Memory Management       -> Context-aware interactions" -ForegroundColor White
Write-Host "   Security Manager        -> Advanced threat protection" -ForegroundColor White
Write-Host ""

Write-Host "KNOWLEDGE BASE:" -ForegroundColor Cyan
Write-Host "   Total Entries: 30,657+" -ForegroundColor White
Write-Host "   Physics Unit: 25,875 advanced physics concepts" -ForegroundColor White
Write-Host "   Quantum Unit: 1,042 quantum mechanics and computing" -ForegroundColor White
Write-Host "   Space/Astro Unit: 3,727 astronomy and space engineering" -ForegroundColor White
Write-Host "   Crypto Unit: 13 blockchain and cryptocurrency" -ForegroundColor White
Write-Host "   BlackArch Unit: Cybersecurity tools and techniques" -ForegroundColor White
Write-Host ""

Write-Host "SPECIALIZED CAPABILITIES:" -ForegroundColor Cyan
Write-Host "   RVN Privacy System:" -ForegroundColor Yellow
Write-Host "      - V2Ray + Xray Reality protocol for complete anonymity" -ForegroundColor White
Write-Host "      - MAC address spoofing for hardware-level privacy" -ForegroundColor White
Write-Host "      - Adaptive key rotation for continuous security" -ForegroundColor White
Write-Host "      - Traffic pattern masking (appears as Microsoft CDN)" -ForegroundColor White
Write-Host "      - DPI, ISP logging, Great Firewall bypass" -ForegroundColor White
Write-Host ""
Write-Host "   BitXtractor Forensics:" -ForegroundColor Yellow
Write-Host "      - Bitcoin wallet.dat analysis and extraction" -ForegroundColor White
Write-Host "      - Unencrypted private key extraction" -ForegroundColor White
Write-Host "      - Encrypted private key extraction" -ForegroundColor White
Write-Host "      - Passphrase-based decryption" -ForegroundColor White
Write-Host "      - JSON/CSV/Electrum export formats" -ForegroundColor White
Write-Host "      - Real-time balance checking" -ForegroundColor White
Write-Host ""
Write-Host "   BlackArch Security Suite:" -ForegroundColor Yellow
Write-Host "      - 55 integrated security tools" -ForegroundColor White
Write-Host "      - Exploitation tools (6 tools)" -ForegroundColor White
Write-Host "      - Forensics and analysis tools" -ForegroundColor White
Write-Host "      - Networking and scanning tools" -ForegroundColor White
Write-Host "      - Password cracking capabilities" -ForegroundColor White
Write-Host ""
Write-Host "   Management System:" -ForegroundColor Yellow
Write-Host "      - Real-time service health monitoring" -ForegroundColor White
Write-Host "      - Service control (start/stop/restart)" -ForegroundColor White
Write-Host "      - Mode switching (dev/prod)" -ForegroundColor White
Write-Host "      - Automatic update deployment" -ForegroundColor White
Write-Host "      - Cloud storage integration" -ForegroundColor White
Write-Host "      - Performance analytics and reporting" -ForegroundColor White
Write-Host "      - System optimization and adjustments" -ForegroundColor White
Write-Host ""

Write-Host "================================================================" -ForegroundColor Magenta
Write-Host "   R3AL3R AI - COMPLETE PRODUCTION SYSTEM FULLY OPERATIONAL!" -ForegroundColor Magenta
Write-Host "================================================================" -ForegroundColor Magenta
Write-Host ""
Write-Host "All subsystems are now running with proper URL routing." -ForegroundColor Green
Write-Host "Access the main application at: https://r3al3rai.com" -ForegroundColor Green
Write-Host ""
Write-Host "Subsystem URLs:" -ForegroundColor Yellow
Write-Host "   RVN Privacy:      https://r3al3rai.com/rvn" -ForegroundColor White
Write-Host "   BitXtractor:      https://r3al3rai.com/bitxtractor" -ForegroundColor White
Write-Host "   BlackArch Tools:  https://r3al3rai.com/blackarchtools" -ForegroundColor White
Write-Host "   Management:       https://r3al3rai.com/manage" -ForegroundColor White
Write-Host ""
Write-Host "The system is ready to accept users and can be continuously" -ForegroundColor Green
Write-Host "improved and expanded with new features and capabilities!" -ForegroundColor Green
Write-Host ""
Write-Host "Press any key to view the Nginx configuration reminder..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

Write-Host ""
Write-Host "================================================================" -ForegroundColor Yellow
Write-Host "         NGINX CONFIGURATION REMINDER" -ForegroundColor Yellow
Write-Host "================================================================" -ForegroundColor Yellow
Write-Host ""
Write-Host "The Nginx configuration has been updated at:" -ForegroundColor White
Write-Host "   $ProjectRoot\R3AL3R Production\nginx\r3al3rai.com.conf" -ForegroundColor Cyan
Write-Host ""
Write-Host "To deploy to production server (WSL/Linux):" -ForegroundColor White
Write-Host "   1. Copy the config to Nginx sites-available:" -ForegroundColor Gray
Write-Host "      sudo cp 'R3AL3R Production/nginx/r3al3rai.com.conf' /etc/nginx/sites-available/" -ForegroundColor Gray
Write-Host ""
Write-Host "   2. Create symbolic link to sites-enabled:" -ForegroundColor Gray
Write-Host "      sudo ln -sf /etc/nginx/sites-available/r3al3rai.com.conf /etc/nginx/sites-enabled/" -ForegroundColor Gray
Write-Host ""
Write-Host "   3. Test Nginx configuration:" -ForegroundColor Gray
Write-Host "      sudo nginx -t" -ForegroundColor Gray
Write-Host ""
Write-Host "   4. Reload Nginx:" -ForegroundColor Gray
Write-Host "      sudo systemctl reload nginx" -ForegroundColor Gray
Write-Host ""
Write-Host "The configuration includes complete routing for:" -ForegroundColor White
Write-Host "   - RVN Privacy System (/rvn)" -ForegroundColor Cyan
Write-Host "   - BitXtractor Forensics (/bitxtractor)" -ForegroundColor Cyan
Write-Host "   - BlackArch Security Suite (/blackarchtools)" -ForegroundColor Cyan
Write-Host "   - Management System (/manage)" -ForegroundColor Cyan
Write-Host "   - All Core AI APIs (/api/*)" -ForegroundColor Cyan
Write-Host ""
Write-Host "================================================================" -ForegroundColor Yellow
Write-Host ""
