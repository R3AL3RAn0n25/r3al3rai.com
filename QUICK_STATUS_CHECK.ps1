# R3ÆLƎR AI - Quick Status Check
# Verifies all services are running and accessible

$services = @(
    @{ Name = "PostgreSQL"; Port = 5432; Type = "Database" }
    @{ Name = "Backend"; Port = 3000; Type = "Node.js" }
    @{ Name = "Frontend"; Port = 5173; Type = "Vite" }
    @{ Name = "Knowledge API"; Port = 5004; Type = "Python" }
    @{ Name = "Droid API"; Port = 5005; Type = "Python" }
    @{ Name = "Storage Facility"; Port = 3003; Type = "Python" }
)

Write-Host "`n" -ForegroundColor Cyan
Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║         R3ÆLƎR AI - SYSTEM STATUS CHECK                   ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

$running = 0
$stopped = 0

foreach ($service in $services) {
    $port = $service.Port
    $name = $service.Name
    $type = $service.Type
    
    try {
        $connection = New-Object System.Net.Sockets.TcpClient
        $connection.Connect("localhost", $port)
        $connection.Close()
        
        Write-Host "✓ $name ($type) - Port $port" -ForegroundColor Green
        $running++
    }
    catch {
        Write-Host "✗ $name ($type) - Port $port" -ForegroundColor Red
        $stopped++
    }
}

Write-Host ""
Write-Host "Summary: $running running, $stopped stopped" -ForegroundColor Yellow
Write-Host ""

# Test API endpoints if backend is running
if ($running -gt 0) {
    Write-Host "Testing API Endpoints..." -ForegroundColor Cyan
    Write-Host ""
    
    try {
        $health = Invoke-RestMethod -Uri "http://localhost:3000/api/health" -TimeoutSec 5
        Write-Host "✓ Backend Health: OK" -ForegroundColor Green
        Write-Host "  - Database: $(if ($health.db.ok) { 'Connected' } else { 'Disconnected' })" -ForegroundColor Yellow
        Write-Host "  - Memory: $($health.node.rss_mb)MB" -ForegroundColor Yellow
    }
    catch {
        Write-Host "✗ Backend Health: Failed" -ForegroundColor Red
    }
    
    try {
        $kb_health = Invoke-RestMethod -Uri "http://localhost:5004/health" -TimeoutSec 5
        Write-Host "✓ Knowledge API: OK" -ForegroundColor Green
        Write-Host "  - Storage Facility: $(if ($kb_health.storage_facility.connected) { 'Connected' } else { 'Disconnected' })" -ForegroundColor Yellow
        Write-Host "  - Total Entries: $($kb_health.storage_facility.total_entries)" -ForegroundColor Yellow
    }
    catch {
        Write-Host "✗ Knowledge API: Failed" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

if ($stopped -eq 0) {
    Write-Host "✓ All systems operational!" -ForegroundColor Green
}
else {
    Write-Host "⚠ Some services are not running. Start them with:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  Backend:  cd application/Backend && npm start" -ForegroundColor Yellow
    Write-Host "  Frontend: cd application/Frontend && npm run dev" -ForegroundColor Yellow
    Write-Host "  Knowledge API: python AI_Core_Worker/knowledge_api.py" -ForegroundColor Yellow
}

Write-Host ""
