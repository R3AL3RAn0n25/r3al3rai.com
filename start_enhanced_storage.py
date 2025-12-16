#!/usr/bin/env python3
"""
Quick start script for R3ÆL3R Enhanced Storage Facility
"""

import os
import sys
import subprocess
import time

def check_postgresql():
    """Check if PostgreSQL is running"""
    try:
        import psycopg2
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            database="r3aler_ai",
            user="r3aler_user_2025",
            password="password123"
        )
        conn.close()
        print("✓ PostgreSQL is running")
        return True
    except Exception as e:
        print(f"✗ PostgreSQL connection failed: {e}")
        print("  Please ensure PostgreSQL is running and credentials are correct")
        return False

def start_storage_facility():
    """Start the enhanced storage facility"""
    print("\n" + "="*60)
    print("R3ÆL3R ENHANCED STORAGE FACILITY - QUICK START")
    print("="*60)

    # Check PostgreSQL
    if not check_postgresql():
        print("\n❌ Cannot start storage facility without PostgreSQL")
        return False

    # Change to AI_Core_Worker directory
    os.chdir(os.path.join(os.path.dirname(__file__), 'AI_Core_Worker'))

    print("\n🚀 Starting Enhanced Storage Facility...")
    print("Features:")
    print("  ✓ Real-time monitoring")
    print("  ✓ Automated failover ready")
    print("  ✓ Predictive maintenance")
    print("  ✓ Web dashboard")

    try:
        # Start the Flask app
        cmd = [sys.executable, 'self_hosted_storage_facility.py']
        print(f"\n📊 Dashboard: http://localhost:3003")
        print(f"🔗 API: http://localhost:3003/api/facility/status/enhanced")
        print(f"📋 Monitoring: http://localhost:3003/api/monitoring/health")
        print("\nPress Ctrl+C to stop\n")

        subprocess.run(cmd)
        return True

    except KeyboardInterrupt:
        print("\n\n🛑 Storage facility stopped")
        return True
    except Exception as e:
        print(f"\n❌ Failed to start storage facility: {e}")
        return False

if __name__ == "__main__":
    success = start_storage_facility()
    sys.exit(0 if success else 1)