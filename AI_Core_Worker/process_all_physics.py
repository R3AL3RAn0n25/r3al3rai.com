#!/usr/bin/env python3
"""
Process ALL downloaded physics datasets for R3ALER AI
Combines camel-ai/physics (19,900) + physics-stackexchange (3,700) + 
Feynman lectures (641) + physics_wiki (1,081) + introvoyz041 (1,297)
Total: ~26,619 physics entries!
"""

import json
import os

def process_camel_ai_physics():
    """Process camel-ai/physics dataset"""
    print("\n📥 Processing camel-ai/physics...")
    
    with open('physics_camel_ai_physics_raw.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    knowledge_base = []
    
    for idx, row_data in enumerate(data.get('rows', [])):
        row = row_data.get('row', {})
        
        # Camel-AI format
        message_1 = row.get('message_1', '')
        message_2 = row.get('message_2', '')
        
        if message_1 and message_2:
            entry = {
                "id": f"physics_camel_{idx}",
                "topic": message_1[:200] if len(message_1) < 500 else "Physics Concept",
                "content": f"Question:\n{message_1}\n\nAnswer:\n{message_2}",
                "category": "physics",
                "subcategory": "camel_ai_physics",
                "level": "undergraduate",
                "source": "CAMEL-AI Physics Dataset"
            }
            knowledge_base.append(entry)
    
    print(f"   ✅ Processed {len(knowledge_base):,} entries")
    return knowledge_base

def process_physics_stackexchange():
    """Process marianna13/physics-stackexchange dataset"""
    print("\n📥 Processing physics-stackexchange...")
    
    with open('physics_marianna13_physics_stackexchange_raw.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    knowledge_base = []
    
    for idx, row_data in enumerate(data.get('rows', [])):
        row = row_data.get('row', {})
        
        # Stack Exchange format: question_title, question_text, answers (list)
        question_title = row.get('question_title', '')
        question_text = row.get('question_text', '')
        answers = row.get('answers', [])
        
        if question_title and answers and len(answers) > 0:
            # Use the top answer
            top_answer = answers[0].get('answer_text', '') if isinstance(answers[0], dict) else str(answers[0])
            
            content = f"Question: {question_title}\n\n"
            if question_text:
                content += f"Details:\n{question_text}\n\n"
            content += f"Answer:\n{top_answer}"
            
            entry = {
                "id": f"physics_stackex_{idx}",
                "topic": question_title[:200],
                "content": content,
                "category": "physics",
                "subcategory": "physics_stackexchange",
                "level": "mixed",
                "source": "Physics StackExchange"
            }
            knowledge_base.append(entry)
    
    print(f"   ✅ Processed {len(knowledge_base):,} entries")
    return knowledge_base

def process_feynman_lectures():
    """Process Feynman Lectures on Physics"""
    print("\n📥 Processing Feynman Lectures...")
    
    with open('physics_enesxgrahovac_the_feynman_lectures_on_physics_raw.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    knowledge_base = []
    
    for idx, item in enumerate(data.get('data', [])):
        # Feynman format: chapter_title, section_title, section_text
        chapter_title = item.get('chapter_title', '')
        section_title = item.get('section_title', '')
        section_text = item.get('section_text', '')
        
        if section_text:
            topic = f"{chapter_title} - {section_title}" if section_title else chapter_title
            
            entry = {
                "id": f"physics_feynman_{idx}",
                "topic": topic[:200],
                "content": section_text,
                "category": "physics",
                "subcategory": "feynman_lectures",
                "level": "undergraduate",
                "source": "Feynman Lectures on Physics"
            }
            knowledge_base.append(entry)
    
    print(f"   ✅ Processed {len(knowledge_base):,} entries")
    return knowledge_base

def process_physics_wiki():
    """Process burgerbee/physics_wiki"""
    print("\n📥 Processing physics_wiki...")
    
    with open('physics_burgerbee_physics_wiki_raw.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    knowledge_base = []
    
    for idx, item in enumerate(data.get('data', [])):
        title = item.get('title', '')
        text = item.get('text', '')
        
        if title and text:
            entry = {
                "id": f"physics_wiki_{idx}",
                "topic": title[:200],
                "content": text,
                "category": "physics",
                "subcategory": "physics_wiki",
                "level": "reference",
                "source": "Physics Wikipedia"
            }
            knowledge_base.append(entry)
    
    print(f"   ✅ Processed {len(knowledge_base):,} entries")
    return knowledge_base

def process_introvoyz_physics():
    """Process introvoyz041/physics"""
    print("\n📥 Processing introvoyz041/physics...")
    
    with open('physics_introvoyz041_physics_raw.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    knowledge_base = []
    
    for idx, item in enumerate(data.get('data', [])):
        # Introvoyz format: questions, solutions, final_answers
        questions = item.get('questions', '')
        solutions = item.get('solutions', '')
        final_answers = item.get('final_answers', '')
        
        if questions and (solutions or final_answers):
            content = f"Question:\n{questions}\n\n"
            if solutions:
                content += f"Solution:\n{solutions}\n\n"
            if final_answers:
                content += f"Final Answer:\n{final_answers}"
            
            entry = {
                "id": f"physics_intro_{idx}",
                "topic": questions[:200],
                "content": content,
                "category": "physics",
                "subcategory": "physics_qa",
                "level": "mixed",
                "source": "Introvoyz Physics QA"
            }
            knowledge_base.append(entry)
    
    print(f"   ✅ Processed {len(knowledge_base):,} entries")
    return knowledge_base

def main():
    print("\n" + "="*80)
    print("🎓 PROCESSING ALL PHYSICS DATASETS FOR R3ALER AI")
    print("="*80)
    
    # Process all datasets
    all_knowledge = []
    
    all_knowledge.extend(process_camel_ai_physics())
    all_knowledge.extend(process_physics_stackexchange())
    all_knowledge.extend(process_feynman_lectures())
    all_knowledge.extend(process_physics_wiki())
    all_knowledge.extend(process_introvoyz_physics())
    
    # Save combined knowledge base
    output_file = 'physics_ALL_knowledge_base.json'
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_knowledge, f, indent=2, ensure_ascii=False)
    
    file_size_mb = os.path.getsize(output_file) / (1024 * 1024)
    
    print("\n" + "="*80)
    print("✅ PROCESSING COMPLETE!")
    print("="*80)
    print(f"\n💾 Output file: {output_file}")
    print(f"📊 File size: {file_size_mb:.2f} MB")
    print(f"📚 Total physics entries: {len(all_knowledge):,}")
    
    # Breakdown by source
    print(f"\n📖 BREAKDOWN BY SOURCE:")
    sources = {}
    for entry in all_knowledge:
        source = entry.get('source', 'Unknown')
        sources[source] = sources.get(source, 0) + 1
    
    for source, count in sorted(sources.items(), key=lambda x: x[1], reverse=True):
        print(f"   - {source}: {count:,} entries")
    
    print("\n" + "="*80)
    print("🎉 ALL PHYSICS KNOWLEDGE READY FOR R3ALER AI!")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
