#!/usr/bin/env python3
import json

# Check physics-stackexchange
print("Checking physics-stackexchange...")
with open('physics_marianna13_physics_stackexchange_raw.json', 'r') as f:
    data = json.load(f)
    print(f"Keys: {list(data.keys())}")
    if 'rows' in data and data['rows']:
        print(f"First row keys: {list(data['rows'][0].keys())}")
        print(f"Row->row keys: {list(data['rows'][0].get('row', {}).keys())[:10]}")

# Check Feynman
print("\nChecking Feynman...")
with open('physics_enesxgrahovac_the_feynman_lectures_on_physics_raw.json', 'r') as f:
    data = json.load(f)
    print(f"Keys: {list(data.keys())}")
    if 'data' in data and data['data']:
        print(f"First item keys: {list(data['data'][0].keys())[:10]}")

# Check introvoyz
print("\nChecking introvoyz...")
with open('physics_introvoyz041_physics_raw.json', 'r') as f:
    data = json.load(f)
    print(f"Keys: {list(data.keys())}")
    if 'data' in data and data['data']:
        print(f"First item keys: {list(data['data'][0].keys())[:10]}")
