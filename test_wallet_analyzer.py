#!/usr/bin/env python3
"""
Test suite for the enhanced wallet analyzer.
Creates test files with known characteristics to verify analysis accuracy.
"""

import os
import tempfile
from wallet_analyzer_enhanced import WalletAnalyzer


def create_test_encrypted_file():
    """Create a test file that mimics encrypted data."""
    test_data = os.urandom(4096)  # Random data simulates encryption
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.dat')
    temp_file.write(test_data)
    temp_file.close()
    return temp_file.name


def create_test_plaintext_file():
    """Create a test file with plaintext data."""
    test_data = b"This is plaintext wallet data. " * 100
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.dat')
    temp_file.write(test_data)
    temp_file.close()
    return temp_file.name


def create_test_berkeley_db_file():
    """Create a test file with Berkeley DB magic bytes."""
    # Berkeley DB header
    bdb_header = b'\x00\x06\x15\x61' + b'\x00' * 16 + b'\x10\x00'  # Page size 4096
    test_data = bdb_header + os.urandom(4000)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.dat')
    temp_file.write(test_data)
    temp_file.close()
    return temp_file.name


def create_test_aes_encrypted_file():
    """Create a test file that mimics AES encrypted data with PKCS padding."""
    # 1024 bytes of random data (simulating encrypted content)
    encrypted_data = os.urandom(1008)
    # Add PKCS#7 padding (16-byte padding for AES)
    padding = b'\x10' * 16
    test_data = encrypted_data + padding
    
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.dat')
    temp_file.write(test_data)
    temp_file.close()
    return temp_file.name


def run_tests():
    """Run all tests and print results."""
    print("=" * 70)
    print("WALLET ANALYZER - TEST SUITE")
    print("=" * 70)
    
    test_files = []
    
    try:
        # Test 1: Encrypted-like file
        print("\n\nTEST 1: Random/Encrypted Data")
        print("-" * 70)
        encrypted_file = create_test_encrypted_file()
        test_files.append(encrypted_file)
        analyzer = WalletAnalyzer(encrypted_file)
        results = analyzer.analyze()
        analyzer.print_report(results)
        
        # Verify high entropy
        assert results['entropy']['value'] > 7.5, "Encrypted file should have high entropy"
        print("✅ Test 1 PASSED: High entropy detected for random data")
        
        # Test 2: Plaintext file
        print("\n\nTEST 2: Plaintext Data")
        print("-" * 70)
        plaintext_file = create_test_plaintext_file()
        test_files.append(plaintext_file)
        analyzer = WalletAnalyzer(plaintext_file)
        results = analyzer.analyze()
        analyzer.print_report(results)
        
        # Verify low entropy
        assert results['entropy']['value'] < 5.0, "Plaintext file should have low entropy"
        print("✅ Test 2 PASSED: Low entropy detected for plaintext data")
        
        # Test 3: Berkeley DB file
        print("\n\nTEST 3: Berkeley DB Format")
        print("-" * 70)
        bdb_file = create_test_berkeley_db_file()
        test_files.append(bdb_file)
        analyzer = WalletAnalyzer(bdb_file)
        results = analyzer.analyze()
        analyzer.print_report(results)
        
        # Verify format detection
        assert 'Berkeley DB' in results['file_format'], "Should detect Berkeley DB format"
        print("✅ Test 3 PASSED: Berkeley DB format detected")
        
        # Test 4: AES encrypted with padding
        print("\n\nTEST 4: AES Encrypted (with PKCS padding)")
        print("-" * 70)
        aes_file = create_test_aes_encrypted_file()
        test_files.append(aes_file)
        analyzer = WalletAnalyzer(aes_file)
        results = analyzer.analyze()
        analyzer.print_report(results)
        
        # Verify padding detection
        evidence = results['encryption_analysis']['evidence']
        has_padding = any('padding' in e.lower() for e in evidence)
        assert has_padding, "Should detect PKCS padding"
        print("✅ Test 4 PASSED: AES padding detected")
        
        print("\n" + "=" * 70)
        print("ALL TESTS PASSED ✅")
        print("=" * 70)
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Cleanup test files
        for file_path in test_files:
            try:
                os.unlink(file_path)
            except:
                pass


if __name__ == '__main__':
    run_tests()
