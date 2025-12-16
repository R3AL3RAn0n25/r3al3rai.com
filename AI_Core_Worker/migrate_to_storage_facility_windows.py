"""
Migrate JSON knowledge bases to PostgreSQL Storage Facility - Windows Version
Connects directly to Windows PostgreSQL
"""

import json
import os
import psycopg2
from datetime import datetime

# Windows PostgreSQL Configuration
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'r3aler_ai',
    'user': 'r3aler_user_2025',
    'password': 'postgres'
}

# Storage units
UNITS = {
    'physics': 'physics_unit',
    'quantum': 'quantum_unit',
    'space': 'space_unit',
    'crypto': 'crypto_unit'
}

def migrate_json_to_unit(json_file: str, unit_id: str):
    """Migrate a JSON knowledge base to a storage unit"""
    
    print(f"\n📥 Migrating {os.path.basename(json_file)} to '{unit_id}' unit...")
    
    if not os.path.exists(json_file):
        print(f"❌ File not found: {json_file}")
        return None
    
    try:
        # Load JSON
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Convert to list
        entries = []
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, str):
                    entries.append({
                        'id': key,
                        'content': value,
                        'topic': key,
                        'category': '',
                        'source': os.path.basename(json_file)
                    })
                elif isinstance(value, dict):
                    entries.append({
                        'id': key,
                        'content': value.get('content', value.get('answer', value.get('explanation', ''))),
                        'topic': value.get('topic', value.get('question', key)),
                        'category': value.get('category', value.get('domain', '')),
                        'subcategory': value.get('subcategory', ''),
                        'level': value.get('level', value.get('difficulty', '')),
                        'source': value.get('source', os.path.basename(json_file))
                    })
        elif isinstance(data, list):
            entries = data
        
        print(f"   Found {len(entries)} entries")
        
        # Connect to PostgreSQL
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        schema = UNITS[unit_id]
        
        # Process in batches
        batch_size = 500
        stored = 0
        errors = 0
        
        for i in range(0, len(entries), batch_size):
            batch = entries[i:i+batch_size]
            print(f"   Batch {i//batch_size + 1}/{(len(entries)-1)//batch_size + 1}...", end='')
            
            for entry in batch:
                try:
                    entry_id = entry.get('id', f"{unit_id}_{stored}")
                    topic = entry.get('topic', '')[:500] if entry.get('topic') else ''
                    content = entry.get('content', '')
                    category = entry.get('category', '')[:200] if entry.get('category') else ''
                    subcategory = entry.get('subcategory', '')[:200] if entry.get('subcategory') else ''
                    level = entry.get('level', '')[:100] if entry.get('level') else ''
                    source = entry.get('source', '')[:200] if entry.get('source') else ''
                    
                    if not content and not topic:
                        continue
                    
                    cursor.execute(f"""
                        INSERT INTO {schema}.knowledge 
                        (entry_id, topic, content, category, subcategory, level, source)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (entry_id) DO UPDATE SET
                            topic = EXCLUDED.topic,
                            content = EXCLUDED.content,
                            category = EXCLUDED.category
                    """, (entry_id, topic, content, category, subcategory, level, source))
                    
                    stored += 1
                except Exception as e:
                    errors += 1
                    if errors < 3:
                        print(f"\n   ⚠️  Error: {e}")
            
            conn.commit()
            print(f" ✅ {stored} stored")
        
        cursor.close()
        conn.close()
        
        print(f"   ✅ Total: {stored} stored, {errors} errors")
        return {'stored': stored, 'errors': errors}
        
    except Exception as e:
        print(f"❌ Migration error: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == '__main__':
    migrations = [
        ('physics_ALL_knowledge_base.json', 'physics'),
        ('quantum_physics_youtoks_FULL_knowledge_base.json', 'quantum'),
        ('space_astro_ALL_knowledge_base.json', 'space'),
    ]
    
    print("\n" + "=" * 60)
    print("🏢 R3ÆL3R STORAGE FACILITY MIGRATION (Windows)")
    print("=" * 60)
    
    total_stored = 0
    total_errors = 0
    
    for json_file, unit_id in migrations:
        result = migrate_json_to_unit(json_file, unit_id)
        if result:
            total_stored += result['stored']
            total_errors += result['errors']
    
    print("\n" + "=" * 60)
    print("📊 MIGRATION COMPLETE!")
    print("=" * 60)
    print(f"✅ Total entries stored: {total_stored}")
    if total_errors > 0:
        print(f"⚠️  Total errors: {total_errors}")
    print("\n🚀 Start facility: python self_hosted_storage_facility_windows.py")
    print("📊 Dashboard: http://localhost:5003\n")
