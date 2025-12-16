#!/usr/bin/env python3
"""
Diagnostic script to check R3ÆLƎR AI component functionality
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

def diagnose_ai_components():
    """Diagnose all AI components"""
    print("🔍 R3ÆLƎR AI Component Diagnostic")
    print("=" * 50)

    issues = []
    working_components = []

    # Test 1: Core AI
    try:
        from AI_Core_Worker.core import Core
        core = Core()
        working_components.append("Core AI")
        print("✅ Core AI: Working")
    except Exception as e:
        issues.append(f"Core AI: {e}")
        print(f"❌ Core AI: Failed - {e}")

    # Test 2: Intelligence Layer
    try:
        from AI_Core_Worker.intelligence_layer import get_intelligence_layer
        intelligence = get_intelligence_layer()
        test_intent = intelligence.classify_intent("What is the capital of France?")
        working_components.append("Intelligence Layer")
        print("✅ Intelligence Layer: Working")
    except Exception as e:
        issues.append(f"Intelligence Layer: {e}")
        print(f"❌ Intelligence Layer: Failed - {e}")

    # Test 3: Knowledge Base
    try:
        from knowledge_base import KnowledgeBase
        kb = KnowledgeBase()
        working_components.append("Knowledge Base")
        print("✅ Knowledge Base: Working")
    except Exception as e:
        issues.append(f"Knowledge Base: {e}")
        print(f"❌ Knowledge Base: Failed - {e}")

    # Test 4: Response Generator
    try:
        from AI_Core_Worker.response_generator import ResponseGenerator
        rg = ResponseGenerator()
        working_components.append("Response Generator")
        print("✅ Response Generator: Working")
    except Exception as e:
        issues.append(f"Response Generator: {e}")
        print(f"❌ Response Generator: Failed - {e}")

    # Test 5: Quantum Processor
    try:
        from AI_Core_Worker.quantum_processor import QuantumProcessor
        qp = QuantumProcessor()
        working_components.append("Quantum Processor")
        print("✅ Quantum Processor: Working")
    except Exception as e:
        issues.append(f"Quantum Processor: {e}")
        print(f"❌ Quantum Processor: Failed - {e}")

    # Test 6: Neural Network
    try:
        from AI_Core_Worker.neural_network import NeuralNetwork
        nn = NeuralNetwork()
        working_components.append("Neural Network")
        print("✅ Neural Network: Working")
    except Exception as e:
        issues.append(f"Neural Network: {e}")
        print(f"❌ Neural Network: Failed - {e}")

    # Test 7: Main R3AL3R_AI
    try:
        from AI_Core_Worker.R3AL3R_AI import R3AL3R_AI
        ai = R3AL3R_AI()
        working_components.append("Main R3AL3R_AI")
        print("✅ Main R3AL3R_AI: Working")
    except Exception as e:
        issues.append(f"Main R3AL3R_AI: {e}")
        print(f"❌ Main R3AL3R_AI: Failed - {e}")

    print()
    print("📊 DIAGNOSTIC SUMMARY:")
    print(f"✅ Working Components: {len(working_components)}")
    for comp in working_components:
        print(f"   • {comp}")

    if issues:
        print(f"❌ Issues Found: {len(issues)}")
        for issue in issues:
            print(f"   • {issue}")
    else:
        print("✅ All components working properly!")

    return working_components, issues

def test_ai_response_generation():
    """Test actual AI response generation"""
    print()
    print("🧪 TESTING AI RESPONSE GENERATION:")
    print("-" * 40)

    try:
        from AI_Core_Worker.R3AL3R_AI import R3AL3R_AI
        ai = R3AL3R_AI()

        test_queries = [
            "What is 2+2?",
            "Explain quantum computing",
            "What is the capital of France?"
        ]

        for query in test_queries:
            print(f"\nQuery: {query}")
            try:
                response = ai.process_query(query)
                response_text = response.get('response', 'No response')
                print(f"Response: {response_text[:100]}...")
                if "apologize" in response_text.lower() or "trouble" in response_text.lower():
                    print("⚠️  WARNING: Response contains apology/fallback message")
                else:
                    print("✅ Response appears normal")
            except Exception as e:
                print(f"❌ Error: {e}")

    except Exception as e:
        print(f"❌ Cannot test AI responses: {e}")

if __name__ == "__main__":
    working, issues = diagnose_ai_components()
    test_ai_response_generation()

    print()
    print("💡 RECOMMENDATIONS:")
    if issues:
        print("• Fix the failing components listed above")
        print("• Check import paths and dependencies")
        print("• Ensure all required services are running")
    else:
        print("• All components appear to be working")
        print("• If responses still contain apologies, check response generation logic")