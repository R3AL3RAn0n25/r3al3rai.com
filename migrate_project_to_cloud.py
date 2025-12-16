#!/usr/bin/env python3
"""
R3AL3R AI - Project Migration Launcher
Run this from the project root directory
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    print("=" * 60)
    print("R3AL3R AI - PROJECT MIGRATION TO CLOUD STORAGE")
    print("=" * 60)
    
    # Get current directory
    current_dir = Path.cwd()
    print(f"Current directory: {current_dir}")
    
    # Find the migration script
    migration_script = current_dir / "application" / "Backend" / "migrate_to_cloud_storage.py"
    
    if not migration_script.exists():
        print(f"ERROR: Migration script not found at {migration_script}")
        print("Please run this from the R3aler-ai project root directory")
        return
    
    print(f"Found migration script: {migration_script}")
    
    # Check if storage facility is running
    print("\nChecking storage facility...")
    try:
        import requests
        response = requests.get("http://localhost:3003/api/facility/status", timeout=5)
        if response.status_code == 200:
            print("[OK] Storage facility is running")
        else:
            print("[ERROR] Storage facility not responding properly")
            print("Please start it first:")
            print("cd AI_Core_Worker")
            print("python self_hosted_storage_facility_windows.py")
            return
    except Exception as e:
        print("[ERROR] Storage facility not accessible")
        print("Please start it first:")
        print("cd AI_Core_Worker")
        print("python self_hosted_storage_facility_windows.py")
        return
    
    # Run migration
    print("\nStarting migration process...")
    try:
        result = subprocess.run([sys.executable, str(migration_script)], 
                              cwd=str(current_dir), 
                              capture_output=False)
        
        if result.returncode == 0:
            print("\n[SUCCESS] Migration completed successfully!")
            print("\nNext steps:")
            print("1. Verify migration: python verify_migration.py")
            print("2. Clean up local files: python cleanup_local_files.py --confirm")
        else:
            print(f"\n[ERROR] Migration failed with return code {result.returncode}")
            
    except Exception as e:
        print(f"\n[ERROR] Error running migration: {e}")

if __name__ == '__main__':
    main()