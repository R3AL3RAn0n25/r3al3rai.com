"""
Add HuggingFace Physics Dataset to R3ALER AI Knowledge Base
This script fetches physics problems and reasoning traces from HuggingFace
and adds them to the knowledge API
"""

import requests
import json
import sys
import os

# HuggingFace Dataset API endpoint
HF_DATASET_API = "https://datasets-server.huggingface.co/rows"
DATASET_NAME = "multimodal-reasoning-lab/Physics"

def fetch_physics_dataset(offset=0, length=100):
    """Fetch physics dataset from HuggingFace"""
    params = {
        "dataset": DATASET_NAME,
        "config": "default",
        "split": "train",
        "offset": offset,
        "length": length
    }
    
    print(f"📡 Fetching {length} rows from HuggingFace Physics dataset (offset={offset})...")
    response = requests.get(HF_DATASET_API, params=params, timeout=30)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Successfully fetched {len(data.get('rows', []))} physics problems")
        return data
    else:
        print(f"✗ Failed to fetch dataset: HTTP {response.status_code}")
        return None

def process_physics_data(hf_data):
    """Convert HuggingFace data to knowledge base format"""
    if not hf_data or 'rows' not in hf_data:
        return []
    
    knowledge_entries = []
    
    for item in hf_data['rows']:
        row = item.get('row', {})
        
        # Extract key fields
        question = row.get('Question', '').strip()
        reasoning = row.get('Text Reasoning Trace', '').strip()
        answer = row.get('Final Answer', '').strip()
        
        if not question:
            continue
        
        # Create a knowledge entry
        # Remove image placeholders for text-based knowledge
        question_clean = question.split('<image_start>')[0].strip()
        reasoning_clean = reasoning.replace('<image_start>', '').replace('<image_end>', '').strip()
        
        entry = {
            'topic': f'Physics Problem {item["row_idx"] + 1}',
            'question': question_clean,
            'reasoning': reasoning_clean[:1000] if len(reasoning_clean) > 1000 else reasoning_clean,  # Truncate if too long
            'answer': answer,
            'category': 'Physics',
            'source': 'HuggingFace: multimodal-reasoning-lab/Physics'
        }
        
        knowledge_entries.append(entry)
    
    print(f"📚 Processed {len(knowledge_entries)} physics knowledge entries")
    return knowledge_entries

def add_to_knowledge_api(entries, kb_api_url="http://localhost:5001"):
    """Add entries to the Knowledge API (if it has an ingest endpoint)"""
    print(f"\n📤 Attempting to add {len(entries)} entries to Knowledge API...")
    
    # Check if Knowledge API is running
    try:
        response = requests.get(f"{kb_api_url}/health", timeout=3)
        if response.status_code != 200:
            print(f"⚠ Knowledge API not responding. Save to file instead.")
            return False
    except requests.exceptions.RequestException:
        print(f"⚠ Knowledge API not reachable at {kb_api_url}")
        return False
    
    # TODO: Implement actual API endpoint to add knowledge
    # For now, save to file that can be imported
    print("ℹ Direct API ingestion not yet implemented. Saving to file...")
    return False

def save_to_file(entries, filename="physics_knowledge_base.json"):
    """Save knowledge entries to JSON file"""
    output_path = os.path.join(os.path.dirname(__file__), filename)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Saved {len(entries)} entries to {output_path}")
    print(f"\nℹ To use this data:")
    print(f"   1. Import this file in your prompts.py")
    print(f"   2. Add entries to R3AELERPrompts.KNOWLEDGE_BASE dictionary")
    print(f"   3. Or create a new endpoint in knowledge_api.py to load this JSON")

def create_import_code(entries, output_file="physics_kb_import.py"):
    """Generate Python code to import this data into prompts.py"""
    output_path = os.path.join(os.path.dirname(__file__), output_file)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('"""Generated Physics Knowledge Base - Import into prompts.py"""\n\n')
        f.write('PHYSICS_KNOWLEDGE_BASE = {\n')
        
        for i, entry in enumerate(entries[:50]):  # Limit to 50 for manageability
            topic = entry['topic'].lower().replace(' ', '_')
            content = f"{entry['question'][:200]}... Answer: {entry['answer'][:200]}..."
            f.write(f'    "{topic}": """{content}""",\n')
        
        f.write('}\n')
    
    print(f"🐍 Generated Python import file: {output_path}")
    print(f"   Add this to AI_Core_Worker/prompts.py")

if __name__ == '__main__':
    print("🧪 R3ALER AI - HuggingFace Physics Dataset Importer")
    print("=" * 60)
    
    # Fetch dataset
    num_rows = 100  # Adjust as needed (max per request is 100)
    offset = 0
    
    hf_data = fetch_physics_dataset(offset=offset, length=num_rows)
    
    if not hf_data:
        print("❌ Failed to fetch dataset. Exiting.")
        sys.exit(1)
    
    # Process data
    knowledge_entries = process_physics_data(hf_data)
    
    if not knowledge_entries:
        print("❌ No knowledge entries created. Exiting.")
        sys.exit(1)
    
    # Save results
    save_to_file(knowledge_entries)
    create_import_code(knowledge_entries)
    
    # Show sample
    print(f"\n📊 Sample Entry:")
    print(f"Topic: {knowledge_entries[0]['topic']}")
    print(f"Question: {knowledge_entries[0]['question'][:150]}...")
    print(f"Answer: {knowledge_entries[0]['answer'][:150]}...")
    
    print(f"\n✅ Physics dataset import complete!")
    print(f"\n💡 Total dataset size: {hf_data.get('num_rows_total', 'unknown')} problems available")
    print(f"   You fetched: {len(knowledge_entries)} problems")
    print(f"\n📝 Next steps:")
    print(f"   1. Review physics_knowledge_base.json")
    print(f"   2. Integrate into your Knowledge API or prompts.py")
    print(f"   3. Run this script again with different offset to fetch more")
