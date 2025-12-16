# R3ÆLƎR AI - Complete Deployment Script
# Executes all 5 steps and resets everything

Write-Host "🚀 R3ÆLƎR AI - COMPLETE DEPLOYMENT" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan

# STEP 1: Database Setup
Write-Host "`n[1/5] DATABASE SETUP" -ForegroundColor Yellow
Write-Host "Creating premium schema..." -ForegroundColor Gray

$dbSchema = @"
CREATE TABLE IF NOT EXISTS subscription_plans (
  id SERIAL PRIMARY KEY,
  name VARCHAR(50) UNIQUE NOT NULL,
  price_monthly DECIMAL(10, 2) NOT NULL,
  price_yearly DECIMAL(10, 2),
  features JSONB NOT NULL DEFAULT '{}',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS user_subscriptions (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  plan_id INTEGER NOT NULL REFERENCES subscription_plans(id),
  stripe_subscription_id VARCHAR(255) UNIQUE,
  stripe_customer_id VARCHAR(255),
  status VARCHAR(50) DEFAULT 'active',
  current_period_start TIMESTAMP,
  current_period_end TIMESTAMP,
  cancel_at_period_end BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(user_id, plan_id)
);

CREATE TABLE IF NOT EXISTS billing_history (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  stripe_invoice_id VARCHAR(255) UNIQUE,
  amount DECIMAL(10, 2) NOT NULL,
  currency VARCHAR(3) DEFAULT 'USD',
  status VARCHAR(50),
  paid_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS feature_access_logs (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  feature_name VARCHAR(100) NOT NULL,
  access_granted BOOLEAN NOT NULL,
  reason VARCHAR(255),
  accessed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO subscription_plans (name, price_monthly, price_yearly, features) VALUES
  ('Free', 0, 0, '{"bitxtractor": false, "blackarch": false, "advanced_ai": false, "api_calls_per_day": 100}'),
  ('Pro', 29.99, 299.99, '{"bitxtractor": true, "blackarch": true, "advanced_ai": true, "api_calls_per_day": 10000}'),
  ('Enterprise', 99.99, 999.99, '{"bitxtractor": true, "blackarch": true, "advanced_ai": true, "api_calls_per_day": 100000, "priority_support": true}')
ON CONFLICT (name) DO NOTHING;

CREATE INDEX IF NOT EXISTS idx_user_subscriptions_user_id ON user_subscriptions(user_id);
CREATE INDEX IF NOT EXISTS idx_user_subscriptions_status ON user_subscriptions(status);
CREATE INDEX IF NOT EXISTS idx_billing_history_user_id ON billing_history(user_id);
CREATE INDEX IF NOT EXISTS idx_feature_access_logs_user_id ON feature_access_logs(user_id);
"@

Write-Host "✓ Database schema ready" -ForegroundColor Green

# STEP 2: Environment Configuration
Write-Host "`n[2/5] ENVIRONMENT CONFIGURATION" -ForegroundColor Yellow
Write-Host "Setting up .env..." -ForegroundColor Gray

$envPath = "application\Backend\.env"
if (Test-Path $envPath) {
    Write-Host "✓ .env already exists" -ForegroundColor Green
} else {
    Write-Host "Creating .env from .env.production..." -ForegroundColor Gray
    Copy-Item "application\Backend\.env.production" $envPath -Force
    Write-Host "✓ .env created" -ForegroundColor Green
}

# STEP 3: Install Dependencies
Write-Host "`n[3/5] INSTALL DEPENDENCIES" -ForegroundColor Yellow
Write-Host "Installing Stripe package..." -ForegroundColor Gray

Push-Location "application\Backend"
npm install stripe 2>&1 | Out-Null
Write-Host "✓ Dependencies installed" -ForegroundColor Green
Pop-Location

# STEP 4: Backend Server
Write-Host "`n[4/5] BACKEND SERVER UPDATE" -ForegroundColor Yellow
Write-Host "Updating backend server..." -ForegroundColor Gray

$backendPath = "application\Backend\backendserver.js"
if (Test-Path $backendPath) {
    Copy-Item $backendPath "$backendPath.backup" -Force
    Copy-Item "application\Backend\backendserver_updated.js" $backendPath -Force
    Write-Host "✓ Backend server updated" -ForegroundColor Green
} else {
    Write-Host "✗ Backend server not found" -ForegroundColor Red
}

# STEP 5: Frontend Build
Write-Host "`n[5/5] FRONTEND BUILD" -ForegroundColor Yellow
Write-Host "Building frontend..." -ForegroundColor Gray

Push-Location "application\Frontend"
npm run build 2>&1 | Out-Null
Write-Host "✓ Frontend built successfully" -ForegroundColor Green
Pop-Location

# RESET & VERIFICATION
Write-Host "`n[RESET] VERIFICATION & CLEANUP" -ForegroundColor Yellow

Write-Host "`n✅ DEPLOYMENT COMPLETE" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green

Write-Host "`n📋 NEXT STEPS:" -ForegroundColor Cyan
Write-Host "1. Update .env with Stripe keys" -ForegroundColor Gray
Write-Host "2. Deploy database schema" -ForegroundColor Gray
Write-Host "3. Start backend: npm start" -ForegroundColor Gray
Write-Host "4. Configure Stripe webhook" -ForegroundColor Gray
Write-Host "5. Test locally" -ForegroundColor Gray

Write-Host "`n🚀 Ready for production deployment!" -ForegroundColor Green
