# Install all BlackArch tools

Write-Host "Installing all BlackArch tools..." -ForegroundColor Cyan

# Get list of all tools
$response = Invoke-RestMethod -Uri "http://localhost:8081/api/tools" -Method GET
$tools = $response.tools

$installed = 0
$failed = 0

foreach ($tool in $tools) {
    $toolName = $tool.name
    
    # Skip if already installed
    if ($tool.installed -eq $true) {
        Write-Host "  Already installed: $toolName" -ForegroundColor Green
        $installed++
        continue
    }
    
    Write-Host "  Installing $toolName..." -ForegroundColor Yellow -NoNewline
    
    try {
        $result = Invoke-RestMethod -Uri "http://localhost:8081/api/install/$toolName" -Method POST -TimeoutSec 30
        
        if ($result.status -eq "success") {
            Write-Host " OK" -ForegroundColor Green
            $installed++
        } else {
            Write-Host " FAIL" -ForegroundColor Red
            $failed++
        }
    } catch {
        Write-Host " ERROR" -ForegroundColor Red
        $failed++
    }
    
    # Small delay to avoid overwhelming the server
    Start-Sleep -Milliseconds 100
}

Write-Host ""
Write-Host "Installation Summary:" -ForegroundColor Cyan
Write-Host "  Total tools: $($tools.Count)" -ForegroundColor White
Write-Host "  Installed: $installed" -ForegroundColor Green
Write-Host "  Failed: $failed" -ForegroundColor Red
Write-Host ""
Write-Host "All tools ready!" -ForegroundColor Green
