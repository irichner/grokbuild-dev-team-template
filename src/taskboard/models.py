"""Task domain models.

A Task may carry zero or more free-form tags (lowercase strings after
normalization). Tags are stored as a per-task ``set[str]`` so mutations
never share state across tasks.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from uuid import uuid4


class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


@dataclass
class Task:
    title: str
    description: str = ""
    status: TaskStatus = TaskStatus.TODO
    priority: int = 0  # higher = more urgent; clamped by board policy
    id: str = field(default_factory=lambda: str(uuid4()))
    tags: set[str] = field(default_factory=set)

    def __post_init__(self) -> None:
        if not self.title or not self.title.strip():
            raise ValueError("title must be a non-empty string")
        self.title = self.title.strip()
        # Defensive copy so callers cannot share mutable tag sets across tasks.
        self.tags = set(self.tags)
