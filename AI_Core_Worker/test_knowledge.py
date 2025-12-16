import sys
import os
sys.path.append(os.path.dirname(__file__))
from prompts import R3AELERPrompts

print("Total topics:", len(R3AELERPrompts.KNOWLEDGE_BASE))
print("All topics:", list(R3AELERPrompts.KNOWLEDGE_BASE.keys()))
print()
print("Law-related topics:", [k for k in R3AELERPrompts.KNOWLEDGE_BASE.keys() if 'law' in k])
print()
if 'missouri_law' in R3AELERPrompts.KNOWLEDGE_BASE:
    content = R3AELERPrompts.KNOWLEDGE_BASE['missouri_law']
    print("Missouri law content length:", len(content))
    print("Content preview:", content[:200])