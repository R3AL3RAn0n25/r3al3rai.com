#!/usr/bin/env python3
"""
Process ALL astrophysics and space engineering datasets
Total: 3,728 entries (Astronomy 678 + Exoplanets 50 + Aerospace 3,000)
"""

import json
import os

def process_astronomy_textbook():
    """Process astronomy textbook Q&A - 678 entries"""
    print("\n📥 Processing Astronomy Textbook Q&A...")
    
    with open('astronomy_textbook_qa_raw.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    knowledge_base = []
    
    for idx, item in enumerate(data.get('data', [])):
        question = item.get('question', '')
        answer = item.get('answer', '')
        context = item.get('context', '')
        
        if question and answer:
            content = f"Question:\n{question}\n\n"
            if context:
                content += f"Context:\n{context}\n\n"
            content += f"Answer:\n{answer}"
            
            entry = {
                "id": f"astronomy_textbook_{idx}",
                "topic": question[:200],
                "content": content,
                "category": "astronomy",
                "subcategory": "astronomy_textbook",
                "level": "undergraduate",
                "source": "Astronomy Textbook Q&A"
            }
            knowledge_base.append(entry)
    
    print(f"   ✅ Processed {len(knowledge_base):,} entries")
    return knowledge_base

def process_exoplanets():
    """Process exoplanets data - 50 entries"""
    print("\n📥 Processing Exoplanets Data...")
    
    with open('exoplanets_raw.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    knowledge_base = []
    
    for idx, item in enumerate(data.get('data', [])):
        # Exoplanet format varies, get all fields
        name = item.get('pl_name', item.get('name', f'Exoplanet {idx}'))
        
        # Create comprehensive entry with all available data
        content_parts = []
        
        for key, value in item.items():
            if value and key not in ['__index_level_0__']:
                content_parts.append(f"{key}: {value}")
        
        if content_parts:
            content = "\n".join(content_parts)
            
            entry = {
                "id": f"exoplanet_{idx}",
                "topic": f"Exoplanet: {name}",
                "content": content,
                "category": "astrophysics",
                "subcategory": "exoplanets",
                "level": "research",
                "source": "Exoplanets Database"
            }
            knowledge_base.append(entry)
    
    print(f"   ✅ Processed {len(knowledge_base):,} entries")
    return knowledge_base

def process_aerospace_corpus():
    """Process aerospace industry corpus - 3,000 entries"""
    print("\n📥 Processing Aerospace Industry Corpus...")
    
    with open('aerospace_BAAI_corpus_raw.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    knowledge_base = []
    
    for idx, row_data in enumerate(data.get('rows', [])):
        row = row_data.get('row', {})
        
        text = row.get('text', '')
        industry_type = row.get('industry_type', 'aerospace')
        
        if text and len(text) > 100:  # Filter out very short entries
            # Use first sentence or first 200 chars as topic
            topic = text.split('.')[0][:200] if '.' in text else text[:200]
            
            entry = {
                "id": f"aerospace_{idx}",
                "topic": topic,
                "content": text,
                "category": "aerospace_engineering",
                "subcategory": industry_type,
                "level": "professional",
                "source": "BAAI Aerospace Industry Corpus"
            }
            knowledge_base.append(entry)
    
    print(f"   ✅ Processed {len(knowledge_base):,} entries")
    return knowledge_base

def main():
    print("\n" + "="*80)
    print("🚀 PROCESSING ALL ASTROPHYSICS & SPACE ENGINEERING DATASETS")
    print("="*80)
    
    # Process all datasets
    all_knowledge = []
    
    all_knowledge.extend(process_astronomy_textbook())
    all_knowledge.extend(process_exoplanets())
    all_knowledge.extend(process_aerospace_corpus())
    
    # Save combined knowledge base
    output_file = 'space_astro_ALL_knowledge_base.json'
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_knowledge, f, indent=2, ensure_ascii=False)
    
    file_size_mb = os.path.getsize(output_file) / (1024 * 1024)
    
    print("\n" + "="*80)
    print("✅ PROCESSING COMPLETE!")
    print("="*80)
    print(f"\n💾 Output file: {output_file}")
    print(f"📊 File size: {file_size_mb:.2f} MB")
    print(f"📚 Total space/astro entries: {len(all_knowledge):,}")
    
    # Breakdown by source
    print(f"\n📖 BREAKDOWN BY SOURCE:")
    sources = {}
    for entry in all_knowledge:
        source = entry.get('source', 'Unknown')
        sources[source] = sources.get(source, 0) + 1
    
    for source, count in sorted(sources.items(), key=lambda x: x[1], reverse=True):
        print(f"   - {source}: {count:,} entries")
    
    # Breakdown by category
    print(f"\n📖 BREAKDOWN BY CATEGORY:")
    categories = {}
    for entry in all_knowledge:
        cat = entry.get('category', 'Unknown')
        categories[cat] = categories.get(cat, 0) + 1
    
    for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
        print(f"   - {cat}: {count:,} entries")
    
    print("\n" + "="*80)
    print("🎉 ALL ASTROPHYSICS & SPACE KNOWLEDGE READY FOR R3ALER AI!")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
