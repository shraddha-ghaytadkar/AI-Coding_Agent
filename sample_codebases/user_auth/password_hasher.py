"""
Password hashing utility module using standard hashlib.
"""
import hashlib
import os


class PasswordHasher:
    @staticmethod
    def hash_password(password: str) -> str:
        """Create a salted SHA256 hash of a password."""
        salt = os.urandom(16).hex()
        hashed = hashlib.sha256((salt + password).encode('utf-8')).hexdigest()
        return f"{salt}${hashed}"

    @staticmethod
    def verify_password(stored_hash: str, password_attempt: str) -> bool:
        """Verify password attempt against stored salt$hash string."""
        try:
            salt, original_hash = stored_hash.split('$', 1)
            attempt_hash = hashlib.sha256((salt + password_attempt).encode('utf-8')).hexdigest()
            return attempt_hash == original_hash
        except Exception:
            return False
