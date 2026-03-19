import json
import os
from dataclasses import dataclass, field, asdict
from typing import List, Optional

TASKS_FILE = "tasks.json"
SCHEMA_VERSION = 2


@dataclass
class Task:
    id: int
    title: str
    done: bool = False
    priority: int = 2           # 1=high, 2=medium, 3=low
    due_date: Optional[str] = None
    tags: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        return cls(
            id=data["id"],
            title=data["title"],
            done=data.get("done", False),
            priority=data.get("priority", 2),
            due_date=data.get("due_date"),
            tags=data.get("tags", []),
        )


def load_tasks() -> List[Task]:
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as f:
        data = json.load(f)
    # v1 format was a bare list; v2 wraps tasks under a "tasks" key
    if isinstance(data, list):
        raw_tasks = data
    else:
        raw_tasks = data.get("tasks", [])
    return [Task.from_dict(t) for t in raw_tasks]


def save_tasks(tasks: List[Task]) -> None:
    payload = {
        "version": SCHEMA_VERSION,
        "tasks": [t.to_dict() for t in tasks],
    }
    with open(TASKS_FILE, "w") as f:
        json.dump(payload, f, indent=2)


def next_id(tasks: List[Task]) -> int:
    if not tasks:
        return 1
    return max(t.id for t in tasks) + 1
