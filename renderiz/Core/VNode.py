from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union


NodeChildren = List[Union["VNode", str]]


@dataclass
class VNode:
    Tag: str
    Props: Dict[str, Any] = field(default_factory=dict)
    Children: NodeChildren = field(default_factory=list)
    Key: Optional[str] = None
    Ref: Optional[str] = None

    def __post_init__(self) -> None:
        if self.Key is None and "key" in self.Props:
            self.Key = str(self.Props.pop("key"))

    def __hash__(self) -> int:
        return hash((self.Tag, self.Key, id(self)))

    def __eq__(self, Other: object) -> bool:
        if not isinstance(Other, VNode):
            return False
        return self.Tag == Other.Tag and self.Key == Other.Key and self.Props == Other.Props

    def Clone(self) -> VNode:
        return VNode(
            Tag=self.Tag,
            Props=dict(self.Props),
            Children=[
                Child.Clone() if isinstance(Child, VNode) else Child
                for Child in self.Children
            ],
            Key=self.Key,
            Ref=self.Ref,
        )

    def PropsFingerprint(self) -> str:
        try:
            Serialized = json.dumps(self.Props, sort_keys=True, default=str)
        except Exception:
            Serialized = str(self.Props)
        return hashlib.md5(Serialized.encode()).hexdigest()[:8]


def CreateElement(
    Tag: str,
    Props: Optional[Dict[str, Any]] = None,
    *Children: Union[VNode, str, list],
) -> VNode:
    FlatChildren: NodeChildren = []
    for Child in Children:
        if isinstance(Child, (list, tuple)):
            FlatChildren.extend(Item for Item in Child if Item is not None and Item is not False)
        elif Child is not None and Child is not False:
            FlatChildren.append(Child)
    return VNode(Tag=Tag, Props=Props or {}, Children=FlatChildren)


H = CreateElement
