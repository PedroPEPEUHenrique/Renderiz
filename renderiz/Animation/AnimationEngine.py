from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Set

from .Easing import Easing
from .Keyframe import Keyframe, KeyframeLibrary


@dataclass
class AnimationConfig:
    KeyframeName: str
    PresetName: str = ""
    Duration: float = 0.4
    EasingName: str = "EaseOut"
    Delay: float = 0.0
    Iterations: int = 1
    FillMode: str = "forwards"
    Direction: str = "normal"

    def ToStyle(self) -> str:
        CssEasing = Easing.ToCSSBezier(self.EasingName)
        IterStr = "infinite" if self.Iterations == 0 else str(self.Iterations)
        return (
            f"{self.KeyframeName} {self.Duration}s {CssEasing} "
            f"{self.Delay}s {IterStr} {self.Direction} {self.FillMode}"
        )

    def ToDict(self) -> dict:
        return {
            "name": self.PresetName or self.KeyframeName,
            "duration": self.Duration,
            "easing": self.EasingName,
            "delay": self.Delay,
            "iterations": self.Iterations,
            "fillMode": self.FillMode,
            "direction": self.Direction,
        }


_PRESETS = {
    "FadeIn": KeyframeLibrary.FadeIn,
    "FadeOut": KeyframeLibrary.FadeOut,
    "SlideInUp": KeyframeLibrary.SlideInUp,
    "SlideInDown": KeyframeLibrary.SlideInDown,
    "SlideInLeft": KeyframeLibrary.SlideInLeft,
    "SlideInRight": KeyframeLibrary.SlideInRight,
    "ZoomIn": KeyframeLibrary.ZoomIn,
    "Pulse": KeyframeLibrary.Pulse,
    "Shake": KeyframeLibrary.Shake,
    "Spin": KeyframeLibrary.Spin,
    "HeartBeat": KeyframeLibrary.HeartBeat,
}


class AnimationEngine:
    def __init__(self) -> None:
        self._CustomKeyframes: Dict[str, Keyframe] = {}
        self._UsedPresets: Set[str] = set()

    def RegisterKeyframe(self, KF: Keyframe) -> AnimationEngine:
        self._CustomKeyframes[KF.Name] = KF
        return self

    def BuildConfig(
        self,
        Preset: str,
        Duration: float = 0.4,
        EasingName: str = "EaseOut",
        Delay: float = 0.0,
        Iterations: int = 1,
        FillMode: str = "forwards",
        Direction: str = "normal",
    ) -> AnimationConfig:
        if Preset not in _PRESETS and Preset not in self._CustomKeyframes:
            raise ValueError(
                f"Unknown animation preset: '{Preset}'. "
                f"Available: {sorted(_PRESETS)} + custom: {list(self._CustomKeyframes)}"
            )
        self._UsedPresets.add(Preset)
        KFName = f"rz{Preset}" if Preset in _PRESETS else Preset
        return AnimationConfig(
            KeyframeName=KFName,
            PresetName=Preset,
            Duration=Duration,
            EasingName=EasingName,
            Delay=Delay,
            Iterations=Iterations,
            FillMode=FillMode,
            Direction=Direction,
        )

    def AnimationStyle(self, Preset: str, **Kwargs) -> str:
        Config = self.BuildConfig(Preset, **Kwargs)
        return f"animation: {Config.ToStyle()};"

    def AnimationInlineStyle(self, Preset: str, **Kwargs) -> Dict[str, str]:
        Config = self.BuildConfig(Preset, **Kwargs)
        return {"animation": Config.ToStyle()}

    def CollectCSS(self) -> str:
        Parts: List[str] = []
        for Preset in self._UsedPresets:
            if Preset in _PRESETS:
                KF = _PRESETS[Preset]()
                Parts.append(KF.ToCss())
        for KF in self._CustomKeyframes.values():
            Parts.append(KF.ToCss())
        return "\n\n".join(Parts)

    def AvailablePresets(self) -> List[str]:
        return sorted(_PRESETS) + list(self._CustomKeyframes)
