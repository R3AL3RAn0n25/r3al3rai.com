# R3ALER AI - WSL System Launcher
# This script launches the WSL version with better Linux compatibility

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║             R3ALER AI - WSL System Launcher               ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

Write-Host "🐧 Launching R3ALER AI in WSL environment..." -ForegroundColor Yellow
Write-Host ""

# Check if WSL is available
try {
    $wslCheck = wsl --status 2>$null
    Write-Host "✓ WSL is available" -ForegroundColor Green
} catch {
    Write-Host "❌ WSL is not available or not installed" -ForegroundColor Red
    Write-Host "Please install WSL2 with Ubuntu to use this launcher" -ForegroundColor Yellow
    pause
    exit 1
}

Write-Host "🚀 Starting R3ALER AI services in WSL..." -ForegroundColor Blue

# Make scripts executable and run
wsl chmod +x scripts/wsl/*.sh
wsl ./scripts/wsl/start-wsl-simple.sh

Write-Host ""
Write-Host "✅ WSL startup completed!" -ForegroundColor Green
Write-Host ""
Write-Host "Access the application at:" -ForegroundColor Cyan
Write-Host "  • Main App: http://localhost:3000" -ForegroundColor White
Write-Host "  • Knowledge API: http://localhost:5001" -ForegroundColor White
Write-Host "  • Droid API: http://localhost:5002" -ForegroundColor White
Write-Host ""
Write-Host "Management commands:" -ForegroundColor Yellow
Write-Host "  • Check status: wsl ./scripts/wsl/check-wsl-status.sh" -ForegroundColor White
Write-Host "  • Stop system: wsl ./scripts/wsl/stop-wsl-system.sh" -ForegroundColor White
Write-Host ""