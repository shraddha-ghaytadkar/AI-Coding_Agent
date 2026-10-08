"""
Utility functions for Task Tracker application.
"""
import uuid
from typing import List


def generate_task_id() -> str:
    """Generate a unique task ID."""
    return str(uuid.uuid4())[:8]


def validate_task_title(title: str) -> bool:
    """Validate that title is non-empty and within character limits."""
    if not title or not isinstance(title, str):
        return False
    stripped = title.strip()
    return 0 < len(stripped) <= 100


def filter_tasks_by_priority(tasks: List[dict], priority: str) -> List[dict]:
    """Filter task dictionaries by priority string."""
    valid_priorities = {"low", "medium", "high"}
    target_priority = priority.lower()
    if target_priority not in valid_priorities:
        return tasks
    return [t for t in tasks if t.get("priority", "").lower() == target_priority]
