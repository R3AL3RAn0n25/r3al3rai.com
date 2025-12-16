@echo off
echo ========================================
echo  R3ÆLƎR AI Demo - Quick Deploy Script
echo ========================================
echo.

cd /d "%~dp0"

echo 🚀 Deploying R3ÆLƎR AI Live Demo...
echo.

echo Step 1: Checking if Vercel CLI is installed...
where vercel >nul 2>nul
if %errorlevel% neq 0 (
    echo Installing Vercel CLI...
    npm install -g vercel
) else (
    echo ✅ Vercel CLI found!
)

echo.
echo Step 2: Deploying to Vercel...
echo (This will open your browser for authentication if needed)
echo.

vercel --prod --yes

echo.
echo ========================================
echo 🎉 DEPLOYMENT COMPLETE!
echo ========================================
echo.
echo Your demo is now live! Copy the deployment URL above.
echo.
echo Next steps:
echo 1. Copy the Vercel URL (looks like: https://r3aler-ai-demo.vercel.app)
echo 2. Use it in your social media posts
echo 3. Check out SOCIAL_MEDIA_GUIDE.md and READY_TO_POST.md
echo.
echo Ready to share your revolutionary AI with the world! 🚀
echo.

pause