# R3ÆLƎR AI - System Verification Guide

## Overview
This guide provides comprehensive verification procedures for all R3ÆLƎR AI system components.

---

## Quick Status Check

### PowerShell (Windows)
```powershell
.\QUICK_STATUS_CHECK.ps1
```

This will verify:
- ✓ PostgreSQL database connection
- ✓ Backend server (Node.js) on port 3000
- ✓ Frontend dev server (Vite) on port 5173
- ✓ Knowledge API (Python) on port 5004
- ✓ Droid API (Python) on port 5005
- ✓ Storage Facility (Python) on port 3003

---

## Complete System Verification

### Python Verification Script
```bash
python SYSTEM_VERIFICATION.py
```

This comprehensive test performs:

#### 1. Database Verification
- PostgreSQL connection test
- Table enumeration
- User count verification
- Connection string validation

#### 2. Backend Verification
- Health endpoint check
- Node.js uptime monitoring
- Memory usage tracking
- Database connectivity status

#### 3. Authentication Verification
- User registration endpoint
- Login endpoint
- JWT token generation
- Token validation

#### 4. Frontend Verification
- Dev server availability
- Login page rendering
- Static asset serving
- CORS configuration

#### 5. API Endpoints Verification
- Status endpoint
- Health endpoint
- Rate limiting
- Error handling

#### 6. Knowledge API Verification
- Service availability
- AI modules status
- Storage Facility connectivity
- Total knowledge entries count

#### 7. Droid API Verification
- Service availability
- Cryptocurrency AI functionality
- Response validation

#### 8. Storage Facility Verification
- Database connectivity
- Entry count verification
- Unit status
- Query performance

#### 9. Features Verification
- BitXtractor accessibility
- BlackArch tool integration
- Knowledge search functionality

---

## Manual Verification Steps

### 1. Database Connection
```bash
# Connect to PostgreSQL
psql -h localhost -U r3aler_user_2025 -d r3aler_ai

# Check tables
\dt

# Verify users table
SELECT COUNT(*) FROM users;
```

### 2. Backend Server
```bash
# Check if running
curl http://localhost:3000/api/health

# Expected response:
{
  "ok": true,
  "node": {
    "uptime_s": 123,
    "rss_mb": 45.2,
    "pid": 1234
  },
  "db": {
    "ok": true
  }
}
```

### 3. Frontend Login
```bash
# Open in browser
http://localhost:5173

# Should display:
- R3ÆLƎR AI login page
- Username input field
- Password input field
- Sign In button
- Register link
```

### 4. Authentication Flow
```bash
# Register user
curl -X POST http://localhost:3000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"TestPass123!"}'

# Login
curl -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"TestPass123!"}'

# Expected response:
{
  "success": true,
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### 5. Knowledge API
```bash
# Health check
curl http://localhost:5004/health

# Search knowledge
curl -X POST http://localhost:5004/api/kb/search \
  -H "Content-Type: application/json" \
  -d '{"query":"quantum physics"}'
```

### 6. Storage Facility
```bash
# Status check
curl http://localhost:3003/api/facility/status

