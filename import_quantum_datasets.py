"""
Import quantum algorithm datasets from HuggingFace into Storage Facility.
Imports:
1. racineai/OGC_Quantum_Circuit_Papers (circuit diagrams + papers)
2. mchen644/Grover_Data (OpenQASM circuit code)
"""

import sys
import os
import psycopg2
from psycopg2.extras import execute_batch
import hashlib
from datetime import datetime
import json

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from datasets import load_dataset
    print("[OK] HuggingFace datasets library loaded")
except ImportError:
    print("[ERROR] HuggingFace datasets library not found. Installing...")
    os.system(f"{sys.executable} -m pip install datasets")
    from datasets import load_dataset
    print("[OK] Installed and loaded datasets library")

# Storage Facility connection (PostgreSQL)
# Match self_hosted_storage_facility.py config
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'postgres',
    'user': 'postgres',
    'password': 'postgres'
}

BATCH_SIZE = 1000


def create_quantum_knowledge_unit(conn):
    """Create quantum knowledge unit and tables if they don't exist."""
    cursor = conn.cursor()
    
    # First, create the knowledge_units table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS knowledge_units (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) UNIQUE NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW()
        );
    """)
    
    # Create knowledge_entries table (main storage)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS knowledge_entries (
            id SERIAL PRIMARY KEY,
            unit_id INTEGER REFERENCES knowledge_units(id) ON DELETE CASCADE,
            content TEXT NOT NULL,
            metadata JSONB,
            content_hash VARCHAR(64) UNIQUE,
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW()
        );
    """)
    
    # Create index on knowledge_entries
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_knowledge_entries_unit 
        ON knowledge_entries(unit_id);
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_knowledge_entries_content_gin 
        ON knowledge_entries USING GIN (to_tsvector('english', content));
    """)
    
    conn.commit()
    print("[OK] Created base Storage Facility schema")
    
    # Create knowledge unit entry
    cursor.execute("""
        INSERT INTO knowledge_units (name, description, created_at)
        VALUES (%s, %s, %s)
        ON CONFLICT (name) DO NOTHING
        RETURNING id;
    """, (
        'quantum',
        'Quantum algorithms, circuits (Shor/Grover/QASM), and research papers',
        datetime.now()
    ))
    
    result = cursor.fetchone()
    if result:
        unit_id = result[0]
        print(f"[OK] Created quantum knowledge unit (ID: {unit_id})")
    else:
        # Get existing ID
        cursor.execute("SELECT id FROM knowledge_units WHERE name = %s", ('quantum',))
        unit_id = cursor.fetchone()[0]
        print(f"[OK] Using existing quantum knowledge unit (ID: {unit_id})")
    
    # Create quantum_circuits table for QASM/circuit data
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quantum_circuits (
            id SERIAL PRIMARY KEY,
            content_hash VARCHAR(64) UNIQUE NOT NULL,
            source_dataset VARCHAR(255) NOT NULL,
            circuit_code TEXT,
            target_state VARCHAR(255),
            description TEXT,
            query TEXT,
            metadata JSONB,
            created_at TIMESTAMP DEFAULT NOW()
        );
    """)
    
    # Create quantum_papers table for research papers/diagrams
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quantum_papers (
            id SERIAL PRIMARY KEY,
            content_hash VARCHAR(64) UNIQUE NOT NULL,
            source_dataset VARCHAR(255) NOT NULL,
            paper_query TEXT,
            image_data TEXT,
            language VARCHAR(10),
            metadata JSONB,
            created_at TIMESTAMP DEFAULT NOW()
        );
    """)
    
    # Create GIN indexes for text search
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_quantum_circuits_code_gin 
        ON quantum_circuits USING GIN (to_tsvector('english', circuit_code));
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_quantum_circuits_desc_gin 
        ON quantum_circuits USING GIN (to_tsvector('english', description));
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_quantum_papers_query_gin 
        ON quantum_papers USING GIN (to_tsvector('english', paper_query));
    """)
    
    conn.commit()
    print("[OK] Created quantum tables and indexes")
    
    return unit_id


def compute_hash(content):
    """Generate SHA-256 hash for deduplication."""
    return hashlib.sha256(content.encode('utf-8')).hexdigest()


