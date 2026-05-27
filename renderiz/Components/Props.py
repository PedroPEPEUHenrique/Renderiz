from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Type


@dataclass
class PropDefinition:
    Type: Type
    Required: bool = False
    Default: Any = None
    Validator: Optional[Callable[[Any], bool]] = None


class PropsMixin:
    PropTypes: Dict[str, PropDefinition] = {}

    def ValidateProps(self, Props: Dict[str, Any]) -> List[str]:
        Errors: List[str] = []
        for Name, Definition in self.PropTypes.items():
            if Name not in Props:
                if Definition.Required:
                    Errors.append(f"Required prop '{Name}' is missing")
                elif Definition.Default is not None:
                    Props[Name] = Definition.Default
                continue

            Value = Props[Name]
            if not isinstance(Value, Definition.Type):
                Errors.append(
                    f"Prop '{Name}' expected {Definition.Type.__name__},"
                    f" got {type(Value).__name__}"
                )
                continue

            if Definition.Validator and not Definition.Validator(Value):
                Errors.append(f"Prop '{Name}' failed custom validation")

        return Errors


class Prop:
    @staticmethod
    def String(Required: bool = False, Default: Optional[str] = None) -> PropDefinition:
        return PropDefinition(Type=str, Required=Required, Default=Default)

    @staticmethod
    def Int(Required: bool = False, Default: Optional[int] = None) -> PropDefinition:
        return PropDefinition(Type=int, Required=Required, Default=Default)

    @staticmethod
    def Float(Required: bool = False, Default: Optional[float] = None) -> PropDefinition:
        return PropDefinition(Type=float, Required=Required, Default=Default)

    @staticmethod
    def Bool(Required: bool = False, Default: bool = False) -> PropDefinition:
        return PropDefinition(Type=bool, Required=Required, Default=Default)

    @staticmethod
    def List(Required: bool = False, Default: Optional[list] = None) -> PropDefinition:
        return PropDefinition(Type=list, Required=Required, Default=Default or [])

    @staticmethod
    def Dict(Required: bool = False, Default: Optional[dict] = None) -> PropDefinition:
        return PropDefinition(Type=dict, Required=Required, Default=Default or {})

    @staticmethod
    def Callable(Required: bool = False) -> PropDefinition:
        return PropDefinition(Type=object, Required=Required)
