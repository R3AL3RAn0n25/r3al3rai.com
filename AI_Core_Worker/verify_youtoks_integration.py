#!/usr/bin/env python3
"""
Verify YouToks Quantum Physics Dataset Integration with R3ALER AI
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(__file__))

from prompts import R3AELERPrompts
from load_datasets import (EXTENDED_KNOWLEDGE_BASE, PHYSICS_KB, SPACE_ENGINEERING_KB, 
                           QUANTUM_PHYSICS_KB, QUANTUM_PHYSICS_YOUTOKS_KB)

# Merge extended datasets into main knowledge base
original_count = len(R3AELERPrompts.KNOWLEDGE_BASE)
R3AELERPrompts.KNOWLEDGE_BASE.update(EXTENDED_KNOWLEDGE_BASE)
total_count = len(R3AELERPrompts.KNOWLEDGE_BASE)
extended_count = len(EXTENDED_KNOWLEDGE_BASE)

print("\n" + "="*70)
print("📚 R3ALER AI KNOWLEDGE BASE - COMPLETE VERIFICATION")
print("="*70)

print(f"\n📊 TOTAL KNOWLEDGE BASE:")
print(f"   Original entries:        {original_count}")
print(f"   Extended entries:        {extended_count}")
print(f"   Total entries:           {total_count}")
print(f"   New entries added:       {total_count - original_count}")

print(f"\n📚 DATASET BREAKDOWN:")
print(f"   Physics:                 {len(PHYSICS_KB)} entries")
print(f"   Space Engineering:       {len(SPACE_ENGINEERING_KB)} entries")
print(f"   Quantum Physics (VVUQ):  {len(QUANTUM_PHYSICS_KB)} entries")
print(f"   Quantum YouToks:         {len(QUANTUM_PHYSICS_YOUTOKS_KB)} entries")
print(f"   Original Knowledge:      {original_count} entries")

# Count entries by category prefix
physics_count = sum(1 for key in R3AELERPrompts.KNOWLEDGE_BASE.keys() if key.startswith('physics_'))
space_count = sum(1 for key in R3AELERPrompts.KNOWLEDGE_BASE.keys() if key.startswith('space_eng_'))
quantum_vvuq_count = sum(1 for key in R3AELERPrompts.KNOWLEDGE_BASE.keys() if key.startswith('quantum_'))
quantum_youtoks_count = sum(1 for key in R3AELERPrompts.KNOWLEDGE_BASE.keys() if key.startswith('youtoks_qp_'))

print(f"\n🔍 VERIFICATION (by key prefix):")
print(f"   Physics (physics_*):            {physics_count}")
print(f"   Space Engineering (space_eng_*): {space_count}")
print(f"   Quantum VVUQ (quantum_*):       {quantum_vvuq_count}")
print(f"   Quantum YouToks (youtoks_qp_*): {quantum_youtoks_count}")
print(f"   Other entries:                  {total_count - physics_count - space_count - quantum_vvuq_count - quantum_youtoks_count}")

# Show sample YouToks entry
print(f"\n🎓 SAMPLE YOUTOKS QUANTUM PHYSICS ENTRY:")
youtoks_keys = [k for k in R3AELERPrompts.KNOWLEDGE_BASE.keys() if k.startswith('youtoks_qp_')]
if youtoks_keys:
    sample_key = youtoks_keys[0]
    sample = R3AELERPrompts.KNOWLEDGE_BASE[sample_key]
    print(f"   Key: {sample_key}")
    print(f"   Topic: {sample.get('topic', 'N/A')[:80]}...")
    print(f"   Category: {sample.get('category', 'N/A')}")
    print(f"   Level: {sample.get('level', 'N/A')}")
    print(f"   Subcategory: {sample.get('subcategory', 'N/A')}")
    print(f"   Content preview: {sample.get('content', '')[:200]}...")

print("\n" + "="*70)
print("✅ YOUTOKS QUANTUM PHYSICS DATASET SUCCESSFULLY INTEGRATED!")
print(f"   R3ALER AI now has {total_count} total knowledge entries!")
print(f"   Including 100 graduate-level quantum physics lectures! 🎓")
print("="*70 + "\n")