def import_grover_circuits(conn):
    """Import mchen644/Grover_Data (OpenQASM circuits)."""
    print("\n=== Importing Grover_Data (OpenQASM circuits) ===")
    print("Using streaming mode - no local storage")
    
    try:
        # Use streaming=True to avoid local caching
        dataset = load_dataset("mchen644/Grover_Data", split="train", streaming=True)
        print(f"[OK] Streaming dataset (no local download)")
    except Exception as e:
        print(f"[ERROR] Failed to load dataset: {e}")
        return 0
    
    cursor = conn.cursor()
    batch = []
    imported = 0
    skipped = 0
    total_processed = 0
    
    for idx, row in enumerate(dataset):
        total_processed += 1
        
        # Progress indicator every 100 rows
        if total_processed % 100 == 0:
            print(f"  Processed {total_processed} rows, imported {imported}...")
        
        # Extract fields (adjust based on actual schema)
        circuit_code = row.get('qasm', row.get('circuit', row.get('code', '')))
        target_state = row.get('target', row.get('target_state', row.get('answer', '')))
        
        if not circuit_code:
            # Fallback: check all fields for QASM-like content
            for key, val in row.items():
                if isinstance(val, str) and ('OPENQASM' in val or 'qreg' in val):
                    circuit_code = val
                    break
        
        if not circuit_code:
            skipped += 1
            continue
        
        # Generate hash for deduplication
        content_hash = compute_hash(circuit_code + str(target_state))
        
        # Prepare metadata
        metadata = {k: v for k, v in row.items() if k not in ['qasm', 'circuit', 'code', 'target', 'target_state']}
        
        batch.append((
            content_hash,
            'mchen644/Grover_Data',
            circuit_code,
            str(target_state) if target_state else None,
            f"Grover circuit for target state: {target_state}" if target_state else "Grover quantum search circuit",
            None,  # query field
            json.dumps(metadata)
        ))
        
        # Insert batch
        if len(batch) >= BATCH_SIZE:
            try:
                execute_batch(cursor, """
                    INSERT INTO quantum_circuits (content_hash, source_dataset, circuit_code, target_state, description, query, metadata)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (content_hash) DO NOTHING;
                """, batch)
                conn.commit()
                imported += cursor.rowcount  # Get actual inserted count
                batch = []
            except Exception as e:
                print(f"  [WARN] Batch insert error: {e}")
                conn.rollback()
                batch = []
    
    # Insert remaining batch
    if batch:
        try:
            execute_batch(cursor, """
                INSERT INTO quantum_circuits (content_hash, source_dataset, circuit_code, target_state, description, query, metadata)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (content_hash) DO NOTHING;
            """, batch)
            conn.commit()
            imported += cursor.rowcount
        except Exception as e:
            print(f"  [WARN] Final batch error: {e}")
            conn.rollback()
    
    print(f"[OK] Imported {imported} Grover circuits, skipped {skipped}, total processed {total_processed}")
    return imported
