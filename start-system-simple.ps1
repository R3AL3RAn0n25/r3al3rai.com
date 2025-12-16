# R3ÆLƎR AI - Simple System Startup
# Starts all components using system Python and proper activation

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║           R3ÆLƎR AI - System Startup (Simple)             ║" -ForegroundColor Cyan  
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Activate virtual environment first
Write-Host "🔧 Activating Python virtual environment..." -ForegroundColor Yellow
& .\.venv\Scripts\Activate.ps1

# Step 1: Start Knowledge API
Write-Host ""
Write-Host "📚 [1/3] Starting Knowledge Base API..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-ExecutionPolicy", "Bypass", "-Command", "cd '$PWD'; .\.venv\Scripts\Activate.ps1; cd AI_Core_Worker; python knowledge_api.py" -WindowStyle Normal
Write-Host "    ✓ Knowledge API starting on http://localhost:5001" -ForegroundColor Green
Start-Sleep -Seconds 3

# Step 2: Start Droid API  
Write-Host ""
Write-Host "🤖 [2/3] Starting Droid API..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-ExecutionPolicy", "Bypass", "-Command", "cd '$PWD'; .\.venv\Scripts\Activate.ps1; cd application\Backend; python droid_api.py" -WindowStyle Normal
Write-Host "    ✓ Droid API starting on http://localhost:5002" -ForegroundColor Green
Start-Sleep -Seconds 3

# Step 3: Start Backend Server
Write-Host ""
Write-Host "🚀 [3/3] Starting Backend Server..." -ForegroundColor Yellow
$backendPath = "application\Backend"
if (Test-Path $backendPath) {
    Set-Location $backendPath
    
    # Check if node_modules exists
    if (-not (Test-Path "node_modules")) {
        Write-Host "    📦 Installing Node.js dependencies..." -ForegroundColor Yellow
        npm install
    }
    
    Write-Host "    ✓ Starting Node.js server..." -ForegroundColor Green
    Write-Host ""
    Write-Host "════════════════════════════════════════════════════════════" -ForegroundColor Gray
    Write-Host "✅ System Status:" -ForegroundColor Green
    Write-Host "   • Knowledge API:  http://localhost:5001" -ForegroundColor White
    Write-Host "   • Droid API:      http://localhost:5002" -ForegroundColor White  
    Write-Host "   • Backend:        http://localhost:3000" -ForegroundColor White
    Write-Host "════════════════════════════════════════════════════════════" -ForegroundColor Gray
    Write-Host ""
    npm start
} else {
    Write-Host "    ❌ Backend path not found: $backendPath" -ForegroundColor Red
    exit 1
}