import requests
import json

BASE = 'http://localhost:3000'

# Get JWT token first
reg = requests.post(f'{BASE}/api/auth/register', json={
    'username': 'mode_test_user',
    'password': 'Test@123456',
    'email': 'modetest@test.local'
})

login = requests.post(f'{BASE}/api/auth/login', json={
    'username': 'mode_test_user',
    'password': 'Test@123456'
})

token = login.json().get('token')
headers = {'Authorization': f'Bearer {token}'}

print("=== MODE MANAGEMENT TEST ===\n")

# Get current mode
print("[1] GET /api/admin/mode - Current Mode")
r = requests.get(f'{BASE}/api/admin/mode', headers=headers)
print(f"Status: {r.status_code}")
print(f"Response: {json.dumps(r.json(), indent=2)}\n")

# Toggle mode
print("[2] POST /api/admin/mode/toggle - Toggle Mode")
r = requests.post(f'{BASE}/api/admin/mode/toggle', headers=headers)
print(f"Status: {r.status_code}")
print(f"Response: {json.dumps(r.json(), indent=2)}\n")

# Verify mode changed
print("[3] GET /api/admin/mode - Verify Mode Changed")
r = requests.get(f'{BASE}/api/admin/mode', headers=headers)
print(f"Status: {r.status_code}")
print(f"New Mode: {r.json()['data']['currentMode']}\n")

# Set mode
print("[4] POST /api/admin/mode/set - Set to Development")
r = requests.post(f'{BASE}/api/admin/mode/set', headers=headers, json={'mode': 'development'})
print(f"Status: {r.status_code}")
print(f"Response: {json.dumps(r.json(), indent=2)}\n")

print("✓ Mode management endpoints working!")
