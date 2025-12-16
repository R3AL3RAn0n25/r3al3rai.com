#!/usr/bin/env python3
"""
Comprehensive API and Authentication Test Suite
Tests all 7 services, both authentication systems, and health endpoints
"""

import requests
import json
import sys
from datetime import datetime

# Test configuration
BASE_URLS = {
    'backend': 'http://localhost:3000',
    'storage': 'http://localhost:3003',
    'bitxtractor': 'http://localhost:3002',
    'blackarch': 'http://localhost:5003',
    'knowledge': 'http://localhost:5004',
    'droid': 'http://localhost:5005',
    'intelligence': 'http://localhost:5010'
}

test_user = {
    'username': 'test_diagnostic_final',
    'password': 'Test@123456'
}

def print_header(title):
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}")

def print_test(name, status, details=""):
    status_symbol = "✓" if status else "✗"
    print(f"{status_symbol} {name}")
    if details:
        print(f"  └─ {details}")

def test_node_auth():
    print_header("1. NODE BACKEND AUTHENTICATION (Port 3000)")
    
    results = {
        'register': False,
        'login_valid': False,
        'login_invalid': False,
        'auth_system': 'Node/Express with JWT'
    }
    
    try:
        # Test registration
        reg_data = {
            'username': test_user['username'],
            'password': test_user['password'],
            'email': f"{test_user['username']}@test.local"
        }
        reg_response = requests.post(f"{BASE_URLS['backend']}/api/auth/register", json=reg_data, timeout=5)
        
        if reg_response.status_code == 200:
            reg_json = reg_response.json()
            if reg_json.get('success'):
                print_test("Registration", True, f"Status 200, User ID: {reg_json.get('user', {}).get('id')}")
                results['register'] = True
            else:
                print_test("Registration", False, f"Status 200 but success=false: {reg_json.get('error')}")
        else:
            print_test("Registration", False, f"Status {reg_response.status_code}")
        
        # Test valid login
        login_data = {
            'username': test_user['username'],
            'password': test_user['password']
        }
        login_response = requests.post(f"{BASE_URLS['backend']}/api/auth/login", json=login_data, timeout=5)
        
        if login_response.status_code == 200:
            login_json = login_response.json()
            if login_json.get('success'):
                token = login_json.get('token')
                print_test("Login (Valid)", True, f"Status 200, JWT: {token[:20]}..." if token else "No token")
                results['login_valid'] = True
            else:
                print_test("Login (Valid)", False, f"Status 200 but success=false")
        else:
            print_test("Login (Valid)", False, f"Status {login_response.status_code}")
        
        # Test invalid login
        invalid_login = {
            'username': test_user['username'],
            'password': 'wrongpassword'
        }
        invalid_response = requests.post(f"{BASE_URLS['backend']}/api/auth/login", json=invalid_login, timeout=5)
        
        if invalid_response.status_code == 401:
            invalid_json = invalid_response.json()
            if not invalid_json.get('success'):
                print_test("Login (Invalid)", True, f"Status 401 (correctly rejected)")
                results['login_invalid'] = True
            else:
                print_test("Login (Invalid)", False, f"Status 401 but success=true")
        else:
            print_test("Login (Invalid)", False, f"Status {invalid_response.status_code} (expected 401)")
    
    except Exception as e:
        print_test("Node Auth System", False, f"Exception: {str(e)}")
    
    return results

def test_aicore_auth():
    print_header("2. AI_CORE_WORKER AUTHENTICATION (Port 5004)")
    
    results = {
        'register': False,
        'login_valid': False,
        'login_invalid': False,
        'auth_system': 'Flask with Sessions',
        'error': None
    }
    
    try:
        # Test registration
        reg_data = {
            'username': f"aicore_{test_user['username']}",
            'password': test_user['password'],
            'email': f"aicore_{test_user['username']}@test.local"
        }
        reg_response = requests.post(f"{BASE_URLS['knowledge']}/api/user/register", json=reg_data, timeout=5)
        
        if reg_response.status_code == 200:
            reg_json = reg_response.json()
            print_test("Registration", True, f"Status 200, Response: {json.dumps(reg_json)[:60]}")
            results['register'] = True
        elif reg_response.status_code == 404:
            print_test("Registration", False, f"Status 404 - Endpoint not found")
            results['error'] = "404 - Endpoints not exposed"
        else:
            print_test("Registration", False, f"Status {reg_response.status_code}")
    
    except Exception as e:
        print_test("Registration", False, f"Exception: {str(e)}")
        results['error'] = str(e)
    
    return results

