"""
Import Physics and Space Engineering Datasets into Knowledge API
This script loads the JSON datasets and adds them to R3AELERPrompts.KNOWLEDGE_BASE
"""

import json
import os

def load_physics_knowledge():
    """Load COMPLETE Physics dataset from JSON file (25,875 entries from 5 sources)."""
    file_path = os.path.join(os.path.dirname(__file__), 'physics_ALL_knowledge_base.json')
    
    if not os.path.exists(file_path):
        print(f"⚠️  Complete Physics dataset not found: {file_path}")
        # Fallback to original small dataset
        file_path = os.path.join(os.path.dirname(__file__), 'physics_knowledge_base.json')
        if not os.path.exists(file_path):
            print(f"⚠️  Physics dataset not found: {file_path}")
            return {}
        
        # Load original format
        with open(file_path, 'r', encoding='utf-8') as f:
            physics_data = json.load(f)
        
        knowledge_dict = {}
        for idx, entry in enumerate(physics_data):
            key = f"physics_{idx}"
            knowledge_dict[key] = {
                "content": f"Topic: {entry['topic']}\n\nQuestion: {entry['question']}\n\nReasoning: {entry.get('reasoning', '')}\n\nAnswer: {entry['answer']}",
                "category": entry.get('category', 'Physics'),
                "topic": entry['topic'],
                "source": entry.get('source', 'HuggingFace Physics Dataset')
            }
        print(f"✅ Loaded {len(knowledge_dict)} Physics entries (original dataset)")
        return knowledge_dict
    
    # Load complete physics dataset
    with open(file_path, 'r', encoding='utf-8') as f:
        physics_data = json.load(f)
    
    # Convert to knowledge base format
    knowledge_dict = {}
    for entry in physics_data:
        key = entry['id']
        knowledge_dict[key] = {
            "content": entry['content'],
            "category": entry.get('category', 'Physics'),
            "topic": entry['topic'],
            "level": entry.get('level', 'mixed'),
            "subcategory": entry.get('subcategory', 'physics'),
            "source": entry.get('source', 'HuggingFace Physics Dataset')
        }
    
    print(f"✅ Loaded {len(knowledge_dict)} Physics entries (complete dataset)")
    return knowledge_dict


def load_space_engineering_knowledge():
    """Load Space Engineering dataset from JSON file."""
def load_space_engineering_knowledge():
    """Load COMPLETE Space Engineering, Astrophysics & Aerospace dataset (3,727 + 97 = 3,824 entries)."""
    
    # Load new comprehensive space/astro dataset
    file_path = os.path.join(os.path.dirname(__file__), 'space_astro_ALL_knowledge_base.json')
    
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            space_astro_data = json.load(f)
        
        knowledge_dict = {}
        for entry in space_astro_data:
            key = entry['id']
            knowledge_dict[key] = {
                "content": entry['content'],
                "category": entry.get('category', 'Space Engineering'),
                "topic": entry['topic'],
                "level": entry.get('level', 'professional'),
                "subcategory": entry.get('subcategory', 'space_engineering'),
                "source": entry.get('source', 'Space & Astrophysics Dataset')
            }
        
        print(f"✅ Loaded {len(knowledge_dict)} Space/Astro/Aerospace entries (complete dataset)")
        return knowledge_dict
    
    # Fallback to original small dataset
    file_path = os.path.join(os.path.dirname(__file__), 'space_engineering_knowledge_base.json')
    
    if not os.path.exists(file_path):
        print(f"⚠️  Space Engineering dataset not found: {file_path}")
        return {}
    
    with open(file_path, 'r', encoding='utf-8') as f:
        space_data = json.load(f)
    
    # Convert to knowledge base format
    knowledge_dict = {}
    for idx, entry in enumerate(space_data):
        key = f"space_eng_{entry.get('keyword', idx)}"
        knowledge_dict[key] = {
            "content": f"Topic: {entry['topic']}\n\nQuestion: {entry['question']}\n\nAnswer: {entry['answer']}",
            "category": entry.get('category', 'Space Engineering'),
            "topic": entry['topic'],
            "keyword": entry.get('keyword', ''),
            "source": entry.get('source', 'HuggingFace Space Engineering Dataset')
        }
    
    print(f"✅ Loaded {len(knowledge_dict)} Space Engineering entries (original dataset)")
    return knowledge_dict


