#!/usr/bin/env python3
"""
Process YouToks Quantum Physics II dataset from HuggingFace for R3ALER AI
Dataset: jilp00/YouToks-Instruct-Quantum-Physics-II (1,042 total entries)
"""

import json
import os

def process_youtoks_quantum_data():
    """Process the YouToks quantum physics dataset into knowledge base format."""
    
    # Read the raw JSON data
    with open('quantum_physics_youtoks_raw.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    knowledge_base = []
    
    # Process each row
    for row_data in data.get('rows', []):
        row = row_data.get('row', {})
        
        # Extract key information
        text = row.get('text', '')
        question = row.get('question', '')
        response = row.get('response', '')
        system_prompt = row.get('system_prompt', '')
        
        # Create a unique topic from the question
        topic = question if question else f"Quantum Physics Lecture Segment {row_data.get('row_idx', 0)}"
        
        # Build the content with question and response
        content_parts = []
        
        if question:
            content_parts.append(f"Question:\n{question}")
        
        if response:
            content_parts.append(f"\nAnswer:\n{response}")
        
        # Add lecture context if available
        if text and len(text) > 100:
            # Truncate very long text
            lecture_text = text[:500] + "..." if len(text) > 500 else text
            content_parts.append(f"\nLecture Context:\n{lecture_text}")
        
        if system_prompt:
            content_parts.append(f"\nContext:\n{system_prompt}")
        
        content = "\n".join(content_parts)
        
        # Create knowledge base entry with unique key
        entry_id = f"youtoks_qp_{row_data.get('row_idx', 0)}"
        entry = {
            "id": entry_id,
            "topic": topic[:200],  # Limit topic length
            "content": content,
            "category": "quantum_physics",
            "subcategory": "quantum_mechanics_lectures",
            "level": "graduate",
            "source": "HuggingFace jilp00/YouToks-Instruct-Quantum-Physics-II",
            "format": "lecture_qa"
        }
        
        knowledge_base.append(entry)
    
    print(f"✅ Processed {len(knowledge_base)} YouToks Quantum Physics entries")
    return knowledge_base

def save_to_json(knowledge_base, filename='quantum_physics_youtoks_knowledge_base.json'):
    """Save the processed knowledge base to JSON file."""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(knowledge_base, f, indent=2, ensure_ascii=False)
    
    file_size = os.path.getsize(filename)
    print(f"✅ Saved to {filename} ({file_size:,} bytes)")

if __name__ == "__main__":
    print("\n🔬 Processing YouToks Quantum Physics II Dataset\n")
    
    # Process the data
    knowledge_base = process_youtoks_quantum_data()
    
    # Save to JSON
    save_to_json(knowledge_base)
    
    print("\n✨ YouToks Quantum Physics dataset ready for integration!")
    print(f"   Total entries: {len(knowledge_base)}")
    
    # Show sample entry
    if knowledge_base:
        print("\n📖 Sample entry:")
        sample = knowledge_base[0]
        print(f"   ID: {sample['id']}")
        print(f"   Topic: {sample['topic'][:80]}...")
        print(f"   Category: {sample['category']}")
        print(f"   Content preview: {sample['content'][:200]}...")
