from __future__ import annotations

from enum import Enum
from typing import Any, Callable, Dict, List, Optional


class LifecycleEvent(Enum):
    BeforeMount = "BEFORE_MOUNT"
    Mounted = "MOUNTED"
    BeforeUpdate = "BEFORE_UPDATE"
    Updated = "UPDATED"
    BeforeUnmount = "BEFORE_UNMOUNT"
    Unmounted = "UNMOUNTED"


class LifecycleMixin:
    def __init__(self) -> None:
        self._Hooks: Dict[LifecycleEvent, List[Callable[..., Any]]] = {
            Event: [] for Event in LifecycleEvent
        }

    def On(self, Event: LifecycleEvent, Hook: Callable[..., Any]) -> None:
        self._Hooks[Event].append(Hook)

    def Off(self, Event: LifecycleEvent, Hook: Callable[..., Any]) -> None:
        self._Hooks[Event] = [H for H in self._Hooks[Event] if H is not Hook]

    def Once(self, Event: LifecycleEvent, Hook: Callable[..., Any]) -> None:
        def Wrapper(*Args: Any, **Kwargs: Any) -> Any:
            Hook(*Args, **Kwargs)
            self.Off(Event, Wrapper)
        self.On(Event, Wrapper)

    def Emit(self, Event: LifecycleEvent, *Args: Any, **Kwargs: Any) -> None:
        for Hook in list(self._Hooks.get(Event, [])):
            Hook(*Args, **Kwargs)

    def ListenerCount(self, Event: LifecycleEvent) -> int:
        return len(self._Hooks.get(Event, []))
