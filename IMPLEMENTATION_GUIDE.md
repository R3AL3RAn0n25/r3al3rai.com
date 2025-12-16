# Implementation Guide - 5 Step Production Deployment

## Files Created

### 1. Database Schema
**File**: `Database/premium_schema.sql`
- Creates subscription_plans table with Free/Pro/Enterprise tiers
- Creates user_subscriptions table for tracking active subscriptions
- Creates billing_history table for payment records
- Creates feature_access_logs table for audit trail

**Deploy**: 
```bash
psql -U r3aler_user_2025 -d r3aler_ai -f Database/premium_schema.sql
```

### 2. Stripe Service
**File**: `application/Backend/stripe_service.js`
- Handles Stripe customer creation
- Manages subscription lifecycle
- Processes webhook events
- Tracks billing history

**Methods**:
- `getOrCreateCustomer(userId, email)`
- `createSubscription(userId, planId, email)`
- `cancelSubscription(userId)`
- `getUserSubscription(userId)`
- `handleWebhook(event)`

### 3. Stripe Routes
**File**: `application/Backend/stripe_routes.js`
- REST endpoints for subscription management
- Checkout session creation
- Billing history retrieval
- Webhook endpoint

**Endpoints**:
- `GET /api/stripe/plans`
- `GET /api/stripe/subscription`
- `POST /api/stripe/checkout`
- `POST /api/stripe/confirm`
- `POST /api/stripe/cancel`
- `GET /api/stripe/billing-history`
- `POST /api/stripe/webhook`

### 4. Subscription Middleware
**File**: `application/Backend/middleware/subscription.js`
- Verifies active subscriptions
- Enforces feature access restrictions
- Applies rate limiting by tier
- Logs feature access

**Middleware**:
- `verifySubscription` - Checks if user has active subscription
- `requireFeature(featureName)` - Restricts feature to specific plans
- `subscriptionRateLimit` - Sets rate limits based on tier

### 5. Production Environment
**File**: `application/Backend/.env.production`
- Stripe API keys configuration
- Production database settings
- Security settings
- CORS configuration for production domain

### 6. Frontend Pricing Page
**File**: `application/Frontend/src/pages/Pricing.tsx`
- Displays all subscription plans
- Monthly/yearly billing toggle
- Stripe checkout integration
- FAQ section

### 7. Deployment Checklist
**File**: `PRODUCTION_DEPLOYMENT_CHECKLIST.md`
- 10-step deployment guide
- Testing procedures
- Monitoring setup
- Security checklist

### 8. Setup Script
**File**: `setup_production.ps1`
- Automated setup for Windows
- Verifies all files
- Installs dependencies
- Configures environment

### 9. Summary Document
**File**: `PRODUCTION_READY_SUMMARY.md`
- Overview of all components
- Quick start guide
- API reference
- Troubleshooting guide

---

## Implementation Steps

### Step 1: Database Setup
1. Run premium_schema.sql
2. Verify tables created
3. Check default plans inserted

### Step 2: Backend Configuration
1. Copy .env.production to .env
2. Update Stripe keys
3. Update database password
4. Generate new JWT_SECRET

### Step 3: Install Dependencies
```bash
cd application/Backend
npm install stripe
```

### Step 4: Update Backend Server
1. Add imports for stripe_service, stripe_routes, subscription middleware
2. Mount stripe routes: `app.use('/api/stripe', stripeRoutes);`
3. Add subscription middleware to premium routes
4. Reference: backendserver_stripe_patch.js

### Step 5: Frontend Integration
1. Add Pricing page to router
2. Update navigation links
3. Build frontend: `npm run build`

### Step 6: Stripe Webhook Setup
1. Go to Stripe Dashboard
2. Add webhook endpoint: https://r3al3rai.com/api/stripe/webhook
3. Select events: subscription.updated, subscription.deleted, invoice.payment_succeeded, invoice.payment_failed
4. Copy webhook secret to .env

### Step 7: Testing
1. Test free tier restrictions
2. Test premium checkout
3. Test webhook delivery
4. Test subscription management

### Step 8: Production Deployment
1. Configure domain DNS
2. Install SSL certificate
3. Configure Nginx reverse proxy
4. Start all services
5. Verify health endpoints

---

## Feature Restrictions

### BitXtractor (Premium Only)
- Middleware: `requireFeature('bitxtractor')`
- Routes: `/api/bitxtractor/*`
- Plans: Pro, Enterprise

### BlackArch (Premium Only)
- Middleware: `requireFeature('blackarch')`
- Routes: `/api/blackarch/*`
- Plans: Pro, Enterprise

### Advanced AI (Premium Only)
- Middleware: `requireFeature('advanced_ai')`
- Routes: `/api/thebrain` (optional)
- Plans: Pro, Enterprise

---

## Database Schema

### subscription_plans
```sql
id, name, price_monthly, price_yearly, features (JSON), created_at
```

### user_subscriptions
```sql
id, user_id, plan_id, stripe_subscription_id, stripe_customer_id, 
status, current_period_start, current_period_end, cancel_at_period_end, 
created_at, updated_at
```

### billing_history
```sql
id, user_id, stripe_invoice_id, amount, currency, status, paid_at, created_at
```

### feature_access_logs
```sql
id, user_id, feature_name, access_granted, reason, accessed_at
```

---

## Environment Variables

Required in .env:
- STRIPE_PUBLIC_KEY
- STRIPE_SECRET_KEY
- STRIPE_WEBHOOK_SECRET
- JWT_SECRET
- DB_PASSWORD
- FRONTEND_URL

---

## Testing Commands

### List Plans
```bash
curl http://localhost:3000/api/stripe/plans
```

### Get User Subscription
```bash
curl -H "Authorization: Bearer <TOKEN>" \
  http://localhost:3000/api/stripe/subscription
```

### Test Feature Restriction
```bash
curl -X POST http://localhost:3000/api/bitxtractor/start \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"wallet_path":"/path/to/wallet.dat"}'
```

---

## Monitoring

### Check Active Subscriptions
```sql
SELECT COUNT(*) FROM user_subscriptions WHERE status = 'active';
```

### Check Revenue
```sql
SELECT SUM(amount) FROM billing_history WHERE status = 'paid';
```

### Check Feature Usage
```sql
SELECT feature_name, COUNT(*) FROM feature_access_logs GROUP BY feature_name;
```

---

## Success Indicators

✅ All 5 files deployed
✅ Database schema applied
✅ Stripe keys configured
✅ Backend routes updated
✅ Frontend pricing page live
✅ Free users blocked from premium features
✅ Premium users can access all features
✅ Stripe payments processing
✅ Webhooks delivering
✅ Subscriptions tracked in database
