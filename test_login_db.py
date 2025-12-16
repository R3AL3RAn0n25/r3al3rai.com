import psycopg2
import requests

# Test database connection and structure
try:
    conn = psycopg2.connect(
        host='localhost',
        database='r3aler_ai',
        user='r3aler_user_2025',
        password='postgres'
    )
    cur = conn.cursor()
    
    # Check table structure
    print("=== Users Table Structure ===")
    cur.execute("""
        SELECT column_name, data_type 
        FROM information_schema.columns 
        WHERE table_name = 'users'
        ORDER BY ordinal_position
    """)
    columns = cur.fetchall()
    for col in columns:
        print(f"  {col[0]}: {col[1]}")
    
    # Check if test user exists
    print("\n=== Checking for 'test' user ===")
    cur.execute("SELECT id, username, password_hash FROM users WHERE username = %s", ('test',))
    user = cur.fetchone()
    if user:
        print(f"  User found: ID={user[0]}, Username={user[1]}")
        print(f"  Password hash: {user[2][:50]}...")
    else:
        print("  User 'test' NOT found in database")
    
    cur.close()
    conn.close()
    
    print("\n=== Testing Login API ===")
    r = requests.post('http://localhost:3002/api/auth/login', 
                     json={'username': 'test', 'password': 'pass123'})
    print(f"  Status: {r.status_code}")
    print(f"  Response: {r.text}")
    
except Exception as e:
    print(f"ERROR: {e}")
