import hashlib
import binascii
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base58

# Common passwords to try
common_passwords = [
    '', 'password', '123456', 'bitcoin', 'wallet', '123456789', 'qwerty',
    'abc123', 'password123', 'admin', 'letmein', 'welcome', 'monkey',
    '1234567890', 'password1', 'qwerty123', 'test', 'guest', 'default',
    '12345678', 'iloveyou', 'princess', 'dragon', 'sunshine', 'master',
    'computer', 'qwertyuiop', 'ashley', 'mustang', 'baseball', 'football',
    'michael', 'jennifer', 'jordan', 'superman', 'trustno1', 'jessica',
    'pepper', 'zaq1zaq1', 'qazwsx', 'fuckyou', 'liverpool', 'whatever'
]

def derive_key(password, salt, iterations=10000):
    '''Derive encryption key from password using PBKDF2'''
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

def decrypt_aes(key, encrypted_data, iv):
    '''Decrypt AES-256-CBC data'''
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted = decryptor.update(encrypted_data) + decryptor.finalize()
    return decrypted

def try_decrypt_wallet_data(password, encrypted_key_data):
    '''Try to decrypt wallet key data with a password'''
    try:
        # Extract salt and encrypted data (this is a simplified version)
        # In real Bitcoin Core wallets, the format is more complex
        # This is just a basic attempt
        if len(encrypted_key_data) < 32:
            return False

        # Try different salt positions (simplified approach)
        for salt_start in [0, 16]:
            if salt_start + 32 > len(encrypted_key_data):
                continue

            salt = encrypted_key_data[salt_start:salt_start+16]
            encrypted = encrypted_key_data[salt_start+16:salt_start+48]

            if len(encrypted) < 16:
                continue

            key = derive_key(password, salt)
            iv = encrypted[:16]  # First 16 bytes as IV
            data_to_decrypt = encrypted[16:]

            try:
                decrypted = decrypt_aes(key, data_to_decrypt, iv)
                # Check if decrypted data looks like a private key (starts with 0x80)
                if decrypted and len(decrypted) >= 32 and decrypted[0] == 0x80:
                    return decrypted
            except:
                continue

    except Exception as e:
        pass
    return False

# Sample encrypted key data from our earlier extraction
# This is the data after 'ckey!' - let's try with the first one
sample_encrypted = binascii.unhexlify('2102c35419a26553ac2b0320968b4c957d845987e48f952cf35401de345d302b')

print('Trying common passwords on sample encrypted key...')
print(f'Encrypted data: {sample_encrypted.hex()}')
print()

success = False
for password in common_passwords:
    result = try_decrypt_wallet_data(password, sample_encrypted)
    if result:
        print(f'✅ SUCCESS with password: "{password}"')
        print(f'Decrypted data: {result.hex()}')

        # Try to convert to WIF
        try:
            # Add compression flag and checksum
            extended = result + b'\x01'  # Compressed key
            sha = hashlib.sha256(extended).digest()
            sha2 = hashlib.sha256(sha).digest()
            checksum = sha2[:4]
            wif_data = extended + checksum
            wif = base58.b58encode(wif_data).decode()
            print(f'WIF: {wif}')
        except Exception as e:
            print(f'Could not convert to WIF: {e}')
        success = True
        break
    else:
        print(f'❌ Failed: {password}')

if not success:
    print('\nNo common passwords worked. The wallet likely uses a strong or custom password.')
    print('Consider using BTCRecover with a larger wordlist or brute force approach.')