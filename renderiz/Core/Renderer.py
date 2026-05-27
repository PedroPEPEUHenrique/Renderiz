from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, List, Union

from .DiffPatcher import Patch
from .VNode import VNode
from .VirtualDOM import VirtualDOM

if TYPE_CHECKING:
    from ..Components.BaseComponent import BaseComponent


class BaseRenderer(ABC):
    def __init__(self) -> None:
        self._VDom = VirtualDOM()

    @abstractmethod
    def Render(self, Root: Union[VNode, "BaseComponent"], FullPage: bool = True) -> str: ...

    @abstractmethod
    def RenderToString(self, Root: Union[VNode, "BaseComponent"]) -> str: ...

    def Update(self, NewRoot: Union[VNode, "BaseComponent"]) -> List[Patch]:
        Resolved = self._ResolveNode(NewRoot)
        return self._VDom.Update(Resolved)

    def _ResolveNode(self, Node: Union[VNode, "BaseComponent"]) -> VNode:
        from ..Components.BaseComponent import BaseComponent
        if isinstance(Node, BaseComponent):
            Rendered = Node.Render()
            return self._ResolveNode(Rendered)
        return Node
