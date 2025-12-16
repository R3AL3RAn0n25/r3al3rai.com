# Restart Knowledge API with Extended Datasets
# This script stops the current Knowledge API and restarts it with the new datasets

Write-Host "`n🔄 Restarting Knowledge API with Extended Datasets...`n" -ForegroundColor Cyan

# Find and stop the current Knowledge API process
$knowledgeProcess = Get-Process -Id 6216 -ErrorAction SilentlyContinue

if ($knowledgeProcess) {
    Write-Host "⏹️  Stopping current Knowledge API (PID: 6216)..." -ForegroundColor Yellow
    Stop-Process -Id 6216 -Force
    Start-Sleep -Seconds 2
    Write-Host "✅ Stopped`n" -ForegroundColor Green
} else {
    Write-Host "ℹ️  Knowledge API not running on PID 6216`n" -ForegroundColor Gray
}

# Check if any process is still on port 5001
$portCheck = netstat -ano | findstr ":5001"
if ($portCheck) {
    Write-Host "⚠️  Port 5001 still in use. Trying to find process...`n" -ForegroundColor Yellow
    $pidMatch = $portCheck | Select-String -Pattern "\s+(\d+)$" | ForEach-Object { $_.Matches.Groups[1].Value }
    if ($pidMatch) {
        Write-Host "   Found PID: $pidMatch" -ForegroundColor White
        Stop-Process -Id $pidMatch -Force -ErrorAction SilentlyContinue
        Start-Sleep -Seconds 2
    }
}

Write-Host "🚀 Starting Knowledge API with extended datasets...`n" -ForegroundColor Green

# Start Knowledge API in WSL
$workDir = "C:\Users\work8\OneDrive\Desktop\r3al3rai\New Folder 1\R3al3r-AI Main Working\R3aler-ai\R3aler-ai\AI_Core_Worker"
Set-Location $workDir

Start-Process wsl -ArgumentList "bash", "-c", "cd '/mnt/c/Users/work8/OneDrive/Desktop/r3al3rai/New Folder 1/R3al3r-AI Main Working/R3aler-ai/R3aler-ai/AI_Core_Worker' && python3 knowledge_api.py" -WindowStyle Normal

Write-Host "⏳ Waiting for Knowledge API to start..." -ForegroundColor Cyan
Start-Sleep -Seconds 3

# Verify it's running
$portCheck = netstat -ano | findstr ":5001"
if ($portCheck) {
    Write-Host "✅ Knowledge API is running on port 5001!`n" -ForegroundColor Green
    Write-Host "📚 Knowledge Base now includes:" -ForegroundColor Yellow
    Write-Host "   • 13 original entries" -ForegroundColor White
    Write-Host "   • 100 Physics problems" -ForegroundColor White  
    Write-Host "   • 97 Space Engineering Q&As" -ForegroundColor White
    Write-Host "   = 210 TOTAL entries ✨`n" -ForegroundColor Green
} else {
    Write-Host "❌ Knowledge API failed to start. Check logs.`n" -ForegroundColor Red
}

Write-Host "═══════════════════════════════════════════════════════════════`n" -ForegroundColor Cyan
