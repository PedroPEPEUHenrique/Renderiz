from __future__ import annotations

from typing import Dict, List, Optional


class StyleRule:
    def __init__(self, Selector: str) -> None:
        self._Selector = Selector
        self._Properties: Dict[str, str] = {}

    def Set(self, Property: str, Value: str) -> StyleRule:
        self._Properties[Property] = Value
        return self

    def ToCss(self) -> str:
        if not self._Properties:
            return ""
        Props = ";\n  ".join(f"{K}: {V}" for K, V in self._Properties.items())
        return f"{self._Selector} {{\n  {Props};\n}}"


class CSSBuilder:
    def __init__(self) -> None:
        self._Rules: List[StyleRule] = []
        self._CSSVars: Dict[str, str] = {}
        self._MediaQueries: List[str] = []
        self._RawBlocks: List[str] = []

    def Rule(self, Selector: str) -> StyleRule:
        Rule = StyleRule(Selector)
        self._Rules.append(Rule)
        return Rule

    def Var(self, Name: str, Value: str) -> CSSBuilder:
        self._CSSVars[f"--{Name}"] = Value
        return self

    def MediaQuery(self, Query: str, InnerCSS: str) -> CSSBuilder:
        self._MediaQueries.append(f"@media {Query} {{\n{InnerCSS}\n}}")
        return self

    def Raw(self, CSS: str) -> CSSBuilder:
        self._RawBlocks.append(CSS)
        return self

    def Build(self) -> str:
        Parts: List[str] = []

        if self._CSSVars:
            VarsCSS = "\n  ".join(f"{K}: {V};" for K, V in self._CSSVars.items())
            Parts.append(f":root {{\n  {VarsCSS}\n}}")

        for Rule in self._Rules:
            Built = Rule.ToCss()
            if Built:
                Parts.append(Built)

        Parts.extend(self._MediaQueries)
        Parts.extend(self._RawBlocks)

        return "\n\n".join(Parts)

    @staticmethod
    def DictToInline(StyleDict: Dict[str, str]) -> str:
        return "; ".join(f"{K}: {V}" for K, V in StyleDict.items())

    @staticmethod
    def Merge(*Dicts: Dict[str, str]) -> Dict[str, str]:
        Result: Dict[str, str] = {}
        for D in Dicts:
            Result.update(D)
        return Result

    @staticmethod
    def Px(Value: float) -> str:
        return f"{Value}px"

    @staticmethod
    def Rem(Value: float) -> str:
        return f"{Value}rem"

    @staticmethod
    def Pct(Value: float) -> str:
        return f"{Value}%"
