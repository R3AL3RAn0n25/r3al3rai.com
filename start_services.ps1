# Start R3ÆLƎR AI Services
Write-Host "🚀 Starting R3ÆLƎR AI Services" -ForegroundColor Cyan

# Start Backend
Write-Host "`n[1/1] Starting Backend Server..." -ForegroundColor Yellow
Push-Location "application\Backend"
npm start
Pop-Location
