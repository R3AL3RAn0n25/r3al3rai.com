"""Production runner for Backend/Intelligence Layer"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from waitress import serve
import intelligence_layer

print("=" * 70)
print("R3AL3R AI Backend - PRODUCTION SERVER (Waitress)")
print("=" * 70)
print("Starting on: http://0.0.0.0:3002")
print("Press Ctrl+C to stop")
print("=" * 70)

serve(intelligence_layer.app, host='0.0.0.0', port=3002, threads=6)
