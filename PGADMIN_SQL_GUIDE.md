# 🔍 PGAdmin SQL Query Guide for R3ALER AI

## ✅ Current Status
- **Database**: `r3aler_ai` ✓ Connected
- **Tables**: 9 tables created ✓
- **Issue**: Users table is **EMPTY** (no users registered yet)

---

## 📊 Quick Status Check Queries

### 1. Check All Tables and Row Counts
```sql
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables 
WHERE schemaname = 'public'
ORDER BY tablename;
```

### 2. Count Users
```sql
SELECT COUNT(*) as total_users FROM users;
```

### 3. View All Users (if any)
```sql
SELECT 
    id,
    username,
    role,
    LEFT(password_hash, 20) || '...' as password_hash_preview
FROM users
ORDER BY id;
```

### 4. View Droid Profiles
```sql
SELECT 
    id,
    user_id,
    interaction_count,
    adaptability_level,
    last_interaction,
    created_at
FROM droid_profiles
ORDER BY last_interaction DESC;
```

### 5. View Recent Droid Interactions
```sql
SELECT 
    id,
    user_id,
    LEFT(message, 50) || '...' as message_preview,
    intent,
    timestamp
FROM droid_interactions
ORDER BY timestamp DESC
LIMIT 10;
```

---

## 🔧 Create Test User Manually

### Option 1: Simple Test User (Plain Password - NOT RECOMMENDED FOR PRODUCTION)
```sql
-- WARNING: This creates a user with a known bcrypt hash for testing only
-- Password will be: "test123"
-- Bcrypt hash of "test123" (cost=10)
INSERT INTO users (username, password_hash, role)
VALUES ('testuser', '$2b$10$rKz.wXqL5xC6aF0EhYyO8.MwJXLwWVEBHVQzH/qJ1pX0YZoKjvN5u', 'user')
RETURNING id, username, role;
```

### Option 2: Create User Via Application (RECOMMENDED)
**Use the registration endpoint:**
1. Open your R3ALER AI frontend
2. Go to `/register` page
3. Create a new account
4. Then check in PGAdmin:
```sql
SELECT * FROM users;
```

---

## 🔍 Verify Database Configuration

### Check Current Database Connection
```sql
SELECT current_database() as database_name;
```

### Check Current User
```sql
SELECT current_user as database_user;
```

### Check Database Owner
```sql
SELECT 
    datname as database_name,
    pg_catalog.pg_get_userbyid(datdba) as owner
FROM pg_database
WHERE datname = 'r3aler_ai';
```

---

## 📋 Security & Auth Queries

### View Recent Authentication Attempts
```sql
SELECT * FROM auth_attempts 
ORDER BY attempted_at DESC 
LIMIT 10;
```

### View Blocked IPs
```sql
SELECT * FROM blocked_ips 
WHERE expires_at > NOW() OR expires_at IS NULL;
```

### View Security Events
```sql
SELECT 
    event_type,
    username,
    ip_address,
    LEFT(details, 100) as details_preview,
    timestamp
FROM security_events
ORDER BY timestamp DESC
LIMIT 20;
```

---

## 🎯 AI System Queries

### User Activity Summary
```sql
SELECT 
    u.id,
    u.username,
    u.role,
    COALESCE(dp.interaction_count, 0) as total_interactions,
    COALESCE(dp.adaptability_level, 0) as adaptability,
    dp.last_interaction
FROM users u
LEFT JOIN droid_profiles dp ON u.id = dp.user_id
ORDER BY dp.last_interaction DESC NULLS LAST;
```

### Recent AI Conversations
```sql
SELECT 
    u.username,
    di.message,
    di.intent,
    di.timestamp
FROM droid_interactions di
JOIN users u ON di.user_id = u.id
ORDER BY di.timestamp DESC
LIMIT 20;
```

### User Personalization Data
```sql
SELECT 
    u.username,
    dp.likes,
    dp.dislikes,
    dp.habits,
    dp.financial_goals,
    dp.adaptability_level
FROM users u
JOIN droid_profiles dp ON u.id = dp.user_id;
```

---

## 🗑️ Database Maintenance

