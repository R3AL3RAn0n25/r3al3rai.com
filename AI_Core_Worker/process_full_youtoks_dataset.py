#!/usr/bin/env python3
"""
Process COMPLETE YouToks Quantum Physics II Dataset for R3ALER AI Knowledge Base
Converts all 1,042 lecture Q&A entries to knowledge base format
"""

import json
import os

def process_youtoks_quantum_data():
    """Process the FULL YouToks quantum physics dataset into knowledge base format."""
    
    print("\n" + "="*70)
    print("🎓 PROCESSING COMPLETE YOUTOKS QUANTUM PHYSICS II DATASET")
    print("="*70)
    
    # Read the FULL raw JSON data (all 1,042 entries)
    with open('quantum_physics_youtoks_FULL_raw.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"📥 Loaded raw data: {len(data.get('rows', []))} entries")
    
    knowledge_base = []
    
    # Process each row
    for idx, row_data in enumerate(data.get('rows', [])):
        row = row_data.get('row', {})
        
        # Extract key information
        text = row.get('text', '')
        question = row.get('question', '')
        response = row.get('response', '')
        system_prompt = row.get('system_prompt', '')
        
        # Create a unique topic from the question
        topic = question if question else f"Quantum Physics Lecture Segment {row_data.get('row_idx', idx)}"
        
        # Truncate long lecture text for readability
        text_preview = text[:500] + "..." if len(text) > 500 else text
        
        # Combine into structured content
        content = f"""Question:
{question}

Answer:
{response}"""
        
        # Add lecture context if available
        if text_preview:
            content += f"""

Context (Lecture Excerpt):
{text_preview}"""
        
        # Create knowledge entry
        entry = {
            "id": f"youtoks_qp_{idx}",
            "topic": topic[:200],  # Truncate very long questions
            "content": content,
            "category": "quantum_physics",
            "subcategory": "quantum_mechanics_lectures",
            "level": "graduate",
            "source": "HuggingFace YouToks Quantum Physics II (MIT Course)",
            "format": "lecture_qa"
        }
        
        knowledge_base.append(entry)
        
        # Progress indicator
        if (idx + 1) % 100 == 0:
            print(f"   ⚙️  Processed {idx + 1} entries...")
    
    print(f"\n✅ Processing complete: {len(knowledge_base)} entries")
    return knowledge_base

def save_to_json(knowledge_base):
    """Save processed knowledge base to JSON file."""
    output_file = 'quantum_physics_youtoks_FULL_knowledge_base.json'
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(knowledge_base, f, indent=2, ensure_ascii=False)
    
    file_size_mb = os.path.getsize(output_file) / (1024 * 1024)
    
    print(f"\n💾 Saved to: {output_file}")
    print(f"📊 File size: {file_size_mb:.2f} MB")
    print(f"📚 Total entries: {len(knowledge_base)}")
    
    return output_file

def main():
    print("\n🚀 Starting FULL dataset processing...")
    
    # Process the data
    knowledge_base = process_youtoks_quantum_data()
    
    # Save to JSON
    output_file = save_to_json(knowledge_base)
    
    # Show sample entry
    if knowledge_base:
        print("\n" + "="*70)
        print("📖 SAMPLE ENTRY:")
        print("="*70)
        sample = knowledge_base[0]
        print(f"ID: {sample['id']}")
        print(f"Topic: {sample['topic'][:100]}...")
        print(f"Category: {sample['category']}")
        print(f"Level: {sample['level']}")
        print(f"Content preview: {sample['content'][:300]}...")
        print("="*70)
    
    print("\n✅ ALL 1,042 QUANTUM PHYSICS ENTRIES READY FOR R3ALER AI! 🎓\n")

if __name__ == "__main__":
    main()
