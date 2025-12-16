"""Production runner for Knowledge API"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from waitress import serve
import knowledge_api

print("=" * 70)
print("R3AL3R AI Knowledge API - PRODUCTION SERVER (Waitress)")
print("=" * 70)
print("Starting on: http://0.0.0.0:5004")
print("Press Ctrl+C to stop")
print("=" * 70)

serve(knowledge_api.app, host='0.0.0.0', port=5004, threads=4)
