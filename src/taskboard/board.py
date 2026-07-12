"""In-memory task board.

Public tag API (in addition to core task CRUD):

- ``add(..., tags=None)`` — optional iterable of tags (normalized + deduped)
- ``add_tag(task_id, tag)`` / ``remove_tag(task_id, tag)`` — mutate membership
  (``remove_tag`` is a no-op when the normalized tag is not present)
- ``list(status=None, tag=None)`` — optional filters; both compose as intersection
"""

from __future__ import annotations

from collections.abc import Iterable

from taskboard.models import Task, TaskStatus
from taskboard.util import clamp, normalize_tag


class TaskBoard:
    """Simple task collection with priority clamping, status transitions, and tags."""

    PRIORITY_MIN = 0
    PRIORITY_MAX = 10

    def __init__(self) -> None:
        self._tasks: dict[str, Task] = {}

    def add(
        self,
        title: str,
        description: str = "",
        priority: int = 0,
        tags: Iterable[str] | None = None,
    ) -> Task:
        p = int(clamp(priority, self.PRIORITY_MIN, self.PRIORITY_MAX))
        normalized: set[str] = set()
        if tags is not None:
            for raw in tags:
                normalized.add(normalize_tag(raw))
        task = Task(title=title, description=description, priority=p, tags=normalized)
        self._tasks[task.id] = task
        return task

    def get(self, task_id: str) -> Task | None:
        return self._tasks.get(task_id)

    def list(
        self,
        status: TaskStatus | None = None,
        tag: str | None = None,
    ) -> list[Task]:
        tasks = list(self._tasks.values())
        if status is not None:
            tasks = [t for t in tasks if t.status == status]
        if tag is not None:
            needle = normalize_tag(tag)
            tasks = [t for t in tasks if needle in t.tags]
        return sorted(tasks, key=lambda t: (-t.priority, t.title))

    def add_tag(self, task_id: str, tag: str) -> Task:
        task = self._require(task_id)
        task.tags.add(normalize_tag(tag))
        return task

    def remove_tag(self, task_id: str, tag: str) -> Task:
        """Remove *tag* from the task. Missing tag is a no-op after normalization."""
        task = self._require(task_id)
        task.tags.discard(normalize_tag(tag))
        return task

    def set_status(self, task_id: str, status: TaskStatus) -> Task:
        task = self._require(task_id)
        task.status = status
        return task

    def set_priority(self, task_id: str, priority: int) -> Task:
        task = self._require(task_id)
        task.priority = int(clamp(priority, self.PRIORITY_MIN, self.PRIORITY_MAX))
        return task

    def remove(self, task_id: str) -> None:
        if task_id not in self._tasks:
            raise KeyError(f"unknown task id: {task_id}")
        del self._tasks[task_id]

    def count(self) -> int:
        return len(self._tasks)

    def _require(self, task_id: str) -> Task:
        task = self._tasks.get(task_id)
        if task is None:
            raise KeyError(f"unknown task id: {task_id}")
        return task
