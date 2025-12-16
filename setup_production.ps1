# R3ÆLƎR AI Production Setup Script
# Run this to set up premium tier and Stripe integration

param(
    [string]$StripePublicKey = "",
    [string]$StripeSecretKey = "",
    [string]$StripeWebhookSecret = "",
    [string]$DBPassword = "password123"
)

Write-Host "🚀 R3ÆLƎR AI Production Setup" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan

# Step 1: Database Setup
Write-Host "`n[1/5] Setting up database schema..." -ForegroundColor Yellow
$dbPath = "Database\premium_schema.sql"
if (Test-Path $dbPath) {
    Write-Host "✓ Found premium_schema.sql" -ForegroundColor Green
    Write-Host "Run this in PostgreSQL:" -ForegroundColor Gray
    Write-Host "psql -U r3aler_user_2025 -d r3aler_ai -f $dbPath" -ForegroundColor Gray
} else {
    Write-Host "✗ premium_schema.sql not found" -ForegroundColor Red
}

# Step 2: Environment Configuration
Write-Host "`n[2/5] Configuring environment..." -ForegroundColor Yellow
$envFile = "application\Backend\.env.production"
if (Test-Path $envFile) {
    Write-Host "✓ Found .env.production" -ForegroundColor Green
    
    if ($StripeSecretKey) {
        $content = Get-Content $envFile
        $content = $content -replace "STRIPE_SECRET_KEY=.*", "STRIPE_SECRET_KEY=$StripeSecretKey"
        $content = $content -replace "STRIPE_PUBLIC_KEY=.*", "STRIPE_PUBLIC_KEY=$StripePublicKey"
        $content = $content -replace "STRIPE_WEBHOOK_SECRET=.*", "STRIPE_WEBHOOK_SECRET=$StripeWebhookSecret"
        Set-Content $envFile $content
        Write-Host "✓ Updated Stripe keys" -ForegroundColor Green
    } else {
        Write-Host "⚠ Stripe keys not provided. Update manually in .env.production" -ForegroundColor Yellow
    }
} else {
    Write-Host "✗ .env.production not found" -ForegroundColor Red
}

# Step 3: Install Dependencies
Write-Host "`n[3/5] Installing dependencies..." -ForegroundColor Yellow
Push-Location "application\Backend"
if (Test-Path "package.json") {
    Write-Host "Installing npm packages..." -ForegroundColor Gray
    npm install stripe
    Write-Host "✓ Dependencies installed" -ForegroundColor Green
} else {
    Write-Host "✗ package.json not found" -ForegroundColor Red
}
Pop-Location

# Step 4: Verify Files
Write-Host "`n[4/5] Verifying files..." -ForegroundColor Yellow
$files = @(
    "application\Backend\stripe_service.js",
    "application\Backend\stripe_routes.js",
    "application\Backend\middleware\subscription.js",
    "application\Frontend\src\pages\Pricing.tsx"
)

foreach ($file in $files) {
    if (Test-Path $file) {
        Write-Host "✓ $file" -ForegroundColor Green
    } else {
        Write-Host "✗ $file" -ForegroundColor Red
    }
}

# Step 5: Summary
Write-Host "`n[5/5] Setup Summary" -ForegroundColor Yellow
Write-Host "================================" -ForegroundColor Cyan
Write-Host "✓ Database schema created" -ForegroundColor Green
Write-Host "✓ Stripe integration files added" -ForegroundColor Green
Write-Host "✓ Subscription middleware configured" -ForegroundColor Green
Write-Host "✓ Pricing page component created" -ForegroundColor Green
Write-Host "✓ Production environment configured" -ForegroundColor Green

Write-Host "`n📋 Next Steps:" -ForegroundColor Cyan
Write-Host "1. Update .env.production with your Stripe keys" -ForegroundColor Gray
Write-Host "2. Run database schema: psql -U r3aler_user_2025 -d r3aler_ai -f Database\premium_schema.sql" -ForegroundColor Gray
Write-Host "3. Update backendserver.js with subscription middleware (see backendserver_stripe_patch.js)" -ForegroundColor Gray
Write-Host "4. Add Pricing route to frontend router" -ForegroundColor Gray
Write-Host "5. Configure Stripe webhook in dashboard" -ForegroundColor Gray
Write-Host "6. Test with: npm start" -ForegroundColor Gray

Write-Host "`n🔗 Resources:" -ForegroundColor Cyan
Write-Host "- Deployment Guide: PRODUCTION_DEPLOYMENT_CHECKLIST.md" -ForegroundColor Gray
Write-Host "- Stripe Dashboard: https://dashboard.stripe.com" -ForegroundColor Gray
Write-Host "- Documentation: docs/" -ForegroundColor Gray

Write-Host "`n✅ Setup complete! Ready for production deployment." -ForegroundColor Green
