# R3ÆLƎR AI Demo - Quick Deploy to Vercel
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " R3ÆLƎR AI Demo - Quick Deploy Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Vercel CLI is installed
Write-Host "🚀 Checking Vercel CLI installation..." -ForegroundColor Yellow
try {
    $vercelVersion = vercel --version 2>$null
    Write-Host "✅ Vercel CLI found: $vercelVersion" -ForegroundColor Green
} catch {
    Write-Host "Installing Vercel CLI..." -ForegroundColor Yellow
    npm install -g vercel
}

Write-Host ""
Write-Host "📦 Deploying to Vercel..." -ForegroundColor Yellow
Write-Host "(This will open your browser for authentication if needed)" -ForegroundColor Gray
Write-Host ""

# Deploy to Vercel
vercel --prod --yes

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "🎉 DEPLOYMENT COMPLETE!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Your demo is now live! Copy the deployment URL above." -ForegroundColor White
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Copy the Vercel URL (looks like: https://r3aler-ai-demo.vercel.app)" -ForegroundColor White
Write-Host "2. Use it in your social media posts from READY_TO_POST.md" -ForegroundColor White
Write-Host "3. Check SOCIAL_MEDIA_GUIDE.md for detailed strategies" -ForegroundColor White
Write-Host ""
Write-Host "Ready to share your revolutionary AI with the world! 🚀" -ForegroundColor Magenta
Write-Host ""

Read-Host "Press Enter to exit"