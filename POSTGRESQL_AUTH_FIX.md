# PostgreSQL Authentication Fix - Troubleshooting Guide

## Error: "password authentication failed for user 'r3aler_user_2025'"

This error occurs when:
1. The user account doesn't exist in PostgreSQL
2. The password is incorrect
3. PostgreSQL authentication method is not configured correctly

---

## SOLUTION A: Using PostgreSQL Command Line (Recommended)

### Step 1: Open PostgreSQL Admin
```bash
# Open Command Prompt as Administrator
# Navigate to PostgreSQL bin directory
cd "C:\Program Files\PostgreSQL\15\bin"

# Connect as postgres user
psql -U postgres
```

### Step 2: Create/Reset User
```sql
-- Option A: Create new user (if doesn't exist)
CREATE USER r3aler_user_2025 WITH PASSWORD 'R3AL3RAdmin816';

-- Option B: Reset existing user password
ALTER USER r3aler_user_2025 WITH PASSWORD 'R3AL3RAdmin816';

-- Create database if needed
CREATE DATABASE r3aler_ai OWNER r3aler_user_2025;

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE r3aler_ai TO r3aler_user_2025;
GRANT ALL PRIVILEGES ON SCHEMA public TO r3aler_ai TO r3aler_user_2025;

-- Verify
\du r3aler_user_2025
\l r3aler_ai

-- Exit
\q
```

### Step 3: Test Connection
```bash
psql -h 127.0.0.1 -U r3aler_user_2025 -d r3aler_ai -W
# Password: R3AL3RAdmin816
```

---

## SOLUTION B: Using pgAdmin (GUI)

1. Open pgAdmin
2. Navigate to Servers → {Your PostgreSQL Server}
3. Right-click on "Login/Group Roles" → Create → Login/Group Role
4. Enter details:
   - Name: r3aler_user_2025
   - Password: R3AL3RAdmin816
   - Confirm password: R3AL3RAdmin816
5. Click "Save"
6. Right-click on r3aler_user_2025 → Properties
7. Go to "Privileges" tab:
   - Toggle ON: Can login
8. In Databases section, right-click r3aler_ai:
   - Click Grant Wizard
   - Select r3aler_user_2025
   - Grant all privileges

---

## SOLUTION C: Using Python (Automated)

```python
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Connect as superuser (postgres)
conn = psycopg2.connect(
    host='127.0.0.1',
    port=5432,
    database='postgres',
    user='postgres',
    password='postgres_password'  # Change this to your postgres password
)
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cursor = conn.cursor()

# Create user
try:
    cursor.execute("""
        CREATE USER r3aler_user_2025 WITH PASSWORD 'R3AL3RAdmin816'
    """)
    print("User created successfully")
except Exception as e:
    print(f"User creation failed: {e}")

# Create database
try:
    cursor.execute("""
        CREATE DATABASE r3aler_ai OWNER r3aler_user_2025
    """)
    print("Database created successfully")
except Exception as e:
    print(f"Database creation failed: {e}")

# Grant privileges
try:
    cursor.execute("""
        GRANT ALL PRIVILEGES ON DATABASE r3aler_ai TO r3aler_user_2025
    """)
    print("Privileges granted successfully")
except Exception as e:
    print(f"Grant privileges failed: {e}")

cursor.close()
conn.close()
```

---

## COMMON ISSUES & SOLUTIONS

### Issue 1: PostgreSQL Service Not Running
**Solution:**
```powershell
# Check status
Get-Service postgresql-x64-15 -ErrorAction SilentlyContinue

# Start service
Start-Service postgresql-x64-15

# Or use Services GUI:
# Services.msc → Find PostgreSQL → Right-click → Start
```

### Issue 2: "FATAL: remaining connection slots are reserved"
**Solution:** Restart PostgreSQL service and retry

### Issue 3: "role 'r3aler_user_2025' does not exist"
**Solution:** The user doesn't exist yet - create it using Step 2 above

### Issue 4: "pg_hba.conf" authentication method issue
**Solution:** Edit PostgreSQL's pg_hba.conf:
```
# Location: C:\Program Files\PostgreSQL\15\data\pg_hba.conf
# Change line:
host    all             all             127.0.0.1/32            md5
# To:
host    all             all             127.0.0.1/32            password
# Or:
host    all             all             127.0.0.1/32            scram-sha-256
# Then restart PostgreSQL service
```

---

## VERIFICATION CHECKLIST

After applying the fix:

- [ ] PostgreSQL service is running
- [ ] User 'r3aler_user_2025' exists
- [ ] User password is 'R3AL3RAdmin816'
- [ ] Database 'r3aler_ai' exists
- [ ] User has CONNECT privilege on database
- [ ] User has CREATE privilege on schema public
- [ ] Can connect with: `psql -h 127.0.0.1 -U r3aler_user_2025 -d r3aler_ai`

---

## RESTART R3ÆLƎR AI SERVICES

After fixing PostgreSQL:

```powershell
# Kill running Python processes
Get-Process python | Stop-Process -Force

# Restart all services
python management_api_secured.py &
python user_auth_api_secured.py &
python knowledge_api.py &
python application/Backend/droid_api.py &
python self_hosted_storage_facility_secured.py &
```

---

## TEST API CONNECTIVITY

```bash
# Test Knowledge API
curl -X POST http://localhost:5004/api/query \
  -H "Content-Type: application/json" \
  -d '{"query":"test"}'

# Should return successful response
```

---

## SUPPORT

If issues persist:
1. Check PostgreSQL logs: C:\Program Files\PostgreSQL\15\data\pg_log\
2. Verify .env.local has correct credentials
3. Check firewall isn't blocking port 5432
4. Ensure PostgreSQL is listening on 127.0.0.1:5432
