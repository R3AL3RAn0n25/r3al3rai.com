#!/usr/bin/env python3
"""
Quick test to verify AI system is responding
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from R3AL3R_AI_fixed import r3aler
    
    # Test queries
    test_queries = [
        "hello",
        "what is your status?",
        "help me",
        "calculate 2+2"
    ]
    
    print("=== R3ALER AI Response Test ===")
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        try:
            response = r3aler.process_query(query)
            print(f"Response: {response.get('response', 'No response')}")
            print(f"Status: {response.get('status', 'unknown')}")
        except Exception as e:
            print(f"Error: {e}")
    
    print("\n=== System Status ===")
    try:
        status = r3aler.get_system_status()
        print(f"Running: {status.get('running', False)}")
        print(f"Components: {len(status.get('components', {}))}")
    except Exception as e:
        print(f"Status error: {e}")
        
except Exception as e:
    print(f"Import error: {e}")