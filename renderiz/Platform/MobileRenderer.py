from __future__ import annotations

import json
from typing import Any, Dict, List, Optional, Union

from ..Animation.AnimationEngine import AnimationEngine
from ..Components.BaseComponent import BaseComponent
from ..Core.Renderer import BaseRenderer
from ..Core.VNode import VNode


_PLATFORM_TAG_MAP: Dict[str, Dict[str, str]] = {
    "react-native": {
        "div": "View",
        "span": "View",
        "p": "Text",
        "h1": "Text",
        "h2": "Text",
        "h3": "Text",
        "h4": "Text",
        "h5": "Text",
        "h6": "Text",
        "button": "TouchableOpacity",
        "img": "Image",
        "ul": "View",
        "ol": "View",
        "li": "View",
        "input": "TextInput",
        "a": "TouchableOpacity",
        "section": "View",
        "article": "View",
        "header": "View",
        "footer": "View",
        "nav": "View",
        "main": "View",
    },
    "flutter": {
        "div": "Container",
        "span": "Container",
        "p": "Text",
        "h1": "Text",
        "h2": "Text",
        "h3": "Text",
        "button": "ElevatedButton",
        "img": "Image",
        "ul": "Column",
        "ol": "Column",
        "li": "Container",
        "input": "TextField",
        "section": "Container",
        "article": "Container",
        "header": "Container",
        "footer": "Container",
        "main": "Container",
    },
}


class MobileRenderer(BaseRenderer):
    def __init__(self, Platform: str = "generic") -> None:
        super().__init__()
        self._Platform = Platform
        self._AnimEngine = AnimationEngine()
        self._TagMap = _PLATFORM_TAG_MAP.get(Platform, {})

    def Render(self, Root: Union[VNode, BaseComponent], FullPage: bool = True) -> str:
        Tree = self._ResolveNode(Root)
        self._VDom.Mount(Tree)
        Payload = self._Serialize(Tree)
        Envelope = {
            "platform": self._Platform,
            "version": "0.1.0",
            "root": Payload,
        }
        return json.dumps(Envelope, ensure_ascii=False, indent=2)

    def RenderToString(self, Root: Union[VNode, BaseComponent]) -> str:
        return self.Render(Root, FullPage=False)

    def RenderToDict(self, Root: Union[VNode, BaseComponent]) -> Dict[str, Any]:
        Tree = self._ResolveNode(Root)
        return self._Serialize(Tree)

    def _Serialize(self, Node: Union[VNode, str, None, BaseComponent]) -> Any:
        if Node is None:
            return None
        if isinstance(Node, bool):
            return None
        if isinstance(Node, str):
            return {"type": "Text", "value": Node}
        if isinstance(Node, BaseComponent):
            return self._Serialize(self._ResolveNode(Node))

        NativeTag = self._TagMap.get(Node.Tag, Node.Tag)
        AnimData = self._ExtractAnimation(Node.Props)
        CleanProps = {
            K: V
            for K, V in Node.Props.items()
            if K not in {"key", "ref", "animation", "lazy"}
        }

        Result: Dict[str, Any] = {
            "type": NativeTag,
            "props": CleanProps,
            "children": [
                S
                for Child in Node.Children
                if (S := self._Serialize(Child)) is not None
            ],
        }

        if Node.Key:
            Result["key"] = Node.Key
        if AnimData:
            Result["animation"] = AnimData
        if Node.Props.get("lazy"):
            Result["lazy"] = True

        return Result

    def _ExtractAnimation(self, Props: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        AnimName = Props.get("animation")
        if not AnimName:
            return None
        try:
            Config = self._AnimEngine.BuildConfig(str(AnimName))
            return Config.ToDict()
        except ValueError:
            return None
