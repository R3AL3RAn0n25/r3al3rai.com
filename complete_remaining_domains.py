"""
R3ÆLƎR AI - Complete Remaining Domain Ingestion
Ingest data for all domains that don't have data yet
"""

import os
import sys
import logging
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from comprehensive_domain_expansion import ComprehensiveDomainExpansion, MAJOR_DOMAINS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def complete_remaining_domains():
    """Complete ingestion for domains that don't have data"""
    logger.info("Completing remaining domain ingestion...")

    expander = ComprehensiveDomainExpansion()

    # Check which domains need data
    storage = expander.storage
    domains_needing_data = []

    try:
        conn = storage.get_connection()
        cursor = conn.cursor()

        for domain_name in MAJOR_DOMAINS.keys():
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {domain_name}_unit.knowledge")
                count = cursor.fetchone()[0]
                if count == 0:  # Only basic overview entries
                    domains_needing_data.append(domain_name)
            except:
                domains_needing_data.append(domain_name)

        cursor.close()
        conn.close()

    except Exception as e:
        logger.error(f"Error checking domain status: {e}")
        return

    logger.info(f"Found {len(domains_needing_data)} domains needing data ingestion")

    total_entries = 0
    successful_domains = 0

    for i, domain_name in enumerate(domains_needing_data, 1):
        logger.info(f"Processing domain {i}/{len(domains_needing_data)}: {domain_name}")

        try:
            domain_info = MAJOR_DOMAINS[domain_name]

            # Skip unit creation (already done), go straight to ingestion
            domain_entries = expander.ingest_domain_datasets(domain_name, domain_info)
            total_entries += domain_entries

            wiki_entries = expander.ingest_domain_wikipedia_knowledge(domain_name, domain_info)
            total_entries += wiki_entries

            # Subdomain tables should already be created, but ensure they exist
            expander.create_domain_subdomain_tables(domain_name, domain_info)

            successful_domains += 1
            logger.info(f"Successfully processed {domain_name}: {domain_entries + wiki_entries} entries")

        except Exception as e:
            logger.error(f"Failed to process {domain_name}: {e}")
            continue

    # Generate completion report
    completion_report = {
        'completion_timestamp': datetime.now().isoformat(),
        'domains_processed': successful_domains,
        'domains_attempted': len(domains_needing_data),
        'total_entries_ingested': total_entries,
        'domains_completed': domains_needing_data[:successful_domains],
        'ingestion_complete': successful_domains == len(domains_needing_data)
    }

    return completion_report

def main():
    """Main completion function"""
    result = complete_remaining_domains()

    print("\n" + "="*80)
    print("R3ÆLƎR AI - Remaining Domain Ingestion Completion Report")
    print("="*80)

    if result:
        print("✅ Domain completion process finished!")
        print(f"📊 Domains processed: {result['domains_processed']}/{result['domains_attempted']}")
        print(f"📚 Total entries ingested: {result['total_entries_ingested']}")
        print(f"🏁 Process complete: {result['ingestion_complete']}")

        if result['domains_completed']:
            print(f"\n📋 Domains Completed:")
            for i, domain in enumerate(result['domains_completed'], 1):
                print(f"  {i:2d}. {domain.replace('_', ' ').title()}")

    else:
        print("❌ Completion process failed")

    print("\n" + "="*80)

if __name__ == "__main__":
    main()