def import_circuit_papers(conn):
    """Import racineai/OGC_Quantum_Circuit_Papers (research papers + diagrams)."""
    print("\n=== Importing OGC_Quantum_Circuit_Papers ===")
    print("Using streaming mode - no local storage")
    
    try:
        # Use streaming to avoid local download
        dataset = load_dataset("racineai/OGC_Quantum_Circuit_Papers", "filtered", split="train", streaming=True)
        print(f"[OK] Streaming 'filtered' subset (no local download)")
    except Exception as e1:
        print(f"  'filtered' subset not available: {e1}")
        try:
            # Fallback to default
            dataset = load_dataset("racineai/OGC_Quantum_Circuit_Papers", split="train", streaming=True)
            print(f"[OK] Streaming default split (no local download)")
        except Exception as e2:
            print(f"[ERROR] Failed to load dataset: {e2}")
            return 0
    
    cursor = conn.cursor()
    batch = []
    imported = 0
    skipped = 0
    total_processed = 0
    
    for idx, row in enumerate(dataset):
        total_processed += 1
        
        # Progress indicator every 100 rows
        if total_processed % 100 == 0:
            print(f"  Processed {total_processed} rows, imported {imported}...")
        
        # Expected fields based on HF preview: id, query, image (or image path), language
        query_text = row.get('query', row.get('question', ''))
        image_data = row.get('image', row.get('img', ''))
        language = row.get('language', row.get('lang', 'en'))
        
        if not query_text:
            skipped += 1
            continue
        
        # Generate hash
        content_hash = compute_hash(query_text + str(image_data)[:100])  # Include image prefix for uniqueness
        
        # Metadata
        metadata = {k: v for k, v in row.items() if k not in ['query', 'question', 'image', 'img', 'language', 'lang']}
        
        # Convert image to string representation if needed (PIL Image -> skip for now, store path/id)
        # Do NOT save image data locally - just store reference or skip
        if hasattr(image_data, 'filename'):
            image_str = f"<image_ref:{image_data.filename}>"
        elif isinstance(image_data, dict) and 'path' in image_data:
            image_str = f"<image_ref:{image_data['path']}>"
        else:
            # Skip storing actual image bytes to save space
            image_str = "<image_data_not_stored>"
        
        batch.append((
            content_hash,
            'racineai/OGC_Quantum_Circuit_Papers',
            query_text,
            image_str,
            language,
            json.dumps(metadata)
        ))
        
        # Insert batch
        if len(batch) >= BATCH_SIZE:
            try:
                execute_batch(cursor, """
                    INSERT INTO quantum_papers (content_hash, source_dataset, paper_query, image_data, language, metadata)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (content_hash) DO NOTHING;
                """, batch)
                conn.commit()
                imported += cursor.rowcount  # Get actual inserted count
                batch = []
            except Exception as e:
                print(f"  [WARN] Batch insert error: {e}")
                conn.rollback()
                batch = []
    
    # Insert remaining batch
    if batch:
        try:
            execute_batch(cursor, """
                INSERT INTO quantum_papers (content_hash, source_dataset, paper_query, image_data, language, metadata)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (content_hash) DO NOTHING;
            """, batch)
            conn.commit()
            imported += cursor.rowcount
        except Exception as e:
            print(f"  [WARN] Final batch error: {e}")
            conn.rollback()
    
    print(f"[OK] Imported {imported} paper entries, skipped {skipped}, total processed {total_processed}")
    return imported
def verify_import(conn):
    """Verify imported data with sample queries."""
    print("\n=== Verification ===")
    cursor = conn.cursor()
    
    # Count circuits
    cursor.execute("SELECT COUNT(*) FROM quantum_circuits;")
    circuit_count = cursor.fetchone()[0]
    print(f"Total quantum_circuits: {circuit_count}")
    
    # Count papers
    cursor.execute("SELECT COUNT(*) FROM quantum_papers;")
    paper_count = cursor.fetchone()[0]
    print(f"Total quantum_papers: {paper_count}")
    
    # Sample circuit
    if circuit_count > 0:
        cursor.execute("""
            SELECT target_state, LEFT(circuit_code, 150) as code_preview, source_dataset
            FROM quantum_circuits
            WHERE circuit_code IS NOT NULL
            LIMIT 1;
        """)
        row = cursor.fetchone()
        if row:
            print(f"\nSample circuit:")
            print(f"  Target: {row[0]}")
            print(f"  Code preview: {row[1]}...")
            print(f"  Source: {row[2]}")
    
    # Sample paper
    if paper_count > 0:
        cursor.execute("""
            SELECT LEFT(paper_query, 150) as query_preview, language, source_dataset
            FROM quantum_papers
            LIMIT 1;
        """)
        row = cursor.fetchone()
        if row:
            print(f"\nSample paper:")
            print(f"  Query: {row[0]}...")
            print(f"  Language: {row[1]}")
            print(f"  Source: {row[2]}")


def main():
    """Main import workflow."""
    print("=" * 60)
    print("QUANTUM DATASET IMPORT TO STORAGE FACILITY")
    print("=" * 60)
    
    try:
        # Connect to PostgreSQL
        print("\nConnecting to PostgreSQL...")
        conn = psycopg2.connect(**DB_CONFIG)
        print("[OK] Connected to Storage Facility")
        
        # Create knowledge unit and tables
        unit_id = create_quantum_knowledge_unit(conn)
        
        # Import datasets
        grover_count = import_grover_circuits(conn)
        paper_count = import_circuit_papers(conn)
        
        # Verify
        verify_import(conn)
        
        print("\n" + "=" * 60)
        print(f"IMPORT COMPLETE")
        print(f"  Grover circuits: {grover_count}")
        print(f"  Research papers: {paper_count}")
        print(f"  Total imported: {grover_count + paper_count}")
        print("=" * 60)
        
        conn.close()
        
    except psycopg2.Error as e:
        print(f"\n[ERROR] Database error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
