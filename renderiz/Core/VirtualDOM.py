from __future__ import annotations

from typing import List, Optional

from .DiffPatcher import DiffPatcher, Patch
from .VNode import VNode


class VirtualDOM:
    def __init__(self) -> None:
        self._Root: Optional[VNode] = None
        self._Patcher = DiffPatcher()

    @property
    def Root(self) -> Optional[VNode]:
        return self._Root

    def Mount(self, Tree: VNode) -> None:
        self._Root = Tree

    def Update(self, NewTree: VNode) -> List[Patch]:
        Patches = self._Patcher.Diff(self._Root, NewTree)
        self._Root = NewTree
        return Patches

    def Reset(self) -> None:
        self._Root = None

    def HasContent(self) -> bool:
        return self._Root is not None

    def Snapshot(self) -> Optional[VNode]:
        return self._Root.Clone() if self._Root else None
