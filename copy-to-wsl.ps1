# Copy AI_Core_Worker to WSL2
Write-Host "Copying AI_Core_Worker to WSL2..." -ForegroundColor Cyan

wsl bash -c "sudo rm -rf /opt/r3aler-ai/AI_Core_Worker/*"
wsl bash -c "sudo cp -r '/mnt/c/Users/work8/OneDrive/Desktop/r3al3rai/New Folder 1/R3al3r-AI Main Working/R3aler-ai/R3aler-ai/AI_Core_Worker/'* /opt/r3aler-ai/AI_Core_Worker/"
wsl bash -c "sudo chown -R r3aler:r3aler /opt/r3aler-ai/AI_Core_Worker"

Write-Host ""
Write-Host "Verifying copy..." -ForegroundColor Cyan
wsl bash -c "sudo ls -lh /opt/r3aler-ai/AI_Core_Worker/run_*.py"

Write-Host ""
Write-Host "Code copied! Now run: wsl bash complete-wsl-deployment.sh" -ForegroundColor Green
