#!/usr/bin/env python3
"""
Space Engineering Dataset Importer
Fetches and processes the Space Engineering dataset from HuggingFace
and converts it to R3ALER AI knowledge base format.
"""

import json
import os

def process_space_engineering_data(input_file='space_engineering_raw.json', max_entries=100):
    """
    Process the Space Engineering dataset and convert to knowledge base format.
    
    Args:
        input_file: Path to the raw JSON file from HuggingFace
        max_entries: Maximum number of entries to process (default: 100)
    """
    print(f"📚 Processing Space Engineering dataset...")
    
    # Load the raw data
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: {input_file} not found!")
        return None
    
    # Extract rows from the HuggingFace response
    if 'rows' not in raw_data:
        print("❌ Error: No 'rows' field in the data!")
        return None
    
    rows = raw_data['rows'][:max_entries]
    print(f"✓ Found {len(rows)} entries")
    
    # Process each entry
    knowledge_base = []
    
    for idx, item in enumerate(rows, 1):
        try:
            row_data = item.get('row', {})
            
            # Extract fields from the dataset
            keyword = row_data.get('keyword', '').strip()
            topic = row_data.get('topic', 'Space Engineering').strip()
            language = row_data.get('language', 'English').strip()
            generated_entry = row_data.get('generated_entry', {})
            messages = generated_entry.get('messages', [])
            
            if len(messages) < 3:
                print(f"⚠️  Skipping entry {idx}: Insufficient messages")
                continue
            
            # Extract system prompt, user question, and assistant answer
            system_prompt = ""
            user_question = ""
            assistant_answer = ""
            
            for msg in messages:
                role = msg.get('role', '')
                content = msg.get('content', '').strip()
                
                if role == 'system':
                    system_prompt = content
                elif role == 'user':
                    user_question = content
                elif role == 'assistant':
                    assistant_answer = content
            
            if not user_question or not assistant_answer:
                print(f"⚠️  Skipping entry {idx}: Missing question or answer")
                continue
            
            # Create knowledge base entry
            entry = {
                "topic": f"{topic} - {keyword.replace('_', ' ').title()}",
                "question": user_question,
                "answer": assistant_answer,
                "category": topic,
                "keyword": keyword,
                "system_context": system_prompt,
                "language": language,
                "source": "HuggingFace: patrickfleith/synthgenai-space-engineering-instruct-1k",
                "type": "space_engineering",
                "tags": ["space", "engineering", keyword.replace('_', ' ')]
            }
            
            knowledge_base.append(entry)
            
            if idx % 20 == 0:
                print(f"  Processed {idx}/{len(rows)} entries...")
                
        except Exception as e:
            print(f"⚠️  Error processing entry {idx}: {e}")
            continue
    
    print(f"✓ Successfully processed {len(knowledge_base)} entries")
    return knowledge_base


def save_to_json(data, output_file='space_engineering_knowledge_base.json'):
    """Save the knowledge base to a JSON file."""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    file_size = os.path.getsize(output_file)
    print(f"✓ Saved to {output_file} ({file_size:,} bytes)")


def generate_import_code(data, output_file='space_engineering_kb_import.py'):
    """Generate Python code to import into knowledge_api.py"""
    
    # Sample a few entries for the import file (not all 100 to keep file size reasonable)
    sample_size = min(50, len(data))
    sample_data = data[:sample_size]
    
    code = f'''"""
Space Engineering Knowledge Base Import
Auto-generated from HuggingFace dataset: patrickfleith/synthgenai-space-engineering-instruct-1k
Total entries available: {len(data)}
Sample included: {sample_size}

To use this in your knowledge_api.py:
1. Copy the SPACE_ENGINEERING_KB dictionary below
2. Add it to your R3AELERPrompts.KNOWLEDGE_BASE
3. Or merge it with existing knowledge
"""

SPACE_ENGINEERING_KB = {{
'''
    
    for idx, entry in enumerate(sample_data):
        topic = entry['topic'].replace("'", "\\'")
        question = entry['question'].replace("'", "\\'")[:200]  # Truncate long questions
        answer = entry['answer'].replace("'", "\\'")[:500]  # Truncate long answers
        category = entry['category']
        
        code += f'''    "{topic}_{idx}": {{
        "topic": "{topic}",
        "question": "{question}{'...' if len(entry['question']) > 200 else ''}",
        "answer": "{answer}{'...' if len(entry['answer']) > 500 else ''}",
        "category": "{category}",
        "source": "HuggingFace Space Engineering Dataset",
        "tags": ["space", "engineering", "{category.lower()}"]
    }},
'''
    
    code += '''}

# Usage example:
# from space_engineering_kb_import import SPACE_ENGINEERING_KB
# R3AELERPrompts.KNOWLEDGE_BASE.update(SPACE_ENGINEERING_KB)
'''
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(code)
    
    file_size = os.path.getsize(output_file)
    print(f"✓ Generated import code: {output_file} ({file_size:,} bytes)")


def main():
    print("=" * 70)
    print("🚀 SPACE ENGINEERING KNOWLEDGE BASE IMPORTER")
    print("=" * 70)
    print()
    
    # Check if raw data file exists
    raw_file = 'space_engineering_raw.json'
    if not os.path.exists(raw_file):
        print(f"❌ Raw data file '{raw_file}' not found!")
        print("Please run the curl command first to download the data.")
        return
    
    # Process the data
    knowledge_base = process_space_engineering_data(raw_file, max_entries=100)
    
    if not knowledge_base:
        print("❌ Failed to process data")
        return
    
    print()
    print("=" * 70)
    print("💾 SAVING OUTPUT FILES")
    print("=" * 70)
    print()
    
    # Save to JSON
    save_to_json(knowledge_base)
    
    # Generate import code
    generate_import_code(knowledge_base)
    
    print()
    print("=" * 70)
    print("📊 DATASET STATISTICS")
    print("=" * 70)
    print()
    print(f"  Total entries:        {len(knowledge_base)}")
    
    # Count categories
    categories = {}
    for entry in knowledge_base:
        cat = entry['category']
        categories[cat] = categories.get(cat, 0) + 1
    
    print(f"  Unique categories:    {len(categories)}")
    print()
    print("  Top categories:")
    for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"    • {cat:30} {count:3} entries")
    
    print()
    print("=" * 70)
    print("✅ SPACE ENGINEERING DATASET READY!")
    print("=" * 70)
    print()
    print("📝 Sample entry:")
    if knowledge_base:
        sample = knowledge_base[0]
        print(f"  Topic:    {sample['topic']}")
        print(f"  Category: {sample['category']}")
        print(f"  Question: {sample['question'][:100]}...")
        print(f"  Answer:   {sample['answer'][:150]}...")
    
    print()
    print("🎯 Next steps:")
    print("  1. Review: space_engineering_knowledge_base.json")
    print("  2. Import: space_engineering_kb_import.py")
    print("  3. Integrate into knowledge_api.py (see SPACE_INTEGRATION_GUIDE.py)")
    print()


if __name__ == '__main__':
    main()
