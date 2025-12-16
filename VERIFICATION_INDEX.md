# R3ÆLƎR AI - Verification & Testing Index

## Quick Navigation

### 📋 Start Here
- **[VERIFICATION_SUMMARY.txt](VERIFICATION_SUMMARY.txt)** - Quick overview of all components and status
- **[SYSTEM_STATUS.md](SYSTEM_STATUS.md)** - Detailed component status and configuration

### 🚀 Getting Started
1. **[START_ALL_SERVICES.ps1](START_ALL_SERVICES.ps1)** - Automated startup script (Recommended)
2. **[QUICK_STATUS_CHECK.ps1](QUICK_STATUS_CHECK.ps1)** - Quick service status verification
3. **[SYSTEM_VERIFICATION.py](SYSTEM_VERIFICATION.py)** - Complete system test suite

### 📖 Documentation
- **[SYSTEM_VERIFICATION_GUIDE.md](SYSTEM_VERIFICATION_GUIDE.md)** - Complete verification procedures
- **[README.md](README.md)** - Project overview and structure

---

## Component Verification

### Database
- **Status:** ✓ Configured
- **Type:** PostgreSQL 15+
- **Port:** 5432
- **Verification:** `psql -h localhost -U r3aler_user_2025 -d r3aler_ai -c "SELECT 1"`

### Backend Server
- **Status:** ✓ Configured
- **Type:** Node.js/Express.js
- **Port:** 3000
- **Verification:** `curl http://localhost:3000/api/health`
- **Startup:** `cd application/Backend && npm start`

### Frontend Application
- **Status:** ✓ Configured
- **Type:** React 18 + Vite
- **Port:** 5173
- **Verification:** `curl http://localhost:5173`
- **Startup:** `cd application/Frontend && npm run dev`

### Knowledge API
- **Status:** ✓ Configured
- **Type:** Python/Flask
- **Port:** 5004
- **Entries:** 30,657+
- **Verification:** `curl http://localhost:5004/health`
- **Startup:** `python AI_Core_Worker/knowledge_api.py`

### Storage Facility
- **Status:** ✓ Configured
- **Type:** Python/Flask
- **Port:** 3003
- **Entries:** 30,657+
- **Verification:** `curl http://localhost:3003/api/facility/status`
- **Startup:** `python AI_Core_Worker/self_hosted_storage_facility_windows.py`

### Droid API
- **Status:** ✓ Configured
- **Type:** Python/Flask
- **Port:** 5005
- **Verification:** `curl http://localhost:5005/health`

---

## Verification Procedures

### Option 1: Automated (Recommended)
```powershell
.\START_ALL_SERVICES.ps1
```
Starts all services and verifies they're running.

### Option 2: Quick Status Check
```powershell
.\QUICK_STATUS_CHECK.ps1
```
Checks if all services are running on their ports.

### Option 3: Complete System Test
```bash
python SYSTEM_VERIFICATION.py
```
Runs comprehensive tests on all components:
- Database connection
- Backend health
- Authentication flow
- Frontend rendering
- API endpoints
- Knowledge API
- Storage Facility
- Features

### Option 4: Manual Verification
See [SYSTEM_VERIFICATION_GUIDE.md](SYSTEM_VERIFICATION_GUIDE.md) for step-by-step manual verification.

---

## Access Points

| Component | URL | Purpose |
|-----------|-----|---------|
| Frontend | http://localhost:5173 | User interface |
| Backend API | http://localhost:3000 | REST API |
| Knowledge API | http://localhost:5004 | Knowledge search |
| Storage Facility | http://localhost:3003 | Data storage |
| Droid API | http://localhost:5005 | Crypto analysis |

---

## Authentication Testing

### Register User
```bash
curl -X POST http://localhost:3000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"TestPass123!"}'
```

### Login
```bash
curl -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"TestPass123!"}'
```

### Use Token
```bash
curl -H "Authorization: Bearer <token>" \
  http://localhost:3000/api/health
```

---

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user

### Health & Status
- `GET /api/health` - Backend health check
- `GET /api/status` - Backend status

### Knowledge
- `POST /api/kb/search` - Search knowledge base
- `GET /api/kb/stats` - Knowledge statistics
- `GET /api/kb/prompts/<type>` - Get system prompts
- `POST /api/kb/ingest` - Ingest new knowledge

