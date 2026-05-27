from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Union

from .VNode import VNode


class PatchOp(Enum):
    Create = "CREATE"
    Delete = "DELETE"
    Replace = "REPLACE"
    UpdateProps = "UPDATE_PROPS"
    UpdateText = "UPDATE_TEXT"
    Move = "MOVE"


@dataclass
class Patch:
    Op: PatchOp
    Path: List[int]
    Payload: Any = None

    def __repr__(self) -> str:
        return f"Patch({self.Op.value}, path={self.Path})"


class DiffPatcher:
    def Diff(
        self,
        OldTree: Optional[Union[VNode, str]],
        NewTree: Optional[Union[VNode, str]],
    ) -> List[Patch]:
        Patches: List[Patch] = []
        self._Compare(OldTree, NewTree, [], Patches)
        return Patches

    def _Compare(
        self,
        Old: Optional[Union[VNode, str]],
        New: Optional[Union[VNode, str]],
        Path: List[int],
        Patches: List[Patch],
    ) -> None:
        if Old is None and New is None:
            return

        if Old is None:
            Patches.append(Patch(PatchOp.Create, list(Path), New))
            return

        if New is None:
            Patches.append(Patch(PatchOp.Delete, list(Path)))
            return

        if isinstance(Old, str) or isinstance(New, str):
            if Old != New:
                Patches.append(Patch(PatchOp.UpdateText, list(Path), New))
            return

        if Old.Tag != New.Tag:
            Patches.append(Patch(PatchOp.Replace, list(Path), New))
            return

        PropDiff = self._DiffProps(Old.Props, New.Props)
        if PropDiff:
            Patches.append(Patch(PatchOp.UpdateProps, list(Path), PropDiff))

        self._DiffChildren(Old.Children, New.Children, Path, Patches)

    def _DiffProps(
        self,
        OldProps: Dict[str, Any],
        NewProps: Dict[str, Any],
    ) -> Optional[Dict[str, Any]]:
        Changes: Dict[str, Any] = {}
        AllKeys = set(OldProps) | set(NewProps)
        for Key in AllKeys:
            OldVal = OldProps.get(Key)
            NewVal = NewProps.get(Key)
            if OldVal != NewVal:
                Changes[Key] = NewVal
        return Changes if Changes else None

    def _DiffChildren(
        self,
        OldList: list,
        NewList: list,
        Path: List[int],
        Patches: List[Patch],
    ) -> None:
        OldKeyed: Dict[str, Tuple[int, Any]] = {}
        for Idx, Child in enumerate(OldList):
            if isinstance(Child, VNode) and Child.Key:
                OldKeyed[Child.Key] = (Idx, Child)

        MaxLen = max(len(OldList), len(NewList))
        for Idx in range(MaxLen):
            ChildPath = Path + [Idx]
            OldChild = OldList[Idx] if Idx < len(OldList) else None
            NewChild = NewList[Idx] if Idx < len(NewList) else None

            if isinstance(NewChild, VNode) and NewChild.Key and NewChild.Key in OldKeyed:
                OldIdx, OldKeyedNode = OldKeyed[NewChild.Key]
                if OldIdx != Idx:
                    Patches.append(Patch(PatchOp.Move, ChildPath, {"From": OldIdx, "To": Idx}))
                self._Compare(OldKeyedNode, NewChild, ChildPath, Patches)
            else:
                self._Compare(OldChild, NewChild, ChildPath, Patches)
