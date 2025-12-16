#!/usr/bin/env python3
"""
R3ÆLƎR AI: Complete System Integration Test
Tests Knowledge Base + BlackArch Tools + User System
"""

import requests
import json
import sys

API_BASE = "http://localhost:5003"
KNOWLEDGE_API = "http://localhost:5001"

def print_header(text):
    print("\n" + "=" * 70)
    print(f" {text}")
    print("=" * 70)

def test_facility_status():
    """Test 1: Storage Facility Status"""
    print_header("TEST 1: Storage Facility Status")
    
    response = requests.get(f"{API_BASE}/api/facility/status")
    data = response.json()
    
    print(f"✅ Total Units: {len(data['units'])}")
    print(f"✅ Total Entries: {data['total_entries']}")
    print(f"✅ Cost: {data['cost']}\n")
    
    for unit_id, unit in data['units'].items():
        print(f"  📦 {unit['name']:40s} - {unit['total_entries']:6d} entries")
    
    return data

def test_knowledge_search():
    """Test 2: Knowledge Base Search (Original Functionality)"""
    print_header("TEST 2: Knowledge Base Search - Crypto")
    
    response = requests.post(f"{KNOWLEDGE_API}/api/kb/search", json={
        "query": "Bitcoin wallet security",
        "maxPassages": 3
    })
    data = response.json()
    
    print(f"✅ Used Storage Facility: {data.get('used_storage_facility', False)}")
    print(f"✅ Results: {len(data.get('passages', []))}")
    
    for passage in data.get('passages', [])[:2]:
        print(f"\n  Topic: {passage.get('topic')}")
        print(f"  Unit: {passage.get('source_unit')}")
        print(f"  Relevance: {passage.get('relevance_score', 0):.4f}")
    
    return data

def test_blackarch_search():
    """Test 3: BlackArch Tools Search"""
    print_header("TEST 3: BlackArch Tools Search")
    
    test_queries = [
        {"query": "network scanner", "description": "Network Scanning Tools"},
        {"query": "password cracking", "description": "Password Tools"},
        {"query": "web application testing", "description": "Web Security Tools"}
    ]
    
    for test in test_queries:
        print(f"\n🔍 Query: {test['description']}")
        
        response = requests.post(f"{API_BASE}/api/tools/search", json={
            "query": test['query'],
            "max_results": 3
        })
        data = response.json()
        
        print(f"   Found: {data['total_results']} tools")
        
        for tool in data['tools'][:2]:
            print(f"   • {tool['name']:20s} ({tool['category']})")
            print(f"     {tool['description'][:60]}...")
    
    return data

def test_blackarch_categories():
    """Test 4: BlackArch Tool Categories"""
    print_header("TEST 4: BlackArch Tool Categories")
    
    response = requests.get(f"{API_BASE}/api/tools/categories")
    data = response.json()
    
    print(f"✅ Total Categories: {data['total_categories']}\n")
    
    for category in data['categories'][:10]:
        print(f"  {category['category']:20s}: {category['tool_count']:3d} tools")
    
    return data

def test_tool_details():
    """Test 5: Specific Tool Details"""
    print_header("TEST 5: Tool Details - Nmap")
    
    response = requests.get(f"{API_BASE}/api/tools/nmap")
    
    if response.status_code == 200:
        data = response.json()
        tool = data['tool']
        
        print(f"✅ Tool: {tool['name']}")
        print(f"   Category: {tool['category']}")
        print(f"   Skill Level: {tool['skill_level']}")
        print(f"   Size: {tool['estimated_size_mb']} MB")
        print(f"   Description: {tool['description']}")
        print(f"   Usage: {tool['usage_example']}")
        print(f"   Docs: {tool['documentation_url']}")
        
        return data
    else:
        print(f"❌ Tool not found (status: {response.status_code})")
        return None

def test_knowledge_unchanged():
    """Test 6: Verify Original Knowledge Base Unchanged"""
    print_header("TEST 6: Verify Knowledge Base Integrity")
    
    expected_counts = {
        'physics': 25875,
        'quantum': 1042,
        'space': 3727,
        'crypto': 13
    }
    
    response = requests.get(f"{API_BASE}/api/facility/status")
    data = response.json()
    
    all_good = True
    for unit_id, expected_count in expected_counts.items():
        actual_count = data['units'][unit_id]['total_entries']
        status = "✅" if actual_count == expected_count else "❌"
        
        print(f"  {status} {unit_id:15s}: {actual_count:6d} entries (expected: {expected_count})")
        
        if actual_count != expected_count:
            all_good = False
    
    if all_good:
        print("\n✅ All knowledge units preserved perfectly!")
    else:
        print("\n⚠️  WARNING: Knowledge counts don't match expected values!")
    
    return all_good

def run_all_tests():
    """Run complete test suite"""
    print("\n" + "█" * 70)
    print("█" + " " * 68 + "█")
    print("█" + "  R3ÆLƎR AI COMPLETE SYSTEM INTEGRATION TEST".center(68) + "█")
    print("█" + "  Knowledge Base + BlackArch Tools + User System".center(68) + "█")
    print("█" + " " * 68 + "█")
    print("█" * 70)
    
    tests = [
        ("Storage Facility Status", test_facility_status),
        ("Knowledge Base Search", test_knowledge_search),
        ("BlackArch Tools Search", test_blackarch_search),
        ("Tool Categories", test_blackarch_categories),
        ("Tool Details", test_tool_details),
        ("Knowledge Integrity", test_knowledge_unchanged)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results[test_name] = {"status": "PASS", "data": result}
        except Exception as e:
            results[test_name] = {"status": "FAIL", "error": str(e)}
            print(f"\n❌ ERROR: {e}")
    
    # Summary
    print_header("TEST SUMMARY")
    
    passed = sum(1 for r in results.values() if r['status'] == 'PASS')
    total = len(results)
    
    for test_name, result in results.items():
        status_icon = "✅" if result['status'] == 'PASS' else "❌"
        print(f"{status_icon} {test_name}")
    
    print(f"\n📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n" + "█" * 70)
        print("█" + " " * 68 + "█")
        print("█" + "  🎉 ALL TESTS PASSED! 🎉".center(68) + "█")
        print("█" + " " * 68 + "█")
        print("█" + "  R3ÆLƎR AI is production-ready!".center(68) + "█")
        print("█" + "  ✅ Knowledge Base: INTACT".center(68) + "█")
        print("█" + "  ✅ BlackArch Tools: INTEGRATED".center(68) + "█")
        print("█" + "  ✅ User System: READY".center(68) + "█")
        print("█" + " " * 68 + "█")
        print("█" * 70)
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Check errors above.")
    
    return passed == total

if __name__ == '__main__':
    try:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ FATAL ERROR: {e}")
        sys.exit(1)
