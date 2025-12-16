#!/usr/bin/env python3
"""
Test BitXtractor Wallet Analyzer API Integration
Tests the new /api/bitxtractor/analyze endpoint
"""

import requests
import json
import tempfile
import os

# API configuration
BACKEND_URL = "http://localhost:3002"  # BitXtractor service port
ANALYZE_ENDPOINT = f"{BACKEND_URL}/api/bitxtractor/analyze"


def create_test_wallet():
    """Create a test wallet file for analysis."""
    # Create a test file that mimics an encrypted wallet
    test_data = b'\x00\x06\x15\x61' + b'\x00' * 16 + b'\x10\x00'  # Berkeley DB header
    test_data += os.urandom(4000)  # Random encrypted-like data
    
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.dat')
    temp_file.write(test_data)
    temp_file.close()
    return temp_file.name


def test_wallet_analysis():
    """Test the wallet analysis endpoint."""
    print("=" * 70)
    print("BitXtractor Wallet Analyzer API Test")
    print("=" * 70)
    
    # Create test wallet
    print("\n[1/3] Creating test wallet file...")
    wallet_path = create_test_wallet()
    print(f"✅ Test wallet created: {wallet_path}")
    
    try:
        # Test wallet analysis
        print("\n[2/3] Sending analysis request to BitXtractor API...")
        response = requests.post(
            ANALYZE_ENDPOINT,
            json={'wallet_path': wallet_path},
            timeout=30
        )
        
        print(f"Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            
            if result.get('success'):
                print("✅ Analysis successful!\n")
                
                # Display analysis results
                analysis = result.get('analysis', {})
                
                print("-" * 70)
                print("ANALYSIS RESULTS:")
                print("-" * 70)
                print(f"File: {analysis.get('file_path')}")
                print(f"Size: {analysis.get('file_size'):,} bytes")
                print(f"Format: {analysis.get('file_format')}")
                
                print("\nEntropy Analysis:")
                entropy = analysis.get('entropy', {})
                print(f"  Shannon Entropy: {entropy.get('value')} / {entropy.get('max_possible')}")
                print(f"  Assessment: {entropy.get('interpretation')}")
                
                print("\nByte Distribution:")
                dist = analysis.get('byte_distribution', {})
                for key, value in dist.items():
                    print(f"  {key}: {value}")
                
                print("\nRandomness Test:")
                rand = analysis.get('randomness_test', {})
                print(f"  Chi-Square: {rand.get('chi_square_value')}")
                print(f"  Result: {rand.get('interpretation')}")
                
                print("\nEncryption Analysis:")
                enc = analysis.get('encryption_analysis', {})
                print(f"  Metadata Detected: {enc.get('has_encryption_metadata')}")
                if enc.get('evidence'):
                    print("  Evidence:")
                    for evidence in enc['evidence']:
                        print(f"    • {evidence}")
                print(f"  Possible Cipher: {enc.get('possible_cipher')}")
                
                print("\nOverall Assessment:")
                print(f"  {analysis.get('likely_encrypted')}")
                
                print("\n" + "=" * 70)
                print("✅ TEST PASSED - API Integration Working!")
                print("=" * 70)
                
            else:
                print(f"❌ Analysis failed: {result.get('error')}")
        else:
            print(f"❌ Request failed with status {response.status_code}")
            print(f"Response: {response.text}")
    
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Cannot connect to BitXtractor API")
        print(f"   Make sure the backend is running on {BACKEND_URL}")
        print("   Start it with: python application/Backend/app.py")
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Cleanup
        print("\n[3/3] Cleaning up test files...")
        try:
            os.unlink(wallet_path)
            print("✅ Test files removed")
        except:
            pass


def test_missing_wallet_path():
    """Test error handling when wallet_path is missing."""
    print("\n" + "=" * 70)
    print("Testing Error Handling (Missing wallet_path)")
    print("=" * 70)
    
    try:
        response = requests.post(
            ANALYZE_ENDPOINT,
            json={},  # No wallet_path
            timeout=10
        )
        
        if response.status_code == 400:
            result = response.json()
            if 'wallet_path required' in result.get('error', ''):
                print("✅ Properly handles missing wallet_path")
            else:
                print(f"⚠️  Unexpected error message: {result.get('error')}")
        else:
            print(f"⚠️  Unexpected status code: {response.status_code}")
    
    except Exception as e:
        print(f"❌ ERROR: {e}")


def test_invalid_wallet_path():
    """Test error handling with invalid wallet path."""
    print("\n" + "=" * 70)
    print("Testing Error Handling (Invalid wallet_path)")
    print("=" * 70)
    
    try:
        response = requests.post(
            ANALYZE_ENDPOINT,
            json={'wallet_path': '/nonexistent/wallet.dat'},
            timeout=10
        )
        
        result = response.json()
        if not result.get('success'):
            print(f"✅ Properly handles invalid path: {result.get('error')}")
        else:
            print("⚠️  Should have failed for nonexistent file")
    
    except Exception as e:
        print(f"❌ ERROR: {e}")


if __name__ == '__main__':
    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "BitXtractor Wallet Analyzer Test Suite" + " " * 14 + "║")
    print("╚" + "═" * 68 + "╝")
    print("\n")
    
    # Run tests
    test_wallet_analysis()
    test_missing_wallet_path()
    test_invalid_wallet_path()
    
    print("\n" + "=" * 70)
    print("All tests completed!")
    print("=" * 70 + "\n")
