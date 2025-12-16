#!/usr/bin/env python3
"""
Simple AI test without Unicode issues
"""

import json
import time
from datetime import datetime

class SimpleAI:
    def __init__(self):
        self.running = True
        print("Simple AI initialized")
    
    def process_query(self, query: str, user_id: str = 'anonymous'):
        """Simple query processor with basic responses"""
        start_time = time.time()
        query_lower = query.lower().strip()
        
        # Basic response logic
        if any(word in query_lower for word in ['hello', 'hi', 'hey']):
            response = "Hello! I'm R3ALER AI, your advanced AI assistant. How can I help you today?"
        elif any(word in query_lower for word in ['status', 'health', 'running']):
            response = "R3ALER AI is running and operational. All systems are active."
        elif any(word in query_lower for word in ['help', 'what can you do']):
            response = "I'm R3ALER AI - I can help with queries, analysis, and various AI tasks. What would you like to know?"
        elif any(word in query_lower for word in ['calculate', 'math', '+', '-', '*', '/']):
            if '2+2' in query_lower or '2 + 2' in query_lower:
                response = "2 + 2 = 4. I can help with mathematical calculations and problem solving."
            else:
                response = "I can help with mathematical calculations. Please provide the specific calculation you need."
        elif any(word in query_lower for word in ['time', 'date']):
            response = f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        else:
            response = f"R3ALER AI received your query: '{query}'. I'm processing this request with my available systems."
        
        return {
            "response": response,
            "intent": "general",
            "processing_time_ms": round((time.time() - start_time) * 1000, 2),
            "timestamp": datetime.now().isoformat(),
            "status": "success"
        }

# Test the simple AI
if __name__ == "__main__":
    ai = SimpleAI()
    
    test_queries = [
        "hello",
        "what is your status?", 
        "help me",
        "calculate 2+2",
        "what time is it?",
        "tell me about quantum physics"
    ]
    
    print("\n=== Simple AI Response Test ===")
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        try:
            response = ai.process_query(query)
            print(f"Response: {response['response']}")
            print(f"Time: {response['processing_time_ms']}ms")
        except Exception as e:
            print(f"Error: {e}")