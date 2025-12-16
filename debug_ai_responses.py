#!/usr/bin/env python3
"""
Debug script to see what AI responses look like
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from AI_Core_Worker.R3AL3R_AI import R3AL3R_AI

def test_ai_responses():
    ai = R3AL3R_AI()

    test_questions = [
        "What is the capital of France?",
        "What is 15 + 27?",
        "What do people typically do when they are hungry?",
        "What is the largest planet in our solar system?"
    ]

    print("Testing AI responses:")
    print("=" * 50)

    for question in test_questions:
        print(f"\nQuestion: {question}")
        try:
            response = ai.process_query(question, user_id="debug_test")
            print(f"Response: {response.get('response', 'NO RESPONSE')}")
            print(f"Intent: {response.get('intent', 'UNKNOWN')}")
            print(f"Knowledge used: {response.get('knowledge_used', 0)}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    test_ai_responses()