# Expected response:
{
  "status": "operational",
  "total_entries": 30657,
  "units_count": 4,
  "units": {
    "physics": 25875,
    "quantum": 1042,
    "space": 3727,
    "crypto": 13
  }
}
```

---

## Startup Procedures

### Option 1: Automated Startup (Recommended)
```powershell
.\START_ALL_SERVICES.ps1
```

### Option 2: Manual Startup

#### Terminal 1 - Backend
```bash
cd application/Backend
npm install  # First time only
npm start
```

#### Terminal 2 - Frontend
```bash
cd application/Frontend
npm install  # First time only
npm run dev
```

#### Terminal 3 - Storage Facility
```bash
python AI_Core_Worker/self_hosted_storage_facility_windows.py
```

#### Terminal 4 - Knowledge API
```bash
python AI_Core_Worker/knowledge_api.py
```

#### Terminal 5 - Droid API (Optional)
```bash
python application/Backend/droid_api.py
```

---

## Service Ports Reference

| Service | Port | Type | Status Endpoint |
|---------|------|------|-----------------|
| PostgreSQL | 5432 | Database | N/A |
| Backend | 3000 | Node.js | /api/health |
| Frontend | 5173 | Vite | / |
| Knowledge API | 5004 | Python/Flask | /health |
| Droid API | 5005 | Python/Flask | /health |
| Storage Facility | 3003 | Python/Flask | /api/facility/status |
| BitXtractor | 3002 | Python | /api/status |
| BlackArch | 8081 | Proxy | /api/status |

---

## Environment Configuration

### Backend (.env)
```
DB_HOST=localhost
DB_PORT=5432
DB_USER=r3aler_user_2025
DB_PASSWORD=password123
DB_NAME=r3aler_ai
JWT_SECRET=<your-secret-key>
PORT=3000
FRONTEND_URL=http://localhost:5173
```

### Knowledge API
```
STORAGE_FACILITY_URL=http://localhost:3003
KNOWLEDGE_API_PORT=5004
```

### Storage Facility
```
DATABASE_URL=postgresql://r3aler_user_2025:password123@localhost:5432/r3aler_ai
STORAGE_PORT=3003
```

---

## Troubleshooting

### Backend Won't Start
```bash
# Check if port 3000 is in use
netstat -ano | findstr :3000

# Kill process using port 3000
taskkill /PID <PID> /F

# Check Node.js installation
node --version
npm --version

# Reinstall dependencies
rm -r node_modules package-lock.json
npm install
```

### Frontend Won't Start
```bash
# Check if port 5173 is in use
netstat -ano | findstr :5173

# Clear Vite cache
rm -r node_modules/.vite

# Reinstall dependencies
npm install
```

### Database Connection Failed
```bash
# Check PostgreSQL service
Get-Service postgresql-x64-*

# Start PostgreSQL
Start-Service postgresql-x64-15

# Test connection
psql -h localhost -U r3aler_user_2025 -d r3aler_ai -c "SELECT 1"
```

### Knowledge API Not Responding
```bash
# Check if Storage Facility is running
curl http://localhost:3003/api/facility/status

# Verify Python environment
python --version
pip list | grep flask

# Check logs
tail -f logs/knowledge_api.log
```

---

## Performance Monitoring

### Check System Resources
```powershell
# CPU and Memory usage
Get-Process | Where-Object {$_.ProcessName -match "node|python"} | Select-Object ProcessName, CPU, Memory
```

### Database Performance
```sql
-- Check active connections
SELECT datname, count(*) FROM pg_stat_activity GROUP BY datname;

-- Check table sizes
SELECT schemaname, tablename, pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) 
FROM pg_tables WHERE schemaname != 'pg_catalog' ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

### API Response Times
```bash
# Measure backend response time
curl -w "Time: %{time_total}s\n" http://localhost:3000/api/health

# Measure knowledge API response time
curl -w "Time: %{time_total}s\n" http://localhost:5004/health
```

---

## Verification Checklist

- [ ] PostgreSQL database is running and accessible
- [ ] Backend server starts without errors
- [ ] Frontend dev server is serving login page
- [ ] User registration endpoint works
- [ ] User login endpoint works and returns JWT token
- [ ] JWT token can be used to access protected endpoints
- [ ] Knowledge API is running and connected to Storage Facility
- [ ] Storage Facility has 30,657+ entries
- [ ] Droid API is running (if needed)
- [ ] All API endpoints return expected responses
- [ ] CORS is properly configured
- [ ] Rate limiting is working
- [ ] Error handling is functional
- [ ] Logs are being generated
- [ ] System can handle concurrent requests

---

## Support

For issues or questions:
1. Check the logs in `logs/` directory
2. Run the verification script: `python SYSTEM_VERIFICATION.py`
3. Review the troubleshooting section above
4. Check service status: `.\QUICK_STATUS_CHECK.ps1`

---

**Last Updated:** 2025-01-30
**Version:** 1.0
