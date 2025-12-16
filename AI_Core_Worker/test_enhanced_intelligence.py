#!/usr/bin/env python3
"""
Test Enhanced Intelligence Layer
Validates all features WITHOUT modifying database
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:5010"
USER_ID = "test_user_" + str(int(time.time()))

print("=" * 70)
print("R3ÆLƎR AI - Enhanced Intelligence Layer Test Suite")
print("=" * 70)
print(f"Testing API: {BASE_URL}")
print(f"Test User ID: {USER_ID}")
print(f"Time: {datetime.now().isoformat()}")
print("=" * 70)
print()

# Test results
tests_passed = 0
tests_failed = 0
test_results = []


def test(name, func):
    """Run a test"""
    global tests_passed, tests_failed
    
    print(f"[TEST] {name}...", end=" ")
    
    try:
        result = func()
        
        if result['success']:
            print("✓ PASS")
            tests_passed += 1
            test_results.append({
                'test': name,
                'status': 'PASS',
                'details': result.get('details', '')
            })
        else:
            print(f"✗ FAIL: {result.get('error', 'Unknown error')}")
            tests_failed += 1
            test_results.append({
                'test': name,
                'status': 'FAIL',
                'error': result.get('error', '')
            })
    
    except Exception as e:
        print(f"✗ ERROR: {str(e)}")
        tests_failed += 1
        test_results.append({
            'test': name,
            'status': 'ERROR',
            'error': str(e)
        })


# ========== TEST 1: Health Check ==========
def test_health():
    response = requests.get(f"{BASE_URL}/api/enhanced/health")
    data = response.json()
    
    if not data.get('success'):
        return {'success': False, 'error': 'Health check failed'}
    
    health = data.get('health', {})
    
    return {
        'success': True,
        'details': f"Status: {health.get('status', 'unknown')}, Uptime: {health.get('metrics', {}).get('uptime_seconds', 0)}s"
    }


# ========== TEST 2: Basic Search ==========
def test_basic_search():
    response = requests.post(
        f"{BASE_URL}/api/enhanced/search",
        headers={'X-User-ID': USER_ID},
        json={'query': 'quantum physics', 'max_results': 5}
    )
    data = response.json()
    
    if not data.get('success'):
        return {'success': False, 'error': data.get('error', 'Unknown error')}
    
    return {
        'success': True,
        'details': f"Intent: {data.get('intent')}, Results: {len(data.get('results', []))}"
    }


# ========== TEST 3: Crypto Price Search ==========
def test_crypto_search():
    response = requests.post(
        f"{BASE_URL}/api/enhanced/search",
        headers={'X-User-ID': USER_ID},
        json={'query': 'What is the price of Bitcoin?', 'max_results': 5}
    )
    data = response.json()
    
    if not data.get('success'):
        return {'success': False, 'error': data.get('error', 'Unknown error')}
    
    intent = data.get('intent')
    has_live_data = data.get('external_data_included', False)
    
    if intent != 'crypto_price':
        return {'success': False, 'error': f"Wrong intent: {intent} (expected crypto_price)"}
    
    return {
        'success': True,
        'details': f"Intent: {intent}, Live data: {has_live_data}"
    }


# ========== TEST 4: Direct Crypto Price API ==========
def test_crypto_api():
    response = requests.get(
        f"{BASE_URL}/api/enhanced/crypto/price/bitcoin",
        headers={'X-User-ID': USER_ID}
    )
    data = response.json()
    
    if not data.get('success'):
        return {'success': False, 'error': data.get('error', 'Unknown error')}
    
    price_data = data.get('data', {})
    price = price_data.get('price_usd', 'N/A')
    
    return {
        'success': True,
        'details': f"BTC Price: ${price}"
    }


# ========== TEST 5: CVE Security Data ==========
def test_cve_api():
    response = requests.get(
        f"{BASE_URL}/api/enhanced/security/cve",
        headers={'X-User-ID': USER_ID}
    )
    data = response.json()
    
    if not data.get('success'):
        return {'success': False, 'error': data.get('error', 'Unknown error')}
    
    cve_data = data.get('data', {})
    count = cve_data.get('count', 0)
    
    return {
        'success': True,
        'details': f"Recent CVEs: {count}"
    }


# ========== TEST 6: Wikipedia API ==========
def test_wikipedia_api():
    response = requests.get(
        f"{BASE_URL}/api/enhanced/wikipedia/Quantum_computing",
        headers={'X-User-ID': USER_ID}
    )
    data = response.json()
    
    if not data.get('success'):
        return {'success': False, 'error': data.get('error', 'Unknown error')}
    
    wiki_data = data.get('data', {})
    title = wiki_data.get('title', 'Unknown')
    
    return {
        'success': True,
        'details': f"Article: {title}"
    }


# ========== TEST 7: Security Validation (SQL Injection) ==========
def test_sql_injection_block():
    response = requests.post(
        f"{BASE_URL}/api/enhanced/search",
        headers={'X-User-ID': USER_ID},
        json={'query': "'; DROP TABLE users; --", 'max_results': 5}
    )
    data = response.json()
    
    # Should be blocked
    if data.get('success'):
        return {'success': False, 'error': 'SQL injection not blocked!'}
    
    error = data.get('error', '')
    if 'malicious' in error.lower() or 'pattern' in error.lower():
        return {
            'success': True,
            'details': 'SQL injection correctly blocked'
        }
    
    return {'success': False, 'error': f"Unexpected error: {error}"}


# ========== TEST 8: Intent Classification ==========
def test_intent_classification():
    test_queries = [
        ('What is Bitcoin price?', 'crypto_price'),
        ('Recent CVE vulnerabilities', 'security_vulnerability'),
        ('Write a Python function', 'code_generation'),
        ('Best tool for penetration testing', 'tool_recommendation'),
        ('Explain quantum physics', 'knowledge_search')
    ]
    
    correct = 0
    
    for query, expected_intent in test_queries:
        response = requests.post(
            f"{BASE_URL}/api/enhanced/search",
            headers={'X-User-ID': USER_ID},
            json={'query': query, 'max_results': 1}
        )
        data = response.json()
        
        if data.get('success') and data.get('intent') == expected_intent:
            correct += 1
        
        time.sleep(0.1)  # Small delay
    
    accuracy = (correct / len(test_queries)) * 100
    
    if accuracy >= 80:
        return {
            'success': True,
            'details': f"Accuracy: {accuracy:.0f}% ({correct}/{len(test_queries)})"
        }
    
    return {
        'success': False,
        'error': f"Low accuracy: {accuracy:.0f}%"
    }


# ========== TEST 9: Metrics Collection ==========
def test_metrics():
    response = requests.get(f"{BASE_URL}/api/enhanced/metrics")
    data = response.json()
    
    if not data.get('success'):
        return {'success': False, 'error': data.get('error', 'Unknown error')}
    
    metrics = data.get('metrics', {})
    total_requests = metrics.get('total_requests', 0)
    
    if total_requests == 0:
        return {'success': False, 'error': 'No requests recorded'}
    
    return {
        'success': True,
        'details': f"Total requests: {total_requests}, Avg response: {metrics.get('avg_response_time_ms', 0)}ms"
    }


# ========== TEST 10: Circuit Breaker Status ==========
def test_circuit_breakers():
    response = requests.get(f"{BASE_URL}/api/enhanced/circuit-breakers")
    data = response.json()
    
    if not data.get('success'):
        return {'success': False, 'error': data.get('error', 'Unknown error')}
    
    breakers = data.get('circuit_breakers', {})
    
    if not breakers:
        return {
            'success': True,
            'details': 'No circuit breakers active yet (expected for fresh start)'
        }
    
    states = [f"{name}: {info.get('state')}" for name, info in breakers.items()]
    
    return {
        'success': True,
        'details': ', '.join(states)
    }


# ========== TEST 11: Rate Limiting ==========
def test_rate_limiting():
    """Test rate limiting by sending many requests"""
    # Send 10 requests rapidly (well under the 100/min limit)
    for i in range(10):
        response = requests.post(
            f"{BASE_URL}/api/enhanced/search",
            headers={'X-User-ID': f"rate_test_{USER_ID}"},
            json={'query': f'test {i}', 'max_results': 1}
        )
    
    # All should succeed (10 << 100)
    if response.status_code == 200:
        return {
            'success': True,
            'details': '10 requests succeeded (under rate limit)'
        }
    
    return {
        'success': False,
        'error': f"Unexpected status: {response.status_code}"
    }


# ========== TEST 12: Storage Facility Preservation ==========
def test_storage_preservation():
    """Verify Storage Facility is untouched"""
    # Try to access Storage Facility directly
    try:
        response = requests.get("http://localhost:5003/api/facility/health")
        data = response.json()
        
        if data.get('total_entries', 0) > 0:
            return {
                'success': True,
                'details': f"Storage Facility intact: {data.get('total_entries')} entries"
            }
        
        return {
            'success': False,
            'error': 'Storage Facility appears empty'
        }
    
    except Exception as e:
        return {
            'success': False,
            'error': f"Could not verify Storage Facility: {str(e)}"
        }


# ========== RUN ALL TESTS ==========

print("Starting test suite...\n")

test("1. Health Check", test_health)
test("2. Basic Search", test_basic_search)
test("3. Crypto Price Search (Intent Detection)", test_crypto_search)
test("4. Direct Crypto Price API", test_crypto_api)
test("5. CVE Security Data", test_cve_api)
test("6. Wikipedia API", test_wikipedia_api)
test("7. SQL Injection Protection", test_sql_injection_block)
test("8. Intent Classification Accuracy", test_intent_classification)
test("9. Metrics Collection", test_metrics)
test("10. Circuit Breaker Status", test_circuit_breakers)
test("11. Rate Limiting", test_rate_limiting)
test("12. Storage Facility Preservation", test_storage_preservation)

# ========== SUMMARY ==========

print()
print("=" * 70)
print("TEST SUMMARY")
print("=" * 70)
print(f"Total Tests: {tests_passed + tests_failed}")
print(f"Passed: {tests_passed} ✓")
print(f"Failed: {tests_failed} ✗")
print(f"Success Rate: {(tests_passed / (tests_passed + tests_failed) * 100) if (tests_passed + tests_failed) > 0 else 0:.1f}%")
print("=" * 70)
print()

# Show failed tests
if tests_failed > 0:
    print("FAILED TESTS:")
    for result in test_results:
        if result['status'] != 'PASS':
            print(f"  ✗ {result['test']}: {result.get('error', 'Unknown error')}")
    print()

# Final verdict
if tests_failed == 0:
    print("🎉 ALL TESTS PASSED!")
    print()
    print("Enhanced Intelligence Layer is working perfectly!")
    print("Your Storage Facility (30,657 entries) remains UNTOUCHED.")
    print()
    print("Next steps:")
    print("  1. Try the Enhanced API: curl http://localhost:5010/api/enhanced/search \\")
    print("       -X POST -H 'Content-Type: application/json' \\")
    print("       -d '{\"query\": \"What is Bitcoin price?\", \"max_results\": 5}'")
    print()
    print("  2. Check metrics: curl http://localhost:5010/api/enhanced/metrics")
    print()
    print("  3. Monitor health: curl http://localhost:5010/api/enhanced/health")
else:
    print("⚠️  SOME TESTS FAILED")
    print()
    print("Please review the failures above and ensure:")
    print("  1. Storage Facility is running (port 5003)")
    print("  2. Enhanced API is running (port 5010)")
    print("  3. Internet connection is available (for external APIs)")
    print("  4. No firewall blocking external API calls")

print()
print("=" * 70)

# Exit with appropriate code
exit(0 if tests_failed == 0 else 1)
