"""
Task Manager Service handling core business logic.
"""
from datetime import datetime
from typing import List, Optional
from models import Task
from utils import generate_task_id, validate_task_title


class TaskManager:
    def __init__(self):
        self._tasks: dict[str, Task] = {}

    def create_task(self, title: str, description: str = "", priority: str = "medium") -> Task:
        if not validate_task_title(title):
            raise ValueError("Invalid task title provided")
        
        task_id = generate_task_id()
        task = Task(
            id=task_id,
            title=title.strip(),
            description=description,
            priority=priority.lower()
        )
        self._tasks[task_id] = task
        return task

    def get_task(self, task_id: str) -> Optional[Task]:
        return self._tasks.get(task_id)

    def mark_complete(self, task_id: str) -> bool:
        task = self._tasks.get(task_id)
        if not task:
            return False
        task.completed = True
        task.completed_at = datetime.now()
        return True

    def list_tasks(self, completed_only: Optional[bool] = None) -> List[Task]:
        all_tasks = list(self._tasks.values())
        if completed_only is None:
            return all_tasks
        return [t for t in all_tasks if t.completed == completed_only]

    def delete_task(self, task_id: str) -> bool:
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False
