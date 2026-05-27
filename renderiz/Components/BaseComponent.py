from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, Optional

from ..Core.VNode import VNode


class BaseComponent(ABC):
    def __init__(self, Props: Optional[Dict[str, Any]] = None) -> None:
        self.Props: Dict[str, Any] = Props or {}
        self._State: Dict[str, Any] = {}
        self._Mounted: bool = False
        self._UpdateCallback: Optional[Callable[[BaseComponent], None]] = None

    @abstractmethod
    def Render(self) -> VNode: ...

    def SetState(self, Updates: Dict[str, Any]) -> None:
        PrevState = dict(self._State)
        self._State.update(Updates)
        if self._Mounted and self._UpdateCallback:
            self._UpdateCallback(self)
        self.OnUpdate(dict(self.Props), PrevState)

    def GetState(self, Key: str, Default: Any = None) -> Any:
        return self._State.get(Key, Default)

    def OnMount(self) -> None:
        pass

    def OnUpdate(self, PrevProps: Dict[str, Any], PrevState: Dict[str, Any]) -> None:
        pass

    def OnUnmount(self) -> None:
        pass

    def Mount(self, UpdateCallback: Optional[Callable[[BaseComponent], None]] = None) -> None:
        self._UpdateCallback = UpdateCallback
        self._Mounted = True
        self.OnMount()

    def Unmount(self) -> None:
        self.OnUnmount()
        self._Mounted = False
        self._UpdateCallback = None

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(Props={self.Props})"
