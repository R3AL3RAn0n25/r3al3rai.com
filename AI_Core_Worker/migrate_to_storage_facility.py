"""
Migrate your existing JSON knowledge bases to PostgreSQL storage facility
"""

import json
import sys
import os
from self_hosted_storage_facility import StorageFacility

def migrate_json_to_unit(json_file: str, unit_id: str):
    """Migrate a JSON knowledge base to a storage unit"""
    
    print(f"\n📥 Migrating {os.path.basename(json_file)} to unit '{unit_id}'...")
    
    if not os.path.exists(json_file):
        print(f"❌ File not found: {json_file}")
        return None
    
    try:
        # Load JSON
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Convert to list if it's a dict
        entries = []
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, str):
                    # Simple string format
                    entries.append({
                        'id': key,
                        'content': value,
                        'topic': key,
                        'category': '',
                        'subcategory': '',
                        'level': '',
                        'source': os.path.basename(json_file)
                    })
                elif isinstance(value, dict):
                    # Dict format
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
        else:
            print(f"❌ Unknown data format in {json_file}")
            return None
        
        print(f"   Found {len(entries)} entries")
        
        # Store in facility in batches
        facility = StorageFacility()
        
        # Process in batches of 1000 to avoid connection issues
        batch_size = 1000
        total_stored = 0
        total_updated = 0
        total_errors = 0
        
        for i in range(0, len(entries), batch_size):
            batch = entries[i:i+batch_size]
            print(f"   Processing batch {i//batch_size + 1}/{(len(entries)-1)//batch_size + 1}...")
            
            try:
                # Create new facility instance for each batch
                batch_facility = StorageFacility()
                result = batch_facility.store_knowledge(unit_id, batch)
                total_stored += result['stored']
                total_updated += result['updated']
                total_errors += result['errors']
            except Exception as e:
                print(f"   ⚠️  Batch error: {e}")
                total_errors += len(batch)
        
        print(f"   ✅ Stored: {total_stored}")
        print(f"   🔄 Updated: {total_updated}")
        if total_errors > 0:
            print(f"   ⚠️  Errors: {total_errors}")
        
        return {
            'stored': total_stored,
            'updated': total_updated,
            'errors': total_errors
        }
        
    except Exception as e:
        print(f"❌ Error migrating {json_file}: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == '__main__':
    # Define migrations
    migrations = [
        ('physics_ALL_knowledge_base.json', 'physics'),
        ('quantum_physics_youtoks_FULL_knowledge_base.json', 'quantum'),
        ('space_astro_ALL_knowledge_base.json', 'space'),
        ('crypto_knowledge_base.json', 'crypto'),
    ]
    
    print("\n" + "=" * 60)
    print("🏢 R3ÆL3R STORAGE FACILITY MIGRATION")
    print("=" * 60)
    
    total_stored = 0
    total_updated = 0
    total_errors = 0
    
    for json_file, unit_id in migrations:
        result = migrate_json_to_unit(json_file, unit_id)
        if result:
            total_stored += result.get('stored', 0)
            total_updated += result.get('updated', 0)
            total_errors += result.get('errors', 0)
    
    print("\n" + "=" * 60)
    print("📊 MIGRATION COMPLETE!")
    print("=" * 60)
    print(f"✅ Total entries stored: {total_stored}")
    print(f"🔄 Total entries updated: {total_updated}")
    if total_errors > 0:
        print(f"⚠️  Total errors: {total_errors}")
    print("\n🚀 Start facility: python self_hosted_storage_facility.py")
    print("📊 Dashboard: http://localhost:5003\n")
