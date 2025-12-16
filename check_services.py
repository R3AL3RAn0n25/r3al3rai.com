import requests
import socket

def check_port(port):
    """Check if a port is listening"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)
    result = sock.connect_ex(('localhost', port))
    sock.close()
    return result == 0

services = [
    ('Backend Server (Node.js)', 3000, '/'),
    ('Storage Facility', 3003, '/api/facility/status'),
    ('Knowledge API', 5001, '/api/kb/health'),
    ('Enhanced Knowledge API', 9999, '/health'),
    ('Droid API', 5005, '/health'),
    ('Intelligence API', 5010, '/api/enhanced/health'),
    ('BitXtractor API', 3004, '/api'),
    ('BlackArch Tools', 8080, '/'),
]

print('=' * 60)
print('R3AL3R AI SERVICE STATUS')
print('=' * 60)

for name, port, endpoint in services:
    port_open = check_port(port)
    
    if port_open:
        try:
            url = f'http://localhost:{port}{endpoint}'
            r = requests.get(url, timeout=2)
            status = f'✔ RUNNING (HTTP {r.status_code})'
        except Exception as e:
            status = f'✔ PORT OPEN (HTTP failed: {str(e)[:30]}...)'
    else:
        status = '✗ DOWN (port closed)'
    
    print(f'{name:30} - {status}')

print('=' * 60)
