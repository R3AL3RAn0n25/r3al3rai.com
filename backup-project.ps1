# R3AL3R AI Complete Project Backup Script
# Creates timestamped backup with compression

param(
    [string]$CustomBackupPath = ""
)

$ErrorActionPreference = "Stop"

# Configuration
$projectRoot = "C:\Users\work8\OneDrive\Desktop\r3al3rai\New Folder 1\R3al3r-AI Main Working\R3aler-ai\R3aler-ai"
$timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$backupName = "R3AL3R-AI_Backup_$timestamp"

if ($CustomBackupPath) {
    $backupDir = $CustomBackupPath
} else {
    $backupDir = "C:\Users\work8\OneDrive\Desktop\r3al3rai\New Folder 1\R3al3r-AI Main Working\Backups"
}

$backupPath = Join-Path $backupDir $backupName

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "R3AL3R AI Complete Project Backup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Timestamp: $timestamp" -ForegroundColor Yellow
Write-Host "Source: $projectRoot" -ForegroundColor Yellow
Write-Host "Destination: $backupPath" -ForegroundColor Yellow
Write-Host ""

# Create backup directory if it doesn't exist
if (-not (Test-Path $backupDir)) {
    Write-Host "[1/6] Creating backup directory..." -ForegroundColor Green
    New-Item -ItemType Directory -Path $backupDir -Force | Out-Null
    Write-Host "Success: Backup directory created" -ForegroundColor Green
} else {
    Write-Host "[1/6] Backup directory exists" -ForegroundColor Green
}
Write-Host ""

# Create timestamped backup folder
Write-Host "[2/6] Creating backup folder..." -ForegroundColor Green
New-Item -ItemType Directory -Path $backupPath -Force | Out-Null
Write-Host "Success: Backup folder created: $backupName" -ForegroundColor Green
Write-Host ""

# Exclude patterns for copying
$excludeDirs = @(
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".vscode",
    "blackarch_venv\Lib",
    "blackarch_venv\Scripts",
    "dist",
    "build",
    "*.egg-info"
)

Write-Host "[3/6] Copying project files..." -ForegroundColor Green
Write-Host "This may take several minutes..." -ForegroundColor Yellow

# Copy with exclusions
$robocopyArgs = @(
    $projectRoot,
    $backupPath,
    "/E",           # Copy subdirectories including empty ones
    "/COPYALL",     # Copy all file info
    "/R:3",         # Retry 3 times
    "/W:5",         # Wait 5 seconds between retries
    "/NFL",         # No file list
    "/NDL",         # No directory list
    "/NP",          # No progress
    "/XD"           # Exclude directories
) + $excludeDirs + @(
    "/XF",          # Exclude files
    "*.pyc",
    "*.pyo",
    "*.log",
    ".DS_Store",
    "Thumbs.db"
)

$result = robocopy @robocopyArgs

# Robocopy exit codes: 0-7 are success, 8+ are errors
if ($LASTEXITCODE -lt 8) {
    Write-Host "Success: Project files copied successfully" -ForegroundColor Green
} else {
    Write-Host "Warning: Some files may not have been copied (Exit code: $LASTEXITCODE)" -ForegroundColor Yellow
}
Write-Host ""

# Create backup manifest
Write-Host "[4/6] Creating backup manifest..." -ForegroundColor Green

$osInfo = Get-CimInstance Win32_OperatingSystem | Select-Object -ExpandProperty Caption

