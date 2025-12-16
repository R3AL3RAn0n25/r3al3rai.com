# Mode Manager Quick Start Guide

## 🎯 What is Mode Manager?

Mode Manager lets you switch R3AL3R AI between development and production modes instantly—no restarts needed. Each mode has different security levels, logging, rate limiting, and performance tuning.

---

## ⚡ 5-Minute Quick Start

### Step 1: Get Your JWT Token

**From Web UI:**
1. Open R3AL3R AI dashboard in browser
2. Login with your credentials
3. Check browser DevTools (F12 → Application → Local Storage)
4. Find `authToken` value
5. Copy it

**Or use the API:**
```powershell
$response = Invoke-RestMethod -Uri "http://localhost:3000/api/auth/login" `
  -Method POST `
  -Body (@{email='r3al3ran0n25@gmail.com'; password='password'} | ConvertTo-Json) `
  -Headers @{'Content-Type'='application/json'}

$token = $response.token
Write-Host "Token: $token"
```

### Step 2: Set Your Token

**Option A - Environment Variable (Persistent):**
```powershell
# Set for current session only
$env:R3AL3R_JWT_TOKEN = "your_token_here"

# Or set permanently for your user
[System.Environment]::SetEnvironmentVariable('R3AL3R_JWT_TOKEN', 'your_token_here', 'User')
```

**Option B - Token File:**
```powershell
# Save token to file
"your_token_here" | Out-File -FilePath .r3al3r_token -Encoding UTF8 -NoNewline
```

**Option C - Command Line:**
```powershell
# Pass token directly each time
python mode_switcher.py status --token "your_token_here"
```

### Step 3: Check Current Mode

**Using Python CLI:**
```powershell
python mode_switcher.py status
```

**Using PowerShell Wrapper:**
```powershell
.\mode-switcher.ps1 status
```

**Using cURL:**
```powershell
$headers = @{
    'Authorization' = "Bearer your_token_here"
    'Content-Type' = 'application/json'
}

Invoke-RestMethod -Uri "http://localhost:3000/api/admin/mode" `
  -Headers $headers
```

### Step 4: Switch Modes

**To Development:**
```powershell
python mode_switcher.py dev
# or
.\mode-switcher.ps1 dev
```

**To Production:**
```powershell
python mode_switcher.py prod
# or
.\mode-switcher.ps1 prod
```

**Toggle (switch between modes):**
```powershell
python mode_switcher.py toggle
# or
.\mode-switcher.ps1 toggle
```

### Step 5: Verify Mode Changed

```powershell
python mode_switcher.py status
```

You should see output like:
```
Fetching current mode...

Current Mode: PRODUCTION
  Security Level:    high
  Log Level:         warn
  Rate Limit:        100 req/min
  Test Endpoints:    Disabled
  Debug Mode:        Disabled
  Database Logging:  Disabled

  Service Timeouts:
    database         3000ms (retries: 5)
    ai_core          8000ms (retries: 5)
    knowledge        5000ms (retries: 5)
    reasoning        10000ms (retries: 5)
    cache            2000ms (retries: 3)
```

---

## 📋 Development Mode Details

**When to use:** Local development, testing, debugging

| Setting | Value |
|---------|-------|
| Security Level | low |
| Log Level | debug |
| Rate Limit | 1000 req/min |
| Test Endpoints | Enabled |
| Debug Endpoints | Enabled |
| Database Logging | Enabled |

**What changes:**
- ✓ More verbose logs (every request, every query)
- ✓ Test endpoints available at `/test/*`
- ✓ Stack traces shown in errors
- ✓ Query timing information logged
- ✓ CORS very permissive
- ✓ Longer service timeouts (5-12 seconds)
- ✓ More retry attempts (2-3)

**Typical flow:**
```
Developer works locally
  ↓
Switches to DEV mode: python mode_switcher.py dev
  ↓
Sees full debug logs + detailed errors
  ↓
Fixes issues faster
  ↓
Switches back to PROD: python mode_switcher.py prod
```

---

## 🔒 Production Mode Details

**When to use:** Deployed system, user-facing, high reliability

| Setting | Value |
|---------|-------|
| Security Level | high |
| Log Level | warn |
| Rate Limit | 100 req/min |
| Test Endpoints | Disabled |
| Debug Endpoints | Disabled |
| Database Logging | Disabled |

**What changes:**
- ✓ Only warnings and errors logged
- ✓ No sensitive data in logs
- ✓ Test endpoints hidden (403 Forbidden)
- ✓ Generic error messages (no stack traces)
- ✓ Strict CORS whitelist
- ✓ Shorter service timeouts (2-10 seconds)
- ✓ More retry attempts (3-5)
- ✓ Rate limiting enforced

**Typical flow:**
```
System deployed to production
  ↓
Stays in PROD mode
  ↓
Rate limiting protects from abuse
  ↓
Only important logs written
  ↓
Better performance, less I/O
```

---

## 🧪 Common Tasks

### Task 1: Debug a Login Issue

```powershell
# 1. Switch to dev mode
python mode_switcher.py dev

# 2. Watch logs (in another terminal)
# Tail the backend logs to see what's happening

# 3. Try the login request
Invoke-RestMethod -Uri "http://localhost:3000/api/auth/login" `
  -Method POST `
  -Body (@{email='test@r3aler.ai'; password='test'} | ConvertTo-Json) `
  -Headers @{'Content-Type'='application/json'}

# 4. Read detailed error in the logs (dev mode shows full stack)

# 5. Fix the issue

# 6. Switch back to prod
python mode_switcher.py prod
```

### Task 2: Test API Under Load

```powershell
# 1. Stay in PROD mode (rate limiting enabled)
python mode_switcher.py status

# Should show: Rate Limit: 100 req/min

