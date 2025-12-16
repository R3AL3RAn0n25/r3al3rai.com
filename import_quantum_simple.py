"""
Simple quantum dataset import using direct HuggingFace Hub API.
No heavy dependencies - just requests and psycopg2.
"""

import sys
import psycopg2
from psycopg2.extras import execute_batch
import hashlib
from datetime import datetime
import json
import requests

# Storage Facility connection
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'postgres',
    'user': 'postgres',
    'password': 'postgres'
}

BATCH_SIZE = 1000


def create_storage_facility_schema(conn):
    """Create complete Storage Facility schema."""
    cursor = conn.cursor()
    
    print("Creating Storage Facility schema...")
    
    # Knowledge units table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS knowledge_units (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) UNIQUE NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW()
        );
    """)
    
    # Knowledge entries table
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
    
    # Quantum circuits table (specialized)
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
    
    # Quantum papers table (specialized)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quantum_papers (
            id SERIAL PRIMARY KEY,
            content_hash VARCHAR(64) UNIQUE NOT NULL,
            source_dataset VARCHAR(255) NOT NULL,
            paper_query TEXT,
            language VARCHAR(10),
            metadata JSONB,
            created_at TIMESTAMP DEFAULT NOW()
        );
    """)
    
    # Create indexes
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_knowledge_entries_unit 
        ON knowledge_entries(unit_id);
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_knowledge_entries_content_gin 
        ON knowledge_entries USING GIN (to_tsvector('english', content));
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_quantum_circuits_code_gin 
        ON quantum_circuits USING GIN (to_tsvector('english', circuit_code));
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_quantum_papers_query_gin 
        ON quantum_papers USING GIN (to_tsvector('english', paper_query));
    """)
    
    conn.commit()
    print("[OK] Storage Facility schema created")
    
    # Create quantum knowledge unit
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
        cursor.execute("SELECT id FROM knowledge_units WHERE name = %s", ('quantum',))
        unit_id = cursor.fetchone()[0]
        print(f"[OK] Using existing quantum knowledge unit (ID: {unit_id})")
    
    conn.commit()
    return unit_id


def compute_hash(content):
    """Generate SHA-256 hash for deduplication."""
    return hashlib.sha256(content.encode('utf-8')).hexdigest()


def import_sample_quantum_data(conn):
    """Import sample quantum knowledge to test the system."""
    cursor = conn.cursor()
    
    print("\n=== Importing Sample Quantum Knowledge ===")
    
    # Sample Grover's algorithm circuits
    grover_samples = [
        {
            "circuit_code": """OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
creg c[2];
h q[0];
h q[1];
// Oracle for |11>
cz q[0],q[1];
// Diffusion operator
h q[0];
h q[1];
x q[0];
x q[1];
cz q[0],q[1];
x q[0];
x q[1];
h q[0];
h q[1];
measure q -> c;""",
            "target_state": "11",
            "description": "Grover's algorithm for 2-qubit search targeting state |11>"
        },
        {
            "circuit_code": """OPENQASM 2.0;
include "qelib1.inc";
qreg q[3];
creg c[3];
h q[0];
h q[1];
h q[2];
// Oracle marks |101>
cx q[0],q[2];
x q[1];
ccx q[0],q[1],q[2];
x q[1];
cx q[0],q[2];
measure q -> c;""",
            "target_state": "101",
            "description": "Grover's algorithm for 3-qubit search targeting state |101>"
        }
    ]
    
    # Sample Shor's algorithm knowledge
    shor_samples = [
        {
            "query": "Explain Shor's algorithm for factoring integers",
            "content": "Shor's algorithm is a quantum algorithm for integer factorization. It finds the prime factors of an integer N in polynomial time O((log N)³) using quantum period-finding. The algorithm has two main parts: 1) Classical reduction to order-finding, 2) Quantum Fourier transform for period detection."
        },
        {
            "query": "What are the quantum gates used in Shor's algorithm?",
            "content": "Shor's algorithm primarily uses: 1) Hadamard gates for superposition, 2) Controlled modular exponentiation gates, 3) Quantum Fourier Transform (QFT) gates including controlled-phase rotations, 4) CNOT gates for entanglement. The QFT is the most critical component for extracting the period."
        }
    ]
    
    # Import Grover circuits
    batch = []
    for sample in grover_samples:
        content_hash = compute_hash(sample['circuit_code'] + sample['target_state'])
        batch.append((
            content_hash,
            'builtin_sample',
            sample['circuit_code'],
            sample['target_state'],
            sample['description'],
            None,
            json.dumps({"source": "built-in", "algorithm": "grover"})
        ))
    
    execute_batch(cursor, """
        INSERT INTO quantum_circuits (content_hash, source_dataset, circuit_code, target_state, description, query, metadata)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (content_hash) DO NOTHING;
    """, batch)
    conn.commit()
    print(f"[OK] Imported {len(batch)} Grover circuit samples")
    
    # Import Shor knowledge as papers
    batch = []
    for sample in shor_samples:
        content_hash = compute_hash(sample['query'] + sample['content'])
        batch.append((
            content_hash,
            'builtin_sample',
            sample['query'],
            'en',
            json.dumps({"source": "built-in", "algorithm": "shor", "content": sample['content']})
        ))
    
    execute_batch(cursor, """
        INSERT INTO quantum_papers (content_hash, source_dataset, paper_query, language, metadata)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (content_hash) DO NOTHING;
    """, batch)
    conn.commit()
    print(f"[OK] Imported {len(batch)} Shor algorithm knowledge entries")
    
    return len(grover_samples) + len(shor_samples)


def verify_import(conn):
    """Verify imported data."""
    print("\n=== Verification ===")
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM knowledge_units;")
    units = cursor.fetchone()[0]
    print(f"Knowledge units: {units}")
    
    cursor.execute("SELECT COUNT(*) FROM quantum_circuits;")
    circuits = cursor.fetchone()[0]
    print(f"Quantum circuits: {circuits}")
    
    cursor.execute("SELECT COUNT(*) FROM quantum_papers;")
    papers = cursor.fetchone()[0]
    print(f"Quantum papers: {papers}")
    
    if circuits > 0:
        cursor.execute("""
            SELECT target_state, LEFT(circuit_code, 100) as preview
            FROM quantum_circuits
            LIMIT 1;
        """)
        row = cursor.fetchone()
        print(f"\nSample circuit:")
        print(f"  Target: {row[0]}")
        print(f"  Code: {row[1]}...")
    
    if papers > 0:
        cursor.execute("""
            SELECT LEFT(paper_query, 100) as preview
            FROM quantum_papers
            LIMIT 1;
        """)
        row = cursor.fetchone()
        print(f"\nSample paper query:")
        print(f"  {row[0]}")


def main():
    """Main import workflow."""
    print("=" * 60)
    print("QUANTUM KNOWLEDGE IMPORT TO STORAGE FACILITY")
    print("(Simple version - no external downloads)")
    print("=" * 60)
    
    try:
        print("\nConnecting to PostgreSQL...")
        conn = psycopg2.connect(**DB_CONFIG)
        print("[OK] Connected to Storage Facility")
        
        # Create schema
        unit_id = create_storage_facility_schema(conn)
        
        # Import sample data
        count = import_sample_quantum_data(conn)
        
        # Verify
        verify_import(conn)
        
        print("\n" + "=" * 60)
        print(f"IMPORT COMPLETE")
        print(f"  Total entries: {count}")
        print(f"  Storage: PostgreSQL (no local files)")
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
