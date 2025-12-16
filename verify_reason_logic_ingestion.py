#!/usr/bin/env python3
"""
Verify Reason & Logic Units Data Ingestion
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from AI_Core_Worker.self_hosted_storage_facility import StorageFacility
import psycopg2
from psycopg2.extras import RealDictCursor

def verify_ingestion():
    sf = StorageFacility()

    conn = sf.get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    # Check reason unit
    cursor.execute('SELECT COUNT(*) as count FROM reason_unit.knowledge')
    reason_count = cursor.fetchone()['count']

    # Check logic unit
    cursor.execute('SELECT COUNT(*) as count FROM logic_unit.knowledge')
    logic_count = cursor.fetchone()['count']

    # Get sample entries
    cursor.execute('SELECT topic, category, source FROM reason_unit.knowledge LIMIT 5')
    reason_samples = cursor.fetchall()

    cursor.execute('SELECT topic, category, source FROM logic_unit.knowledge LIMIT 5')
    logic_samples = cursor.fetchall()

    # Get category breakdown
    cursor.execute("""
        SELECT category, COUNT(*) as count
        FROM reason_unit.knowledge
        GROUP BY category
        ORDER BY count DESC
    """)
    reason_categories = cursor.fetchall()

    cursor.execute("""
        SELECT category, COUNT(*) as count
        FROM logic_unit.knowledge
        GROUP BY category
        ORDER BY count DESC
    """)
    logic_categories = cursor.fetchall()

    cursor.close()
    conn.close()

    print("="*60)
    print("R3ÆLƎR AI - Reason & Logic Units Verification")
    print("="*60)
    print(f"Reason unit entries: {reason_count}")
    print(f"Logic unit entries: {logic_count}")
    print()

    print("Reason unit samples:")
    for sample in reason_samples:
        print(f"  - {sample['topic']} ({sample['category']}) - {sample['source']}")
    print()

    print("Logic unit samples:")
    for sample in logic_samples:
        print(f"  - {sample['topic']} ({sample['category']}) - {sample['source']}")
    print()

    print("Reason unit categories:")
    for cat in reason_categories:
        print(f"  - {cat['category']}: {cat['count']} entries")
    print()

    print("Logic unit categories:")
    for cat in logic_categories:
        print(f"  - {cat['category']}: {cat['count']} entries")
    print()

    print("="*60)

if __name__ == "__main__":
    verify_ingestion()