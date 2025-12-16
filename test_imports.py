"""Test if all imports work correctly after file reorganization"""
import sys
import os

# Add AI_Core_Worker to path
ai_core_path = os.path.join(os.path.dirname(__file__), 'AI_Core_Worker')
sys.path.insert(0, ai_core_path)

print("=" * 70)
print("R3AL3R AI - IMPORT VERIFICATION TEST")
print("=" * 70)
print()

# Test 1: R3ALER Prompts
print("Testing: R3ALER Prompts...")
try:
    from prompts import R3AELERPrompts
    print("  ✓ R3ALER Prompts imported successfully")
except ImportError as e:
    print(f"  ✗ ERROR: {e}")

# Test 2: AI Core Worker
print("\nTesting: AI Core Worker...")
try:
    from AI_Core_Worker import RealerAI
    print("  ✓ AI Core Worker imported successfully")
except ImportError as e:
    print(f"  ✗ ERROR: {e}")

# Test 3: AI Intelligence Modules
print("\nTesting: AI Intelligence Modules...")
try:
    from activity_tracker import ActivityTracker
    print("  ✓ Activity Tracker imported successfully")
except ImportError as e:
    print(f"  ✗ ERROR: {e}")

try:
    from personalization_engine import PersonalizationEngine
    print("  ✓ Personalization Engine imported successfully")
except ImportError as e:
    print(f"  ✗ ERROR: {e}")

try:
    from recommendation_engine import RecommendationEngine
    print("  ✓ Recommendation Engine imported successfully")
except ImportError as e:
    print(f"  ✗ ERROR: {e}")

try:
    from self_learning_engine import SelfLearningEngine
    print("  ✓ Self Learning Engine imported successfully")
except ImportError as e:
    print(f"  ✗ ERROR: {e}")

try:
    from evolution_engine import EvolutionEngine
    print("  ✓ Evolution Engine imported successfully")
except ImportError as e:
    print(f"  ✗ ERROR: {e}")

# Test 4: Core AI modules
print("\nTesting: Core AI Modules...")
try:
    from core import Core
    print("  ✓ Core imported successfully")
except ImportError as e:
    print(f"  ✗ ERROR: {e}")

try:
    from intelligence_layer import get_intelligence_layer
    print("  ✓ Intelligence Layer imported successfully")
except ImportError as e:
    print(f"  ✗ ERROR: {e}")

try:
    from security_manager import SecurityManager
    print("  ✓ Security Manager imported successfully")
except ImportError as e:
    print(f"  ✗ ERROR: {e}")

try:
    from memory_manager import MemoryManager
    print("  ✓ Memory Manager imported successfully")
except ImportError as e:
    print(f"  ✗ ERROR: {e}")

print()
print("=" * 70)
print("IMPORT TEST COMPLETE")
print("=" * 70)
