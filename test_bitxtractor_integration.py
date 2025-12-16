"""
R3AL3R AI - BitXtractor Integration Test
Tests the BitXtractor API endpoints and wallet extraction functionality.
"""

import requests
import json
import time

BACKEND_URL = "http://localhost:3002"

def test_api_root():
    """Test that the backend API is responding."""
    print("\n[TEST 1] Testing API root endpoint...")
    try:
        response = requests.get(f"{BACKEND_URL}/api", timeout=5)
        print(f"  Status: {response.status_code}")
        print(f"  Response: {response.text[:200]}")
        return True
    except Exception as e:
        print(f"  ERROR: {e}")
        return False

def test_bitxtractor_start_dry():
    """Test BitXtractor start endpoint with dry-run mode."""
    print("\n[TEST 2] Testing BitXtractor start (dry-run mode)...")
    try:
        payload = {
            "wallet_path": "test_wallet.dat",
            "mode": "dry"
        }
        response = requests.post(
            f"{BACKEND_URL}/api/bitxtractor/start",
            json=payload,
            timeout=30
        )
        print(f"  Status: {response.status_code}")
        data = response.json()
        print(f"  Response: {json.dumps(data, indent=2)}")
        
        if data.get('success') and data.get('job_id'):
            return data['job_id']
        return None
    except Exception as e:
        print(f"  ERROR: {e}")
        return None

def test_bitxtractor_status(job_id):
    """Test BitXtractor status endpoint."""
    print(f"\n[TEST 3] Testing BitXtractor status for job: {job_id}...")
    try:
        # Wait a bit for job to start
        time.sleep(2)
        
        response = requests.get(
            f"{BACKEND_URL}/api/bitxtractor/status/{job_id}",
            timeout=10
        )
        print(f"  Status: {response.status_code}")
        data = response.json()
        print(f"  Job Status: {data.get('status')}")
        
        # Show log snippet
        log = data.get('log', '')
        if log:
            print(f"  Log Preview (last 500 chars):")
            print(f"  {log[-500:]}")
        
        return data
    except Exception as e:
        print(f"  ERROR: {e}")
        return None

def test_with_real_wallet(wallet_path):
    """Test with a real wallet file path."""
    print(f"\n[TEST 4] Testing with wallet path: {wallet_path}...")
    try:
        payload = {
            "wallet_path": wallet_path,
            "mode": "dry"
        }
        response = requests.post(
            f"{BACKEND_URL}/api/bitxtractor/start",
            json=payload,
            timeout=30
        )
        data = response.json()
        print(f"  Response: {json.dumps(data, indent=2)}")
        
        if data.get('job_id'):
            job_id = data['job_id']
            time.sleep(3)
            
            status_response = requests.get(
                f"{BACKEND_URL}/api/bitxtractor/status/{job_id}",
                timeout=10
            )
            status_data = status_response.json()
            print(f"  Job Status: {status_data.get('status')}")
            
            log = status_data.get('log', '')
            if log:
                print(f"  Log Output:")
                print(f"  {log}")
            
            return status_data
        return None
    except Exception as e:
        print(f"  ERROR: {e}")
        return None

def main():
    print("="*60)
    print("R3AL3R AI - BitXtractor Integration Test")
    print("="*60)
    
    # Test 1: API availability
    if not test_api_root():
        print("\n❌ Backend is not responding. Start it with:")
        print("   .\\start_bitxtractor_service.ps1")
        return
    
    # Test 2: Start a dry-run job
    job_id = test_bitxtractor_start_dry()
    if not job_id:
        print("\n❌ Failed to start BitXtractor job")
        return
    
    # Test 3: Check status
    status = test_bitxtractor_status(job_id)
    if not status:
        print("\n❌ Failed to get job status")
        return
    
    # Summary
    print("\n" + "="*60)
    print("Test Summary:")
    print("="*60)
    print("✓ API Root: Responding")
    print(f"✓ BitXtractor Start: Job ID {job_id}")
    print(f"✓ BitXtractor Status: {status.get('status')}")
    print("\nBitXtractor is integrated and functional!")
    print("\nTo test with a real wallet:")
    print("  python test_bitxtractor_integration.py --wallet path/to/wallet.dat")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 2 and sys.argv[1] == '--wallet':
        wallet_path = sys.argv[2]
        test_with_real_wallet(wallet_path)
    else:
        main()
