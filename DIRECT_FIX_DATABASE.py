#!/usr/bin/env python3
"""
R3ÆLƎR AI - RESET PostgreSQL User Password
Direct password reset for r3aler_user_2025
"""

import subprocess
import sys
import os

def find_psql():
    """Find psql executable"""
    possible_paths = [
        'psql',
        'C:\\Program Files\\PostgreSQL\\15\\bin\\psql.exe',
        'C:\\Program Files\\PostgreSQL\\14\\bin\\psql.exe',
        'C:\\Program Files\\PostgreSQL\\13\\bin\\psql.exe',
        'C:\\Program Files (x86)\\PostgreSQL\\15\\bin\\psql.exe',
        'C:\\Program Files (x86)\\PostgreSQL\\14\\bin\\psql.exe',
    ]
    
    for path in possible_paths:
        if path == 'psql':
            try:
                subprocess.run(['psql', '--version'], capture_output=True, timeout=2)
                return 'psql'
            except:
                continue
        elif os.path.exists(path):
            return path
    
    return None

def main():
    print("\n" + "="*70)
    print("R3ÆLƎR AI - PostgreSQL Password Reset")
    print("="*70 + "\n")
    
    # Find psql
    print("Finding PostgreSQL...")
    psql_path = find_psql()
    
    if not psql_path:
        print("✗ PostgreSQL not found")
        print("  Ensure PostgreSQL is installed and in PATH")
        return 1
    
    print(f"✓ Found: {psql_path}\n")
    
    # Reset password directly
    sql = "ALTER USER r3aler_user_2025 WITH PASSWORD 'R3AL3RAdmin816';"
    
    print("Resetting password for r3aler_user_2025...")
    
    try:
        result = subprocess.run(
            [psql_path, '-U', 'postgres', '-c', sql],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            print("✓ Password reset successfully\n")
            
            print("="*70)
            print("DATABASE CREDENTIALS")
            print("="*70)
            print(f"Host:        127.0.0.1:5432")
            print(f"Database:    r3aler_ai")
            print(f"User:        r3aler_user_2025")
            print(f"Password:    R3AL3RAdmin816")
            print("="*70 + "\n")
            
            print("Next: Restart services")
            print("  Get-Process python | Stop-Process -Force")
            print("  .\\START_ALL_SERVICES.ps1")
            
            return 0
        else:
            if "password authentication failed" in result.stderr:
                print("✗ Need postgres superuser password\n")
                print("Run in Command Prompt as Administrator:")
                print("  cd 'C:\\Program Files\\PostgreSQL\\15\\bin'")
                print("  psql -U postgres")
                print("  ALTER USER r3aler_user_2025 WITH PASSWORD 'R3AL3RAdmin816';")
                print("  \\q")
            else:
                print(f"✗ Error: {result.stderr}")
            return 1
            
    except Exception as e:
        print(f"✗ Failed: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
