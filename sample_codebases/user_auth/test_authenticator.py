"""
Unit tests for User Authentication system.
"""
import unittest
from authenticator import Authenticator
from user_db import UserDB


class TestAuthenticator(unittest.TestCase):
    def setUp(self):
        self.db = UserDB()
        self.auth = Authenticator(self.db)
        self.auth.register("alice", "Secret123", "alice@example.com")

    def test_successful_login(self):
        self.assertTrue(self.auth.authenticate("alice", "Secret123"))

    def test_failed_login(self):
        self.assertFalse(self.auth.authenticate("alice", "WrongPass"))

    def test_account_lockout_after_failed_attempts(self):
        self.assertFalse(self.auth.authenticate("alice", "Wrong1"))
        self.assertFalse(self.auth.authenticate("alice", "Wrong2"))
        self.assertFalse(self.auth.authenticate("alice", "Wrong3"))

        with self.assertRaises(PermissionError):
            self.auth.authenticate("alice", "Secret123")

    def test_short_password_rejection(self):
        with self.assertRaises(ValueError):
            self.auth.register("bob", "123", "bob@example.com")


if __name__ == "__main__":
    unittest.main()
