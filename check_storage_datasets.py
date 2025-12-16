#!/usr/bin/env python3
"""
Check current datasets in the storage facility
"""

import requests
import json

def check_storage_facility():
    """Check what datasets are currently stored"""
    try:
        response = requests.get('http://localhost:3003/api/facility/status', timeout=10)
        if response.status_code == 200:
            status = response.json()
            print("🗄️  R3AL3R Storage Facility Status")
            print("=" * 50)
            print(f"📊 Total Entries: {status['total_entries']:,}")
            print(f"🏗️  Total Units: {status['total_units']}")
            print(f"💾 Cost: {status['cost']}")
            print(f"📍 Status: {status['status']}")
            print()

            print("📚 Knowledge Units:")
            print("-" * 30)
            for unit_name, unit_info in status['units'].items():
                print(f"🔹 {unit_name.upper()}")
                print(f"   Description: {unit_info['description']}")
                print(f"   Entries: {unit_info['total_entries']:,}")
                print(f"   Categories: {unit_info['categories']}")
                print(f"   Sources: {unit_info['sources']}")
                print(f"   Size: {unit_info['size']}")
                print()

            # Check for specific datasets
            print("🔍 Dataset Analysis:")
            print("-" * 20)

            # Physics datasets
            physics_entries = status['units'].get('physics', {}).get('total_entries', 0)
            if physics_entries > 1000:
                print("✅ Physics: Large dataset (>1000 entries)")
            elif physics_entries > 100:
                print("✅ Physics: Medium dataset (100-1000 entries)")
            elif physics_entries > 0:
                print("⚠️  Physics: Small dataset (<100 entries)")
            else:
                print("❌ Physics: No data")

            # Quantum datasets
            quantum_entries = status['units'].get('quantum', {}).get('total_entries', 0)
            if quantum_entries > 100:
                print("✅ Quantum: Good dataset (>100 entries)")
            elif quantum_entries > 0:
                print("⚠️  Quantum: Small dataset (<100 entries)")
            else:
                print("❌ Quantum: No data")

            # Space/Astro datasets
            space_entries = status['units'].get('space', {}).get('total_entries', 0)
            if space_entries > 1000:
                print("✅ Space/Astro: Large dataset (>1000 entries)")
            elif space_entries > 100:
                print("✅ Space/Astro: Medium dataset (100-1000 entries)")
            else:
                print("❌ Space/Astro: Minimal data")

            # Crypto datasets
            crypto_entries = status['units'].get('crypto', {}).get('total_entries', 0)
            if crypto_entries > 10:
                print("✅ Crypto: Has data")
            else:
                print("❌ Crypto: Minimal data")

            # Medical datasets
            medical_entries = status['units'].get('medical', {}).get('total_entries', 0)
            if medical_entries > 0:
                print("✅ Medical: Has data")
            else:
                print("❌ Medical: No data")

            # Reason/Logic datasets
            reason_entries = status['units'].get('reason', {}).get('total_entries', 0)
            logic_entries = status['units'].get('logic', {}).get('total_entries', 0)
            if reason_entries > 0 or logic_entries > 0:
                print("✅ Reasoning/Logic: Has data")
            else:
                print("❌ Reasoning/Logic: No data")

        else:
            print(f"❌ Error accessing storage facility: {response.status_code}")
            print(f"Response: {response.text}")

    except Exception as e:
        print(f"❌ Cannot connect to storage facility: {e}")

if __name__ == "__main__":
    check_storage_facility()