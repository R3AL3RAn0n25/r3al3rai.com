"""
Test R3ÆL3R Storage Facility
"""

import requests
import json

API_URL = "http://localhost:5003"

print("\n" + "=" * 60)
print("🧪 TESTING R3ÆL3R STORAGE FACILITY")
print("=" * 60)

# Test 1: Facility Status
print("\n📊 Test 1: Getting Facility Status...")
try:
    response = requests.get(f"{API_URL}/api/facility/status")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Status: {data['status']}")
        print(f"✅ Total Units: {data['total_units']}")
        print(f"✅ Total Entries: {data['total_entries']:,}")
        print(f"✅ Cost: {data['cost']}")
        
        print("\n📦 Storage Units:")
        for unit_id, unit in data['units'].items():
            print(f"   • {unit['name']}: {unit['total_entries']:,} entries ({unit['size']})")
    else:
        print(f"❌ Status check failed: {response.status_code}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 2: Search Physics Unit
print("\n🔍 Test 2: Searching Physics Unit for 'quantum mechanics'...")
try:
    response = requests.post(
        f"{API_URL}/api/unit/physics/search",
        json={"query": "quantum mechanics", "limit": 3}
    )
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Found {len(data['results'])} results")
        for i, result in enumerate(data['results'][:3], 1):
            print(f"\n   Result {i}:")
            print(f"   Topic: {result['topic'][:80]}...")
            print(f"   Relevance: {result['relevance']:.4f}")
            print(f"   Category: {result.get('category', 'N/A')}")
    else:
        print(f"❌ Search failed: {response.status_code}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 3: Search All Units
print("\n🔍 Test 3: Searching ALL units for 'black hole'...")
try:
    response = requests.post(
        f"{API_URL}/api/facility/search",
        json={"query": "black hole", "limit_per_unit": 2}
    )
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Found {data['total_results']} results across all units")
        for result in data['results'][:5]:
            print(f"\n   • Unit: {result['unit_name']}")
            print(f"     Topic: {result['topic'][:70]}...")
            print(f"     Relevance: {result['relevance']:.4f}")
    else:
        print(f"❌ Search failed: {response.status_code}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 4: Search Quantum Unit
print("\n🔍 Test 4: Searching Quantum Unit for 'particle'...")
try:
    response = requests.post(
        f"{API_URL}/api/unit/quantum/search",
        json={"query": "particle", "limit": 3}
    )
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Found {len(data['results'])} results")
        for i, result in enumerate(data['results'][:3], 1):
            print(f"\n   Result {i}:")
            print(f"   Topic: {result['topic'][:80]}...")
            print(f"   Relevance: {result['relevance']:.4f}")
    else:
        print(f"❌ Search failed: {response.status_code}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 5: Search Space Unit
print("\n🔍 Test 5: Searching Space Unit for 'exoplanet'...")
try:
    response = requests.post(
        f"{API_URL}/api/unit/space/search",
        json={"query": "exoplanet", "limit": 3}
    )
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Found {len(data['results'])} results")
        for i, result in enumerate(data['results'][:3], 1):
            print(f"\n   Result {i}:")
            print(f"   Topic: {result['topic'][:80]}...")
            print(f"   Relevance: {result['relevance']:.4f}")
    else:
        print(f"❌ Search failed: {response.status_code}")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 60)
print("✅ STORAGE FACILITY TESTS COMPLETE!")
print("=" * 60)
print("\n📊 Dashboard: http://localhost:5001")
print("🌐 Open the dashboard in your browser to see the visual interface!\n")
