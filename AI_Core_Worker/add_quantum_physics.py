#!/usr/bin/env python3
"""
Process Quantum Physics dataset from HuggingFace for R3ALER AI Knowledge Base
Dataset: englund/quantum-physics-vvuq-complete
"""

import json
import os

def process_quantum_physics_data():
    """Process the quantum physics dataset into knowledge base format."""
    
    # Read the raw JSON data
    with open('quantum_physics_raw.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    knowledge_base = []
    
    # Process each row
    for row_data in data.get('rows', []):
        row = row_data.get('row', {})
        
        # Skip corrupted/error entries (has_error = True)
        if row.get('has_error', False):
            continue
        
        # Extract key information
        problem_id = row.get('id', '')
        domain = row.get('domain', 'quantum_physics')
        title = row.get('title', '')
        physics_level = row.get('physics_level', 'graduate')
        problem_type = row.get('problem_type', 'original')
        natural_problem = row.get('natural_language_problem', '')
        solution_approach = row.get('solution_approach', '')
        key_concepts = row.get('key_concepts', [])
        
        # Create a unique topic combining domain and title
        topic = f"Quantum Physics - {title}"
        
        # Build the content with problem and solution
        content_parts = []
        
        if natural_problem:
            content_parts.append(f"Problem:\n{natural_problem}")
        
        if solution_approach:
            content_parts.append(f"\nSolution Approach:\n{solution_approach}")
        
        if key_concepts:
            content_parts.append(f"\nKey Concepts: {', '.join(key_concepts)}")
        
        content = "\n".join(content_parts)
        
        # Create knowledge base entry
        entry = {
            "topic": topic,
            "content": content,
            "category": "quantum_physics",
            "subcategory": domain,
            "level": physics_level,
            "problem_type": problem_type,
            "concepts": key_concepts,
            "source": "HuggingFace englund/quantum-physics-vvuq-complete",
            "id": problem_id
        }
        
        knowledge_base.append(entry)
    
    print(f"✅ Processed {len(knowledge_base)} valid Quantum Physics entries")
    print(f"   (Skipped {len(data.get('rows', [])) - len(knowledge_base)} corrupted entries)")
    
    return knowledge_base

def save_to_json(knowledge_base, filename='quantum_physics_knowledge_base.json'):
    """Save the processed knowledge base to JSON file."""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(knowledge_base, f, indent=2, ensure_ascii=False)
    
    file_size = os.path.getsize(filename)
    print(f"✅ Saved to {filename} ({file_size:,} bytes)")

def generate_python_dict(knowledge_base, output_file='quantum_physics_kb_dict.py'):
    """Generate Python dictionary format for direct import."""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('"""Quantum Physics Knowledge Base for R3ALER AI"""\n\n')
        f.write('QUANTUM_PHYSICS_KB = {\n')
        
        for entry in knowledge_base:
            # Create a safe key from the ID
            key = entry['id'].replace('-', '_')
            
            f.write(f'    "{key}": {{\n')
            f.write(f'        "content": """{entry["content"]}""",\n')
            f.write(f'        "category": "{entry["category"]}",\n')
            f.write(f'        "topic": "{entry["topic"]}",\n')
            f.write(f'        "source": "{entry["source"]}",\n')
            f.write(f'        "level": "{entry["level"]}",\n')
            f.write(f'        "subcategory": "{entry["subcategory"]}",\n')
            f.write(f'    }},\n')
        
        f.write('}\n')
    
    print(f"✅ Generated Python dictionary: {output_file}")

if __name__ == "__main__":
    print("\n🔬 Processing Quantum Physics Dataset for R3ALER AI\n")
    
    # Process the data
    knowledge_base = process_quantum_physics_data()
    
    # Save to JSON
    save_to_json(knowledge_base)
    
    # Generate Python dictionary
    generate_python_dict(knowledge_base)
    
    print("\n✨ Quantum Physics dataset ready for integration!")
    print(f"   Total entries: {len(knowledge_base)}")
    
    # Show sample entry
    if knowledge_base:
        print("\n📖 Sample entry:")
        sample = knowledge_base[0]
        print(f"   Topic: {sample['topic']}")
        print(f"   Category: {sample['category']}")
        print(f"   Level: {sample['level']}")
        print(f"   Content preview: {sample['content'][:150]}...")
