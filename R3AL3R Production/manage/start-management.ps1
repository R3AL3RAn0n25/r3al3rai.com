# R3ÆLƎR AI Management System Startup Script
# This script starts the management interface and API

Write-Host "R3ÆLƎR AI Management System" -ForegroundColor Magenta
Write-Host "===========================" -ForegroundColor Magenta
Write-Host ""

# Check if we're in the right directory
if (!(Test-Path "management_api.py")) {
    Write-Host "Error: management_api.py not found. Please run this script from the manage directory." -ForegroundColor Red
    exit 1
}

# Check if virtual environment exists
if (!(Test-Path ".venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv .venv
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Cyan
& ".venv\Scripts\Activate.ps1"

# Install requirements
Write-Host "Installing requirements..." -ForegroundColor Cyan
pip install -r requirements.txt

# Start the management API
Write-Host "Starting R3ÆLƎR AI Management API..." -ForegroundColor Green
Write-Host "Management interface will be available at: https://www.r3al3rai.com/manage/" -ForegroundColor Green
Write-Host "API endpoints available at: https://www.r3al3rai.com/api/" -ForegroundColor Green
Write-Host ""
Write-Host "Press Ctrl+C to stop the management system" -ForegroundColor Yellow
Write-Host ""

try {
    python management_api.py
} catch {
    Write-Host "Error starting management API: $_" -ForegroundColor Red
} finally {
    Write-Host "Management system stopped." -ForegroundColor Yellow
}