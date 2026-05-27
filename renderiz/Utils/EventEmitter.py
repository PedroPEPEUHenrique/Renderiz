from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional


class EventEmitter:
    def __init__(self) -> None:
        self._Listeners: Dict[str, List[Callable[..., Any]]] = {}

    def On(self, Event: str, Listener: Callable[..., Any]) -> EventEmitter:
        self._Listeners.setdefault(Event, []).append(Listener)
        return self

    def Off(self, Event: str, Listener: Callable[..., Any]) -> EventEmitter:
        if Event in self._Listeners:
            self._Listeners[Event] = [
                L for L in self._Listeners[Event] if L is not Listener
            ]
        return self

    def Once(self, Event: str, Listener: Callable[..., Any]) -> EventEmitter:
        def Wrapper(*Args: Any, **Kwargs: Any) -> Any:
            Listener(*Args, **Kwargs)
            self.Off(Event, Wrapper)
        return self.On(Event, Wrapper)

    def Emit(self, Event: str, *Args: Any, **Kwargs: Any) -> EventEmitter:
        for Listener in list(self._Listeners.get(Event, [])):
            Listener(*Args, **Kwargs)
        return self

    def RemoveAll(self, Event: Optional[str] = None) -> EventEmitter:
        if Event is None:
            self._Listeners.clear()
        else:
            self._Listeners.pop(Event, None)
        return self

    def ListenerCount(self, Event: str) -> int:
        return len(self._Listeners.get(Event, []))

    def EventNames(self) -> List[str]:
        return list(self._Listeners)
