#!/usr/bin/env python3
"""
R3AL3R AI - Migration Verification Launcher
Run this from the project root directory
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    print("=" * 60)
    print("R3AL3R AI - MIGRATION VERIFICATION")
    print("=" * 60)
    
    # Get current directory
    current_dir = Path.cwd()
    print(f"Current directory: {current_dir}")
    
    # Find the verification script
    verify_script = current_dir / "application" / "Backend" / "verify_cloud_migration.py"
    
    if not verify_script.exists():
        print(f"ERROR: Verification script not found at {verify_script}")
        print("Please run this from the R3aler-ai project root directory")
        return
    
    print(f"Found verification script: {verify_script}")
    
    # Run verification
    print("\nVerifying migration...")
    try:
        result = subprocess.run([sys.executable, str(verify_script)], 
                              cwd=str(current_dir), 
                              capture_output=False)
        
        if result.returncode == 0:
            print("\n[SUCCESS] Verification completed!")
        else:
            print(f"\n[ERROR] Verification failed with return code {result.returncode}")
            
    except Exception as e:
        print(f"\n[ERROR] Error running verification: {e}")

if __name__ == '__main__':
    main()