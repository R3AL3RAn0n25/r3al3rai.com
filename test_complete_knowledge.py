#!/usr/bin/env python3
"""Test complete scientific knowledge base integration."""

import requests
import json

BASE_URL = "http://localhost:5001"

def test_knowledge_search(query, max_results=3):
    """Test knowledge base search."""
    url = f"{BASE_URL}/api/kb/search"
    payload = {
        "query": query,
        "max_results": max_results
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        print(f"\n{'='*80}")
        print(f"🔍 Query: {query}")
        print(f"{'='*80}")
        print(f"✅ Found {len(data.get('results', []))} results")
        
        for i, result in enumerate(data.get('results', [])[:max_results], 1):
            print(f"\n📚 Result {i}:")
            print(f"   Topic: {result.get('topic', 'N/A')}")
            print(f"   Category: {result.get('category', 'N/A')}")
            print(f"   Source: {result.get('source', 'N/A')}")
            content = result.get('content', '')
            print(f"   Content: {content[:200]}...")
            
        return data
    except Exception as e:
        print(f"❌ Error testing {query}: {e}")
        return None

def test_knowledge_sources():
    """Test knowledge sources endpoint."""
    url = f"{BASE_URL}/api/knowledge-sources"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        print(f"\n{'='*80}")
        print(f"📊 KNOWLEDGE BASE STATISTICS")
        print(f"{'='*80}")
        print(f"Total Entries: {data.get('total_entries', 0):,}")
        print(f"Total Sources: {data.get('sources', {}).get('count', 0)}")
        
        print(f"\n📚 Sources by Category:")
        for source, count in sorted(data.get('sources', {}).get('list', {}).items(), 
                                    key=lambda x: x[1], reverse=True)[:15]:
            print(f"   {source}: {count:,} entries")
            
        return data
    except Exception as e:
        print(f"❌ Error getting sources: {e}")
        return None

def main():
    """Run all tests."""
    print("\n" + "="*80)
    print("🧪 TESTING COMPLETE SCIENTIFIC KNOWLEDGE BASE")
    print("="*80)
    
    # Test knowledge sources
    sources = test_knowledge_sources()
    
    # Test queries across all domains
    test_queries = [
        ("quantum entanglement", "Quantum Physics"),
        ("thermodynamics laws", "Physics"),
        ("exoplanet detection", "Astronomy"),
        ("orbital mechanics", "Aerospace"),
        ("wave function collapse", "Quantum Physics"),
        ("Newton's laws", "Physics"),
    ]
    
    for query, domain in test_queries:
        print(f"\n🎯 Testing {domain}...")
        test_knowledge_search(query, max_results=2)
    
    print(f"\n{'='*80}")
    print("✅ KNOWLEDGE BASE TEST COMPLETE")
    print(f"{'='*80}\n")

if __name__ == "__main__":
    main()
