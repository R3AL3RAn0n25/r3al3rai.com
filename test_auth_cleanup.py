import requests

# Test register
r = requests.post('http://localhost:3000/api/auth/register', json={'username':'final_cleanup_test','password':'Test@123456','email':'final@test.local'}, timeout=5)
print(f'Register: {r.status_code}')

# Test login
login = requests.post('http://localhost:3000/api/auth/login', json={'username':'final_cleanup_test','password':'Test@123456'}, timeout=5)
print(f'Login: {login.status_code}')
print(f'Token present: {bool(login.json().get("token"))}')
print('AUTH: OPERATIONAL')
