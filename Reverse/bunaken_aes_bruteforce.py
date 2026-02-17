from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import hashlib
import base64
# Read the encrypted flag file
with open('flag.txt.bunakencrypted', 'r') as f:
    encrypted_b64 = f.read().strip()
# Decode from base64
encrypted = base64.b64decode(encrypted_b64)
# Extract IV and ciphertext
iv = encrypted[:16] # First 16 bytes = IV
ciphertext = encrypted[16:] # Rest = encrypted data
print(f'Encrypted file length: {len(encrypted)} bytes')
print(f'IV: {iv.hex()}')
print(f'Ciphertext length: {len(ciphertext)} bytes\n')
# Wordlist based on challenge theme
possible_keys = [
    'bunaken',
    'indonesia',
    'manado',
    'sulawesi'
]
# Try each key
for key_string in possible_keys:
    try:
        # Derive key: SHA-256 hash truncated to 16 bytes
        key_hash = hashlib.sha256(key_string.encode()).digest()
        key = key_hash[:16]
       
        # Decrypt with AES-128-CBC
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted = cipher.decrypt(ciphertext)
        decrypted_unpadded = unpad(decrypted, 16)
       
        result = decrypted_unpadded.decode('utf-8', errors='ignore')
       
        print(f'[*] Trying key: "{key_string}"')
        print(f' Result: {result}\n')
       
        # Check if flag format found
        if 'C2C{' in result or 'flag{' in result:
            print('✓✓✓ FLAG FOUND! ✓✓✓')
            print(f'Key: "{key_string}"')
            print(f'Flag: {result.strip()}')
            break
           
    except Exception as e:
        print(f'[X] Key "{key_string}" failed: {e}\n')
