"""
Test Knowledge API Integration with Storage Facility
"""
import requests
import json

print("\n🧪 Testing R3ÆLƎR AI Knowledge API Integration")
print("="*60)

# Test 1: Health Check
print("\n1️⃣  Testing Health Endpoint...")
try:
    response = requests.get('http://localhost:5001/health')
    health = response.json()
    print(f"✅ Knowledge API Status: {health['status']}")
    print(f"   Storage Facility Connected: {health['storage_facility']['connected']}")
    print(f"   Total Entries: {health['storage_facility']['total_entries']}")
except Exception as e:
    print(f"❌ Health check failed: {e}")

# Test 2: Search for Cryptocurrency Knowledge
print("\n2️⃣  Testing Cryptocurrency Knowledge Search...")
try:
    response = requests.post(
        'http://localhost:5001/api/kb/search',
        json={'query': 'Bitcoin wallet.dat encryption', 'maxPassages': 3}
    )
    search_result = response.json()
    
    print(f"✅ Search Success: {search_result['success']}")
    print(f"   Used Storage Facility: {search_result.get('used_storage_facility', False)}")
    print(f"   Fallback Mode: {search_result.get('fallback_mode', False)}")
    print(f"   Results Found: {len(search_result.get('passages', []))}")
    
    if search_result.get('passages'):
        print(f"\n   📄 Sample Result:")
        first_result = search_result['passages'][0]
        print(f"      Topic: {first_result['meta']['topic']}")
        print(f"      Category: {first_result['meta']['category']}")
        print(f"      Relevance: {first_result['meta'].get('relevance', 'N/A')}")
        print(f"      Preview: {first_result['text'][:200]}...")
except Exception as e:
    print(f"❌ Crypto search failed: {e}")
    import traceback
    traceback.print_exc()

# Test 3: Search for Physics Knowledge
print("\n3️⃣  Testing Physics Knowledge Search...")
try:
    response = requests.post(
        'http://localhost:5001/api/kb/search',
        json={'query': 'quantum mechanics', 'maxPassages': 2}
    )
    search_result = response.json()
    
    print(f"✅ Search Success: {search_result['success']}")
    print(f"   Used Storage Facility: {search_result.get('used_storage_facility', False)}")
    print(f"   Results Found: {len(search_result.get('passages', []))}")
    
    if search_result.get('local_results'):
        for result in search_result['local_results'][:2]:
            print(f"\n   📄 {result['topic']}")
            print(f"      Unit: {result.get('unit', 'N/A')}")
            print(f"      Relevance: {result.get('relevance', 'N/A')}")
except Exception as e:
    print(f"❌ Physics search failed: {e}")

# Test 4: Get System Prompt
print("\n4️⃣  Testing System Prompt Retrieval...")
try:
    response = requests.get('http://localhost:5001/api/kb/prompts/crypto')
    prompt_result = response.json()
    
    print(f"✅ Prompt Retrieved: {prompt_result['success']}")
    print(f"   Type: {prompt_result.get('type', 'N/A')}")
    print(f"   Preview: {prompt_result['prompt'][:150]}...")
except Exception as e:
    print(f"❌ Prompt retrieval failed: {e}")

# Test 5: Direct Storage Facility Test
print("\n5️⃣  Testing Direct Storage Facility Connection...")
try:
    response = requests.post(
        'http://localhost:5003/api/facility/search',
        json={'query': 'Bitcoin encryption', 'limit_per_unit': 2}
    )
    facility_result = response.json()
    
    print(f"✅ Storage Facility Search Success")
    print(f"   Results Found: {len(facility_result.get('results', []))}")
    
    if facility_result.get('results'):
        for result in facility_result['results'][:2]:
            print(f"\n   📄 {result['topic']}")
            print(f"      Unit: {result['unit_name']}")
            print(f"      Category: {result['category']}")
            print(f"      Relevance: {result['relevance']:.4f}")
except Exception as e:
    print(f"❌ Storage Facility test failed: {e}")

print("\n" + "="*60)
print("✅ Integration Testing Complete!")
print("="*60 + "\n")
