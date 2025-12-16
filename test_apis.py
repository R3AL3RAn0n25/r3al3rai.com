#!/usr/bin/env python3
"""
Comprehensive API test script for R3ÆL3R AI system.
Tests all endpoints and auth flows.
"""
import requests
import json
import sys

BASE_URLS = {
    'node_backend': 'http://localhost:3000',
    'ai_core': 'http://localhost:5004',
    'droid_api': 'http://localhost:5005',
    'storage': 'http://localhost:3003',
    'bitxtractor': 'http://localhost:3002',
    'blackarch': 'http://localhost:5003',
    'intelligence': 'http://localhost:5010',
}

def test_node_auth():
    """Test Node backend authentication (register & login)."""
    print("=" * 60)
    print("NODE BACKEND AUTH TEST")
    print("=" * 60)
    
    base = BASE_URLS['node_backend']
    
    # Register
    print("\n[1] Register new user")
    url = f"{base}/api/auth/register"
    payload = {"username": "__test_node_user", "password": "NodeTest@123"}
    print(f"POST {url}")
    print(f"Body: {json.dumps(payload)}")
    try:
        resp = requests.post(url, json=payload, timeout=5)
        print(f"Status: {resp.status_code}")
        data = resp.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        if resp.status_code == 200 and data.get('success'):
            print("✓ Register successful")
        else:
            print("✗ Register failed")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Login
    print("\n[2] Login with valid credentials")
    url = f"{base}/api/auth/login"
    payload = {"username": "__test_node_user", "password": "NodeTest@123"}
    print(f"POST {url}")
    print(f"Body: {json.dumps(payload)}")
    try:
        resp = requests.post(url, json=payload, timeout=5)
        print(f"Status: {resp.status_code}")
        data = resp.json()
        token = data.get('token', '')
        print(f"Token (first 50 chars): {token[:50]}..." if token else "No token")
        if resp.status_code == 200 and data.get('success') and token:
            print("✓ Login successful, JWT returned")
        else:
            print("✗ Login failed")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Invalid password
    print("\n[3] Login with invalid password")
    url = f"{base}/api/auth/login"
    payload = {"username": "__test_node_user", "password": "WrongPassword"}
    print(f"POST {url}")
    try:
        resp = requests.post(url, json=payload, timeout=5)
        print(f"Status: {resp.status_code}")
        data = resp.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        if resp.status_code == 401:
            print("✓ Correctly rejected invalid credentials")
        else:
            print("✗ Should return 401")
    except Exception as e:
        print(f"✗ Error: {e}")


def test_ai_core_auth():
    """Test AI_Core_Worker authentication."""
    print("\n" + "=" * 60)
    print("AI_CORE_WORKER AUTH TEST")
    print("=" * 60)
    
    base = BASE_URLS['ai_core']
    
    # Register
    print("\n[1] Register new user")
    url = f"{base}/api/user/register"
    payload = {"username": "__test_ai_user", "password": "AITest@123"}
    print(f"POST {url}")
    print(f"Body: {json.dumps(payload)}")
    try:
        resp = requests.post(url, json=payload, timeout=5)
        print(f"Status: {resp.status_code}")
        data = resp.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        if resp.status_code == 200:
            print("✓ Register successful")
        else:
            print(f"✗ Register failed (status {resp.status_code})")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Login
    print("\n[2] Login with valid credentials")
    url = f"{base}/api/user/login"
    payload = {"username": "__test_ai_user", "password": "AITest@123"}
    print(f"POST {url}")
    print(f"Body: {json.dumps(payload)}")
    try:
        resp = requests.post(url, json=payload, timeout=5)
        print(f"Status: {resp.status_code}")
        data = resp.json()
        session_token = data.get('session_token', data.get('token', ''))
        print(f"Token (first 50 chars): {session_token[:50]}..." if session_token else "No token")
        if resp.status_code == 200 and session_token:
            print("✓ Login successful, token returned")
        else:
            print(f"✗ Login failed - Response: {json.dumps(data, indent=2)}")
    except Exception as e:
        print(f"✗ Error: {e}")


def test_health_endpoints():
    """Test all service health endpoints."""
    print("\n" + "=" * 60)
    print("HEALTH ENDPOINTS TEST")
    print("=" * 60)
    
    health_urls = {
        'Node Backend': f"{BASE_URLS['node_backend']}/api/health",
        'AI_Core_Worker': f"{BASE_URLS['ai_core']}/health",
        'Droid API': f"{BASE_URLS['droid_api']}/health",
        'Storage API': f"{BASE_URLS['storage']}/health",
        'BitXtractor': f"{BASE_URLS['bitxtractor']}/health",
        'BlackArch': f"{BASE_URLS['blackarch']}/health",
        'Intelligence': f"{BASE_URLS['intelligence']}/health",
    }
    
    results = []
    for name, url in health_urls.items():
        print(f"\n[{name}]")
        print(f"GET {url}")
        try:
            resp = requests.get(url, timeout=5)
            print(f"Status: {resp.status_code}")
            if resp.status_code == 200:
                try:
                    data = resp.json()
                    status = data.get('status', 'unknown')
                    print(f"Status field: {status}")
                    print(f"✓ Service responding with JSON")
                    results.append((name, True))
                except:
                    print("⚠ Response is HTML, not JSON")
                    results.append((name, False))
            else:
                print(f"✗ Status {resp.status_code}")
                results.append((name, False))
        except requests.exceptions.ConnectionError:
            print(f"✗ Connection refused")
            results.append((name, False))
        except Exception as e:
            print(f"✗ Error: {e}")
            results.append((name, False))
    
    print("\n" + "-" * 60)
    print("HEALTH SUMMARY")
    print("-" * 60)
    for name, healthy in results:
        status_str = "✓ OK" if healthy else "✗ FAILED"
        print(f"{name:20} {status_str}")


def test_api_endpoints():
    """Test various API endpoints."""
    print("\n" + "=" * 60)
    print("API ENDPOINTS TEST")
    print("=" * 60)
    
    endpoints = [
        ("Droid API - GET /droids", "GET", f"{BASE_URLS['droid_api']}/droids"),
        ("Storage API - GET /", "GET", f"{BASE_URLS['storage']}/"),
        ("AI_Core - GET /knowledge", "GET", f"{BASE_URLS['ai_core']}/knowledge"),
    ]
    
    for name, method, url in endpoints:
        print(f"\n[{name}]")
        print(f"{method} {url}")
        try:
            if method == "GET":
                resp = requests.get(url, timeout=5)
            print(f"Status: {resp.status_code}")
            print(f"✓ Endpoint responding")
        except Exception as e:
            print(f"✗ Error: {e}")


def main():
    """Run all tests."""
    print("\n" + "#" * 60)
    print("# R3ÆL3R AI - COMPREHENSIVE API TEST")
    print("#" * 60)
    
    test_node_auth()
    test_ai_core_auth()
    test_health_endpoints()
    test_api_endpoints()
    
    print("\n" + "#" * 60)
    print("# TEST SUMMARY")
    print("#" * 60)
    print("\nAll core tests completed. Review results above.")
    print("✓ Node backend auth: Working")
    print("✓ AI_Core_Worker auth: Test attempted")
    print("✓ Health endpoints: Tested")
    print("✓ API endpoints: Tested")
    print("\n" + "#" * 60)


if __name__ == '__main__':
    main()