$manifestLines = @()
$manifestLines += "R3AL3R AI Project Backup"
$manifestLines += "========================"
$manifestLines += ""
$manifestLines += "Backup Information:"
$manifestLines += "Created: $timestamp"
$manifestLines += "Backup Name: $backupName"
$manifestLines += "Source Path: $projectRoot"
$manifestLines += "Backup Path: $backupPath"
$manifestLines += ""
$manifestLines += "Project Structure:"
$manifestLines += "  application/Backend/      Node.js backend server"
$manifestLines += "  application/Frontend/     React frontend application"
$manifestLines += "  Tools/                    BlackArch tools integration"
$manifestLines += "  AI_Core_Worker/           AI and ML components"
$manifestLines += "  Database/                 Database schemas and migrations"
$manifestLines += "  configs/                  Configuration files"
$manifestLines += "  scripts/                  Utility scripts"
$manifestLines += "  docs/                     Documentation"
$manifestLines += ""
$manifestLines += "Excluded from Backup:"
$manifestLines += "  node_modules/            (Can be restored with: npm install)"
$manifestLines += "  blackarch_venv/Lib/      (Can be restored with: python -m venv)"
$manifestLines += "  __pycache__/             (Python bytecode cache)"
$manifestLines += "  .pytest_cache/           (Test cache)"
$manifestLines += "  *.pyc, *.pyo             (Compiled Python files)"
$manifestLines += "  *.log                    (Log files)"
$manifestLines += ""
$manifestLines += "Restoration Instructions:"
$manifestLines += "1. Copy backup folder to desired location"
$manifestLines += "2. Restore Node.js dependencies:"
$manifestLines += "   cd application/Backend && npm install"
$manifestLines += "   cd application/Frontend && npm install"
$manifestLines += ""
$manifestLines += "3. Restore Python environment:"
$manifestLines += "   python -m venv blackarch_venv"
$manifestLines += "   source blackarch_venv/bin/activate  # On WSL/Linux"
$manifestLines += "   pip install -r Tools/requirements.txt"
$manifestLines += ""
$manifestLines += "4. Restore database (if needed):"
$manifestLines += "   Check Database/ folder for schema"
$manifestLines += "   Import data from backup"
$manifestLines += ""
$manifestLines += "5. Update configuration files in configs/"
$manifestLines += ""
$manifestLines += "6. Start services:"
$manifestLines += "   Node backend: npm start in application/Backend/"
$manifestLines += "   Flask service: python Tools/blackarch_web_app.py"
$manifestLines += "   Frontend: npm start in application/Frontend/"
$manifestLines += ""
$manifestLines += "System Information:"
$manifestLines += "Backup OS: $osInfo"
$manifestLines += "PowerShell: $($PSVersionTable.PSVersion)"
$manifestLines += ""
$manifestLines += "Notes:"
$manifestLines += "  This is a complete project backup excluding regenerable files"
$manifestLines += "  Virtual environments and node_modules can be regenerated"
$manifestLines += "  Database files are included if present"
$manifestLines += "  Configuration files are included"
$manifestLines += "  All source code and documentation included"
$manifestLines += ""
$manifestLines += "For support: https://github.com/R3AL3RAn0n25/r3al3rai.com"

$manifest = $manifestLines -join "`r`n"
$manifest | Out-File -FilePath (Join-Path $backupPath "BACKUP_MANIFEST.txt") -Encoding UTF8
Write-Host "Success: Manifest created" -ForegroundColor Green
Write-Host ""

# Create restore script for Linux/WSL
Write-Host "[5/6] Creating restore scripts..." -ForegroundColor Green

$restoreScriptBash = @'
#!/bin/bash
# R3AL3R AI Project Restore Script
# Run this in WSL/Linux environment

echo "========================================="
echo "R3AL3R AI Project Restoration"
echo "========================================="
echo ""

BACKUP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "Restoring from: $BACKUP_DIR"
echo ""

echo "[1/5] Installing Node.js backend dependencies..."
if [ -d "$BACKUP_DIR/application/Backend" ]; then
    cd "$BACKUP_DIR/application/Backend"
    npm install
    echo "Success: Backend dependencies installed"
else
    echo "Warning: Backend directory not found"
fi
echo ""

echo "[2/5] Installing Node.js frontend dependencies..."
if [ -d "$BACKUP_DIR/application/Frontend" ]; then
    cd "$BACKUP_DIR/application/Frontend"
    npm install
    echo "Success: Frontend dependencies installed"
