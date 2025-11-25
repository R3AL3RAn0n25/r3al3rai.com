# R3ÆLƎR AI Management System Deployment Script
# This script deploys the management interface to the production environment

param(
    [switch]$Force,
    [switch]$SkipNginxReload
)

Write-Host "R3ÆLƎR AI Management System Deployment" -ForegroundColor Magenta
Write-Host "=====================================" -ForegroundColor Magenta
Write-Host ""

# Configuration
$nginxWebRoot = "/var/www/r3al3rai.com"
$manageSource = "$PSScriptRoot"
$manageDest = "$nginxWebRoot/manage"

# Check if running as administrator (for nginx reload)
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (!$isAdmin -and !$SkipNginxReload) {
    Write-Host "Warning: Not running as administrator. Nginx reload will be skipped." -ForegroundColor Yellow
    Write-Host "Run this script as administrator to automatically reload nginx configuration." -ForegroundColor Yellow
    $SkipNginxReload = $true
}

# Check if management directory exists
if (!(Test-Path $manageSource)) {
    Write-Host "Error: Management source directory not found: $manageSource" -ForegroundColor Red
    exit 1
}

# Create destination directory if it doesn't exist
if (!(Test-Path $nginxWebRoot)) {
    Write-Host "Creating nginx web root directory..." -ForegroundColor Cyan
    New-Item -ItemType Directory -Path $nginxWebRoot -Force | Out-Null
}

if (!(Test-Path $manageDest)) {
    Write-Host "Creating management directory..." -ForegroundColor Cyan
    New-Item -ItemType Directory -Path $manageDest -Force | Out-Null
} elseif (!$Force) {
    $response = Read-Host "Management directory already exists. Overwrite? (y/N)"
    if ($response -ne 'y' -and $response -ne 'Y') {
        Write-Host "Deployment cancelled." -ForegroundColor Yellow
        exit 0
    }
}

# Copy management files
Write-Host "Copying management files..." -ForegroundColor Cyan
try {
    # Copy HTML, JS, CSS files
    Copy-Item "$manageSource/index.html" -Destination $manageDest -Force
    Copy-Item "$manageSource/management_api.py" -Destination $manageDest -Force
    Copy-Item "$manageSource/requirements.txt" -Destination $manageDest -Force
    Copy-Item "$manageSource/start-management.ps1" -Destination $manageDest -Force

    # Create necessary directories
    $uploadsDir = "$manageDest/uploads"
    $datasetsDir = "$manageDest/uploads/datasets"
    $upgradesDir = "$manageDest/uploads/upgrades"
    $logsDir = "$manageDest/logs"

    New-Item -ItemType Directory -Path $uploadsDir -Force | Out-Null
    New-Item -ItemType Directory -Path $datasetsDir -Force | Out-Null
    New-Item -ItemType Directory -Path $upgradesDir -Force | Out-Null
    New-Item -ItemType Directory -Path $logsDir -Force | Out-Null

    Write-Host "Management files deployed successfully!" -ForegroundColor Green
} catch {
    Write-Host "Error copying files: $_" -ForegroundColor Red
    exit 1
}

# Reload nginx configuration
if (!$SkipNginxReload) {
    Write-Host "Reloading nginx configuration..." -ForegroundColor Cyan
    try {
        # Test configuration first
        $testResult = & nginx -t 2>&1
        if ($LASTEXITCODE -eq 0) {
            # Reload configuration
            & nginx -s reload
            if ($LASTEXITCODE -eq 0) {
                Write-Host "Nginx configuration reloaded successfully!" -ForegroundColor Green
            } else {
                Write-Host "Error reloading nginx configuration!" -ForegroundColor Red
                exit 1
            }
        } else {
            Write-Host "Nginx configuration test failed:" -ForegroundColor Red
            Write-Host $testResult -ForegroundColor Red
            exit 1
        }
    } catch {
        Write-Host "Error testing/reloading nginx: $_" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "Skipping nginx reload. Remember to reload nginx manually:" -ForegroundColor Yellow
    Write-Host "  sudo nginx -t && sudo nginx -s reload" -ForegroundColor Yellow
}

# Setup Python virtual environment and install dependencies
Write-Host "Setting up Python environment..." -ForegroundColor Cyan
try {
    Push-Location $manageDest

    # Create virtual environment if it doesn't exist
    if (!(Test-Path ".venv")) {
        Write-Host "Creating virtual environment..." -ForegroundColor Cyan
        & python -m venv .venv
    }

    # Activate and install requirements
    Write-Host "Installing Python dependencies..." -ForegroundColor Cyan
    & ".venv\Scripts\Activate.ps1"
    & pip install -r requirements.txt

    Pop-Location
    Write-Host "Python environment setup complete!" -ForegroundColor Green
} catch {
    Write-Host "Error setting up Python environment: $_" -ForegroundColor Red
    Pop-Location
    exit 1
}

Write-Host ""
Write-Host "Deployment Summary:" -ForegroundColor Green
Write-Host "- Management interface: https://www.r3al3rai.com/manage/" -ForegroundColor White
Write-Host "- Management API: https://www.r3al3rai.com/api/" -ForegroundColor White
Write-Host "- Files deployed to: $manageDest" -ForegroundColor White
Write-Host ""
Write-Host "To start the management system:" -ForegroundColor Cyan
Write-Host "  cd '$manageDest'" -ForegroundColor White
Write-Host "  .\start-management.ps1" -ForegroundColor White
Write-Host ""
Write-Host "The management system provides:" -ForegroundColor Cyan
Write-Host "- Real-time system monitoring" -ForegroundColor White
Write-Host "- Service control (start/stop/restart)" -ForegroundColor White
Write-Host "- Log viewing and reports" -ForegroundColor White
Write-Host "- AI system details and testing" -ForegroundColor White
Write-Host "- Dataset upload and management" -ForegroundColor White
Write-Host "- System upgrades" -ForegroundColor White
Write-Host ""
Write-Host "Deployment completed successfully!" -ForegroundColor Green