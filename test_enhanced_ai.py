#!/usr/bin/env python3
"""
Test script for the enhanced R3ÆLƎR AI system
"""

import sys
import os
import time

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from AI_Core_Worker.R3AL3R_AI import R3AL3R_AI

def test_basic_functionality():
    """Test basic AI functionality"""
    print("🧪 Testing Enhanced R3ÆLƎR AI System")
    print("=" * 50)

    # Initialize AI system
    print("🚀 Initializing R3ÆLƎR AI...")
    ai = R3AL3R_AI()

    # Test system status
    print("📊 Getting system status...")
    status = ai.get_system_status()
    print(f"System Status: {status}")
    print()

    # Test query processing
    test_queries = [
        "What is quantum physics?",
        "How does cryptocurrency work?",
        "Tell me about space exploration",
        "Explain a medical condition"
    ]

    print("🧠 Testing query processing...")
    for query in test_queries:
        print(f"\nQuery: {query}")
        try:
            result = ai.process_query(query)
            print(f"Response: {result.get('response', 'No response')[:200]}...")
            print(f"Processing time: {result.get('processing_time', 'Unknown')}")
        except Exception as e:
            print(f"Error processing query: {e}")

    # Test system optimization
    print("\n⚡ Running system optimization...")
    ai.optimize_system()

    # Final status
    print("\n📈 Final system status:")
    final_status = ai.get_system_status()
    print(f"Components active: {len([c for c in final_status['components'].values() if c != 'error'])}")

    # Cleanup
    ai.stop()
    print("\n✅ Test completed successfully!")

if __name__ == "__main__":
    test_basic_functionality()