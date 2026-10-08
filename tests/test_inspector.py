"""
Unit tests for CodebaseInspector.
"""
import os
import unittest
from services.inspector import CodebaseInspector


class TestCodebaseInspector(unittest.TestCase):
    def setUp(self):
        self.inspector = CodebaseInspector()
        self.sample_dir = os.path.join(os.path.dirname(__file__), "..", "sample_codebases", "task_tracker")

    def test_scan_codebase_finds_python_files(self):
        file_map = self.inspector.scan_codebase(self.sample_dir)
        self.assertIn("models.py", file_map)
        self.assertIn("service.py", file_map)
        self.assertIn("utils.py", file_map)
        self.assertIn("test_service.py", file_map)

    def test_analyze_ast_extracts_classes_and_functions(self):
        file_map = self.inspector.scan_codebase(self.sample_dir)
        summaries = self.inspector.analyze_ast(file_map)
        
        service_summary = next(s for s in summaries if s.filepath == "service.py")
        self.assertIn("TaskManager", service_summary.classes)
        self.assertTrue(any("create_task" in f for f in service_summary.functions or []))


if __name__ == "__main__":
    unittest.main()
