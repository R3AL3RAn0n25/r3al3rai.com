# How to Access R3ALER AI Database in PGAdmin

## Connection Details

**Server/Host Information:**
- **Host**: `localhost` (or `127.0.0.1`)
- **Port**: `5432`
- **Database**: `r3aler_ai`
- **Username**: `r3aler_user_2025`
- **Password**: `postgres`

## Step-by-Step Guide

### 1. Open PGAdmin
- Launch PGAdmin 4 from your Windows Start menu

### 2. Create/Register Server (First Time Only)
If you haven't already connected to this server:

1. Right-click on **"Servers"** in the left panel
2. Select **"Register" → "Server..."**

**General Tab:**
- Name: `R3ALER AI - Local` (or any name you prefer)

**Connection Tab:**
- Host name/address: `localhost`
- Port: `5432`
- Maintenance database: `postgres`
- Username: `r3aler_user_2025`
- Password: `postgres`
- ☑ Save password (optional)

**SSL Tab:**
- SSL mode: `Prefer` (default is fine)

3. Click **"Save"**

### 3. Access the Database
Once connected, navigate in the left tree panel:

```
Servers
└── R3ALER AI - Local (or your server name)
    └── Databases
        └── r3aler_ai          ← Your application database
            └── Schemas
                └── public
                    └── Tables  ← Your 7 tables are here
```

### 4. View Tables
Expand the tree to see your tables:
- `auth_attempts`
- `blocked_ips`
- `heart_storage`
- `security_events`
- `subscription_tiers`
- `treadmill_logs`
- `users`

### 5. Query Data
Right-click on any table and select:
- **"View/Edit Data" → "All Rows"** - See table contents in grid
- **"Query Tool"** - Run custom SQL queries

Or click on the database name and use **Tools → Query Tool** to run SQL:

```sql
-- View all users
SELECT * FROM users;

-- View subscription tiers
SELECT * FROM subscription_tiers;

-- View security events
SELECT * FROM security_events ORDER BY timestamp DESC LIMIT 100;
```

### 6. Quick Access to Query Tool
- Select `r3aler_ai` database in the tree
- Press `Alt + Shift + Q` (Windows shortcut)
- Or click the ⚡ Query Tool icon in the toolbar

## Common Tasks in PGAdmin

### View Table Structure
Right-click table → **"Properties"** → **"Columns"** tab

### See Current Data
Right-click table → **"View/Edit Data"** → **"All Rows"**

### Run SQL Queries
1. Select `r3aler_ai` database
2. Click **Tools** → **Query Tool**
3. Type your SQL
4. Press **F5** or click ▶ Execute button

### Export Data
1. Right-click table
2. Select **"Import/Export Data..."**
3. Choose format (CSV, etc.)

### Monitor Database Size
Right-click `r3aler_ai` → **"Properties"** → **"Statistics"** tab

## Troubleshooting

**Can't connect?**
- Verify PostgreSQL service is running:
  ```powershell
  Get-Service postgresql-x64-17
  ```
- Check connection details match above
- Try password: `postgres` or `R3@l3r_dfe8q9wpxn3m`

**Don't see tables?**
- Make sure you're looking under: `Databases → r3aler_ai → Schemas → public → Tables`
- Click refresh icon (🔄) in PGAdmin

**Permission denied?**
- You're logged in as `r3aler_user_2025` who owns all tables
- This should not happen with correct username/password

## Quick Reference

| What | Where in PGAdmin |
|------|------------------|
| View all tables | r3aler_ai → Schemas → public → Tables |
| Run SQL queries | Tools → Query Tool (or Alt+Shift+Q) |
| View table data | Right-click table → View/Edit Data → All Rows |
| See indexes | r3aler_ai → Schemas → public → Tables → [table] → Indexes |
| Database size | Right-click r3aler_ai → Properties → Statistics |
