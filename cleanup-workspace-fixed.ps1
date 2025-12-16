# R3ALER AI Workspace Cleanup Script
# This script organizes the workspace by keeping essential files and archiving/removing unnecessary ones

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor White
Write-Host "║             R3ALER AI - Workspace Cleanup                 ║" -ForegroundColor White  
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor White
Write-Host ""

$workspaceRoot = "C:\Users\work8\OneDrive\Desktop\r3al3rai\New Folder 1\R3al3r-AI Main Working\R3aler-ai\R3aler-ai"
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

# Files to keep in root directory (essential project files)
$keepInRoot = @(
    ".env",
    ".env.example", 
    ".gitignore",
    "README.md",
    "QUICK_REFERENCE.md",
    "SYSTEMD_MANAGEMENT.md"
)

# Directories to keep (core project structure)
$keepDirectories = @(
    ".git",
    ".venv", 
    "application",
    "AI_Core_Worker",
    "Database",
    "Tools", 
    "systemd",
    "scripts",
    "configs",
    "data",
    "docs",
    ".archive"
)

# Files to archive (old scripts and reports)
$filesToArchive = @(
    "*.ps1",
    "*.sh", 
    "*.bat",
    "*_REPORT.md",
    "*_STATUS*.md",
    "*INTEGRATION.md",
    "*SETUP*.md",
    "*GUIDE*.md",
    "*NOTICE*.md",
    "*HARDENING*.md",
    "*.py",
    "*.js",
    "*.tsx"
)

# Directories to archive (old/unused) - using proper PowerShell array syntax
$dirsToArchive = @(
    "unused",
    "deploy-package",
    "R`&D Blueprints",
    "dictionaries",
    "icons",
    "services",
    "server",
    ".bak_stash"
)

Write-Host "📁 Moving documentation files..." -ForegroundColor Yellow

# Move documentation to docs directory
Get-ChildItem -Path $workspaceRoot -Filter "*.md" | Where-Object { 
    $_.Name -notin $keepInRoot 
} | ForEach-Object {
    Write-Host "  Moving $($_.Name) to docs/" -ForegroundColor Gray
    Move-Item $_.FullName "$docsDir\$($_.Name)" -Force
}

Write-Host ""
Write-Host "📦 Archiving old directories..." -ForegroundColor Yellow

# Archive directories
foreach ($dir in $dirsToArchive) {
    $dirPath = Join-Path $workspaceRoot $dir
    if (Test-Path $dirPath) {
        Write-Host "  Archiving directory: $dir" -ForegroundColor Gray
        Move-Item $dirPath "$archiveDir\$dir" -Force
    }
}

Write-Host ""
Write-Host "📦 Archiving script files..." -ForegroundColor Yellow

# Archive script files (but keep some essential ones)
$essentialScripts = @(
    "install-services-simple.sh",
    "cleanup-workspace.ps1"
)

Get-ChildItem -Path $workspaceRoot -File | Where-Object {
    ($_.Extension -in @(".ps1", ".sh", ".bat", ".py", ".js")) -and
    ($_.Name -notin $essentialScripts) -and
    ($_.Name -notlike "manage*") -and
    ($_.Directory.Name -eq (Split-Path $workspaceRoot -Leaf))
} | ForEach-Object {
    Write-Host "  Archiving script: $($_.Name)" -ForegroundColor Gray
    Move-Item $_.FullName "$archiveDir\$($_.Name)" -Force
}

Write-Host ""
Write-Host "🧹 Removing temporary files..." -ForegroundColor Yellow

# Remove temporary and build artifacts
$tempPatterns = @(
    "desktop.ini",
    "*.tmp",
    "*.log",
    "*.cache"
)

foreach ($pattern in $tempPatterns) {
    Get-ChildItem -Path $workspaceRoot -Filter $pattern -Recurse -Force | ForEach-Object {
        Write-Host "  Removing: $($_.FullName.Replace($workspaceRoot, '.'))" -ForegroundColor Gray
        Remove-Item $_.FullName -Force
    }
}

