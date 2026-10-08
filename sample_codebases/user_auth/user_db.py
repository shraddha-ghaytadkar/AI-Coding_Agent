"""
User database model & storage layer.
"""
from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class UserRecord:
    username: str
    password_hash: str
    email: str
    role: str = "user"
    failed_login_attempts: int = 0
    is_locked: bool = False


class UserDB:
    def __init__(self):
        self._users: Dict[str, UserRecord] = {}

    def add_user(self, username: str, password_hash: str, email: str, role: str = "user") -> UserRecord:
        key = username.lower()
        if key in self._users:
            raise ValueError(f"User '{username}' already exists")
        record = UserRecord(username=username, password_hash=password_hash, email=email, role=role)
        self._users[key] = record
        return record

    def get_user(self, username: str) -> Optional[UserRecord]:
        return self._users.get(username.lower())
