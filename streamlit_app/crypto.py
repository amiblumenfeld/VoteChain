"""
Cryptographic utilities for the Secure Voting System.

This module provides RSA key generation, blind signatures, and related
cryptographic operations needed for the voting system.
"""

from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256, SHA512
from Crypto.Random import random
import os
from typing import Tuple, Optional


def generate_rsa_keys(key_size: int = 2048) -> Tuple[RSA.RsaKey, RSA.RsaKey]:
    """
    Generate RSA public and private key pair.
    
    Args:
        key_size: Size of RSA key in bits (default 2048)
        
    Returns:
        Tuple of (private_key, public_key)
    """
    key = RSA.generate(key_size)
    return key, key.publickey()


def sign_message(message: str, private_key: RSA.RsaKey) -> str:
    """
    Sign a message using RSA private key (PKCS1 v1.5).
    
    Args:
        message: Plain text message to sign
        private_key: RSA private key
        
    Returns:
        Hex-encoded signature string
    """
    hash_obj = SHA256.new(message.encode('utf-8'))
    signer = PKCS1_v1_5.new(private_key)
    signature = signer.sign(hash_obj)
    return signature.hex()


def verify_signature(message: str, signature_hex: str, public_key: RSA.RsaKey) -> bool:
    """
    Verify a message signature using RSA public key.
    
    Args:
        message: Plain text message
        signature_hex: Hex-encoded signature
        public_key: RSA public key
        
    Returns:
        True if signature is valid, False otherwise
    """
    try:
        hash_obj = SHA256.new(message.encode('utf-8'))
        verifier = PKCS1_v1_5.new(public_key)
        signature = bytes.fromhex(signature_hex)
        return verifier.verify(hash_obj, signature)
    except Exception:
        return False


def blind_message(message: str, public_key: RSA.RsaKey) -> Tuple[str, str]:
    """
    Blind a message using RSA blinding for blind signatures.
    
    Args:
        message: Plain text message to blind
        public_key: RSA public key (for blinding)
        
    Returns:
        Tuple of (blinded_message_hex, blinding_factor_hex)
    """
    message_int = int.from_bytes(SHA256.new(message.encode('utf-8')).digest(), 'big')
    
    # Generate random blinding factor
    blinding_factor = random.randint(2, public_key.n - 1)
    
    # Blind message: m' = m * r^e mod n
    blinded_message = (message_int * pow(blinding_factor, public_key.e, public_key.n)) % public_key.n
    
    return hex(blinded_message)[2:], hex(blinding_factor)[2:]


def unblind_signature(signature_hex: str, blinding_factor_hex: str, 
                     public_key: RSA.RsaKey) -> str:
    """
    Unblind a blinded signature to reveal the actual signature.
    
    Args:
        signature_hex: Hex-encoded blinded signature
        blinding_factor_hex: Hex-encoded blinding factor used in blinding
        public_key: RSA public key (inverse needed)
        
    Returns:
        Hex-encoded unblinded signature
    """
    signature_int = int(signature_hex, 16)
    blinding_factor = int(blinding_factor_hex, 16)
    
    # Compute modular inverse of blinding factor: r^-1 mod n
    blinding_factor_inv = pow(blinding_factor, -1, public_key.n)
    
    # Unblind: S = S' * r^-1 mod n
    unblinded_sig = (signature_int * blinding_factor_inv) % public_key.n
    
    return hex(unblinded_sig)[2:]


def sign_blinded_message(blinded_message_hex: str, private_key: RSA.RsaKey) -> str:
    """
    Sign a blinded message using RSA private key.
    
    Args:
        blinded_message_hex: Hex-encoded blinded message
        private_key: RSA private key
        
    Returns:
        Hex-encoded signature of blinded message
    """
    blinded_int = int(blinded_message_hex, 16)
    
    # Sign: S' = m'^d mod n
    signature = pow(blinded_int, private_key.d, private_key.n)
    
    return hex(signature)[2:]


def export_key_to_file(key: RSA.RsaKey, filepath: str) -> None:
    """
    Export RSA key to PEM file.
    
    Args:
        key: RSA key object
        filepath: Path to save the key file
    """
    with open(filepath, 'wb') as f:
        f.write(key.export_key())


def import_key_from_file(filepath: str) -> Optional[RSA.RsaKey]:
    """
    Import RSA key from PEM file.
    
    Args:
        filepath: Path to PEM key file
        
    Returns:
        RSA key object or None if import fails
    """
    try:
        with open(filepath, 'rb') as f:
            key = RSA.import_key(f.read())
            return key
    except Exception:
        return None


def import_key_from_bytes(key_bytes: bytes) -> Optional[RSA.RsaKey]:
    """
    Import RSA key from bytes.
    
    Args:
        key_bytes: PEM-encoded key bytes
        
    Returns:
        RSA key object or None if import fails
    """
    try:
        key = RSA.import_key(key_bytes)
        return key
    except Exception:
        return None


def hash_message(message: str) -> str:
    """
    Generate SHA256 hash of a message.
    
    Args:
        message: Message to hash
        
    Returns:
        Hex-encoded hash string (truncated to first 12 chars for display)
    """
    hash_obj = SHA256.new(message.encode('utf-8'))
    return hash_obj.hexdigest()


def truncate_hash(hash_str: str, length: int = 12) -> str:
    """
    Truncate hash for display purposes.
    
    Args:
        hash_str: Full hash string
        length: Number of characters to keep
        
    Returns:
        Truncated hash string with ellipsis (e.g., "a7f3b2...c9d1")
    """
    if len(hash_str) <= length:
        return hash_str
    return f"{hash_str[:length//2]}...{hash_str[-length//2:]}"
