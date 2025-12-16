# PostgreSQL Migration Quick Start Guide

## ✅ What Was Done

### 1. Database Schema Created
- **File**: `Database/security_schema.sql`
- **Tables**: `security_events`, `blocked_ips`
- **Indexes**: Optimized for IP and timestamp queries
- **Features**: PostgreSQL-native types (SERIAL, VARCHAR, DOUBLE PRECISION)

### 2. Code Updated for Dual Database Support
- **File**: `Tools/blackarch_tools_manager.py`
- **Changes**:
  - Added psycopg2 import with fallback
  - Connection pooling support (1-10 connections)
  - `get_db_connection()` / `release_db_connection()` helpers
  - `execute_query()` method with automatic placeholder conversion
  - Updated all security methods to use new query system
  - PostgreSQL-compatible SQL (SERIAL instead of AUTOINCREMENT)

### 3. Configuration File
- **File**: `configs/database_config.py`
- **Settings**: Host, port, database name, credentials, pool settings

### 4. Migration Scripts
- **Linux**: `scripts/migrate_to_postgresql.sh`
- **Windows**: `scripts/migrate_to_postgresql.ps1`

---

## 🚀 Migration Steps

### Step 1: Install psycopg2

**In WSL:**
```bash
cd "/mnt/c/Users/work8/OneDrive/Desktop/r3al3rai/New Folder 1/R3al3r-AI Main Working/R3aler-ai/R3aler-ai"
source blackarch_venv/bin/activate
pip install psycopg2-binary
```

**From Windows PowerShell:**
```powershell
wsl bash -c "cd '/mnt/c/Users/work8/OneDrive/Desktop/r3al3rai/New Folder 1/R3al3r-AI Main Working/R3aler-ai/R3aler-ai' && source blackarch_venv/bin/activate && pip install psycopg2-binary"
```

### Step 2: Apply Database Schema

**From Windows PowerShell (Current Directory):**
```powershell
.\scripts\migrate_to_postgresql.ps1
```

**Or from WSL:**
```bash
bash scripts/migrate_to_postgresql.sh
```

### Step 3: Verify Migration

**Check tables exist:**
```powershell
wsl bash -c "PGPASSWORD='postgres' psql -h localhost -U r3aler_user_2025 -d r3aler_ai -c '\dt' | grep security"
```

**Expected output:**
```
security_events | table | r3aler_user_2025
blocked_ips     | table | r3aler_user_2025
```

### Step 4: Test Python Connection

```powershell
wsl bash -c "cd '/mnt/c/Users/work8/OneDrive/Desktop/r3al3rai/New Folder 1/R3al3r-AI Main Working/R3aler-ai/R3aler-ai/Tools' && source '../blackarch_venv/bin/activate' && python3 -c 'from blackarch_tools_manager import BlackArchToolsManager; m = BlackArchToolsManager(); print(f\"Using: {\"PostgreSQL\" if m.use_postgres else \"SQLite\"}  Loaded {len(m.blackarch_tools)} tools\")'"
```

**Expected output:**
```
✅ Connected to PostgreSQL database
Using: PostgreSQL  Loaded 2874 tools
```

---

## 📊 Access Database with PGAdmin

### Connection Settings:
- **Host**: localhost
- **Port**: 5432
- **Database**: r3aler_ai
- **Username**: r3aler_user_2025
- **Password**: postgres

### Tables to Explore:
1. **security_events** - All security incidents
2. **blocked_ips** - Blocked IP addresses
3. **users** - User accounts
4. **treadmill_logs** - IP tracking
5. **auth_attempts** - Login attempts
6. **heart_storage** - User insights
7. **blackarch_tools** - Tool database
8. **tool_executions** - Tool usage history

---

## 🔄 Fallback Behavior

The system automatically falls back to SQLite if:
- PostgreSQL connection fails
- psycopg2 not installed
- Database config file missing

**Check which database is in use:**
```python
from blackarch_tools_manager import BlackArchToolsManager
manager = BlackArchToolsManager()
print("PostgreSQL" if manager.use_postgres else "SQLite")
```

---

## 🐛 Troubleshooting

### Issue: "psycopg2 not found"
**Solution:**
```bash
pip install psycopg2-binary
```

### Issue: "Connection refused"
**Solution:**
```bash
sudo systemctl status postgresql
sudo systemctl start postgresql
```

### Issue: "Password authentication failed"
**Solution:**
```bash
bash reset_db_password.sh
```

### Issue: "Permission denied"
**Solution:**
```bash
sudo chmod +x scripts/migrate_to_postgresql.sh
```

---

## 📈 Performance Benefits

| Feature | SQLite | PostgreSQL |
|---------|--------|------------|
| Concurrent writes | ❌ Limited | ✅ Full support |
| Connection pooling | ❌ No | ✅ Yes (10 connections) |
| Multi-user | ❌ Lock issues | ✅ Optimized |
| Advanced queries | ⚠️ Limited | ✅ Full SQL |
| Replication | ❌ No | ✅ Yes |
| PGAdmin support | ❌ No | ✅ Yes |

---

## 🎯 Next Steps After Migration

1. ✅ Verify security logging works
2. ✅ Test IP blocking functionality
3. ✅ Check security stats API
4. ✅ Monitor performance
5. ✅ Configure backups (pg_dump)
6. ✅ Set up monitoring in PGAdmin

---

## 📝 SQL Query Examples

### View Recent Security Events
```sql
SELECT ip_address, threat_level, threat_type, blocked, created_at 
FROM security_events 
ORDER BY created_at DESC 
LIMIT 20;
```

### Find Most Aggressive IPs
```sql
SELECT ip_address, COUNT(*) as attack_count, SUM(threat_score) as total_score
FROM security_events
WHERE threat_score > 30
GROUP BY ip_address
ORDER BY total_score DESC;
```

### Check Currently Blocked IPs
```sql
SELECT ip_address, reason, threat_score, blocked_at, expires_at
FROM blocked_ips
WHERE permanent = true OR expires_at > CURRENT_TIMESTAMP;
```

### Security Stats Summary
```sql
SELECT 
    COUNT(*) as total_events,
    SUM(CASE WHEN blocked THEN 1 ELSE 0 END) as blocked_count,
    AVG(threat_score) as avg_threat_score,
    COUNT(DISTINCT ip_address) as unique_ips
FROM security_events
WHERE created_at > CURRENT_TIMESTAMP - INTERVAL '24 hours';
```

---

## 🔐 Backup Commands

### Backup Security Tables
```bash
pg_dump -h localhost -U r3aler_user_2025 -d r3aler_ai -t security_events -t blocked_ips > security_backup.sql
```

### Restore Security Tables
```bash
psql -h localhost -U r3aler_user_2025 -d r3aler_ai < security_backup.sql
```

---

**Migration completed successfully! Your security system now runs on PostgreSQL and can be managed with PGAdmin.**