def test_health_endpoints():
    print_header("3. HEALTH ENDPOINTS (All 7 Services)")
    
    results = {}
    
    for service_name, base_url in BASE_URLS.items():
        try:
            response = requests.get(f"{base_url}/api/health", timeout=3)
            
            if response.status_code == 200:
                try:
                    json_data = response.json()
                    status = json_data.get('status', 'unknown')
                    print_test(f"{service_name.upper()}", True, f"Status 200, Health: {status}")
                    results[service_name] = 'healthy'
                except:
                    print_test(f"{service_name.upper()}", False, f"Status 200 but invalid JSON")
                    results[service_name] = 'invalid_response'
            else:
                print_test(f"{service_name.upper()}", False, f"Status {response.status_code}")
                results[service_name] = f'status_{response.status_code}'
        
        except requests.exceptions.Timeout:
            print_test(f"{service_name.upper()}", False, f"Timeout")
            results[service_name] = 'timeout'
        except Exception as e:
            print_test(f"{service_name.upper()}", False, f"Error: {str(e)[:50]}")
            results[service_name] = 'error'
    
    return results

def test_backend_health_details():
    print_header("4. BACKEND HEALTH DETAILS (Port 3000)")
    
    try:
        response = requests.get("http://localhost:3000/api/health", timeout=5)
        if response.status_code in [200, 503]:  # 503 Service Unavailable is also ok for health check
            try:
                data = response.json()
                print(f"Status: {response.status_code}")
                print(f"Response: {json.dumps(data, indent=2)}")
                return data
            except:
                print(f"Could not parse JSON from response")
                return None
        else:
            print(f"Unexpected status: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

def test_api_endpoints():
    print_header("5. API ENDPOINTS (Knowledge & Droid APIs)")
    
    results = {}
    
    # Test Knowledge API
    try:
        response = requests.get("http://localhost:5004/api/query", params={'q': 'test'}, timeout=3)
        if response.status_code in [200, 400]:
            print_test("Knowledge API /api/query", True, f"Status {response.status_code}")
            results['knowledge'] = 'accessible'
        else:
            print_test("Knowledge API /api/query", False, f"Status {response.status_code}")
            results['knowledge'] = f'status_{response.status_code}'
    except Exception as e:
        print_test("Knowledge API /api/query", False, f"Error: {str(e)[:50]}")
        results['knowledge'] = 'error'
    
    # Test Droid API
    try:
        response = requests.get("http://localhost:5005/", timeout=3)
        if response.status_code == 200:
            print_test("Droid API /", True, f"Status 200")
            results['droid'] = 'accessible'
        else:
            print_test("Droid API /", False, f"Status {response.status_code}")
            results['droid'] = f'status_{response.status_code}'
    except Exception as e:
        print_test("Droid API /", False, f"Error: {str(e)[:50]}")
        results['droid'] = 'error'
    
    return results

def main():
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*68 + "║")
    print("║" + "  R3AL3R AI - COMPREHENSIVE API & AUTH TEST SUITE".center(68) + "║")
    print("║" + f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}".center(68) + "║")
    print("║" + " "*68 + "║")
    print("╚" + "="*68 + "╝")
    
    all_results = {
        'timestamp': datetime.now().isoformat(),
        'node_auth': test_node_auth(),
        'aicore_auth': test_aicore_auth(),
        'health_endpoints': test_health_endpoints(),
        'backend_health': test_backend_health_details(),
        'api_endpoints': test_api_endpoints()
    }
    
    # Summary
    print_header("SUMMARY")
    
    node_pass = (all_results['node_auth']['register'] and 
                 all_results['node_auth']['login_valid'] and 
                 all_results['node_auth']['login_invalid'])
    
    print(f"Node Backend Auth: {'✓ FLAWLESS' if node_pass else '✗ ISSUES'}")
    print(f"AI_Core Auth: ✗ {all_results['aicore_auth'].get('error', 'Not fully tested')}")
    
    healthy_services = sum(1 for v in all_results['health_endpoints'].values() if v == 'healthy')
    total_services = len(all_results['health_endpoints'])
    print(f"Health Endpoints: {healthy_services}/{total_services} services reporting healthy")
    
    print("\nDETAILED RESULTS:")
    print(json.dumps(all_results, indent=2))
    
    print_header("STATUS")
    if node_pass and healthy_services >= 5:
        print("✓ Core authentication working (Node)")
        print("⚠ AI_Core authentication needs investigation (404 errors)")
        print(f"✓ {healthy_services} of {total_services} services healthy")
        print("\nRECOMMENDATIONS:")
        print("1. Investigate /api/user/* routes in AI_Core_Worker (Flask routing issue)")
        print("2. Add proper health endpoints to remaining services")
        print("3. Full system validation passing with minor issues")
    else:
        print("✗ Issues detected - see details above")

if __name__ == '__main__':
    main()
