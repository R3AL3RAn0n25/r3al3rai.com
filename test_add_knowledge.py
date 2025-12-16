"""
Test script demonstrating how to add new knowledge to R3ÆLƎR AI Storage Facility
This shows the automatic ingestion process
"""
import requests
import json

print("╔════════════════════════════════════════════════════════════╗")
print("║     R3ÆLƎR AI - Add New Knowledge Test                    ║")
print("╚════════════════════════════════════════════════════════════╝\n")

# Example: Adding new cryptocurrency knowledge
new_crypto_knowledge = {
    "unit": "crypto",
    "entries": [
        {
            "entry_id": "ethereum_smart_contracts",
            "topic": "Ethereum Smart Contracts",
            "category": "Cryptocurrency",
            "subcategory": "Smart Contracts",
            "level": "Advanced",
            "content": """Smart contracts on Ethereum are self-executing programs that run on the Ethereum Virtual Machine (EVM).

Key Characteristics:
• Written in Solidity (primary language) or Vyper
• Deployed to blockchain with unique contract address
• Immutable once deployed (cannot be modified)
• Deterministic execution (same inputs = same outputs)

Common Use Cases:
- Decentralized Finance (DeFi) protocols
- Non-Fungible Tokens (NFTs)
- Decentralized Autonomous Organizations (DAOs)
- Token standards (ERC-20, ERC-721, ERC-1155)

Security Considerations:
• Reentrancy attacks (use Checks-Effects-Interactions pattern)
• Integer overflow/underflow (Solidity 0.8+ has built-in checks)
• Access control vulnerabilities
• Front-running risks
• Gas optimization

Forensic Analysis:
- Transaction traces via etherscan.io
- Contract source code verification
- Event log analysis
- State variable inspection
- Bytecode decompilation tools (e.g., Dedaub, Heimdall)""",
            "source": "R3ÆLƎR Cryptocurrency Knowledge Base"
        },
        {
            "entry_id": "monero_privacy",
            "topic": "Monero (XMR) Privacy Features",
            "category": "Cryptocurrency",
            "subcategory": "Privacy Coins",
            "level": "Expert",
            "content": """Monero is a privacy-focused cryptocurrency using advanced cryptographic techniques.

Privacy Technologies:
1. Ring Signatures
   • Mixes sender's transaction with others (default ring size: 16)
   • Makes it cryptographically impossible to determine true sender

2. Stealth Addresses
   • One-time addresses for each transaction
   • Receiver's public address not recorded on blockchain

3. RingCT (Ring Confidential Transactions)
   • Hides transaction amounts
   • Uses Pedersen commitments and range proofs

4. Dandelion++
   • Network-level privacy
   • Obscures transaction origin IP

Forensic Challenges:
- Cannot trace transaction flow through blockchain analysis
- Amount privacy prevents balance determination
- Timing analysis and IP correlation are primary investigative vectors
- Exchange KYC data may be only connection point

Wallet Formats:
- GUI wallet: wallet file + keys file
- CLI wallet: Similar structure to Bitcoin Core
- Mobile: Monerujo (Android), Cake Wallet (iOS)
- Hardware: Ledger, Trezor support""",
            "source": "R3ÆLƎR Cryptocurrency Knowledge Base"
        }
    ]
}

print("📝 Knowledge to Add:")
print(f"   Unit: {new_crypto_knowledge['unit']}")
print(f"   Entries: {len(new_crypto_knowledge['entries'])}")
print()

for i, entry in enumerate(new_crypto_knowledge['entries'], 1):
    print(f"   {i}. {entry['topic']} ({entry['level']})")

print("\n" + "="*60)
print("🚀 Sending to Knowledge API /api/kb/ingest endpoint...")
print("="*60 + "\n")

try:
    # Send to Knowledge API (which forwards to Storage Facility)
    response = requests.post(
        'http://localhost:5001/api/kb/ingest',
        json=new_crypto_knowledge,
        timeout=30
    )
    
    if response.status_code == 200:
        result = response.json()
        print("✅ SUCCESS! Knowledge stored in PostgreSQL")
        print(f"\n📊 Results:")
        print(f"   Unit: {result.get('unit')}")
        print(f"   Entries Added: {result.get('entries_added')}")
        print(f"   Message: {result.get('message')}")
        
        storage_response = result.get('storage_facility_response', {})
        if storage_response:
            print(f"\n💾 Storage Facility Details:")
            print(f"   Total Processed: {storage_response.get('total_processed')}")
            print(f"   New Entries: {storage_response.get('stored')}")
            print(f"   Updated Entries: {storage_response.get('updated')}")
            print(f"   Errors: {storage_response.get('errors')}")
            
    else:
        print(f"❌ ERROR: Status {response.status_code}")
        print(f"Response: {response.text}")
        
except requests.exceptions.ConnectionError:
    print("❌ ERROR: Cannot connect to Knowledge API")
    print("   Make sure Knowledge API is running on port 5001")
    print("   Start it with: cd AI_Core_Worker && python knowledge_api.py")
except Exception as e:
    print(f"❌ ERROR: {e}")

# Verify the knowledge was stored
print("\n" + "="*60)
print("🔍 Verifying storage with search query...")
print("="*60 + "\n")

try:
    search_response = requests.post(
        'http://localhost:5001/api/kb/search',
        json={'query': 'Ethereum smart contracts', 'maxPassages': 2},
        timeout=10
    )
    
    if search_response.status_code == 200:
        search_data = search_response.json()
        
        if search_data.get('used_storage_facility'):
            print("✅ Knowledge API is using Storage Facility")
            results = search_data.get('local_results', [])
            
            if results:
                print(f"\n📄 Found {len(results)} results:")
                for i, result in enumerate(results, 1):
                    print(f"\n   Result {i}:")
                    print(f"      Topic: {result.get('topic')}")
                    print(f"      Category: {result.get('category')}")
                    print(f"      Relevance: {result.get('relevance', 0):.4f}")
                    
                # Check if our new entry is in the results
                ethereum_found = any('Ethereum' in r.get('topic', '') for r in results)
                if ethereum_found:
                    print("\n✅ NEW KNOWLEDGE VERIFIED - Ethereum entry found in search results!")
                else:
                    print("\n⚠️ New knowledge stored but not in top results (may need more relevant query)")
            else:
                print("\n⚠️ No results found - try a different search query")
        else:
            print("⚠️ WARNING: Knowledge API is using fallback mode")
            print("   Storage Facility integration may not be working")
    else:
        print(f"❌ Search failed with status {search_response.status_code}")
        
except Exception as e:
    print(f"❌ Verification failed: {e}")

print("\n" + "="*60)
print("✅ Test Complete!")
print("="*60)
print("\n📝 How to Add Your Own Knowledge:")
print("   1. Create a JSON structure like 'new_crypto_knowledge' above")
print("   2. POST to http://localhost:5001/api/kb/ingest")
print("   3. Knowledge is automatically stored in PostgreSQL")
print("   4. Immediately available for AI queries!\n")
print("💡 Supported units: crypto, physics, quantum, space\n")
