# Start R3ÆLƎR Knowledge Base API (Windows PowerShell)

Write-Host "🧠 Starting R3ÆLƎR AI Knowledge Base API..." -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Gray

$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

# Check Python
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Python not found. Please install Python 3.8+" -ForegroundColor Red
    exit 1
}

# Install dependencies
Write-Host "📦 Installing dependencies..." -ForegroundColor Yellow
python -m pip install -r requirements-kb-api.txt

# Start API
Write-Host ""
Write-Host "🚀 Starting Knowledge API on http://localhost:5001" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Gray
python knowledge_api.py
