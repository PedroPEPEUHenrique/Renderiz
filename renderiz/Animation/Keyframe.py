from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class KeyframeStop:
    Percent: float
    Properties: Dict[str, str] = field(default_factory=dict)

    def ToCss(self) -> str:
        Props = "; ".join(f"{K}: {V}" for K, V in self.Properties.items())
        return f"  {self.Percent:.0f}% {{ {Props} }}"


@dataclass
class Keyframe:
    Name: str
    Stops: List[KeyframeStop] = field(default_factory=list)

    def AddStop(self, Percent: float, **Properties: str) -> Keyframe:
        self.Stops.append(KeyframeStop(Percent=Percent, Properties=dict(Properties)))
        return self

    def ToCss(self) -> str:
        Sorted = sorted(self.Stops, key=lambda S: S.Percent)
        StopsCss = "\n".join(Stop.ToCss() for Stop in Sorted)
        return f"@keyframes {self.Name} {{\n{StopsCss}\n}}"


class KeyframeLibrary:
    @staticmethod
    def FadeIn(Name: str = "rzFadeIn") -> Keyframe:
        return Keyframe(Name).AddStop(0, opacity="0").AddStop(100, opacity="1")

    @staticmethod
    def FadeOut(Name: str = "rzFadeOut") -> Keyframe:
        return Keyframe(Name).AddStop(0, opacity="1").AddStop(100, opacity="0")

    @staticmethod
    def SlideInUp(Name: str = "rzSlideInUp") -> Keyframe:
        return (
            Keyframe(Name)
            .AddStop(0, opacity="0", transform="translateY(24px)")
            .AddStop(100, opacity="1", transform="translateY(0)")
        )

    @staticmethod
    def SlideInDown(Name: str = "rzSlideInDown") -> Keyframe:
        return (
            Keyframe(Name)
            .AddStop(0, opacity="0", transform="translateY(-24px)")
            .AddStop(100, opacity="1", transform="translateY(0)")
        )

    @staticmethod
    def SlideInLeft(Name: str = "rzSlideInLeft") -> Keyframe:
        return (
            Keyframe(Name)
            .AddStop(0, opacity="0", transform="translateX(-24px)")
            .AddStop(100, opacity="1", transform="translateX(0)")
        )

    @staticmethod
    def SlideInRight(Name: str = "rzSlideInRight") -> Keyframe:
        return (
            Keyframe(Name)
            .AddStop(0, opacity="0", transform="translateX(24px)")
            .AddStop(100, opacity="1", transform="translateX(0)")
        )

    @staticmethod
    def ZoomIn(Name: str = "rzZoomIn") -> Keyframe:
        return (
            Keyframe(Name)
            .AddStop(0, opacity="0", transform="scale(0.85)")
            .AddStop(100, opacity="1", transform="scale(1)")
        )

    @staticmethod
    def Pulse(Name: str = "rzPulse") -> Keyframe:
        return (
            Keyframe(Name)
            .AddStop(0, transform="scale(1)")
            .AddStop(50, transform="scale(1.05)")
            .AddStop(100, transform="scale(1)")
        )

    @staticmethod
    def Shake(Name: str = "rzShake") -> Keyframe:
        return (
            Keyframe(Name)
            .AddStop(0, transform="translateX(0)")
            .AddStop(20, transform="translateX(-8px)")
            .AddStop(40, transform="translateX(8px)")
            .AddStop(60, transform="translateX(-6px)")
            .AddStop(80, transform="translateX(6px)")
            .AddStop(100, transform="translateX(0)")
        )

    @staticmethod
    def Spin(Name: str = "rzSpin") -> Keyframe:
        return (
            Keyframe(Name)
            .AddStop(0, transform="rotate(0deg)")
            .AddStop(100, transform="rotate(360deg)")
        )

    @staticmethod
    def HeartBeat(Name: str = "rzHeartBeat") -> Keyframe:
        return (
            Keyframe(Name)
            .AddStop(0, transform="scale(1)")
            .AddStop(14, transform="scale(1.3)")
            .AddStop(28, transform="scale(1)")
            .AddStop(42, transform="scale(1.3)")
            .AddStop(70, transform="scale(1)")
        )
