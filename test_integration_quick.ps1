# R3ÆLƎR AI - Quick Integration Test
# Tests Storage Facility → Knowledge API → Backend flow
# Run this in a SEPARATE terminal to avoid killing services!

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║          R3ÆLƎR AI - Quick Integration Test                ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Test 1: Storage Facility
Write-Host "🏢 [1/4] Testing Storage Facility..." -ForegroundColor Yellow
try {
    $sfStatus = Invoke-RestMethod -Uri "http://localhost:5003/api/facility/status" -TimeoutSec 5
    Write-Host "    ✅ Status: $($sfStatus.status)" -ForegroundColor Green
    Write-Host "    ✅ Total Entries: $($sfStatus.total_entries)" -ForegroundColor Green
    Write-Host "    ✅ Units: $($sfStatus.total_units)" -ForegroundColor Green
} catch {
    Write-Host "    ❌ Storage Facility not running on port 5003" -ForegroundColor Red
    Write-Host "    Run: .\start_storage_facility.ps1" -ForegroundColor Yellow
}

# Test 2: Knowledge API Health
Write-Host ""
Write-Host "📚 [2/4] Testing Knowledge API..." -ForegroundColor Yellow
try {
    $kbHealth = Invoke-RestMethod -Uri "http://localhost:5001/health" -TimeoutSec 5
    Write-Host "    ✅ Status: $($kbHealth.status)" -ForegroundColor Green
    Write-Host "    ✅ Storage Connected: $($kbHealth.storage_facility.connected)" -ForegroundColor Green
    Write-Host "    ✅ Total Entries: $($kbHealth.storage_facility.total_entries)" -ForegroundColor Green
} catch {
    Write-Host "    ❌ Knowledge API not running on port 5001" -ForegroundColor Red
    Write-Host "    The API should auto-start with the Storage Facility" -ForegroundColor Yellow
}

# Test 3: Crypto Knowledge Search
Write-Host ""
Write-Host "🔍 [3/4] Testing Crypto Knowledge Search..." -ForegroundColor Yellow
try {
    $searchBody = @{
        query = "Bitcoin wallet.dat"
        maxPassages = 3
    } | ConvertTo-Json
    
    $searchResult = Invoke-RestMethod -Uri "http://localhost:5001/api/kb/search" `
        -Method Post `
        -Body $searchBody `
        -ContentType "application/json" `
        -TimeoutSec 10
    
    $usingSF = $searchResult.used_storage_facility
    $resultsCount = $searchResult.local_results.Count
    
    if ($usingSF) {
        Write-Host "    ✅ Using Storage Facility: YES" -ForegroundColor Green
        Write-Host "    ✅ Results Found: $resultsCount" -ForegroundColor Green
        
        if ($resultsCount -gt 0) {
            Write-Host ""
            Write-Host "    📄 Sample Result:" -ForegroundColor Cyan
            $firstResult = $searchResult.local_results[0]
            Write-Host "       Topic: $($firstResult.topic)" -ForegroundColor White
            Write-Host "       Category: $($firstResult.category)" -ForegroundColor White
            Write-Host "       Unit: $($firstResult.unit)" -ForegroundColor White
            Write-Host "       Relevance: $([math]::Round($firstResult.relevance, 4))" -ForegroundColor White
        }
    } else {
        Write-Host "    ⚠️  Using Fallback Mode (not Storage Facility)" -ForegroundColor Yellow
        Write-Host "    Check if Storage Facility is running properly" -ForegroundColor Yellow
    }
} catch {
    Write-Host "    ❌ Search failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 4: Backend Server
Write-Host ""
Write-Host "🚀 [4/4] Testing Backend Server..." -ForegroundColor Yellow
try {
    $backendStatus = Invoke-RestMethod -Uri "http://localhost:3000/api/status" -TimeoutSec 5
    Write-Host "    ✅ Backend is running" -ForegroundColor Green
} catch {
    Write-Host "    ⚠️  Backend not running on port 3000" -ForegroundColor Yellow
    Write-Host "    Run: .\start-complete-system-fixed.ps1" -ForegroundColor Yellow
}

# Summary
Write-Host ""
Write-Host "════════════════════════════════════════════════════════════" -ForegroundColor Gray
Write-Host "✅ Integration Test Complete!" -ForegroundColor Green
Write-Host "════════════════════════════════════════════════════════════" -ForegroundColor Gray
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "  1. Ensure all services are green (✅)" -ForegroundColor White
Write-Host "  2. If Storage Facility shows fallback, restart Knowledge API" -ForegroundColor White
Write-Host "  3. Test with: python test_end_to_end.py" -ForegroundColor White
Write-Host ""
Write-Host "Press Enter to exit..." -ForegroundColor Gray
Read-Host