def load_quantum_physics_knowledge():
    """Load Quantum Physics dataset from JSON file (small VVUQ dataset)."""
    file_path = os.path.join(os.path.dirname(__file__), 'quantum_physics_knowledge_base.json')
    
    if not os.path.exists(file_path):
        print(f"⚠️  Quantum Physics VVUQ dataset not found: {file_path}")
        return {}
    
    with open(file_path, 'r', encoding='utf-8') as f:
        quantum_data = json.load(f)
    
    # Convert to knowledge base format
    knowledge_dict = {}
    for entry in quantum_data:
        key = entry['id'].replace('-', '_')
        knowledge_dict[key] = {
            "content": entry['content'],
            "category": entry.get('category', 'Quantum Physics'),
            "topic": entry['topic'],
            "level": entry.get('level', 'graduate'),
            "subcategory": entry.get('subcategory', 'quantum_physics'),
            "source": entry.get('source', 'HuggingFace Quantum Physics Dataset')
        }
    
    print(f"✅ Loaded {len(knowledge_dict)} Quantum Physics VVUQ entries")
    return knowledge_dict


def load_quantum_physics_youtoks():
    """Load COMPLETE YouToks Quantum Physics II dataset from JSON file (ALL 1,042 lecture entries)."""
    file_path = os.path.join(os.path.dirname(__file__), 'quantum_physics_youtoks_FULL_knowledge_base.json')
    
    if not os.path.exists(file_path):
        print(f"⚠️  YouToks Quantum Physics FULL dataset not found: {file_path}")
        return {}
    
    with open(file_path, 'r', encoding='utf-8') as f:
        quantum_data = json.load(f)
    
    # Convert to knowledge base format
    knowledge_dict = {}
    for entry in quantum_data:
        key = entry['id']
        knowledge_dict[key] = {
            "content": entry['content'],
            "category": entry.get('category', 'Quantum Physics'),
            "topic": entry['topic'],
            "level": entry.get('level', 'graduate'),
            "subcategory": entry.get('subcategory', 'quantum_mechanics_lectures'),
            "source": entry.get('source', 'HuggingFace YouToks Quantum Physics')
        }
    
    print(f"✅ Loaded {len(knowledge_dict)} YouToks Quantum Physics lecture entries")
    return knowledge_dict


# Load all datasets
PHYSICS_KB = load_physics_knowledge()
SPACE_ENGINEERING_KB = load_space_engineering_knowledge()
QUANTUM_PHYSICS_KB = load_quantum_physics_knowledge()
QUANTUM_PHYSICS_YOUTOKS_KB = load_quantum_physics_youtoks()

# Combined knowledge base
EXTENDED_KNOWLEDGE_BASE = {
    **PHYSICS_KB,
    **SPACE_ENGINEERING_KB,
    **QUANTUM_PHYSICS_KB,
    **QUANTUM_PHYSICS_YOUTOKS_KB
}

print(f"\n📊 Total Extended Knowledge: {len(EXTENDED_KNOWLEDGE_BASE)} entries")
print(f"   - Physics: {len(PHYSICS_KB):,}")
print(f"   - Space/Astro/Aerospace: {len(SPACE_ENGINEERING_KB):,}")
print(f"   - Quantum Physics (VVUQ): {len(QUANTUM_PHYSICS_KB)}")
print(f"   - Quantum Physics (YouToks): {len(QUANTUM_PHYSICS_YOUTOKS_KB):,}")
