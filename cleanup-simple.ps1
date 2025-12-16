# R3ALER AI Workspace Cleanup Script - Simple Version
$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor White
Write-Host "║             R3ALER AI - Workspace Cleanup                 ║" -ForegroundColor White  
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor White
Write-Host ""

$workspaceRoot = Get-Location
$archiveDir = "$workspaceRoot\.archive"
$docsDir = "$workspaceRoot\docs"

# Create directories
if (!(Test-Path $archiveDir)) {
    New-Item -ItemType Directory -Path $archiveDir -Force | Out-Null
}
if (!(Test-Path $docsDir)) {
    New-Item -ItemType Directory -Path $docsDir -Force | Out-Null
}

Write-Host "🧹 Starting workspace cleanup..." -ForegroundColor Blue
Write-Host ""

# Files to keep in root
$keepInRoot = @(
    ".env",
    ".env.example", 
    ".gitignore",
    "README.md",
    "QUICK_REFERENCE.md",
    "SYSTEMD_MANAGEMENT.md",
    "install-services-simple.sh",
    "cleanup-workspace-fixed.ps1"
)

Write-Host "📁 Moving documentation files..." -ForegroundColor Yellow

# Move documentation files to docs
Get-ChildItem -Path $workspaceRoot -Filter "*.md" | Where-Object { 
    $_.Name -notin $keepInRoot 
} | ForEach-Object {
    Write-Host "  Moving $($_.Name) to docs/" -ForegroundColor Gray
    Move-Item $_.FullName "$docsDir\$($_.Name)" -Force
}

Write-Host ""
Write-Host "📦 Archiving old directories..." -ForegroundColor Yellow

# Archive old directories
$dirsToArchive = @(
    "unused",
    "deploy-package", 
    "dictionaries",
    "icons",
    "services",
    "server",
    ".bak_stash"
)

foreach ($dir in $dirsToArchive) {
    $dirPath = Join-Path $workspaceRoot $dir
    if (Test-Path $dirPath) {
        Write-Host "  Archiving directory: $dir" -ForegroundColor Gray
        Move-Item $dirPath "$archiveDir\$dir" -Force
    }
}

# Handle R&D Blueprints separately (special characters)
$rdDir = Join-Path $workspaceRoot "R&D Blueprints"
if (Test-Path $rdDir) {
    Write-Host "  Archiving directory: R&D Blueprints" -ForegroundColor Gray
    Move-Item $rdDir "$archiveDir\R&D Blueprints" -Force
}

Write-Host ""
Write-Host "📦 Archiving old script files..." -ForegroundColor Yellow

# Archive old scripts
$scriptPatterns = @("*.ps1", "*.sh", "*.bat")
foreach ($pattern in $scriptPatterns) {
    Get-ChildItem -Path $workspaceRoot -Filter $pattern | Where-Object {
        $_.Name -notin $keepInRoot
    } | ForEach-Object {
        Write-Host "  Archiving script: $($_.Name)" -ForegroundColor Gray
        Move-Item $_.FullName "$archiveDir\$($_.Name)" -Force
    }
}

# Archive old Python/JS files in root
$codeFiles = @("*.py", "*.js", "*.tsx")
foreach ($pattern in $codeFiles) {
    Get-ChildItem -Path $workspaceRoot -Filter $pattern | ForEach-Object {
        Write-Host "  Archiving code file: $($_.Name)" -ForegroundColor Gray
        Move-Item $_.FullName "$archiveDir\$($_.Name)" -Force
    }
}

Write-Host ""
Write-Host "🧹 Removing temporary files..." -ForegroundColor Yellow

# Remove temporary files
$tempFiles = @("desktop.ini", "*.tmp", "*.log")
foreach ($pattern in $tempFiles) {
    Get-ChildItem -Path $workspaceRoot -Filter $pattern -Force | ForEach-Object {
        Write-Host "  Removing: $($_.Name)" -ForegroundColor Gray
        Remove-Item $_.FullName -Force
    }
}

# Remove specific files
$removeFiles = @(
    "filter-repo-rules.txt",
    "DroidTerminal",
    ".env.local-secure",
    "R3aler-ai.code-workspace-MAINGIT.code-workspace"
)

foreach ($file in $removeFiles) {
    $filePath = Join-Path $workspaceRoot $file
    if (Test-Path $filePath) {
        Write-Host "  Removing: $file" -ForegroundColor Gray
        Remove-Item $filePath -Force
    }
}

Write-Host ""
Write-Host "✅ Workspace cleanup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📊 Final Structure:" -ForegroundColor White
Write-Host "├── application/          (Core web app)" -ForegroundColor Cyan
Write-Host "├── AI_Core_Worker/       (AI & knowledge systems)" -ForegroundColor Cyan  
Write-Host "├── Tools/                (Recovery utilities)" -ForegroundColor Cyan
Write-Host "├── Database/             (PostgreSQL schema)" -ForegroundColor Cyan
Write-Host "├── systemd/              (Service management)" -ForegroundColor Cyan
Write-Host "├── scripts/              (Installation & management)" -ForegroundColor Cyan
Write-Host "├── configs/              (Configuration files)" -ForegroundColor Cyan
Write-Host "├── data/                 (Application data)" -ForegroundColor Cyan
Write-Host "├── docs/                 (Documentation)" -ForegroundColor Cyan
Write-Host "├── .archive/             (Archived files)" -ForegroundColor Yellow
Write-Host "└── .git/, .venv/, .env   (Environment)" -ForegroundColor Gray
Write-Host ""
Write-Host "🎯 Remaining files in root:" -ForegroundColor White
Get-ChildItem -Path $workspaceRoot -File | Select-Object Name | ForEach-Object {
    Write-Host "• $($_.Name)" -ForegroundColor Green
}
Write-Host ""
Write-Host "📁 Archived items moved to .archive/" -ForegroundColor Yellow
Write-Host "📚 Documentation moved to docs/" -ForegroundColor Blue
Write-Host ""