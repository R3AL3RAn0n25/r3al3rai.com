"""Production runner for Enhanced Intelligence API"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from waitress import serve
import AI_Core_Worker.enhanced_knowledge_api as enhanced_knowledge_api

print("=" * 70)
print("R3AL3R AI Enhanced Intelligence - PRODUCTION SERVER (Waitress)")
print("=" * 70)
print("Starting on: http://0.0.0.0:5010")
print("Press Ctrl+C to stop")
print("=" * 70)

serve(enhanced_knowledge_api.app, host='0.0.0.0', port=5010, threads=4)
