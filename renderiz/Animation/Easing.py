from __future__ import annotations

import math
from typing import Callable


EasingFn = Callable[[float], float]


class Easing:
    @staticmethod
    def Linear(T: float) -> float:
        return T

    @staticmethod
    def EaseIn(T: float) -> float:
        return T * T

    @staticmethod
    def EaseOut(T: float) -> float:
        return T * (2 - T)

    @staticmethod
    def EaseInOut(T: float) -> float:
        return T * T * (3 - 2 * T)

    @staticmethod
    def EaseInCubic(T: float) -> float:
        return T ** 3

    @staticmethod
    def EaseOutCubic(T: float) -> float:
        return 1 - (1 - T) ** 3

    @staticmethod
    def EaseInOutCubic(T: float) -> float:
        return 4 * T ** 3 if T < 0.5 else 1 - (-2 * T + 2) ** 3 / 2

    @staticmethod
    def EaseInQuart(T: float) -> float:
        return T ** 4

    @staticmethod
    def EaseOutQuart(T: float) -> float:
        return 1 - (1 - T) ** 4

    @staticmethod
    def EaseInElastic(T: float) -> float:
        if T in (0.0, 1.0):
            return T
        return -(2 ** (10 * T - 10)) * math.sin((T * 10 - 10.75) * (2 * math.pi) / 3)

    @staticmethod
    def EaseOutElastic(T: float) -> float:
        if T in (0.0, 1.0):
            return T
        return 2 ** (-10 * T) * math.sin((T * 10 - 0.75) * (2 * math.pi) / 3) + 1

    @staticmethod
    def EaseOutBounce(T: float) -> float:
        N1, D1 = 7.5625, 2.75
        if T < 1 / D1:
            return N1 * T * T
        elif T < 2 / D1:
            T -= 1.5 / D1
            return N1 * T * T + 0.75
        elif T < 2.5 / D1:
            T -= 2.25 / D1
            return N1 * T * T + 0.9375
        else:
            T -= 2.625 / D1
            return N1 * T * T + 0.984375

    @staticmethod
    def Spring(T: float, Stiffness: float = 100.0, Damping: float = 10.0) -> float:
        if T <= 0:
            return 0.0
        if T >= 1:
            return 1.0
        Discriminant = Stiffness - Damping ** 2 / 4
        Omega = math.sqrt(max(0.0, Discriminant))
        Decay = math.exp(-Damping * T / 2)
        if Omega == 0:
            return 1 - (1 + Damping * T / 2) * Decay
        return 1 - Decay * (math.cos(Omega * T) + (Damping / (2 * Omega)) * math.sin(Omega * T))

    @staticmethod
    def ToCSSBezier(Name: str) -> str:
        Map: dict = {
            "Linear": "linear",
            "EaseIn": "ease-in",
            "EaseOut": "ease-out",
            "EaseInOut": "ease-in-out",
            "EaseInCubic": "cubic-bezier(0.55, 0.055, 0.675, 0.19)",
            "EaseOutCubic": "cubic-bezier(0.215, 0.61, 0.355, 1)",
            "EaseInOutCubic": "cubic-bezier(0.645, 0.045, 0.355, 1)",
            "EaseInQuart": "cubic-bezier(0.895, 0.03, 0.685, 0.22)",
            "EaseOutQuart": "cubic-bezier(0.165, 0.84, 0.44, 1)",
            "EaseOutBounce": "cubic-bezier(0.68, -0.55, 0.265, 1.55)",
        }
        return Map.get(Name, "ease")

    @staticmethod
    def Interpolate(Start: float, End: float, T: float, Fn: EasingFn = None) -> float:
        EasedT = Fn(T) if Fn else T
        return Start + (End - Start) * EasedT
