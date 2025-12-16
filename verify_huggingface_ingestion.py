"""
R3ÆLƎR AI - HuggingFace Dataset Ingestion Verification
Verify the comprehensive ingestion of all HuggingFace reasoning and logic datasets
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

def verify_huggingface_ingestion():
    """Verify HuggingFace dataset ingestion"""
    logger.info("Verifying HuggingFace dataset ingestion...")

    storage = StorageFacility()

    try:
        conn = storage.get_connection()
        cursor = conn.cursor()

        # Check reason unit
        cursor.execute("""
            SELECT COUNT(*) as total,
                   COUNT(DISTINCT category) as categories,
                   COUNT(DISTINCT source) as sources
            FROM reason_unit.knowledge
            WHERE source LIKE 'huggingface_%'
        """)
        reason_stats = cursor.fetchone()

        # Check logic unit
        cursor.execute("""
            SELECT COUNT(*) as total,
                   COUNT(DISTINCT category) as categories,
                   COUNT(DISTINCT source) as sources
            FROM logic_unit.knowledge
            WHERE source LIKE 'huggingface_%'
        """)
        logic_stats = cursor.fetchone()

        # Get sample entries
        cursor.execute("""
            SELECT topic, category, source
            FROM reason_unit.knowledge
            WHERE source LIKE 'huggingface_%'
            LIMIT 5
        """)
        reason_samples = cursor.fetchall()

        cursor.execute("""
            SELECT topic, category, source
            FROM logic_unit.knowledge
            WHERE source LIKE 'huggingface_%'
            LIMIT 5
        """)
        logic_samples = cursor.fetchall()

        cursor.close()
        conn.close()

        # Generate report
        report = {
            'verification_timestamp': datetime.now().isoformat(),
            'reason_unit': {
                'total_datasets': reason_stats[0],
                'categories': reason_stats[1],
                'sources': reason_stats[2],
                'sample_entries': [{'topic': r[0], 'category': r[1], 'source': r[2]} for r in reason_samples]
            },
            'logic_unit': {
                'total_datasets': logic_stats[0],
                'categories': logic_stats[1],
                'sources': logic_stats[2],
                'sample_entries': [{'topic': r[0], 'category': r[1], 'source': r[2]} for r in logic_samples]
            },
            'total_ingested': reason_stats[0] + logic_stats[0],
            'expected_total': 80  # Based on our dataset list
        }

        return report

    except Exception as e:
        logger.error(f"Verification failed: {e}")
        return {'error': str(e)}

def main():
    """Main verification function"""
    result = verify_huggingface_ingestion()

    print("\n" + "="*80)
    print("R3ÆLƎR AI - HuggingFace Dataset Ingestion Verification Report")
    print("="*80)

    if 'error' in result:
        print(f"❌ Verification failed: {result['error']}")
    else:
        print("✅ Verification completed successfully!")
        print(f"📊 Total datasets expected: {result['expected_total']}")
        print(f"📊 Total datasets ingested: {result['total_ingested']}")
        print()

        print("Reason Unit:")
        print(f"  • Datasets: {result['reason_unit']['total_datasets']}")
        print(f"  • Categories: {result['reason_unit']['categories']}")
        print(f"  • Sources: {result['reason_unit']['sources']}")
        print("  Sample entries:")
        for entry in result['reason_unit']['sample_entries'][:3]:
            print(f"    - {entry['topic']} ({entry['category']})")
        print()

        print("Logic Unit:")
        print(f"  • Datasets: {result['logic_unit']['total_datasets']}")
        print(f"  • Categories: {result['logic_unit']['categories']}")
        print(f"  • Sources: {result['logic_unit']['sources']}")
        print("  Sample entries:")
        for entry in result['logic_unit']['sample_entries'][:3]:
            print(f"    - {entry['topic']} ({entry['category']})")
        print()

        if result['total_ingested'] >= result['expected_total']:
            print("🎉 All HuggingFace datasets successfully ingested!")
        else:
            print(f"⚠️  Partial ingestion: {result['total_ingested']}/{result['expected_total']} datasets")

    print("="*80)

if __name__ == "__main__":
    main()