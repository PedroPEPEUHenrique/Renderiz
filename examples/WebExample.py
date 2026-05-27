"""
Exemplo de uso do Renderiz para Web.

Demonstra:
  - Componentes reutilizáveis com PascalCase
  - Lazy loading em cards
  - Animações com AnimationEngine
  - Transições suaves via Transition
  - Virtual DOM (VNode tree)
  - Renderização de página completa
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from renderiz import (
    BaseComponent,
    H,
    WebRenderer,
    Transition,
    Registry,
)


class Badge(BaseComponent):
    def Render(self):
        Label = self.Props.get("Label", "")
        Color = self.Props.get("Color", "#6366f1")
        return H(
            "span",
            {
                "style": {
                    "background": Color,
                    "color": "#fff",
                    "padding": "2px 10px",
                    "border-radius": "999px",
                    "font-size": "0.75rem",
                    "font-weight": "600",
                }
            },
            Label,
        )


class Button(BaseComponent):
    def Render(self):
        Label = self.Props.get("Label", "Clique")
        Variant = self.Props.get("Variant", "primary")
        OnClick = self.Props.get("OnClick", "#")
        Animation = self.Props.get("Animation", "FadeIn")

        BgMap = {
            "primary": "#6366f1",
            "secondary": "#e5e7eb",
            "danger": "#ef4444",
        }
        TextMap = {
            "primary": "#fff",
            "secondary": "#111",
            "danger": "#fff",
        }
        Bg = BgMap.get(Variant, "#6366f1")
        Color = TextMap.get(Variant, "#fff")
        Transition_CSS = Transition.Fast(["background", "transform", "box-shadow"]).ToCss()

        return H(
            "a",
            {
                "href": OnClick,
                "animation": Animation,
                "style": {
                    "display": "inline-block",
                    "background": Bg,
                    "color": Color,
                    "padding": "10px 22px",
                    "border-radius": "8px",
                    "font-weight": "600",
                    "text-decoration": "none",
                    "cursor": "pointer",
                    "transition": Transition_CSS,
                },
            },
            Label,
        )


class Card(BaseComponent):
    def Render(self):
        Title = self.Props.get("Title", "")
        Description = self.Props.get("Description", "")
        Tag = self.Props.get("Tag", None)
        Lazy = self.Props.get("Lazy", True)

        Children = [
            H("h3", {"style": {"margin-bottom": "8px", "color": "#1e1e2e"}}, Title),
            H("p", {"style": {"color": "#6b7280", "line-height": "1.6"}}, Description),
        ]

        if Tag:
            Children.append(
                H("div", {"style": {"margin-top": "12px"}}, Badge({"Label": Tag, "Color": "#6366f1"}))
            )

        return H(
            "div",
            {
                "lazy": Lazy,
                "animation": "SlideInUp",
                "style": {
                    "background": "#fff",
                    "border-radius": "12px",
                    "padding": "24px",
                    "box-shadow": "0 2px 12px rgba(0,0,0,0.08)",
                    "border": "1px solid #e5e7eb",
                },
            },
            *Children,
        )


class Header(BaseComponent):
    def Render(self):
        Title = self.Props.get("Title", "Renderiz")
        Subtitle = self.Props.get("Subtitle", "")
        return H(
            "header",
            {
                "animation": "FadeIn",
                "style": {
                    "text-align": "center",
                    "padding": "64px 24px 48px",
                    "background": "linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)",
                    "color": "#fff",
                    "border-radius": "0 0 24px 24px",
                },
            },
            H(
                "h1",
                {"style": {"font-size": "2.5rem", "font-weight": "800", "margin-bottom": "12px"}},
                Title,
            ),
            H(
                "p",
                {"style": {"font-size": "1.1rem", "opacity": "0.9", "max-width": "480px", "margin": "0 auto"}},
                Subtitle,
            ),
        )


class CardGrid(BaseComponent):
    def Render(self):
        Cards = self.Props.get("Cards", [])
        return H(
            "section",
            {
                "style": {
                    "display": "grid",
                    "grid-template-columns": "repeat(auto-fill, minmax(280px, 1fr))",
                    "gap": "24px",
                    "padding": "40px 24px",
                    "max-width": "1100px",
                    "margin": "0 auto",
                }
            },
            *[Card(CardProps) for CardProps in Cards],
        )


class App(BaseComponent):
    def Render(self):
        Cards = [
            {
                "Title": "Virtual DOM",
                "Description": "Diffing e patching eficiente da árvore de nós. Apenas as mudanças reais são aplicadas.",
                "Tag": "Core",
                "Lazy": True,
            },
            {
                "Title": "Lazy Loading",
                "Description": "Componentes carregados sob demanda com IntersectionObserver. Zero impacto no tempo inicial.",
                "Tag": "Performance",
                "Lazy": True,
            },
            {
                "Title": "Animações",
                "Description": "11 presets prontos: FadeIn, SlideInUp, ZoomIn, Pulse, Shake e mais. Easing customizável.",
                "Tag": "Animation",
                "Lazy": True,
            },
            {
                "Title": "Componentes",
                "Description": "Sistema de componentes reutilizáveis com Props tipadas, State e Lifecycle hooks.",
                "Tag": "Components",
                "Lazy": True,
            },
            {
                "Title": "Web & Mobile",
                "Description": "WebRenderer gera HTML/CSS/JS. MobileRenderer gera JSON para React Native e Flutter.",
                "Tag": "Platform",
                "Lazy": True,
            },
            {
                "Title": "Transições Suaves",
                "Description": "API de transições CSS com easing matemático: EaseInOut, Spring, Bounce, Elastic.",
                "Tag": "Animation",
                "Lazy": True,
            },
        ]

        return H(
            "div",
            {"style": {"min-height": "100vh", "background": "#f8fafc"}},
            Header({
                "Title": "Renderiz",
                "Subtitle": "Framework Python para renderização de alta performance em Web e Mobile",
            }),
            CardGrid({"Cards": Cards}),
            H(
                "footer",
                {
                    "style": {
                        "text-align": "center",
                        "padding": "32px",
                        "color": "#9ca3af",
                        "font-size": "0.875rem",
                    }
                },
                "Renderiz v0.1.0 — Python rendering framework",
            ),
        )


if __name__ == "__main__":
    Renderer = WebRenderer(Title="Renderiz — Demo")
    Output = Renderer.Render(App())

    OutPath = os.path.join(os.path.dirname(__file__), "output.html")
    with open(OutPath, "w", encoding="utf-8") as F:
        F.write(Output)

    print(f"[OK] HTML gerado em: {OutPath}")
    print(f"     {len(Output):,} bytes")
