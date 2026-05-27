from __future__ import annotations

import html
from typing import Any, Dict, List, Optional, Union

from ..Animation.AnimationEngine import AnimationEngine
from ..Components.BaseComponent import BaseComponent
from ..Core.Renderer import BaseRenderer
from ..Core.VNode import VNode
from ..Performance.LazyLoader import LazyLoader
from ..Utils.CSSBuilder import CSSBuilder


_VOID_ELEMENTS = frozenset({
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
})

_RAW_TEXT_ELEMENTS = frozenset({"script", "style"})

_BASE_RESET = """\
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: system-ui, -apple-system, sans-serif; line-height: 1.5; }
img, video { max-width: 100%; display: block; }"""


class WebRenderer(BaseRenderer):
    def __init__(self, Title: str = "Renderiz App", Lang: str = "pt-BR") -> None:
        super().__init__()
        self._Title = Title
        self._Lang = Lang
        self._AnimEngine = AnimationEngine()
        self._LazyLoader = LazyLoader()
        self._ExtraCSS: List[str] = []
        self._ExtraJS: List[str] = []
        self._HasLazy = False

    def Render(self, Root: Union[VNode, BaseComponent], FullPage: bool = True) -> str:
        self._HasLazy = False
        Resolved = self._ResolveNode(Root)
        self._VDom.Mount(Resolved)

        Body = self._RenderNode(Resolved)
        CSS = self._BuildCSS()
        JS = self._BuildJS()

        return self._WrapDocument(Body, CSS, JS) if FullPage else Body

    def RenderToString(self, Root: Union[VNode, BaseComponent]) -> str:
        return self.Render(Root, FullPage=False)

    def AddCSS(self, CSS: str) -> WebRenderer:
        self._ExtraCSS.append(CSS)
        return self

    def AddScript(self, JS: str) -> WebRenderer:
        self._ExtraJS.append(JS)
        return self

    def SetTitle(self, Title: str) -> WebRenderer:
        self._Title = Title
        return self

    def _RenderNode(self, Node: Union[VNode, str, None, BaseComponent]) -> str:
        if Node is None:
            return ""
        if isinstance(Node, bool):
            return ""
        if isinstance(Node, (int, float)):
            return html.escape(str(Node))
        if isinstance(Node, str):
            return html.escape(Node)
        if isinstance(Node, BaseComponent):
            return self._RenderNode(self._ResolveNode(Node))

        Tag = Node.Tag

        if Tag == "Fragment":
            return "".join(self._RenderNode(Child) for Child in Node.Children)

        PropsStr = self._BuildProps(Node.Props)

        if Tag in _VOID_ELEMENTS:
            return f"<{Tag}{PropsStr}>"

        if Tag in _RAW_TEXT_ELEMENTS:
            Inner = "".join(
                Child if isinstance(Child, str) else self._RenderNode(Child)
                for Child in Node.Children
            )
        else:
            Inner = "".join(self._RenderNode(Child) for Child in Node.Children)

        return f"<{Tag}{PropsStr}>{Inner}</{Tag}>"

    def _BuildProps(self, Props: Dict[str, Any]) -> str:
        Parts: List[str] = []
        Classes: List[str] = []

        for Key, Value in Props.items():
            if Key in {"key", "ref"}:
                continue

            if Key in {"className", "class"}:
                if isinstance(Value, list):
                    Classes.extend(V for V in Value if V)
                else:
                    Classes.append(str(Value))
                continue

            if Key == "style":
                if isinstance(Value, dict):
                    Value = CSSBuilder.DictToInline(Value)
                Parts.append(f'style="{html.escape(str(Value))}"')
                continue

            if Key == "animation":
                try:
                    Config = self._AnimEngine.BuildConfig(str(Value))
                    Parts.append(f'style="animation: {Config.ToStyle()}"')
                except ValueError:
                    pass
                continue

            if Key == "lazy":
                if Value:
                    self._HasLazy = True
                    Parts.append("data-lazy")
                continue

            if Key == "htmlFor":
                Key = "for"

            if isinstance(Value, bool):
                if Value:
                    Parts.append(html.escape(Key))
            elif Value is not None:
                Parts.append(f'{html.escape(Key)}="{html.escape(str(Value))}"')

        if Classes:
            Parts.insert(0, f'class="{html.escape(" ".join(Classes))}"')

        return (" " + " ".join(Parts)) if Parts else ""

    def _BuildCSS(self) -> str:
        Parts: List[str] = [_BASE_RESET]
        AnimCSS = self._AnimEngine.CollectCSS()
        if AnimCSS:
            Parts.append(AnimCSS)
        if self._HasLazy:
            Parts.append(self._LazyLoader.GenerateStyles())
        Parts.extend(self._ExtraCSS)
        return "\n\n".join(Parts)

    def _BuildJS(self) -> str:
        Parts: List[str] = []
        if self._HasLazy:
            Parts.append(self._LazyLoader.GenerateScript())
        Parts.extend(self._ExtraJS)
        return "\n\n".join(Parts)

    def _WrapDocument(self, Body: str, CSS: str, JS: str) -> str:
        StyleTag = f"<style>\n{CSS}\n</style>" if CSS else ""
        ScriptTag = f"<script>\n{JS}\n</script>" if JS else ""
        return (
            f'<!DOCTYPE html>\n'
            f'<html lang="{self._Lang}">\n'
            f'<head>\n'
            f'  <meta charset="UTF-8">\n'
            f'  <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
            f'  <title>{html.escape(self._Title)}</title>\n'
            f'  {StyleTag}\n'
            f'</head>\n'
            f'<body>\n'
            f'  <div id="app">\n'
            f'    {Body}\n'
            f'  </div>\n'
            f'  {ScriptTag}\n'
            f'</body>\n'
            f'</html>'
        )
