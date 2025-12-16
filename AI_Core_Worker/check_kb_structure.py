#!/usr/bin/env python3
"""Check knowledge base structure."""

from load_datasets import EXTENDED_KNOWLEDGE_BASE
from prompts import R3AELERPrompts
import json

print(f"Extended KB entries: {len(EXTENDED_KNOWLEDGE_BASE)}")
print(f"R3ÆLƎR KB entries: {len(R3AELERPrompts.KNOWLEDGE_BASE)}")

# Check first extended entry
if EXTENDED_KNOWLEDGE_BASE:
    first_key = list(EXTENDED_KNOWLEDGE_BASE.keys())[0]
    first_value = EXTENDED_KNOWLEDGE_BASE[first_key]
    print(f"\nFirst Extended Entry:")
    print(f"  Key: {first_key}")
    print(f"  Value type: {type(first_value)}")
    if isinstance(first_value, dict):
        print(f"  Value keys: {list(first_value.keys())}")
        print(f"  Sample: {json.dumps(first_value, indent=2)[:500]}")
    else:
        print(f"  Value: {first_value[:200]}...")

# Check first R3ÆLƎR entry
if R3AELERPrompts.KNOWLEDGE_BASE:
    first_key = list(R3AELERPrompts.KNOWLEDGE_BASE.keys())[0]
    first_value = R3AELERPrompts.KNOWLEDGE_BASE[first_key]
    print(f"\nFirst R3ÆLƎR Entry:")
    print(f"  Key: {first_key}")
    print(f"  Value type: {type(first_value)}")
    if isinstance(first_value, dict):
        print(f"  Value keys: {list(first_value.keys())}")
        print(f"  Sample: {json.dumps(first_value, indent=2)[:500]}")
    else:
        print(f"  Value: {first_value[:200]}...")
