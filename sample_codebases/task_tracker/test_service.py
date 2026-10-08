"""
Unit tests for Task Tracker Service.
"""
import unittest
from models import Task
from service import TaskManager


class TestTaskManager(unittest.TestCase):
    def setUp(self):
        self.manager = TaskManager()

    def test_create_task_success(self):
        task = self.manager.create_task("Buy Groceries", "Milk, Bread, Eggs", priority="high")
        self.assertIsNotNone(task.id)
        self.assertEqual(task.title, "Buy Groceries")
        self.assertEqual(task.priority, "high")
        self.assertFalse(task.completed)

    def test_create_task_invalid_title(self):
        with self.assertRaises(ValueError):
            self.manager.create_task("")

    def test_mark_complete(self):
        task = self.manager.create_task("Finish Report")
        success = self.manager.mark_complete(task.id)
        self.assertTrue(success)
        self.assertTrue(task.completed)
        self.assertIsNotNone(task.completed_at)

    def test_list_tasks_filter(self):
        t1 = self.manager.create_task("Task 1")
        t2 = self.manager.create_task("Task 2")
        self.manager.mark_complete(t1.id)

        completed_tasks = self.manager.list_tasks(completed_only=True)
        self.assertEqual(len(completed_tasks), 1)
        self.assertEqual(completed_tasks[0].id, t1.id)

    def test_delete_task(self):
        task = self.manager.create_task("Temp Task")
        self.assertTrue(self.manager.delete_task(task.id))
        self.assertIsNone(self.manager.get_task(task.id))


if __name__ == "__main__":
    unittest.main()
