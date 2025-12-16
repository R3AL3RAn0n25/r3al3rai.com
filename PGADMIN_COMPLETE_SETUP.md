# 🔧 Complete PGAdmin 4 Setup Guide for R3ALER AI

## ❌ Step 1: Remove Incorrect Server Connection

If you already have a server configured in PGAdmin that's not showing the correct data:

1. **Open PGAdmin 4**
2. In the left Browser panel, find your existing server connection
3. **Right-click** on the server name → **Remove/Delete Server**
4. Confirm the deletion (this only removes the connection, not the database)

---

## ✅ Step 2: Add Correct Server Connection

### Click "Add New Server"

1. **Right-click "Servers"** in the left panel
2. Select **"Register" → "Server..."**

### General Tab
```
Name: R3ALER AI PostgreSQL
```

### Connection Tab
```
Host name/address: localhost
Port:              5432
Maintenance database: postgres
Username:          postgres
Password:          postgres
Save password:     ✓ (Check this box)
```

### Advanced Tab (Optional)
```
DB restriction:    r3aler_ai
```
This will show only the R3ALER AI database by default.

### Click "Save"

---

## 📊 Step 3: Verify Database Structure

After connecting, you should see:

### Database: `r3aler_ai`
Owner: `r3aler_user_2025`

### Current Tables (7):
1. **users** - User accounts and authentication
2. **subscription_tiers** - Subscription plans
3. **security_events** - Security audit logs
4. **blocked_ips** - IP blacklist
5. **auth_attempts** - Login attempt tracking
6. **heart_storage** - Health monitoring data
7. **treadmill_logs** - Activity logs

### ⚠️ MISSING TABLES (Droid API):
- **droid_profiles** - User AI personalization data
- **droid_interactions** - Chat history and learning data

**These tables will be created automatically when you start the Droid API for the first time.**

---

## 🔍 Step 4: Browse Your Data

### To view table contents:
1. Expand **Servers → R3ALER AI PostgreSQL**
2. Expand **Databases → r3aler_ai**
3. Expand **Schemas → public**
4. Expand **Tables**
5. **Right-click any table** → **View/Edit Data** → **All Rows**

### Quick Queries in Query Tool:

**Open Query Tool:**
- Right-click on `r3aler_ai` database → **Query Tool**

**Sample Queries:**

```sql
-- Check all users
SELECT id, username, email, created_at FROM users;

-- Check subscription tiers
SELECT * FROM subscription_tiers;

-- View recent security events
SELECT * FROM security_events ORDER BY timestamp DESC LIMIT 10;

-- Count records in each table
SELECT 
    'users' as table_name, COUNT(*) as records FROM users
UNION ALL SELECT 'auth_attempts', COUNT(*) FROM auth_attempts
UNION ALL SELECT 'blocked_ips', COUNT(*) FROM blocked_ips
UNION ALL SELECT 'security_events', COUNT(*) FROM security_events
UNION ALL SELECT 'subscription_tiers', COUNT(*) FROM subscription_tiers
UNION ALL SELECT 'heart_storage', COUNT(*) FROM heart_storage
UNION ALL SELECT 'treadmill_logs', COUNT(*) FROM treadmill_logs;

-- Database size
SELECT 
    pg_size_pretty(pg_database_size('r3aler_ai')) as database_size;
```

---

## 🐛 Troubleshooting

### Issue: "Could not connect to server"
**Solution:**
1. Verify PostgreSQL service is running:
   ```powershell
   Get-Service postgresql-x64-17
   ```
2. If stopped, start it:
   ```powershell
   Start-Service postgresql-x64-17
   ```

### Issue: "Password authentication failed"
**Solution:**
1. Use username: `postgres`
2. Use password: `postgres`
3. If that doesn't work, your postgres password may be different

### Issue: "Database doesn't exist"
**Solution:**
The database `r3aler_ai` already exists. Make sure you're connecting to the right server (localhost:5432).

### Issue: "Don't see Droid tables"
**Solution:**
The Droid API creates these tables on first startup. To create them now:

```sql
-- Run this in PGAdmin Query Tool
CREATE TABLE IF NOT EXISTS droid_profiles (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL UNIQUE,
    likes JSONB DEFAULT '[]'::jsonb,
    dislikes JSONB DEFAULT '[]'::jsonb,
    habits JSONB DEFAULT '[]'::jsonb,
    financial_goals JSONB DEFAULT '[]'::jsonb,
    interaction_count INTEGER DEFAULT 0,
    adaptability_level INTEGER DEFAULT 0,
    last_interaction TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS droid_interactions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    message TEXT NOT NULL,
    intent VARCHAR(50),
    context JSONB DEFAULT '{}'::jsonb,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_droid_profiles_user_id ON droid_profiles(user_id);
CREATE INDEX IF NOT EXISTS idx_droid_interactions_user_id ON droid_interactions(user_id);
CREATE INDEX IF NOT EXISTS idx_droid_interactions_timestamp ON droid_interactions(timestamp);
```

---

## 📋 Connection Summary

| Parameter | Value |
|-----------|-------|
| Host | localhost |
| Port | 5432 |
| Database | r3aler_ai |
| Username | postgres |
| Password | postgres |
| Owner | r3aler_user_2025 |

---

## 🎯 What You Should See

After proper setup, PGAdmin should show:

```
Servers
└── R3ALER AI PostgreSQL
    └── Databases (4)
        ├── postgres (system)
        ├── template0 (system)
        ├── template1 (system)
        └── r3aler_ai ⭐ (YOUR DATABASE)
            └── Schemas
                └── public
                    ├── Tables (7-9)
                    │   ├── auth_attempts
                    │   ├── blocked_ips
                    │   ├── droid_interactions (after Droid API starts)
                    │   ├── droid_profiles (after Droid API starts)
                    │   ├── heart_storage
                    │   ├── security_events
                    │   ├── subscription_tiers
                    │   ├── treadmill_logs
                    │   └── users
                    └── Views, Functions, etc.
```

---

## 🚀 Quick Start Commands

**After setting up PGAdmin, test your connection:**

```sql
-- Test 1: Check database version
SELECT version();

-- Test 2: List all tables
SELECT tablename FROM pg_tables WHERE schemaname = 'public';

-- Test 3: Check database size
SELECT pg_size_pretty(pg_database_size(current_database()));

-- Test 4: View table row counts
SELECT 
    schemaname,
    tablename,
    n_tup_ins as "rows_inserted",
    n_tup_upd as "rows_updated",
    n_tup_del as "rows_deleted"
FROM pg_stat_user_tables
WHERE schemaname = 'public'
ORDER BY tablename;
```

---

## 💡 Pro Tips

1. **Bookmark Frequently Used Queries**: Save your common queries in PGAdmin
2. **Use Query History**: Press F7 in Query Tool to see previous queries
3. **Export Data**: Right-click table → Import/Export to backup data
4. **Auto-refresh**: Enable auto-refresh in table view for real-time monitoring
5. **Create Dashboard**: Use the Dashboard tab to monitor database performance

---

## 📞 Need Help?

If you're still not seeing the correct data:
1. Verify you're connected to `localhost:5432`
2. Check the database name is `r3aler_ai`
3. Make sure PostgreSQL service is running
4. Try refreshing the browser tree (Right-click → Refresh)

**Current Status:**
- ✅ PostgreSQL 17 running
- ✅ Database `r3aler_ai` exists
- ✅ 7 tables present (Backend tables)
- ⏳ 2 tables pending (Droid API tables - will be created on first Droid API startup)
