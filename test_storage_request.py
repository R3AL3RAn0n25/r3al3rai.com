import requests

# Test the actual request the Knowledge API makes
response = requests.post(
    'http://localhost:5003/api/facility/search',
    json={'query': "Bitcoin wallet", 'limit_per_unit': 5},
    timeout=10
)

print(f"Status Code: {response.status_code}")
print(f"Response: {response.json()}")

if response.status_code == 200:
    facility_data = response.json()
    results = facility_data.get('results', [])
    
    print(f"\nFound {len(results)} results")
    
    for i, result in enumerate(results[:3], 1):
        print(f"\nResult {i}:")
        print(f"  entry_id: {result.get('entry_id')}")
        print(f"  unit_name: {result.get('unit_name')}")
        print(f"  source_unit: {result.get('source_unit')}")
        print(f"  topic: {result.get('topic')}")
        print(f"  category: {result.get('category')}")
        print(f"  subcategory: {result.get('subcategory')}")
        print(f"  relevance: {result.get('relevance')}")
