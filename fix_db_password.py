#!/usr/bin/env python3
"""
R3ÆLƎR AI - PostgreSQL Authentication Fix
Resets database user password and validates connection
"""

import os
import sys
import subprocess
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env.local')

DB_HOST = os.getenv('DB_HOST', '127.0.0.1')
DB_PORT = int(os.getenv('DB_PORT', 5432))
DB_NAME = os.getenv('DB_NAME', 'r3aler_ai')
DB_USER = os.getenv('DB_USER', 'r3aler_user_2025')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'R3AL3RAdmin816')

def attempt_connection():
    """Test the current database connection"""
    print("\n" + "="*60)
    print("R3ÆLƎR AI - DATABASE CONNECTION TEST")
    print("="*60 + "\n")
    
    print(f"Attempting connection to PostgreSQL...")
    print(f"  Host: {DB_HOST}:{DB_PORT}")
    print(f"  Database: {DB_NAME}")
    print(f"  User: {DB_USER}")
    
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            connect_timeout=5
        )
        print("\n✓ Connection SUCCESSFUL" + "\n")
        conn.close()
        return True
    except psycopg2.OperationalError as e:
        print(f"\n✗ Connection FAILED")
        print(f"  Error: {e}\n")
        return False
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}\n")
        return False

def reset_postgres_user():
    """Attempt to reset user password using psql"""
    print("\nAttempting to reset user password using psql...\n")
    
    # Build the SQL command
    sql_command = f"ALTER USER {DB_USER} WITH PASSWORD '{DB_PASSWORD}';"
    
    # Try to find psql
    psql_paths = [
        'psql',  # In PATH
        'C:\\Program Files\\PostgreSQL\\15\\bin\\psql.exe',
        'C:\\Program Files\\PostgreSQL\\14\\bin\\psql.exe',
        'C:\\Program Files\\PostgreSQL\\13\\bin\\psql.exe',
        'C:\\Program Files (x86)\\PostgreSQL\\15\\bin\\psql.exe',
    ]
    
    psql_exe = None
    for path in psql_paths:
        if os.path.exists(path) or path == 'psql':
            try:
                result = subprocess.run([path, '--version'], capture_output=True, timeout=2)
                if result.returncode == 0:
                    psql_exe = path
                    print(f"✓ Found psql: {path}")
                    break
            except:
                continue
    
    if not psql_exe:
        print("✗ Could not find psql executable")
        print("  Please ensure PostgreSQL is installed and in PATH")
        return False
    
    print(f"\nNote: You may need to enter the PostgreSQL superuser password")
    print("(Usually the password for the 'postgres' user)\n")
    
    return True

def create_connection_string():
    """Generate and display a connection string"""
    print("\n" + "="*60)
    print("DATABASE CONNECTION STRING")
    print("="*60 + "\n")
    
    connstr = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    print(f"Connection String:")
    print(f"  {connstr}\n")
    
    # Also show for SQLAlchemy if needed
    sqlalchemy_url = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    print(f"SQLAlchemy URL:")
    print(f"  {sqlalchemy_url}\n")

def main():
    print("\n" + "╔" + "="*58 + "╗")
    print("║" + " "*58 + "║")
    print("║" + "  R3ÆLƎR AI - PostgreSQL Authentication Fix".center(58) + "║")
    print("║" + " "*58 + "║")
    print("╚" + "="*58 + "╝\n")
    
    # Test current connection
    if attempt_connection():
        print("SUCCESS: Database connection is working correctly!")
        print("\nNo fixes needed. R3ÆLƎR AI APIs can proceed with normal operation.")
        return 0
    
    # Connection failed - attempt to fix
    print("\nConnection failed. Attempting to fix...\n")
    
    reset_postgres_user()
    
    print("\n" + "="*60)
    print("MANUAL FIX REQUIRED")
    print("="*60 + "\n")
    
    print("To fix the authentication error, you need to:")
    print("")
    print("1. Open PostgreSQL client (psql) as administrator:")
    print(f"   psql -U postgres -h {DB_HOST} -p {DB_PORT}")
    print("")
    print("2. Run this SQL command to reset the user password:")
    print(f"   ALTER USER {DB_USER} WITH PASSWORD '{DB_PASSWORD}';")
    print("")
    print("3. Or create the user if it doesn't exist:")
    print(f"   CREATE USER {DB_USER} WITH PASSWORD '{DB_PASSWORD}';")
    print(f"   GRANT ALL PRIVILEGES ON DATABASE {DB_NAME} TO {DB_USER};")
    print("")
    print("4. Verify the user was created:")
    print(f"   \\du {DB_USER}")
    print("")
    print("5. After fixing, test the connection again:")
    print("   python fix_db_password.py")
    print("")
    
    create_connection_string()
    
    print("="*60)
    print("TROUBLESHOOTING CHECKLIST:")
    print("="*60 + "\n")
    print("☐ PostgreSQL service is running (check Services)")
    print("☐ PostgreSQL is listening on 127.0.0.1:5432")
    print("☐ User 'r3aler_user_2025' exists in PostgreSQL")
    print("☐ User password is set to: R3AL3RAdmin816")
    print("☐ Database 'r3aler_ai' exists")
    print("☐ User has CONNECT privilege on database")
    print("")
    
    return 1

if __name__ == '__main__':
    sys.exit(main())
