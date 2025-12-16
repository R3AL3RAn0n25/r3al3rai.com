# Backend Integration Steps

## Step 1: Add Imports

At the top of `application/Backend/backendserver.js`, add:

```javascript
import { verifySubscription, requireFeature } from './middleware/subscription.js';
import stripeRoutes from './stripe_routes.js';
```

---

## Step 2: Mount Stripe Routes

After this line:
```javascript
app.use('/api', globalRateLimiter, auditLogger);
```

Add:
```javascript
app.use('/api/stripe', stripeRoutes);
```

---

## Step 3: Update BitXtractor Routes

Find these routes and add the subscription middleware:

### Before:
```javascript
app.post('/api/bitxtractor/start', verifyJWT, async (req, res) => {
```

### After:
```javascript
app.post('/api/bitxtractor/start', verifyJWT, verifySubscription, requireFeature('bitxtractor'), async (req, res) => {
```

---

### Before:
```javascript
app.get('/api/bitxtractor/status/:jobId', verifyJWT, async (req, res) => {
```

### After:
```javascript
app.get('/api/bitxtractor/status/:jobId', verifyJWT, verifySubscription, requireFeature('bitxtractor'), async (req, res) => {
```

---

### Before:
```javascript
app.get('/api/bitxtractor/download/:jobId', verifyJWT, async (req, res) => {
```

### After:
```javascript
app.get('/api/bitxtractor/download/:jobId', verifyJWT, verifySubscription, requireFeature('bitxtractor'), async (req, res) => {
```

---

## Step 4: Update BlackArch Routes

Find these routes and add the subscription middleware:

### Before:
```javascript
app.post('/api/blackarch/install/:tool', verifyJWT, async (req, res) => {
```

### After:
```javascript
app.post('/api/blackarch/install/:tool', verifyJWT, verifySubscription, requireFeature('blackarch'), async (req, res) => {
```

---

### Before:
```javascript
app.post('/api/blackarch/execute/:tool', verifyJWT, async (req, res) => {
```

### After:
```javascript
app.post('/api/blackarch/execute/:tool', verifyJWT, verifySubscription, requireFeature('blackarch'), async (req, res) => {
```

---

### Before:
```javascript
app.post('/api/blackarch/workflows/run', verifyJWT, async (req, res) => {
```

### After:
```javascript
app.post('/api/blackarch/workflows/run', verifyJWT, verifySubscription, requireFeature('blackarch'), async (req, res) => {
```

---

### Before:
```javascript
app.post('/api/blackarch/install/:tool_name', verifyJWT, async (req, res) => {
```

### After:
```javascript
app.post('/api/blackarch/install/:tool_name', verifyJWT, verifySubscription, requireFeature('blackarch'), async (req, res) => {
```

---

### Before:
```javascript
app.post('/api/blackarch/execute/:tool_name', verifyJWT, async (req, res) => {
```

### After:
```javascript
app.post('/api/blackarch/execute/:tool_name', verifyJWT, verifySubscription, requireFeature('blackarch'), async (req, res) => {
```

---

## Step 5: Verify Changes

After making all changes, verify:

1. **Syntax Check**:
   ```bash
   node -c application/Backend/backendserver.js
   ```

2. **Start Server**:
   ```bash
   npm start
   ```

3. **Test Endpoints**:
   ```bash
   # Should work (no auth required)
   curl http://localhost:3000/api/stripe/plans
   
   # Should require token
   curl -X POST http://localhost:3000/api/bitxtractor/start
   # Response: 401 Unauthorized
   
   # With free user token (should fail)
   curl -X POST http://localhost:3000/api/bitxtractor/start \
     -H "Authorization: Bearer <FREE_USER_TOKEN>"
   # Response: 403 Forbidden - requires Pro plan
   
   # With premium user token (should work)
   curl -X POST http://localhost:3000/api/bitxtractor/start \
     -H "Authorization: Bearer <PREMIUM_USER_TOKEN>"
   # Response: 200 OK
   ```

---

## Summary of Changes

| Route | Before | After |
|-------|--------|-------|
| POST /api/bitxtractor/start | verifyJWT | verifyJWT, verifySubscription, requireFeature('bitxtractor') |
| GET /api/bitxtractor/status/:jobId | verifyJWT | verifyJWT, verifySubscription, requireFeature('bitxtractor') |
| GET /api/bitxtractor/download/:jobId | verifyJWT | verifyJWT, verifySubscription, requireFeature('bitxtractor') |
| POST /api/blackarch/install/:tool | verifyJWT | verifyJWT, verifySubscription, requireFeature('blackarch') |
| POST /api/blackarch/execute/:tool | verifyJWT | verifyJWT, verifySubscription, requireFeature('blackarch') |
| POST /api/blackarch/workflows/run | verifyJWT | verifyJWT, verifySubscription, requireFeature('blackarch') |

---

## Testing After Integration

### Test 1: Free User Cannot Access BitXtractor
```bash
# Register free user
curl -X POST http://localhost:3000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"freeuser","password":"test123"}'

# Login
TOKEN=$(curl -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"freeuser","password":"test123"}' | jq -r '.token')

# Try BitXtractor (should fail)
curl -X POST http://localhost:3000/api/bitxtractor/start \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"wallet_path":"/path/to/wallet.dat"}'

# Expected response:
# {
#   "success": false,
#   "error": "bitxtractor requires a paid subscription",
#   "required_plan": "Pro"
# }
```

### Test 2: Premium User Can Access BitXtractor
```bash
# Create premium subscription in database
psql -U r3aler_user_2025 -d r3aler_ai -c "
INSERT INTO user_subscriptions (user_id, plan_id, stripe_subscription_id, status)
SELECT id, 2, 'sub_test_' || id, 'active' FROM users WHERE username = 'freeuser'
"

# Try BitXtractor again (should work)
curl -X POST http://localhost:3000/api/bitxtractor/start \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"wallet_path":"/path/to/wallet.dat"}'

# Expected response: 200 OK with BitXtractor response
```

---

## Rollback Instructions

If you need to revert changes:

1. **Restore Original File**:
   ```bash
   git checkout application/Backend/backendserver.js
   ```

2. **Or Manually Remove**:
   - Remove the two new imports
   - Remove the `app.use('/api/stripe', stripeRoutes);` line
   - Remove subscription middleware from all routes

3. **Restart Server**:
   ```bash
   npm start
   ```

---

## Troubleshooting

### Import Error: Cannot find module
- Verify files exist:
  - `application/Backend/stripe_service.js`
  - `application/Backend/stripe_routes.js`
  - `application/Backend/middleware/subscription.js`

### Syntax Error
- Check for missing commas or parentheses
- Run: `node -c application/Backend/backendserver.js`

### Middleware Not Working
- Verify middleware order (verifyJWT must come first)
- Check database has subscription_plans table
- Verify user has active subscription in database

### 403 Forbidden on Premium Routes
- Check user subscription status: `SELECT * FROM user_subscriptions WHERE user_id = X;`
- Verify subscription status is 'active'
- Check plan has feature enabled in features JSON

---

## Verification Checklist

- [ ] Imports added to backendserver.js
- [ ] Stripe routes mounted
- [ ] BitXtractor routes updated (3 routes)
- [ ] BlackArch routes updated (5 routes)
- [ ] Server starts without errors
- [ ] Free user blocked from premium features
- [ ] Premium user can access premium features
- [ ] Subscription middleware working
- [ ] Feature access logged
- [ ] All tests passing
