# R3AL3R AI - Start All Services
# Launches each service in its own dedicated terminal window

$ErrorActionPreference = "Continue"
$ProjectRoot = "C:\Users\work8\OneDrive\Desktop\r3al3rai\New Folder 1\R3al3r-AI Main Working\R3aler-ai\R3aler-ai"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  R3AL3R AI - Starting All Services" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Function to start service in new terminal
function Start-ServiceInTerminal {
    $ServiceName = $args[0]
    $Command = $args[1]
    $Port = $args[2]
    Write-Host "Starting $ServiceName (Port $Port)..." -ForegroundColor Yellow
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "Write-Host ''; Write-Host '========================================' -ForegroundColor Cyan; Write-Host '  $ServiceName' -ForegroundColor Cyan; Write-Host '  Port: $Port' -ForegroundColor Green; Write-Host '========================================' -ForegroundColor Cyan; Write-Host ''; cd '$ProjectRoot'; .\.venv\Scripts\Activate.ps1; $Command"
    Start-Sleep -Seconds 2
    Write-Host "  ✓ $ServiceName terminal opened" -ForegroundColor Green
}
# Start BlackArch API
Start-ServiceInTerminal "BlackArch API" "python Tools/blackarch_web_app.py" 5003

# Start Knowledge API
Start-ServiceInTerminal "Knowledge API" "python AI_Core_Worker/knowledge_api.py" 5001

# Start Backend/BitXtractor
Start-ServiceInTerminal "Backend/BitXtractor" "python application/Backend/app.py" 3002

# Start Intelligence API
Start-ServiceInTerminal "Intelligence API" "python AI_Core_Worker/intelligence_layer.py" 5010

# Start BitXtractor Service (WSL mode)
Write-Host "Starting BitXtractor Service (WSL Mode - Port 3002)..." -ForegroundColor Yellow

Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-Command",
    "Write-Host ''; Write-Host '========================================' -ForegroundColor Cyan; Write-Host '  BitXtractor Service (WSL)' -ForegroundColor Cyan; Write-Host '  Port: 3002' -ForegroundColor Green; Write-Host '========================================' -ForegroundColor Cyan; Write-Host ''; cd '$ProjectRoot'; .\start_bitxtractor_service.ps1 -WSL"
)

Start-Sleep -Seconds 2
Write-Host "  ✓ BitXtractor Service terminal opened" -ForegroundColor Green

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  All Services Started!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Services Running:" -ForegroundColor Yellow
Write-Host "  • BlackArch API         - http://localhost:5003" -ForegroundColor White
Write-Host "  • Knowledge API         - http://localhost:5001" -ForegroundColor White
Write-Host "  • Backend/BitXtractor   - http://localhost:3002" -ForegroundColor White
Write-Host "  • Intelligence API      - http://localhost:5010" -ForegroundColor White
Write-Host "  • BitXtractor Service   - http://localhost:3002" -ForegroundColor White
Write-Host ""
Write-Host "Press any key to exit this launcher..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
