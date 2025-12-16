import requests

r = requests.post('http://localhost:3000/api/auth/login', json={'username':'test','password':'test'}, timeout=5)
print(f'Status: {r.status_code}')
print(f'Content-Type: {r.headers.get("content-type")}')
print(f'Body: {r.text[:500]}')
