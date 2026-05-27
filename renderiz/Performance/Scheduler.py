from __future__ import annotations

import threading
import time
from collections import deque
from dataclasses import dataclass, field
from typing import Any, Callable, Deque, List


@dataclass(order=True)
class RenderTask:
    Priority: int
    CreatedAt: float = field(compare=False, default_factory=time.monotonic)
    ComponentId: str = field(compare=False, default="")
    Callback: Callable[[], Any] = field(compare=False, default=lambda: None)


class Scheduler:
    def __init__(self, BatchInterval: float = 0.016) -> None:
        self._Queue: Deque[RenderTask] = deque()
        self._Lock = threading.Lock()
        self._BatchInterval = BatchInterval
        self._Scheduled: set = set()

    def Schedule(
        self,
        ComponentId: str,
        Callback: Callable[[], Any],
        Priority: int = 0,
    ) -> None:
        with self._Lock:
            if ComponentId not in self._Scheduled:
                self._Queue.append(
                    RenderTask(
                        Priority=-Priority,
                        ComponentId=ComponentId,
                        Callback=Callback,
                    )
                )
                self._Scheduled.add(ComponentId)

    def Flush(self) -> List[Any]:
        with self._Lock:
            Tasks = sorted(self._Queue)
            self._Queue.clear()
            self._Scheduled.clear()

        Results: List[Any] = []
        for Task in Tasks:
            try:
                Results.append(Task.Callback())
            except Exception as Exc:
                Results.append(Exc)
        return Results

    def IsEmpty(self) -> bool:
        return len(self._Queue) == 0

    def Clear(self) -> None:
        with self._Lock:
            self._Queue.clear()
            self._Scheduled.clear()

    def Size(self) -> int:
        return len(self._Queue)
