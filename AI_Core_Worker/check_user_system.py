import psycopg2

# Connect to PostgreSQL
conn = psycopg2.connect(
    host='localhost',
    port=5432,
    database='r3aler_ai',
    user='r3aler_user_2025',
    password='postgres'
)

cursor = conn.cursor()

print("\n" + "=" * 70)
print(" R3ÆLƎR AI: USER SYSTEM DATABASE STATUS")
print("=" * 70)

# Check user_unit tables
print("\n✅ USER_UNIT TABLES:")
cursor.execute("""
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema = 'user_unit' 
    ORDER BY table_name
""")
for (table,) in cursor.fetchall():
    print(f"   • user_unit.{table}")

# Check counts
print("\n📊 CURRENT DATA:")
cursor.execute("SELECT COUNT(*) FROM user_unit.profiles")
print(f"   Registered Users: {cursor.fetchone()[0]}")

cursor.execute("SELECT COUNT(*) FROM user_unit.sessions")
print(f"   Active Sessions: {cursor.fetchone()[0]}")

cursor.execute("SELECT COUNT(*) FROM user_unit.activity_log")
print(f"   Activity Logs: {cursor.fetchone()[0]}")

cursor.execute("SELECT COUNT(*) FROM user_unit.tool_preferences")
print(f"   Tool Preferences: {cursor.fetchone()[0]}")

# Show table structure
print("\n📋 user_unit.profiles STRUCTURE:")
cursor.execute("""
    SELECT column_name, data_type, is_nullable
    FROM information_schema.columns
    WHERE table_schema = 'user_unit' AND table_name = 'profiles'
    ORDER BY ordinal_position
""")
for col, dtype, nullable in cursor.fetchall():
    print(f"   • {col:20s} {dtype:20s} {'NULL' if nullable == 'YES' else 'NOT NULL'}")

print("\n📋 user_unit.activity_log STRUCTURE:")
cursor.execute("""
    SELECT column_name, data_type, is_nullable
    FROM information_schema.columns
    WHERE table_schema = 'user_unit' AND table_name = 'activity_log'
    ORDER BY ordinal_position
""")
for col, dtype, nullable in cursor.fetchall():
    print(f"   • {col:20s} {dtype:20s} {'NULL' if nullable == 'YES' else 'NOT NULL'}")

print("\n" + "=" * 70)
print(" ✅ DATABASE READY - AWAITING USER TRACKING IMPLEMENTATION")
print("=" * 70 + "\n")

conn.close()
