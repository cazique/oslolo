
# src/oslolo/core/crypto/encryption.py
# Placeholder for future encryption implementation using 'cryptography' library.
# This would be integrated into format handlers that support encryption.

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

class Encryptor:
    def __init__(self, key: bytes):
        """Initializes with a 256-bit (32-byte) key."""
        if len(key) != 32:
            raise ValueError("Key must be 32 bytes for AES-256.")
        self.aesgcm = AESGCM(key)
        
    def encrypt(self, data: bytes, associated_data: bytes = None) -> bytes:
        """Encrypts data. Returns nonce + ciphertext + tag."""
        import os
        nonce = os.urandom(12)  # GCM standard nonce size
        ciphertext = self.aesgcm.encrypt(nonce, data, associated_data)
        return nonce + ciphertext
        
    def decrypt(self, encrypted_data: bytes, associated_data: bytes = None) -> bytes:
        """Decrypts data. Assumes nonce is prepended."""
        nonce = encrypted_data[:12]
        ciphertext = encrypted_data[12:]
        return self.aesgcm.decrypt(nonce, ciphertext, associated_data)