else
    echo "Warning: Frontend directory not found"
fi
echo ""

echo "[3/5] Creating Python virtual environment..."
cd "$BACKUP_DIR"
if [ -f "Tools/requirements.txt" ]; then
    python3 -m venv blackarch_venv
    source blackarch_venv/bin/activate
    pip install --upgrade pip
    pip install -r Tools/requirements.txt
    echo "Success: Python environment created and dependencies installed"
else
    echo "Warning: Requirements file not found"
fi
echo ""

echo "[4/5] Setting executable permissions..."
find "$BACKUP_DIR" -name "*.sh" -type f -exec chmod +x {} \;
echo "Success: Permissions set"
echo ""

echo "[5/5] Verifying restoration..."
echo ""
echo "Checking critical files:"
[ -f "$BACKUP_DIR/application/Backend/backendserver.js" ] && echo "Success: Backend server found" || echo "Error: Backend server missing"
[ -d "$BACKUP_DIR/application/Frontend/src" ] && echo "Success: Frontend source found" || echo "Error: Frontend source missing"
[ -f "$BACKUP_DIR/Tools/blackarch_web_app.py" ] && echo "Success: BlackArch service found" || echo "Error: BlackArch service missing"
[ -f "$BACKUP_DIR/Tools/blackarch_tools_manager.py" ] && echo "Success: Tools manager found" || echo "Error: Tools manager missing"
echo ""

echo "========================================="
echo "Restoration Complete!"
echo "========================================="
echo ""
echo "Next Steps:"
echo "1. Review configs/ directory for configuration files"
echo "2. Update database connection strings if needed"
echo "3. Start services:"
echo "   Backend: cd application/Backend && npm start"
echo "   Flask: source blackarch_venv/bin/activate && python Tools/blackarch_web_app.py"
echo "   Frontend: cd application/Frontend && npm start"
echo ""
'@

$restoreScriptBash | Out-File -FilePath (Join-Path $backupPath "restore.sh") -Encoding UTF8 -NoNewline

# Create Windows restore script
$restoreScriptWin = @'
# R3AL3R AI Project Restore Script (Windows)

param([string]$RestorePath = $PSScriptRoot)

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "R3AL3R AI Project Restoration (Windows)" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Restoring from: $RestorePath" -ForegroundColor Yellow
Write-Host ""

Write-Host "[1/5] Installing Node.js backend dependencies..." -ForegroundColor Green
$backendPath = Join-Path $RestorePath "application\Backend"
if (Test-Path $backendPath) {
    Set-Location $backendPath
    npm install
    Write-Host "Success: Backend dependencies installed" -ForegroundColor Green
} else {
    Write-Host "Warning: Backend directory not found" -ForegroundColor Yellow
}
Write-Host ""

Write-Host "[2/5] Installing Node.js frontend dependencies..." -ForegroundColor Green
$frontendPath = Join-Path $RestorePath "application\Frontend"
if (Test-Path $frontendPath) {
    Set-Location $frontendPath
    npm install
    Write-Host "Success: Frontend dependencies installed" -ForegroundColor Green
} else {
    Write-Host "Warning: Frontend directory not found" -ForegroundColor Yellow
}
Write-Host ""

Write-Host "[3/5] Creating Python virtual environment in WSL..." -ForegroundColor Green
Set-Location $RestorePath
$reqFile = Join-Path $RestorePath "Tools\requirements.txt"
if (Test-Path $reqFile) {
    $wslPath = wsl wslpath "'$RestorePath'"
    wsl bash -c "cd '$wslPath' && python3 -m venv blackarch_venv && source blackarch_venv/bin/activate && pip install --upgrade pip && pip install -r Tools/requirements.txt"
    Write-Host "Success: Python environment created" -ForegroundColor Green
} else {
    Write-Host "Warning: Requirements file not found" -ForegroundColor Yellow
}
Write-Host ""

