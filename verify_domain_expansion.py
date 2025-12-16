"""
R3ÆLƎR AI - Comprehensive Domain Expansion Verification
Verify the creation of all domain units and their contents
"""

import os
import sys
import logging
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from AI_Core_Worker.self_hosted_storage_facility import StorageFacility

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Domain list for verification
MAJOR_DOMAINS = [
    "physics", "chemistry", "biology", "mathematics", "astronomy", "geology", "environmental_science",
    "computer_science", "artificial_intelligence", "data_science", "engineering",
    "history", "philosophy", "literature", "languages",
    "psychology", "sociology", "economics", "political_science",
    "visual_arts", "music", "performing_arts",
    "medicine", "law", "business", "education"
]

def verify_domain_expansion():
    """Verify all domain units and their contents"""
    logger.info("Verifying comprehensive domain expansion...")

    storage = StorageFacility()
    results = {}

    try:
        conn = storage.get_connection()
        cursor = conn.cursor()

        total_units = 0
        total_entries = 0
        units_with_data = 0

        for domain in MAJOR_DOMAINS:
            unit_name = f"{domain}_unit"

            try:
                # Check if unit exists
                cursor.execute("""
                    SELECT COUNT(*) as table_count
                    FROM information_schema.tables
                    WHERE table_schema = %s
                """, (unit_name,))

                table_count = cursor.fetchone()[0]

                # Check knowledge table entries
                cursor.execute(f"""
                    SELECT COUNT(*) as entry_count,
                           COUNT(DISTINCT category) as categories,
                           COUNT(DISTINCT source) as sources
                    FROM {unit_name}.knowledge
                """)

                entry_stats = cursor.fetchone()
                entry_count = entry_stats[0]

                total_units += 1
                total_entries += entry_count

                if entry_count > 0:
                    units_with_data += 1

                results[domain] = {
                    'unit_exists': table_count > 0,
                    'tables_created': table_count,
                    'entries_ingested': entry_count,
                    'categories': entry_stats[1],
                    'sources': entry_stats[2]
                }

                # Get sample entries
                if entry_count > 0:
                    cursor.execute(f"""
                        SELECT topic, category, source
                        FROM {unit_name}.knowledge
                        LIMIT 3
                    """)
                    samples = cursor.fetchall()
                    results[domain]['sample_entries'] = [
                        {'topic': s[0], 'category': s[1], 'source': s[2]} for s in samples
                    ]

            except Exception as e:
                logger.warning(f"Error checking {domain}: {e}")
                results[domain] = {
                    'unit_exists': False,
                    'error': str(e)
                }

        cursor.close()
        conn.close()

        # Generate comprehensive report
        report = {
            'verification_timestamp': datetime.now().isoformat(),
            'total_domains': len(MAJOR_DOMAINS),
            'units_created': total_units,
            'units_with_data': units_with_data,
            'total_entries_ingested': total_entries,
            'domain_details': results,
            'expansion_success_rate': f"{units_with_data}/{len(MAJOR_DOMAINS)} domains with data"
        }

        return report

    except Exception as e:
        logger.error(f"Verification failed: {e}")
        return {'error': str(e)}

def main():
    """Main verification function"""
    result = verify_domain_expansion()

    print("\n" + "="*100)
    print("R3ÆLƎR AI - Comprehensive Domain Expansion Verification Report")
    print("="*100)

    if 'error' in result:
        print(f"❌ Verification failed: {result['error']}")
    else:
        print("✅ Domain expansion verification completed!")
        print(f"📊 Total domains: {result['total_domains']}")
        print(f"🏗️ Units created: {result['units_created']}")
        print(f"📚 Units with data: {result['units_with_data']}")
        print(f"📝 Total entries: {result['total_entries_ingested']}")
        print(f"🎯 Success rate: {result['expansion_success_rate']}")

        print(f"\n📋 Domain Status:")
        for domain, details in result['domain_details'].items():
            status = "✅" if details.get('unit_exists', False) else "❌"
            entries = details.get('entries_ingested', 0)
            print(f"  {status} {domain.replace('_', ' ').title():25} | Tables: {details.get('tables_created', 0):2d} | Entries: {entries:3d}")

        print(f"\n🔍 Sample Entries from Key Domains:")

        # Show samples from first few domains
        sample_domains = ['physics', 'computer_science', 'biology', 'mathematics']
        for domain in sample_domains:
            if domain in result['domain_details'] and 'sample_entries' in result['domain_details'][domain]:
                print(f"\n{domain.replace('_', ' ').title()}:")
                for entry in result['domain_details'][domain]['sample_entries']:
                    print(f"  • {entry['topic']} ({entry['category']})")

    print("\n" + "="*100)

if __name__ == "__main__":
    main()