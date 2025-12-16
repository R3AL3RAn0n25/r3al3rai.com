# R3ÆLƎR Management System Desktop Launcher
# PowerShell script to launch the standalone desktop application

param(
    [switch]$InstallDeps,
    [switch]$Help
)

if ($Help) {
    Write-Host "R3ÆLƎR Desktop Application Launcher"
    Write-Host ""
    Write-Host "Usage: .\launch_desktop_app.ps1 [-InstallDeps] [-Help]"
    Write-Host ""
    Write-Host "Parameters:"
    Write-Host "  -InstallDeps    Install/update Python dependencies"
    Write-Host "  -Help          Show this help message"
    Write-Host ""
    exit 0
}

Write-Host "Starting R3ÆLƎR Management System Desktop Application..." -ForegroundColor Green
Write-Host ""

# Check Python installation
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8+ from https://python.org" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Install dependencies if requested or if not already installed
if ($InstallDeps -or -not (Test-Path "requirements_desktop.txt")) {
    Write-Host "Installing/updating Python dependencies..." -ForegroundColor Yellow
    try {
        pip install -r requirements_desktop.txt --quiet
        Write-Host "Dependencies installed successfully" -ForegroundColor Green
    } catch {
        Write-Host "Warning: Could not install dependencies automatically" -ForegroundColor Yellow
        Write-Host "Please run: pip install -r requirements_desktop.txt" -ForegroundColor Yellow
    }
}

# Check if main application file exists
if (-not (Test-Path "r3aler_desktop_app.py")) {
    Write-Host "ERROR: r3aler_desktop_app.py not found in current directory" -ForegroundColor Red
    Write-Host "Please ensure you're running this from the R3AL3R project directory" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Launch the desktop application
Write-Host "Launching R3ÆLƎR Desktop Application..." -ForegroundColor Green
Write-Host "Close this window to stop the application" -ForegroundColor Cyan
Write-Host ""

try {
    python r3aler_desktop_app.py
} catch {
    Write-Host "ERROR: Failed to launch application: $($_.Exception.Message)" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}