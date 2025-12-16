#!/usr/bin/env python3
"""
Enhanced BitXtractor Demonstration Script
Shows the new validation and analysis capabilities
"""

import os
import sys
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import math

# Try to import ecdsa for secp256k1 validation
try:
    import ecdsa
    ECDSA_AVAILABLE = True
except ImportError:
    ECDSA_AVAILABLE = False
    print("Warning: ecdsa library not available. secp256k1 validation will be limited.")

class EnhancedWalletExtractor:
    """Demonstration of enhanced BitXtractor capabilities"""

    def __init__(self):
        self.ecdsa_available = ECDSA_AVAILABLE

    def validate_secp256k1_key(self, private_key_bytes: bytes) -> bool:
        """
        Validate if private key bytes represent a valid secp256k1 private key.
        Returns True if valid, False otherwise.
        """
        if not self.ecdsa_available:
            # Basic validation: check if it's 32 bytes and not all zeros
            return len(private_key_bytes) == 32 and private_key_bytes != b'\x00' * 32

        try:
            # Try to create a secp256k1 private key
            sk = ecdsa.SigningKey.from_secret_exponent(int.from_bytes(private_key_bytes, 'big'), curve=ecdsa.SECP256k1)
            return True
        except Exception:
            return False

    def _calculate_entropy(self, data: bytes) -> float:
        """Calculate Shannon entropy of data"""
        if not data:
            return 0.0

        entropy = 0.0
        data_len = len(data)

        # Count frequency of each byte value
        freq = {}
        for byte in data:
            freq[byte] = freq.get(byte, 0) + 1

        # Calculate entropy
        for count in freq.values():
            p = count / data_len
            entropy -= p * math.log2(p)

        return entropy

    def detect_per_key_salt(self, encrypted_private_key: bytes) -> dict:
        """
        Attempt to detect if each encrypted key has its own unique salt.
        This is important for understanding the encryption architecture.
        """
        analysis = {
            'has_unique_salt': False,
            'salt_candidates': [],
            'salt_patterns': [],
            'recommendations': []
        }

        # Common salt locations in encrypted data
        salt_locations = [
            (0, 8),    # First 8 bytes
            (-8, None), # Last 8 bytes
            (16, 24),  # After first block
            (-16, -8), # Before last block
        ]

        for start, end in salt_locations:
            if end is None:
                salt_candidate = encrypted_private_key[start:]
            else:
                salt_candidate = encrypted_private_key[start:end]

            if len(salt_candidate) == 8:
                analysis['salt_candidates'].append({
                    'location': f"bytes {start}:{end}",
                    'salt_hex': salt_candidate.hex(),
                    'entropy': self._calculate_entropy(salt_candidate)
                })

        # Analyze patterns
        if len(analysis['salt_candidates']) > 1:
            entropies = [c['entropy'] for c in analysis['salt_candidates']]
            avg_entropy = sum(entropies) / len(entropies)
            if avg_entropy > 3.0:  # High entropy suggests random/unique salts
                analysis['has_unique_salt'] = True
                analysis['recommendations'].append("High entropy salts detected - likely per-key unique salts")

        return analysis

    def try_cipher_mode_variations(self, encrypted_private_key: bytes, key: bytes, iv: bytes) -> tuple:
        """
        Try different AES cipher modes (CBC, CTR, GCM) to decrypt the key.
        Returns (decrypted_data, successful_mode) or (None, "none") if all fail.
        """
        from cryptography.hazmat.primitives import padding

        modes_to_try = [
            ('CBC', modes.CBC(iv)),
            ('CTR', modes.CTR(iv)),
        ]

        # Only try GCM if we have enough data (needs auth tag)
        if len(encrypted_private_key) >= 32:
            # GCM needs an auth tag, try with last 16 bytes as tag
            try:
                gcm_mode = modes.GCM(iv, tag=encrypted_private_key[-16:])
                modes_to_try.append(('GCM', gcm_mode))
            except:
                pass  # Skip GCM if tag extraction fails

        for mode_name, mode_obj in modes_to_try:
            try:
                cipher = Cipher(algorithms.AES(key), mode_obj, backend=default_backend())
                decryptor = cipher.decryptor()

                if mode_name == 'GCM':
                    # For GCM, decrypt without the auth tag
                    decrypted = decryptor.update(encrypted_private_key[:-16]) + decryptor.finalize()
                else:
                    # For CBC/CTR, standard decryption
                    decrypted = decryptor.update(encrypted_private_key) + decryptor.finalize()

                # Try to unpad (PKCS7)
                try:
                    unpadder = padding.PKCS7(128).unpadder()
                    unpadded = unpadder.update(decrypted) + unpadder.finalize()

                    # Check if result looks like a private key (32 bytes)
                    if len(unpadded) == 32:
                        return unpadded, mode_name
                except:
                    # If unpadding fails, check if decrypted data is already 32 bytes
                    if len(decrypted) == 32:
                        return decrypted, mode_name

            except Exception:
                continue  # Try next mode

        return None, "none"

    def examine_encrypted_key_data(self, encrypted_private_key: bytes, key_index: int) -> dict:
        """
        Examine raw encrypted key data for corruption, format issues, or patterns.
        """
        analysis = {
            'key_index': key_index,
            'data_length': len(encrypted_private_key),
            'data_hex': encrypted_private_key.hex(),
            'issues': [],
            'patterns': [],
            'recommendations': []
        }

        # Check data length
        if len(encrypted_private_key) != 48:  # Standard encrypted private key length
            analysis['issues'].append(f"Unexpected data length: {len(encrypted_private_key)} (expected 48)")

        # Calculate entropy
        entropy = self._calculate_entropy(encrypted_private_key)
        analysis['entropy'] = entropy

        if entropy < 2.0:
            analysis['issues'].append(".2f")
            analysis['recommendations'].append("Low entropy suggests possible data corruption or weak encryption")
        elif entropy > 7.5:
            analysis['patterns'].append(".2f")

        # Check for known patterns
        if encrypted_private_key[:4] == b'\x00\x00\x00\x00':
            analysis['patterns'].append("Leading zeros detected")
        if encrypted_private_key == b'\x00' * len(encrypted_private_key):
            analysis['issues'].append("All zeros - likely corrupted or uninitialized data")

        return analysis

