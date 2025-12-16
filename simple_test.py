#!/usr/bin/env python3
import requests
import json

# Test search with forced local mode
response = requests.post('http://localhost:5001/api/kb/search', 
                        json={'query': 'quantum', 'mode': 'local', 'maxPassages': 5})
print("Status:", response.status_code)
data = response.json()
print(f"Success: {data.get('success')}")
print(f"Source: {data.get('source')}")
print(f"Used External: {data.get('used_external')}")
print(f"Results: {len(data.get('results', []))}")
print(f"Local Results: {len(data.get('local_results', []))}")
print(f"\nFull response keys: {list(data.keys())}")
if data.get('local_results'):
    print("\nFirst local result:")
    print(json.dumps(data['local_results'][0], indent=2)[:800])