# 2. Run load test with wrk, Apache Bench, or PowerShell
# This will hit the 100 req/min limit after 100 requests

# 3. To test without limits, switch to dev
python mode_switcher.py dev

# Now rate limit is 1000 req/min (testing only)

# 4. Run your test

# 5. Switch back to prod
python mode_switcher.py prod
```

### Task 3: Deploy to Production

```powershell
# 1. Verify you're in production mode
python mode_switcher.py status
# Should show: Current Mode: PRODUCTION

# 2. If not, set it
python mode_switcher.py prod

# 3. Verify config
python mode_switcher.py status
# Check all settings are correct:
# - Security Level: high
# - Log Level: warn
# - Rate Limit: 100 req/min
# - Debug Endpoints: Disabled

# 4. Deploy
# ... your deployment process ...

# 5. Monitor (mode stays in production)
python mode_switcher.py status
```

### Task 4: Check System Configuration

```powershell
# Quick status check
python mode_switcher.py status

# Sample output:
# Current Mode: DEVELOPMENT
#   Security Level:    low
#   Log Level:         debug
#   Rate Limit:        1000 req/min
#   Test Endpoints:    Enabled
#   Debug Mode:        Enabled
#   Database Logging:  Enabled
#   Service Timeouts:
#     database         5000ms (retries: 3)
#     ai_core          10000ms (retries: 3)
#     knowledge        8000ms (retries: 3)
#     reasoning        12000ms (retries: 3)
#     cache            3000ms (retries: 2)
```

---

## 🛠️ Troubleshooting

### Problem: "JWT token not found"

**Solution:**
```powershell
# 1. Check if token is set
Write-Host $env:R3AL3R_JWT_TOKEN

# 2. If empty, set it
$env:R3AL3R_JWT_TOKEN = "your_token_here"

# 3. Or pass it directly
python mode_switcher.py status --token "your_token_here"

# 4. Or save to file
"your_token_here" | Out-File -FilePath .r3al3r_token -Encoding UTF8 -NoNewline
```

### Problem: "Unauthorized" (401)

**Solution:**
```powershell
# 1. Token might be expired - get a new one
Invoke-RestMethod -Uri "http://localhost:3000/api/auth/login" `
  -Method POST `
  -Body (@{email='admin@r3aler.ai'; password='your_password'} | ConvertTo-Json) `
  -Headers @{'Content-Type'='application/json'}

# 2. Set the new token
$env:R3AL3R_JWT_TOKEN = "new_token_here"

# 3. Try again
python mode_switcher.py status
```

### Problem: "Failed to connect to localhost:3000"

**Solution:**
```powershell
# 1. Check if backend is running
netstat -ano | Select-String "3000"

# 2. If not running, start it
cd application/Backend
npm start

# 3. Wait for startup message

# 4. Try again
python mode_switcher.py status
```

### Problem: Mode doesn't change

**Solution:**
```powershell
# 1. Verify you're authenticated
python mode_switcher.py status

# 2. Try explicit mode set
python mode_switcher.py set prod
# instead of
python mode_switcher.py prod

# 3. Check backend logs for errors
# Should show "Mode changed to production"

# 4. Verify persistence
python mode_switcher.py status
# Should show PRODUCTION mode
```

---

## 📚 Reference: Command Examples

### Python CLI Tool

```powershell
# Get current mode
python mode_switcher.py status

# Set to development
python mode_switcher.py dev

# Set to production
python mode_switcher.py prod

# Toggle between modes
python mode_switcher.py toggle

# With custom token
python mode_switcher.py status --token "eyJhbGc..."

# With custom URL
python mode_switcher.py status --url "https://api.r3aler.ai"

# With both
python mode_switcher.py dev --token "eyJhbGc..." --url "https://api.r3aler.ai"
```

### PowerShell Wrapper

```powershell
# Get current mode
.\mode-switcher.ps1 status

# Set to development
.\mode-switcher.ps1 dev

# Set to production
.\mode-switcher.ps1 prod

# Toggle between modes
.\mode-switcher.ps1 toggle

# Show help
.\mode-switcher.ps1 help

# With custom token
.\mode-switcher.ps1 status -Token "eyJhbGc..."

# With custom URL
.\mode-switcher.ps1 status -Url "https://api.r3aler.ai"
```

### REST API (cURL/PowerShell)

```powershell
# Get current mode
$headers = @{'Authorization' = 'Bearer eyJhbGc...'}
Invoke-RestMethod -Uri "http://localhost:3000/api/admin/mode" -Headers $headers

# Toggle mode
Invoke-RestMethod -Uri "http://localhost:3000/api/admin/mode/toggle" `
  -Method POST -Headers $headers

# Set specific mode
$body = @{mode='production'} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:3000/api/admin/mode/set" `
  -Method POST -Headers $headers -Body $body -ContentType 'application/json'
```

---

## 📖 More Information

- **Full Documentation:** See `MODE_MANAGER_README.md`
- **API Details:** See API Reference section in MODE_MANAGER_README.md
- **Architecture:** See `ARCHITECTURE_DIAGRAM.md`
- **Deployment:** See `/docs/deployment.md`

---

## 🎓 Learning Path

**New to Mode Manager?**
1. Read this Quick Start guide (you're here!)
2. Follow the 5-Minute Quick Start section
3. Try the Common Tasks
4. Read `MODE_MANAGER_README.md` for details

**Already know Mode Manager?**
1. Jump to Common Tasks
2. Reference the Command Examples
3. Check Troubleshooting if issues

**Need deep dive?**
1. Read full `MODE_MANAGER_README.md`
2. Check API Reference section
3. Review configuration presets
4. Study implementation files

---

**Last Updated:** November 29, 2024
**Quick Start Version:** 1.0.0
**Status:** Ready to Use ✓