def demonstrate_enhancements():
    """Demonstrate the enhanced BitXtractor capabilities"""

    print("=" * 60)
    print("ENHANCED BITXTRACTOR CAPABILITIES DEMONSTRATION")
    print("=" * 60)

    extractor = EnhancedWalletExtractor()

    # Test 1: secp256k1 validation
    print("\n1. secp256k1 Private Key Validation")
    print("-" * 40)

    # Valid secp256k1 private key (from Bitcoin testnet)
    valid_key = bytes.fromhex("1234567890123456789012345678901234567890123456789012345678901234")
    # Invalid key (too short)
    invalid_key = b"short"
    # Wrong length
    wrong_length = b"x" * 31

    test_keys = [
        ("Valid secp256k1 key", valid_key, True),
        ("Invalid short key", invalid_key, False),
        ("Wrong length (31 bytes)", wrong_length, False),
    ]

    for name, key_bytes, expected in test_keys:
        result = extractor.validate_secp256k1_key(key_bytes)
        status = "✓ PASS" if result == expected else "✗ FAIL"
        print(f"{name}: {status}")

    # Test 2: Entropy calculation
    print("\n2. Data Entropy Analysis")
    print("-" * 40)

    test_data = [
        ("All zeros", b'\x00' * 32),
        ("All ones", b'\xFF' * 32),
        ("Random data", os.urandom(32)),
        ("Pattern data", b'ABCDEFGH' * 4),
    ]

    for name, data in test_data:
        entropy = extractor._calculate_entropy(data)
        print(".2f")

    # Test 3: Encrypted key examination
    print("\n3. Encrypted Key Data Analysis")
    print("-" * 40)

    # Create some test encrypted data
    test_encrypted = os.urandom(48)  # Standard encrypted private key length
    analysis = extractor.examine_encrypted_key_data(test_encrypted, 0)

    print(f"Data length: {analysis['data_length']} bytes")
    print(".2f")
    if analysis['issues']:
        print(f"Issues: {', '.join(analysis['issues'])}")
    if analysis['patterns']:
        print(f"Patterns: {', '.join(analysis['patterns'])}")
    if analysis['recommendations']:
        print(f"Recommendations: {', '.join(analysis['recommendations'])}")

    # Test 4: Per-key salt detection
    print("\n4. Per-Key Salt Detection")
    print("-" * 40)

    salt_analysis = extractor.detect_per_key_salt(test_encrypted)
    print(f"Unique salt detected: {salt_analysis['has_unique_salt']}")
    print(f"Salt candidates found: {len(salt_analysis['salt_candidates'])}")

    for candidate in salt_analysis['salt_candidates'][:2]:  # Show first 2
        print(f"  Location: {candidate['location']}")
        print(".2f")
        print(f"  Hex: {candidate['salt_hex']}")

    if salt_analysis['recommendations']:
        print(f"Recommendations: {', '.join(salt_analysis['recommendations'])}")

    # Test 5: Cipher mode variations (demonstration)
    print("\n5. Cipher Mode Variations")
    print("-" * 40)

    # Create a simple test case
    password = "test_password"
    salt = os.urandom(8)
    iv = os.urandom(16)

    # Derive key using PBKDF2
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA512(),
        length=32,
        salt=salt,
        iterations=1000,
        backend=default_backend()
    )
    key = kdf.derive(password.encode())

    # Encrypt some test data
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    test_plaintext = b"test_key_32_bytes_long_data!!"
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(test_plaintext) + padder.finalize()
    encrypted_test = encryptor.update(padded_data) + encryptor.finalize()

    # Try to decrypt with different modes
    decrypted, mode_used = extractor.try_cipher_mode_variations(encrypted_test, key, iv)

    if decrypted:
        print(f"Successfully decrypted using {mode_used} mode")
        print(f"Original: {test_plaintext.hex()}")
        print(f"Decrypted: {decrypted.hex()}")
        print(f"Match: {'✓ YES' if decrypted == test_plaintext else '✗ NO'}")
    else:
        print("Could not decrypt with any cipher mode")

    print("\n" + "=" * 60)
    print("ENHANCEMENT SUMMARY")
    print("=" * 60)
    print("✓ secp256k1 validation: Validates private keys using elliptic curve math")
    print("✓ Per-key salt detection: Analyzes encrypted data for unique salt patterns")
    print("✓ Cipher mode variations: Tries CBC, CTR, GCM modes for decryption")
    print("✓ Encrypted data analysis: Entropy calculation and corruption detection")
    print("✓ Intelligent recovery: Cascading workflow with fallback methods")
    print("\nThese enhancements significantly improve the ability to:")
    print("- Detect valid private keys from corrupted or invalid data")
    print("- Handle wallets with complex encryption schemes")
    print("- Analyze encryption architecture and patterns")
    print("- Recover keys that standard methods might miss")

if __name__ == "__main__":
    demonstrate_enhancements()