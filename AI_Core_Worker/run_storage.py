"""Production runner for Storage Facility"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from waitress import serve
import self_hosted_storage_facility

print("=" * 70)
print("R3AL3R AI Storage Facility - PRODUCTION SERVER (Waitress)")
print("=" * 70)
print("Starting on: http://0.0.0.0:3003")
print("Press Ctrl+C to stop")
print("=" * 70)

serve(self_hosted_storage_facility.app, host='0.0.0.0', port=3003, threads=6)
