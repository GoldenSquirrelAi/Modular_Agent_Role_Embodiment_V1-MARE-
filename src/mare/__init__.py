"""MARE Protocol package."""
from __future__ import annotations

import time
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Optional

from .router import MARERouter, Task


class TaskStatus(str, Enum):
    """Enumeration of task execution states."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class TaskResult:
    """Result returned from ``MARESystem.execute_task``."""
    task_id: str
    status: TaskStatus
    rep_used: str
    confidence: float
    execution_time: float
    result: Any = None


class MARESystem:
    """Minimal placeholder implementation of the MARE system."""

    def __init__(self, rep_directory: Optional[str] = None):
        self.router = MARERouter(rep_directory=rep_directory)
        self._task_counter = 0

    def execute_task(self, description: str, required_output: str = "") -> TaskResult:
        self._task_counter += 1
        task = Task(
            id=f"task-{self._task_counter}",
            description=description,
            input_context="",
            required_output=required_output,
        )
        rep = self.router.route_task(task)
        start = time.time()
        # Placeholder for actual execution
        exec_time = time.time() - start
        return TaskResult(
            task_id=task.id,
            status=TaskStatus.COMPLETED,
            rep_used=rep,
            confidence=1.0,
            execution_time=exec_time,
            result={"output": required_output},
        )

    def list_available_reps(self) -> Dict[str, Any]:
        """Return available REP definitions."""
        return {name: rep.filepath for name, rep in self.router.reps.items()}

    def get_system_stats(self) -> Dict[str, Any]:
        """Return basic system statistics."""
        return {"tasks_executed": self._task_counter}

    def get_system_health(self) -> Dict[str, Any]:
        """Return simple health information."""
        return {"system_status": "healthy", "uptime_seconds": 0.0}

    def shutdown(self) -> None:
        """Placeholder shutdown hook."""
        return None


def create_mare_system(rep_directory: Optional[str] = None) -> MARESystem:
    """Factory for :class:`MARESystem`."""
    return MARESystem(rep_directory=rep_directory)


__all__ = [
    "MARESystem",
    "create_mare_system",
    "TaskStatus",
    "TaskResult",
    "MARERouter",
    "Task",
]