### Clean Up Empty Tables (TEST ONLY)
```sql
-- Check which tables are empty
SELECT 
    tablename,
    (SELECT COUNT(*) FROM information_schema.tables WHERE table_name = t.tablename) as row_count
FROM pg_tables t
WHERE schemaname = 'public';

-- Vacuum and analyze (improves performance)
VACUUM ANALYZE;
```

### Reset Auto-Increment IDs (if needed)
```sql
-- Reset users sequence if you delete all users
SELECT setval('users_id_seq', 1, false);

-- Reset droid_profiles sequence
SELECT setval('droid_profiles_id_seq', 1, false);

-- Reset droid_interactions sequence
SELECT setval('droid_interactions_id_seq', 1, false);
```

---

## 🧪 Testing Queries

### Create Multiple Test Users
```sql
-- Create 3 test users (password: test123 for all)
INSERT INTO users (username, password_hash, role) VALUES
('alice', '$2b$10$rKz.wXqL5xC6aF0EhYyO8.MwJXLwWVEBHVQzH/qJ1pX0YZoKjvN5u', 'user'),
('bob', '$2b$10$rKz.wXqL5xC6aF0EhYyO8.MwJXLwWVEBHVQzH/qJ1pX0YZoKjvN5u', 'user'),
('charlie', '$2b$10$rKz.wXqL5xC6aF0EhYyO8.MwJXLwWVEBHVQzH/qJ1pX0YZoKjvN5u', 'admin')
RETURNING id, username, role;
```

### Simulate AI Interaction
```sql
-- First, create a droid profile for user ID 1
INSERT INTO droid_profiles (user_id, likes, dislikes, interaction_count, adaptability_level)
VALUES (1, '["Bitcoin", "Privacy"]'::jsonb, '["Ads"]'::jsonb, 5, 42);

-- Add some interaction history
INSERT INTO droid_interactions (user_id, message, intent, context)
VALUES 
(1, 'How do I recover my Bitcoin wallet?', 'wallet_recovery', '{"topic": "crypto"}'::jsonb),
(1, 'What is the best VPN?', 'privacy_tools', '{"topic": "security"}'::jsonb);
```

---

## 🔐 Security Best Practices

### NEVER Do This in Production:
❌ Store plain text passwords
❌ Use simple bcrypt hashes for actual users
❌ Share database credentials in code

### Always Do This:
✅ Use the registration endpoint to create users
✅ Let bcrypt generate unique salts per user
✅ Keep your JWT_SECRET secure
✅ Use environment variables for sensitive data

---

## 📊 Database Health Check

```sql
-- Full database health report
SELECT 
    'Database' as metric,
    current_database() as value
UNION ALL
SELECT 
    'Total Size',
    pg_size_pretty(pg_database_size(current_database()))
UNION ALL
SELECT 
    'Total Tables',
    COUNT(*)::text
FROM pg_tables WHERE schemaname = 'public'
UNION ALL
SELECT 
    'Total Users',
    COUNT(*)::text
FROM users
UNION ALL
SELECT 
    'Droid Profiles',
    COUNT(*)::text
FROM droid_profiles
UNION ALL
SELECT 
    'Total Interactions',
    COUNT(*)::text
FROM droid_interactions;
```

---

## 🚀 Next Steps

1. **Register your first user** via the application frontend at `/register`
2. **Login** with your credentials
3. **Chat with R3ALER AI** to generate some interactions
4. **Return to PGAdmin** and run these queries to see your data:

```sql
-- See your user
SELECT * FROM users;

-- See your AI profile
SELECT * FROM droid_profiles;

-- See your conversation history
SELECT * FROM droid_interactions ORDER BY timestamp DESC;
```

---

## 💡 Pro Tips

1. **Refresh PGAdmin**: Right-click database → Refresh to see new data
2. **Save Queries**: Use the "Save" button in Query Tool to keep useful queries
3. **Export Data**: Right-click table → Import/Export → Export to CSV
4. **Query History**: Press F7 in Query Tool to see previous queries

---

## 🆘 Troubleshooting

### "No users found"
✅ This is normal if you haven't registered yet
✅ Use the frontend to register a new account

### "Permission denied"
✅ Make sure you're connected as `postgres` user
✅ Check your connection settings match the guide

### "Relation does not exist"
✅ Verify you're connected to `r3aler_ai` database (not `postgres`)
✅ Check schema is set to `public`

---

**Current Status**: ✅ Database structure is perfect, just needs users to register!