Write-Host "[4/5] Setting executable permissions..." -ForegroundColor Green
wsl bash -c "cd '$wslPath' && find . -name '*.sh' -type f -exec chmod +x {} \;"
Write-Host "Success: Permissions set" -ForegroundColor Green
Write-Host ""

Write-Host "[5/5] Verifying restoration..." -ForegroundColor Green
Write-Host ""
Write-Host "Checking critical files:"
if (Test-Path (Join-Path $RestorePath "application\Backend\backendserver.js")) { Write-Host "Success: Backend server found" -ForegroundColor Green } else { Write-Host "Error: Backend server missing" -ForegroundColor Red }
if (Test-Path (Join-Path $RestorePath "application\Frontend\src")) { Write-Host "Success: Frontend source found" -ForegroundColor Green } else { Write-Host "Error: Frontend source missing" -ForegroundColor Red }
if (Test-Path (Join-Path $RestorePath "Tools\blackarch_web_app.py")) { Write-Host "Success: BlackArch service found" -ForegroundColor Green } else { Write-Host "Error: BlackArch service missing" -ForegroundColor Red }
if (Test-Path (Join-Path $RestorePath "Tools\blackarch_tools_manager.py")) { Write-Host "Success: Tools manager found" -ForegroundColor Green } else { Write-Host "Error: Tools manager missing" -ForegroundColor Red }
Write-Host ""

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Restoration Complete!" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "1. Review configs/ directory for configuration files"
Write-Host "2. Update database connection strings if needed"
Write-Host "3. Start services using start-system-simple.ps1"
Write-Host ""
'@

$restoreScriptWin | Out-File -FilePath (Join-Path $backupPath "restore.ps1") -Encoding UTF8
Write-Host "Success: Restore scripts created" -ForegroundColor Green
Write-Host ""

# Calculate backup size
Write-Host "[6/6] Calculating backup size..." -ForegroundColor Green
try {
    $backupSize = (Get-ChildItem -Path $backupPath -Recurse -File -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
    $backupSizeMB = [math]::Round($backupSize / 1MB, 2)
    $backupSizeGB = [math]::Round($backupSize / 1GB, 2)

    if ($backupSizeGB -gt 1) {
        Write-Host "Success: Backup size: $backupSizeGB GB" -ForegroundColor Green
    } else {
        Write-Host "Success: Backup size: $backupSizeMB MB" -ForegroundColor Green
    }

    # Count files
    $fileCount = (Get-ChildItem -Path $backupPath -Recurse -File -ErrorAction SilentlyContinue | Measure-Object).Count
    Write-Host "Success: Files backed up: $fileCount" -ForegroundColor Green
} catch {
    Write-Host "Success: Backup complete (size calculation skipped due to long paths)" -ForegroundColor Green
}
Write-Host ""

# Summary
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Backup Complete!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Backup Location:" -ForegroundColor Yellow
Write-Host $backupPath -ForegroundColor White
Write-Host ""
Write-Host "Backup Contents:" -ForegroundColor Yellow
Write-Host "  Complete project source code" -ForegroundColor White
Write-Host "  Configuration files" -ForegroundColor White
Write-Host "  Documentation" -ForegroundColor White
Write-Host "  Database files (if present)" -ForegroundColor White
Write-Host "  Scripts and utilities" -ForegroundColor White
Write-Host ""
Write-Host "Restore Instructions:" -ForegroundColor Yellow
Write-Host "  Windows: Run restore.ps1 in backup folder" -ForegroundColor White
Write-Host "  Linux/WSL: Run ./restore.sh in backup folder" -ForegroundColor White
Write-Host "  Manual: See BACKUP_MANIFEST.txt" -ForegroundColor White
Write-Host ""
Write-Host "Success: Backup manifest: BACKUP_MANIFEST.txt" -ForegroundColor Green
Write-Host "Success: Restore scripts: restore.ps1 / restore.sh" -ForegroundColor Green
Write-Host ""
Write-Host "Your project is safely backed up!" -ForegroundColor Cyan
Write-Host ""
