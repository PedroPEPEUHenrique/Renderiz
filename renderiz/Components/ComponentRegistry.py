from __future__ import annotations

from typing import Dict, Optional, Type

from .BaseComponent import BaseComponent


class ComponentRegistry:
    _Instance: Optional[ComponentRegistry] = None
    _Registry: Dict[str, Type[BaseComponent]] = {}

    def __new__(cls) -> ComponentRegistry:
        if cls._Instance is None:
            cls._Instance = super().__new__(cls)
        return cls._Instance

    def Register(self, Name: str, Component: Type[BaseComponent]) -> None:
        if not issubclass(Component, BaseComponent):
            raise TypeError(f"'{Name}' must extend BaseComponent")
        self._Registry[Name] = Component

    def Get(self, Name: str) -> Optional[Type[BaseComponent]]:
        return self._Registry.get(Name)

    def Create(self, Name: str, Props: Optional[dict] = None) -> BaseComponent:
        ComponentClass = self.Get(Name)
        if ComponentClass is None:
            raise KeyError(f"Component '{Name}' not registered. Available: {list(self._Registry)}")
        return ComponentClass(Props or {})

    def All(self) -> Dict[str, Type[BaseComponent]]:
        return dict(self._Registry)

    def Clear(self) -> None:
        self._Registry.clear()

    def __contains__(self, Name: str) -> bool:
        return Name in self._Registry


Registry = ComponentRegistry()
