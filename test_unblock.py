#!/usr/bin/env python3
"""Quick test to unblock and verify health endpoint"""
import requests

print('Unblocking localhost from security filter...')
url = 'http://localhost:3000/api/test/unblock-localhost'
try:
    resp = requests.post(url, timeout=5)
    print(f'Status: {resp.status_code}')
    print(f'Response: {resp.json()}')
except Exception as e:
    print(f'Error: {e}')

print('\nNow testing /api/health endpoint...')
url = 'http://localhost:3000/api/health'
try:
    resp = requests.get(url, timeout=5)
    print(f'Status: {resp.status_code}')
    data = resp.json()
    print('Response (formatted):')
    print(f'  OK: {data.get("ok")}')
    print(f'  Node uptime: {data.get("node", {}).get("uptime_s")}s')
    print(f'  DB OK: {data.get("db", {}).get("ok")}')
    print(f'  BlackArch OK: {data.get("blackarch", {}).get("ok")}')
except Exception as e:
    print(f'Error: {e}')
