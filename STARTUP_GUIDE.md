# 🚀 R3ÆLƎR AI - STARTUP GUIDE

## ✅ BUILD STATUS

### Frontend ✅
- Built successfully in 1.82s
- Output: `application/Backend/build/`
- Ready for production

### Backend ✅
- Dependencies installed (Stripe included)
- Subscription middleware integrated
- Protected routes configured
- Ready to start

### Database ⏳
- Schema file ready: `deploy_database.sql`
- Needs deployment

---

## 🔧 STARTUP STEPS

### Step 1: Configure Stripe Keys (5 min)

Edit `application/Backend/.env`:

```env
STRIPE_PUBLIC_KEY=pk_live_51SXYwUHevfJDhqUa4vGk8OFHgnZk75AqAiGggZKwhg2ugOiE7ZIXQkUbX2fg1LRJQuFizdICRHbpSm6SMnrV9D1000r7eR2TNU
STRIPE_SECRET_KEY=<YOUR_ROTATED_SECRET_KEY>
STRIPE_WEBHOOK_SECRET=<YOUR_WEBHOOK_SECRET>
JWT_SECRET=<GENERATE_NEW>
```

Generate JWT_SECRET:
```bash
node -e "console.log(require('crypto').randomBytes(32).toString('base64'))"
```

### Step 2: Deploy Database (5 min)

```bash
psql -U r3aler_user_2025 -d r3aler_ai -f deploy_database.sql
```

Verify:
```bash
psql -U r3aler_user_2025 -d r3aler_ai -c "SELECT * FROM subscription_plans;"
```

Should show 3 rows: Free, Pro, Enterprise

### Step 3: Start Backend (2 min)

```bash
cd application/Backend
npm start
```

Expected output:
```
==================================================
✓ R3aler-AI Server Started Successfully
==================================================
📍 Local:   http://localhost:3000
📍 API:     http://localhost:3000/api/status
==================================================
```

### Step 4: Test Endpoints (5 min)

```bash
# Test Stripe plans
curl http://localhost:3000/api/stripe/plans

# Should return:
# {
#   "success": true,
#   "plans": [
#     {"id": 1, "name": "Free", "price_monthly": 0, ...},
#     {"id": 2, "name": "Pro", "price_monthly": 29.99, ...},
#     {"id": 3, "name": "Enterprise", "price_monthly": 99.99, ...}
#   ]
# }
```

### Step 5: Test Feature Restrictions (10 min)

```bash
# Register user
curl -X POST http://localhost:3000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"test123"}'

# Login
TOKEN=$(curl -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"test123"}' | jq -r '.token')

# Try BitXtractor (should fail with 403)
curl -X POST http://localhost:3000/api/bitxtractor/start \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"wallet_path":"/path/to/wallet.dat"}'

# Expected: 403 Forbidden with upgrade message
```

### Step 6: Create Premium User (5 min)

```bash
# Add subscription to user
psql -U r3aler_user_2025 -d r3aler_ai -c "
INSERT INTO user_subscriptions (user_id, plan_id, stripe_subscription_id, status)
SELECT id, 2, 'sub_test_' || id, 'active' FROM users WHERE username = 'testuser'
"

# Try BitXtractor again (should work)
curl -X POST http://localhost:3000/api/bitxtractor/start \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"wallet_path":"/path/to/wallet.dat"}'

# Expected: 200 OK
```

---

## 📊 SYSTEM STATUS

| Component | Status | Action |
|-----------|--------|--------|
| Frontend | ✅ Built | Ready |
| Backend | ✅ Ready | Start |
| Database | ⏳ Ready | Deploy |
| Stripe Keys | ⏳ Ready | Configure |
| Subscription System | ✅ Integrated | Test |

---

## 🆘 TROUBLESHOOTING

### Backend Won't Start
```bash
# Check if port 3000 is in use
netstat -ano | findstr :3000

# Kill process if needed
taskkill /PID <PID> /F

# Try again
npm start
```

### Database Connection Error
```bash
# Verify PostgreSQL is running
psql -U r3aler_user_2025 -d r3aler_ai -c "SELECT 1;"

# Check .env DATABASE_URL
cat application/Backend/.env | grep DATABASE_URL
```

### Stripe Keys Not Working
```bash
# Verify keys in .env
cat application/Backend/.env | grep STRIPE

# Test Stripe connection
node -e "const Stripe = require('stripe'); const s = new Stripe(process.env.STRIPE_SECRET_KEY); s.plans.list().then(() => console.log('✓ Connected')).catch(e => console.error('✗ Error:', e.message));"
```

### Feature Access Denied
```bash
# Check subscription
psql -U r3aler_user_2025 -d r3aler_ai -c "SELECT * FROM user_subscriptions WHERE user_id = 1;"

# Verify status is 'active'
# Verify plan has feature enabled
```

---

## ✅ SUCCESS CRITERIA

After startup, verify:

- [x] Frontend built successfully
- [x] Backend dependencies installed
- [x] Subscription middleware integrated
- [ ] Database schema deployed
- [ ] Stripe keys configured
- [ ] Backend server started
- [ ] /api/stripe/plans returns 3 plans
- [ ] Free user blocked from premium features
- [ ] Premium user can access premium features

---

## 🎯 NEXT STEPS

1. Configure Stripe keys in .env
2. Deploy database schema
3. Start backend server
4. Test all endpoints
5. Configure Stripe webhook
6. Deploy to production

---

## 📞 SUPPORT

For issues, check:
- `STARTUP_REPORT.md` - Build status
- `FINAL_DEPLOYMENT_STEPS.txt` - Detailed steps
- `BUILD_FIX.md` - Build troubleshooting
- `README_DEPLOYMENT.md` - Complete overview

---

**Ready to launch!** 🚀
