from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

from .Easing import Easing


@dataclass
class TransitionProperty:
    Property: str
    Duration: float = 0.3
    EasingName: str = "EaseInOut"
    Delay: float = 0.0

    def ToCss(self) -> str:
        CssEasing = Easing.ToCSSBezier(self.EasingName)
        return f"{self.Property} {self.Duration}s {CssEasing} {self.Delay}s"


class Transition:
    def __init__(self) -> None:
        self._Properties: List[TransitionProperty] = []

    def Add(
        self,
        Property: str,
        Duration: float = 0.3,
        EasingName: str = "EaseInOut",
        Delay: float = 0.0,
    ) -> Transition:
        self._Properties.append(TransitionProperty(Property, Duration, EasingName, Delay))
        return self

    def ToCss(self) -> str:
        return ", ".join(P.ToCss() for P in self._Properties)

    def ToStyleDict(self) -> Dict[str, str]:
        return {"transition": self.ToCss()}

    def ToInlineStyle(self) -> str:
        return f"transition: {self.ToCss()};"

    @staticmethod
    def Smooth(Properties: Optional[List[str]] = None, Duration: float = 0.3) -> Transition:
        T = Transition()
        for Prop in Properties or ["opacity", "transform"]:
            T.Add(Prop, Duration=Duration, EasingName="EaseInOut")
        return T

    @staticmethod
    def Fast(Properties: Optional[List[str]] = None) -> Transition:
        T = Transition()
        for Prop in Properties or ["opacity", "transform"]:
            T.Add(Prop, Duration=0.15, EasingName="EaseOut")
        return T

    @staticmethod
    def Slow(Properties: Optional[List[str]] = None) -> Transition:
        T = Transition()
        for Prop in Properties or ["opacity", "transform"]:
            T.Add(Prop, Duration=0.6, EasingName="EaseInOut")
        return T

    @staticmethod
    def All(Duration: float = 0.3) -> Transition:
        return Transition().Add("all", Duration=Duration, EasingName="EaseInOut")
