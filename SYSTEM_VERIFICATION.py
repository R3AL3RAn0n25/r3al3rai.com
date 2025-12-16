#!/usr/bin/env python3
"""
R3ÆLƎR AI - Complete System Verification
Tests all components: Database, Backend, Frontend, APIs, and Features
"""

import requests
import json
import subprocess
import time
import sys
import os
from datetime import datetime

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}\n")

def print_success(text):
    print(f"{Colors.GREEN}✓ {text}{Colors.RESET}")

def print_error(text):
    print(f"{Colors.RED}✗ {text}{Colors.RESET}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠ {text}{Colors.RESET}")

def print_info(text):
    print(f"{Colors.BLUE}ℹ {text}{Colors.RESET}")

class SystemVerification:
    def __init__(self):
        self.results = {
            'database': {},
            'backend': {},
            'frontend': {},
            'apis': {},
            'features': {},
            'timestamp': datetime.now().isoformat()
        }
        self.test_token = None
        self.test_user = f"testuser_{int(time.time())}"
        self.test_password = "TestPass123!"

    def verify_database(self):
        print_header("DATABASE VERIFICATION")
        
        # Check PostgreSQL connection
        try:
            import psycopg2
            conn = psycopg2.connect(
                host="localhost",
                port=5432,
                user="r3aler_user_2025",
                password="password123",
                database="r3aler_ai"
            )
            cursor = conn.cursor()
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
            print_success(f"PostgreSQL connected: {version.split(',')[0]}")
            
            # Check tables
            cursor.execute("""
                SELECT table_name FROM information_schema.tables 
                WHERE table_schema = 'public'
            """)
            tables = [row[0] for row in cursor.fetchall()]
            print_success(f"Database tables found: {len(tables)}")
            for table in tables:
                print_info(f"  - {table}")
            
            # Check users table
            cursor.execute("SELECT COUNT(*) FROM users")
            user_count = cursor.fetchone()[0]
            print_success(f"Users in database: {user_count}")
            
            cursor.close()
            conn.close()
            self.results['database']['status'] = 'connected'
            self.results['database']['tables'] = tables
            return True
        except Exception as e:
            print_error(f"Database connection failed: {str(e)}")
            self.results['database']['status'] = 'failed'
            self.results['database']['error'] = str(e)
            return False

    def verify_backend(self):
        print_header("BACKEND SERVER VERIFICATION")
        
        backend_url = "http://localhost:3000"
        
        # Check health endpoint
        try:
            response = requests.get(f"{backend_url}/api/health", timeout=5)
            if response.status_code == 200:
                health = response.json()
                print_success(f"Backend health: {health.get('ok', False)}")
                print_info(f"  - Node uptime: {health['node']['uptime_s']}s")
                print_info(f"  - Memory: {health['node']['rss_mb']}MB")
                print_info(f"  - Database: {'Connected' if health['db']['ok'] else 'Disconnected'}")
                self.results['backend']['health'] = health
                return True
            else:
                print_error(f"Backend health check failed: {response.status_code}")
                self.results['backend']['status'] = 'unhealthy'
                return False
        except requests.exceptions.ConnectionError:
            print_error("Cannot connect to backend on port 3000")
            print_warning("Ensure backend is running: npm start")
            self.results['backend']['status'] = 'not_running'
            return False
        except Exception as e:
            print_error(f"Backend verification failed: {str(e)}")
            self.results['backend']['status'] = 'error'
            return False

    def verify_authentication(self):
        print_header("AUTHENTICATION VERIFICATION")
        
        backend_url = "http://localhost:3000"
        
        # Register test user
        try:
            print_info(f"Registering test user: {self.test_user}")
            response = requests.post(
                f"{backend_url}/api/auth/register",
                json={"username": self.test_user, "password": self.test_password},
                timeout=5
            )
            
            if response.status_code in [200, 409]:  # 409 = user exists
                print_success("User registration endpoint working")
                self.results['backend']['auth_register'] = True
            else:
                print_error(f"Registration failed: {response.status_code}")
                self.results['backend']['auth_register'] = False
                return False
            
            # Login test user
            print_info("Attempting login...")
            response = requests.post(
                f"{backend_url}/api/auth/login",
                json={"username": self.test_user, "password": self.test_password},
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and data.get('token'):
                    self.test_token = data['token']
                    print_success(f"Login successful, token obtained")
                    self.results['backend']['auth_login'] = True
                    return True
                else:
                    print_error("Login returned invalid response")
                    self.results['backend']['auth_login'] = False
                    return False
            else:
                print_error(f"Login failed: {response.status_code}")
                self.results['backend']['auth_login'] = False
                return False
                
        except Exception as e:
            print_error(f"Authentication verification failed: {str(e)}")
            self.results['backend']['auth_error'] = str(e)
            return False

    def verify_frontend(self):
        print_header("FRONTEND VERIFICATION")
        
        frontend_url = "http://localhost:5173"  # Vite dev server
        
        try:
            response = requests.get(frontend_url, timeout=5)
            if response.status_code == 200:
                print_success("Frontend dev server is running on port 5173")
                
                # Check for login page
                if 'R3ÆLƎR' in response.text or 'login' in response.text.lower():
                    print_success("Login page is being served")
                    self.results['frontend']['status'] = 'running'
                    self.results['frontend']['login_page'] = True
                    return True
                else:
                    print_warning("Frontend loaded but login page not detected")
                    self.results['frontend']['status'] = 'running'
                    self.results['frontend']['login_page'] = False
                    return True
            else:
                print_error(f"Frontend returned status: {response.status_code}")
                self.results['frontend']['status'] = 'error'
                return False
        except requests.exceptions.ConnectionError:
            print_warning("Frontend dev server not running on port 5173")
            print_info("Try: cd application/Frontend && npm run dev")
            self.results['frontend']['status'] = 'not_running'
            return False
        except Exception as e:
            print_error(f"Frontend verification failed: {str(e)}")
            self.results['frontend']['status'] = 'error'
            return False

    def verify_api_endpoints(self):
        print_header("API ENDPOINTS VERIFICATION")
        
        if not self.test_token:
            print_warning("Skipping API tests - no authentication token")
            return False
        
        backend_url = "http://localhost:3000"
        headers = {"Authorization": f"Bearer {self.test_token}"}
        
        endpoints = [
            ("/api/status", "GET", None),
            ("/api/health", "GET", None),
        ]
        
        results = {}
        for endpoint, method, data in endpoints:
            try:
                if method == "GET":
                    response = requests.get(f"{backend_url}{endpoint}", headers=headers, timeout=5)
                else:
                    response = requests.post(f"{backend_url}{endpoint}", json=data, headers=headers, timeout=5)
                
                if response.status_code in [200, 201]:
                    print_success(f"{method} {endpoint}: {response.status_code}")
                    results[endpoint] = True
                else:
                    print_warning(f"{method} {endpoint}: {response.status_code}")
                    results[endpoint] = False
            except Exception as e:
                print_error(f"{method} {endpoint}: {str(e)}")
                results[endpoint] = False
        
        self.results['apis']['endpoints'] = results
        return any(results.values())

    def verify_knowledge_api(self):
        print_header("KNOWLEDGE API VERIFICATION")
        
        knowledge_url = "http://localhost:5004"
        
        try:
            response = requests.get(f"{knowledge_url}/health", timeout=5)
            if response.status_code == 200:
                health = response.json()
                print_success("Knowledge API is running")
                print_info(f"  - AI Modules: {'Loaded' if health.get('ai_modules_loaded') else 'Not loaded'}")
                print_info(f"  - Storage Facility: {'Connected' if health['storage_facility'].get('connected') else 'Disconnected'}")
                print_info(f"  - Total Entries: {health['storage_facility'].get('total_entries', 0)}")
                self.results['apis']['knowledge_api'] = health
                return True
            else:
                print_warning(f"Knowledge API health check: {response.status_code}")
                self.results['apis']['knowledge_api'] = 'unhealthy'
                return False
        except requests.exceptions.ConnectionError:
            print_warning("Knowledge API not running on port 5004")
            self.results['apis']['knowledge_api'] = 'not_running'
            return False
        except Exception as e:
            print_error(f"Knowledge API verification failed: {str(e)}")
            self.results['apis']['knowledge_api'] = 'error'
            return False

    def verify_droid_api(self):
        print_header("DROID API VERIFICATION")
        
        droid_url = "http://localhost:5005"
        
        try:
            response = requests.get(f"{droid_url}/health", timeout=5)
            if response.status_code == 200:
                print_success("Droid API is running")
                self.results['apis']['droid_api'] = 'running'
                return True
            else:
                print_warning(f"Droid API health check: {response.status_code}")
                self.results['apis']['droid_api'] = 'unhealthy'
                return False
        except requests.exceptions.ConnectionError:
            print_warning("Droid API not running on port 5005")
            self.results['apis']['droid_api'] = 'not_running'
            return False
        except Exception as e:
            print_error(f"Droid API verification failed: {str(e)}")
            self.results['apis']['droid_api'] = 'error'
            return False

    def verify_storage_facility(self):
        print_header("STORAGE FACILITY VERIFICATION")
        
        storage_url = "http://localhost:3003"
        
        try:
            response = requests.get(f"{storage_url}/api/facility/status", timeout=5)
            if response.status_code == 200:
                status = response.json()
                print_success("Storage Facility is running")
                print_info(f"  - Total Entries: {status.get('total_entries', 0)}")
                print_info(f"  - Units: {status.get('units_count', 0)}")
                self.results['apis']['storage_facility'] = status
                return True
            else:
                print_warning(f"Storage Facility status: {response.status_code}")
                self.results['apis']['storage_facility'] = 'unhealthy'
                return False
        except requests.exceptions.ConnectionError:
            print_warning("Storage Facility not running on port 3003")
            self.results['apis']['storage_facility'] = 'not_running'
            return False
        except Exception as e:
            print_error(f"Storage Facility verification failed: {str(e)}")
            self.results['apis']['storage_facility'] = 'error'
            return False

    def verify_features(self):
        print_header("FEATURES VERIFICATION")
        
        if not self.test_token:
            print_warning("Skipping feature tests - no authentication token")
            return False
        
        backend_url = "http://localhost:3000"
        headers = {"Authorization": f"Bearer {self.test_token}"}
        
        features = {
            'bitxtractor': '/api/bitxtractor/status/test',
            'blackarch': '/api/blackarch/execute/nmap',
            'knowledge_search': '/api/kb/search',
        }
        
        for feature, endpoint in features.items():
            try:
                if 'search' in endpoint:
                    response = requests.post(
                        f"{backend_url}{endpoint}",
                        json={"query": "test"},
                        headers=headers,
                        timeout=5
                    )
                else:
                    response = requests.get(f"{backend_url}{endpoint}", headers=headers, timeout=5)
                
                if response.status_code in [200, 201, 400, 403]:
                    print_success(f"{feature}: Endpoint accessible")
                    self.results['features'][feature] = 'accessible'
                else:
                    print_warning(f"{feature}: {response.status_code}")
                    self.results['features'][feature] = f'status_{response.status_code}'
            except Exception as e:
                print_warning(f"{feature}: {str(e)}")
                self.results['features'][feature] = 'error'

    def generate_report(self):
        print_header("SYSTEM VERIFICATION REPORT")
        
        report = {
            'timestamp': self.results['timestamp'],
            'summary': {
                'database': self.results['database'].get('status', 'unknown'),
                'backend': self.results['backend'].get('health', {}).get('ok', False),
                'frontend': self.results['frontend'].get('status', 'unknown'),
                'apis': {
                    'knowledge': self.results['apis'].get('knowledge_api', 'unknown'),
                    'droid': self.results['apis'].get('droid_api', 'unknown'),
                    'storage': self.results['apis'].get('storage_facility', 'unknown'),
                }
            },
            'details': self.results
        }
        
        print(json.dumps(report, indent=2))
        
        # Save report
        report_file = "SYSTEM_VERIFICATION_REPORT.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        print_success(f"Report saved to {report_file}")

    def run_all_checks(self):
        print(f"\n{Colors.BOLD}{Colors.BLUE}R3ÆLƎR AI - SYSTEM VERIFICATION{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.BLUE}Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.RESET}\n")
        
        checks = [
            ("Database", self.verify_database),
            ("Backend", self.verify_backend),
            ("Authentication", self.verify_authentication),
            ("Frontend", self.verify_frontend),
            ("API Endpoints", self.verify_api_endpoints),
            ("Knowledge API", self.verify_knowledge_api),
            ("Droid API", self.verify_droid_api),
            ("Storage Facility", self.verify_storage_facility),
            ("Features", self.verify_features),
        ]
        
        passed = 0
        failed = 0
        
        for name, check in checks:
            try:
                if check():
                    passed += 1
                else:
                    failed += 1
            except Exception as e:
                print_error(f"{name} check failed with exception: {str(e)}")
                failed += 1
        
        print_header("VERIFICATION SUMMARY")
        print_success(f"Passed: {passed}/{len(checks)}")
        if failed > 0:
            print_error(f"Failed: {failed}/{len(checks)}")
        
        self.generate_report()
        
        return failed == 0

if __name__ == "__main__":
    verifier = SystemVerification()
    success = verifier.run_all_checks()
    sys.exit(0 if success else 1)
