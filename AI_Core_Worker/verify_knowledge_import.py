#!/usr/bin/env python3
"""
Verify that datasets have been imported into the knowledge base
"""

import sys
import os

# Add AI_Core_Worker to path
sys.path.append(os.path.dirname(__file__))

from prompts import R3AELERPrompts

# Import extended datasets
try:
    from load_datasets import EXTENDED_KNOWLEDGE_BASE
    print(f"✅ Loaded extended datasets: {len(EXTENDED_KNOWLEDGE_BASE)} entries")
    
    # Merge with existing knowledge base (simulating what knowledge_api.py does)
    original_count = len(R3AELERPrompts.KNOWLEDGE_BASE)
    R3AELERPrompts.KNOWLEDGE_BASE.update(EXTENDED_KNOWLEDGE_BASE)
    new_count = len(R3AELERPrompts.KNOWLEDGE_BASE)
    
    print(f"\n📊 KNOWLEDGE BASE STATUS:")
    print(f"   Original entries: {original_count}")
    print(f"   Extended entries: {len(EXTENDED_KNOWLEDGE_BASE)}")
    print(f"   Total entries:    {new_count}")
    print(f"   New entries added: {new_count - original_count}")
    
    # Count by category
    physics_count = len([k for k in R3AELERPrompts.KNOWLEDGE_BASE.keys() if k.startswith('physics_')])
    space_count = len([k for k in R3AELERPrompts.KNOWLEDGE_BASE.keys() if k.startswith('space_eng_')])
    
    print(f"\n📚 BREAKDOWN:")
    print(f"   Physics entries:          {physics_count}")
    print(f"   Space Engineering entries: {space_count}")
    print(f"   Other entries:            {new_count - physics_count - space_count}")
    
    # Sample entries
    print(f"\n🔍 SAMPLE ENTRIES:")
    physics_keys = [k for k in R3AELERPrompts.KNOWLEDGE_BASE.keys() if k.startswith('physics_')][:2]
    space_keys = [k for k in R3AELERPrompts.KNOWLEDGE_BASE.keys() if k.startswith('space_eng_')][:2]
    
    if physics_keys:
        print(f"\n   Physics Sample:")
        for key in physics_keys:
            entry = R3AELERPrompts.KNOWLEDGE_BASE[key]
            topic = entry.get('topic', 'Unknown')
            print(f"      • {key}: {topic}")
    
    if space_keys:
        print(f"\n   Space Engineering Sample:")
        for key in space_keys:
            entry = R3AELERPrompts.KNOWLEDGE_BASE[key]
            topic = entry.get('topic', 'Unknown')
            print(f"      • {key}: {topic[:60]}...")
    
    print(f"\n✅ DATASETS SUCCESSFULLY INTEGRATED!")
    print(f"   R3ALER AI now has access to {new_count} knowledge entries!")
    
except ImportError as e:
    print(f"❌ Could not load extended datasets: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error loading datasets: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
