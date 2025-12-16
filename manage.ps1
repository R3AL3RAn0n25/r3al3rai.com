# R3ALER AI - System Management Script
# Provides quick access to all system operations

param(
    [string]$Action = "help"
)

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "              R3ALER AI - System Manager                   " -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

switch ($Action.ToLower()) {
    "start-windows" {
        Write-Host "Starting R3ALER AI (Windows mode)..." -ForegroundColor Blue
        & ".\scripts\windows\start-system.bat"
    }
    
    "start-wsl" {
        Write-Host "Starting R3ALER AI (WSL mode)..." -ForegroundColor Blue
        wsl chmod +x scripts/wsl/*.sh
        wsl ./scripts/wsl/start-wsl-simple.sh
    }
    
    "stop-wsl" {
        Write-Host "Stopping WSL services..." -ForegroundColor Yellow
        wsl ./scripts/wsl/stop-wsl-system.sh
    }
    
    "status-wsl" {
        Write-Host "Checking WSL status..." -ForegroundColor Blue
        wsl ./scripts/wsl/check-wsl-status.sh
    }
    
    "firewall" {
        Write-Host "Configuring Windows Firewall..." -ForegroundColor Yellow
        Write-Host "This requires Administrator privileges" -ForegroundColor Red
        Start-Process PowerShell -Verb RunAs -ArgumentList "-ExecutionPolicy Bypass -File scripts\windows\add-firewall-rules.ps1"
    }
    
    "wallet" {
        Write-Host "Launching Wallet Extractor..." -ForegroundColor Green
        Set-Location "Tools\tools"
        Write-Host "Available commands:" -ForegroundColor Yellow
        Write-Host "  python wallet_extractor.py --help" -ForegroundColor White
        Write-Host "  python wallet_extractor.py --check-deps --json" -ForegroundColor White
        Write-Host "  powershell -ExecutionPolicy Bypass -File .\xtractor.ps1 --help" -ForegroundColor White
    }
    
    "help" {
        Write-Host "R3ALER AI System Manager - Available Commands:" -ForegroundColor Green
        Write-Host ""
        Write-Host "System Startup:" -ForegroundColor Yellow
        Write-Host "  .\manage.ps1 start-windows  - Start using Windows/PowerShell" -ForegroundColor White
        Write-Host "  .\manage.ps1 start-wsl      - Start using WSL (recommended)" -ForegroundColor White
        Write-Host ""
        Write-Host "System Management:" -ForegroundColor Yellow
        Write-Host "  .\manage.ps1 stop-wsl       - Stop WSL services" -ForegroundColor White
        Write-Host "  .\manage.ps1 status-wsl     - Check WSL service status" -ForegroundColor White
        Write-Host "  .\manage.ps1 firewall       - Configure Windows Firewall" -ForegroundColor White
        Write-Host ""
        Write-Host "Tools:" -ForegroundColor Yellow
        Write-Host "  .\manage.ps1 wallet         - Access wallet extractor tools" -ForegroundColor White
        Write-Host ""
        Write-Host "Quick Start:" -ForegroundColor Cyan
        Write-Host "  1. .\manage.ps1 firewall    (run as admin, one time setup)" -ForegroundColor White
        Write-Host "  2. .\manage.ps1 start-wsl    (start the system)" -ForegroundColor White
        Write-Host "  3. Open: http://localhost:3000" -ForegroundColor White
    }
    
    default {
        Write-Host "Unknown action: $Action" -ForegroundColor Red
        Write-Host "Run: .\manage.ps1 help" -ForegroundColor Yellow
    }
}