### BitXtractor
- `POST /api/bitxtractor/start` - Start BitXtractor
- `GET /api/bitxtractor/status/:jobId` - Check status
- `GET /api/bitxtractor/download/:jobId` - Download results

### BlackArch
- `POST /api/blackarch/install/:tool` - Install tool
- `POST /api/blackarch/execute/:tool` - Execute tool
- `POST /api/blackarch/workflows/run` - Run workflow

---

## Troubleshooting

### Port Already in Use
```powershell
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

### Database Connection Failed
```powershell
Get-Service postgresql-x64-*
Start-Service postgresql-x64-15
```

### Frontend Not Loading
```bash
rm -r node_modules/.vite
npm install
npm run dev
```

### Knowledge API Not Responding
```bash
curl http://localhost:3003/api/facility/status
python AI_Core_Worker/knowledge_api.py
```

See [SYSTEM_VERIFICATION_GUIDE.md](SYSTEM_VERIFICATION_GUIDE.md) for more troubleshooting.

---

## Configuration

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

## Logs

**Log Locations:**
- `logs/audit.log` - Audit trail
- `logs/error.log` - Error logs
- `logs/management.log` - Management logs
- `logs/knowledge_api.log` - Knowledge API logs

---

## Performance Metrics

**Expected Response Times:**
- Backend: < 100ms
- Knowledge search: < 500ms
- Database queries: < 50ms
- Frontend load: < 2s

**Resource Usage:**
- Backend: ~50-100MB RAM
- Frontend: ~30-50MB RAM
- Knowledge API: ~100-150MB RAM
- Storage Facility: ~150-200MB RAM
- PostgreSQL: ~200-300MB RAM

---

## Verification Checklist

- [ ] PostgreSQL running and accessible
- [ ] Backend server starts without errors
- [ ] Frontend dev server serving login page
- [ ] User registration working
- [ ] User login working
- [ ] JWT tokens being generated
- [ ] Protected routes accessible with token
- [ ] Knowledge API running
- [ ] Storage Facility connected
- [ ] 30,657+ entries in database
- [ ] Droid API running
- [ ] All endpoints responding
- [ ] CORS properly configured
- [ ] Rate limiting working
- [ ] Error handling functional
- [ ] Logs being generated

---

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (React)                      │
│              http://localhost:5173                       │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│              Backend (Express.js)                        │
│              http://localhost:3000                       │
│  ┌──────────────────────────────────────────────────┐   │
│  │ Auth │ BitXtractor │ BlackArch │ Stripe │ Routes │   │
│  └──────────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
┌───────▼──┐  ┌──────▼──┐  ┌─────▼──────┐
│ Knowledge│  │ Storage │  │  Droid API │
│   API    │  │Facility │  │  (Crypto)  │
│ :5004    │  │  :3003  │  │   :5005    │
└───────┬──┘  └──────┬──┘  └─────┬──────┘
        │            │            │
        └────────────┼────────────┘
                     │
        ┌────────────▼────────────┐
        │   PostgreSQL Database   │
        │   localhost:5432        │
        │   r3aler_ai database    │
        └─────────────────────────┘
```

---

## Next Steps

1. **Review Status:** Read [VERIFICATION_SUMMARY.txt](VERIFICATION_SUMMARY.txt)
2. **Start Services:** Run `.\START_ALL_SERVICES.ps1`
3. **Verify System:** Run `python SYSTEM_VERIFICATION.py`
4. **Access Frontend:** Open http://localhost:5173
5. **Create Account:** Register new user
6. **Test Features:** Use terminal and search knowledge
7. **Monitor:** Run `.\QUICK_STATUS_CHECK.ps1` regularly

---

## Support

For detailed information:
- **Verification Guide:** [SYSTEM_VERIFICATION_GUIDE.md](SYSTEM_VERIFICATION_GUIDE.md)
- **System Status:** [SYSTEM_STATUS.md](SYSTEM_STATUS.md)
- **Summary:** [VERIFICATION_SUMMARY.txt](VERIFICATION_SUMMARY.txt)
- **Project README:** [README.md](README.md)

---

**System Status: ✓ READY FOR VERIFICATION**

All components are configured and ready to be started and verified.

---

*Last Updated: 2025-01-30*  
*Version: 1.0*  
*R3ÆLƎR AI - Advanced AI System*
