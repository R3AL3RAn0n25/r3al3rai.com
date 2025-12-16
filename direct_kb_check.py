#!/usr/bin/env python3
"""Direct KB check."""
import sys
sys.path.append('AI_Core_Worker')

from load_datasets import EXTENDED_KNOWLEDGE_BASE
from prompts import R3AELERPrompts

print(f"Extended KB: {len(EXTENDED_KNOWLEDGE_BASE)} entries")
print(f"R3ÆLƎR KB before merge: {len(R3AELERPrompts.KNOWLEDGE_BASE)} entries")

# Simulate the merge
R3AELERPrompts.KNOWLEDGE_BASE.update(EXTENDED_KNOWLEDGE_BASE)

print(f"R3ÆLƎR KB after merge: {len(R3AELERPrompts.KNOWLEDGE_BASE)} entries")

# Test search manually
q = 'quantum'
results = []
for key, value in R3AELERPrompts.KNOWLEDGE_BASE.items():
    if isinstance(value, dict):
        topic = value.get('topic', key)
        content = value.get('content', '')
        if q in topic.lower() or q in content.lower():
            results.append({'key': key, 'topic': topic, 'content': content[:100]})
            if len(results) >= 3:
                break
    else:
        if q in key.lower() or q in value.lower():
            results.append({'key': key, 'content': value[:100]})
            if len(results) >= 3:
                break

print(f"\nManual search for 'quantum': {len(results)} results")
for r in results:
    print(f"  - {r}")
