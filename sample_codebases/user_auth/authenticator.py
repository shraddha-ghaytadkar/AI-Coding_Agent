"""
Authentication controller service.
"""
from password_hasher import PasswordHasher
from user_db import UserDB


class Authenticator:
    MAX_FAILED_ATTEMPTS = 3

    def __init__(self, db: UserDB):
        self.db = db

    def register(self, username: str, password: str, email: str, role: str = "user"):
        if len(password) < 6:
            raise ValueError("Password must be at least 6 characters long")
        pw_hash = PasswordHasher.hash_password(password)
        return self.db.add_user(username, pw_hash, email, role)

    def authenticate(self, username: str, password: str) -> bool:
        user = self.db.get_user(username)
        if not user:
            return False

        if user.is_locked:
            raise PermissionError("Account is locked due to excessive failed attempts")

        if PasswordHasher.verify_password(user.password_hash, password):
            user.failed_login_attempts = 0
            return True
        else:
            user.failed_login_attempts += 1
            if user.failed_login_attempts >= self.MAX_FAILED_ATTEMPTS:
                user.is_locked = True
            return False
