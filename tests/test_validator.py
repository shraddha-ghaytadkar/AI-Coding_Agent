"""
Unit tests for SubprocessValidator.
"""
import os
import unittest
from services.validator import SubprocessValidator


class TestSubprocessValidator(unittest.TestCase):
    def setUp(self):
        self.validator = SubprocessValidator(timeout_seconds=15)
        self.sample_dir = os.path.join(os.path.dirname(__file__), "..", "sample_codebases", "task_tracker")

    def test_validation_passes_on_unmodified_sample_codebase(self):
        # Passing empty modifications tests the baseline test suite
        result = self.validator.validate(self.sample_dir, modified_files={})
        self.assertTrue(result.passed, f"Validation failed with log: {result.output_log}")
        self.assertGreaterEqual(result.total_tests, 1)
        self.assertEqual(result.failed_tests, 0)


if __name__ == "__main__":
    unittest.main()