Write-Host ""
Write-Host "📋 Creating project structure overview..." -ForegroundColor Yellow

# Create a clean README for the project structure - proper here-string syntax
$readmeContent = @'
# R3ALER AI - Cryptocurrency Recovery & Analysis System

## 🏗️ Project Structure

### Core Application
- **application/** - Main web application
  - Backend/ - Node.js API server (Express, PostgreSQL)
  - Frontend/ - React web interface
  
### AI & Knowledge Systems  
- **AI_Core_Worker/** - AI processing and knowledge base
  - knowledge_api.py - Knowledge base API server
  - prompts.py - AI prompt definitions and knowledge base
  - openai_integration.py - OpenAI API integration

### Tools & Utilities
- **Tools/** - Cryptocurrency recovery tools
  - tools/wallet_extractor.py - Enhanced wallet recovery with BTCRecover
  - Distribution versions (portable, offline, standalone)

### Configuration & Deployment
- **Database/** - PostgreSQL schema and setup
- **systemd/** - SystemD service definitions for process management
- **scripts/** - Installation and management scripts
- **configs/** - Configuration files (Tailwind, TypeScript)
- **data/** - Application data and assets

### Documentation
- **docs/** - Project documentation, setup guides, reports
- **.archive/** - Archived files and old versions

## 🚀 Quick Start

### Prerequisites
- WSL2 with Ubuntu 24.04+
- Node.js 18+
- Python 3.12+
- PostgreSQL

### Installation
1. Install SystemD services:
   ```bash
   ./install-services-simple.sh
   ```

2. Start all services:
   ```bash
   sudo systemctl start r3aler-ai.target
   ```

3. Access the application:
   - Frontend: http://localhost:3000
   - Knowledge API: http://localhost:5002
   - Droid API: http://localhost:5001

### Management
```bash
# Service management
sudo systemctl status r3aler-backend
sudo systemctl restart r3aler-ai.target
sudo journalctl -u r3aler-backend -f

# Using PowerShell wrapper
. .\scripts\windows\manage-services.ps1
Start-R3alerServices
```

## 📚 Documentation
- **System Management**: docs/SYSTEMD_MANAGEMENT.md
- **Quick Reference**: QUICK_REFERENCE.md 
- **Environment Setup**: docs/ENV_SETUP.md

## 🔧 Development
- **Backend**: Node.js with Express, JWT authentication, PostgreSQL
- **Frontend**: React with modern JavaScript/TypeScript
- **AI**: OpenAI integration, custom knowledge base, prompt engineering
- **Tools**: Python-based cryptocurrency recovery utilities

## 🛡️ Security
- SystemD process isolation
- Environment variable management
- Database credential rotation
- Firewall configuration included

Built with 💎 by R3AL3RAn0n25
'@

Set-Content -Path "$workspaceRoot\README.md" -Value $readmeContent -Encoding UTF8

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
Write-Host "├── .git/                 (Version control)" -ForegroundColor Gray
Write-Host "├── .venv/                (Python environment)" -ForegroundColor Gray
Write-Host "└── README.md             (Project overview)" -ForegroundColor White
Write-Host ""
Write-Host "🎯 Key Files:" -ForegroundColor White
Write-Host "• README.md - Project overview and quick start" -ForegroundColor Green
Write-Host "• QUICK_REFERENCE.md - Command reference" -ForegroundColor Green  
Write-Host "• SYSTEMD_MANAGEMENT.md - Service management guide" -ForegroundColor Green
Write-Host "• install-services-simple.sh - SystemD installer" -ForegroundColor Green
Write-Host ""
Write-Host "📁 Archived: Old scripts, reports, and unused files moved to .archive/" -ForegroundColor Yellow
Write-Host "📚 Documentation: All .md files organized in docs/ directory" -ForegroundColor Blue
Write-Host ""