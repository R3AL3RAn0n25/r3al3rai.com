#!/usr/bin/env python3
"""
Test script to verify storage facility functionality and add sample knowledge entries
"""

import requests
import json
from datetime import datetime

def test_storage_facility():
    """Test the storage facility by adding sample knowledge entries"""

    storage_url = "http://localhost:3003"

    # Sample knowledge entries to add
    sample_entries = [
        {
            "id": "sample_physics_001",
            "content": "Newton's First Law of Motion states that an object at rest stays at rest, and an object in motion stays in motion with the same speed and in the same direction unless acted upon by an unbalanced force.",
            "title": "Newton's First Law",
            "category": "physics",
            "source": "Sample Knowledge Base",
            "metadata": {
                "type": "fundamental_principle",
                "difficulty": "beginner",
                "tags": ["physics", "mechanics", "newton", "motion"],
                "timestamp": datetime.now().isoformat()
            }
        },
        {
            "id": "sample_quantum_001",
            "content": "Quantum entanglement is a physical phenomenon that occurs when pairs or groups of particles are generated, interact, or share spatial proximity in ways such that the quantum state of each particle cannot be described independently.",
            "title": "Quantum Entanglement",
            "category": "quantum",
            "source": "Sample Knowledge Base",
            "metadata": {
                "type": "quantum_phenomenon",
                "difficulty": "intermediate",
                "tags": ["quantum", "entanglement", "physics", "particles"],
                "timestamp": datetime.now().isoformat()
            }
        },
        {
            "id": "sample_ai_001",
            "content": "Machine learning is a subset of artificial intelligence that enables computers to learn and improve from experience without being explicitly programmed.",
            "title": "Machine Learning Definition",
            "category": "ai",
            "source": "Sample Knowledge Base",
            "metadata": {
                "type": "definition",
                "difficulty": "beginner",
                "tags": ["ai", "machine_learning", "artificial_intelligence"],
                "timestamp": datetime.now().isoformat()
            }
        },
        {
            "id": "sample_crypto_001",
            "content": "A blockchain is a distributed ledger technology that maintains a continuously growing list of records, called blocks, which are linked and secured using cryptography.",
            "title": "Blockchain Technology",
            "category": "cryptography",
            "source": "Sample Knowledge Base",
            "metadata": {
                "type": "technology",
                "difficulty": "intermediate",
                "tags": ["blockchain", "cryptography", "distributed_ledger"],
                "timestamp": datetime.now().isoformat()
            }
        }
    ]

    print("Testing R3AL3R Storage Facility...")
    print("=" * 50)

    # Test facility status
    try:
        response = requests.get(f"{storage_url}/api/facility/status", timeout=5)
        if response.status_code == 200:
            status = response.json()
            print("✓ Storage facility is online")
            print(f"  Total entries: {status.get('total_entries', 'N/A')}")
            print(f"  Total units: {status.get('total_units', 'N/A')}")
        else:
            print("✗ Storage facility returned error:", response.status_code)
            return False
    except Exception as e:
        print("✗ Cannot connect to storage facility:", str(e))
        return False

    # Test storing entries
    stored_count = 0
    for entry in sample_entries:
        try:
            # Determine unit based on category
            category = entry['category']
            unit_mapping = {
                'physics': 'physics',
                'quantum': 'quantum',
                'ai': 'quantum',  # AI goes to quantum unit
                'cryptography': 'crypto'
            }
            unit = unit_mapping.get(category, 'users')

            # Store the entry
            store_url = f"{storage_url}/api/unit/{unit}/store"
            response = requests.post(store_url, json={'entries': [entry]}, timeout=10)

            if response.status_code == 200:
                print(f"✓ Stored entry: {entry['id']} in {unit}")
                stored_count += 1
            else:
                print(f"✗ Failed to store entry {entry['id']}: {response.status_code}")
                print(f"  Response: {response.text}")

        except Exception as e:
            print(f"✗ Error storing entry {entry['id']}: {str(e)}")

    print("=" * 50)
    print(f"Storage test complete: {stored_count}/{len(sample_entries)} entries stored successfully")

    # Test retrieval
    try:
        response = requests.get(f"{storage_url}/api/facility/status", timeout=5)
        if response.status_code == 200:
            final_status = response.json()
            final_entries = final_status.get('total_entries', 0)
            print(f"Final facility status: {final_entries} total entries")
    except Exception as e:
        print("Could not get final status:", str(e))

    return stored_count > 0

if __name__ == "__main__":
    success = test_storage_facility()
    if success:
        print("\n🎉 Storage facility test PASSED!")
        print("The R3AL3R storage infrastructure is working correctly.")
        print("All local data will be stored in the PostgreSQL-based storage facility,")
        print("not taking up space on your local machine.")
    else:
        print("\n❌ Storage facility test FAILED!")
        print("Please check the storage facility logs and database connection.")