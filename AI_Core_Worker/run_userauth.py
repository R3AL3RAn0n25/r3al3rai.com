"""Production runner for User Auth API"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from waitress import serve
import user_auth_api

print("=" * 70)
print("R3AL3R AI User Auth - PRODUCTION SERVER (Waitress)")
print("=" * 70)
print("Starting on: http://0.0.0.0:5006")
print("Press Ctrl+C to stop")
print("=" * 70)

serve(user_auth_api.app, host='0.0.0.0', port=5006, threads=4)
