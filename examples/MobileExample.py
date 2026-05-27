"""
Exemplo de uso do Renderiz para Mobile.

Demonstra:
  - Componentes que renderizam para JSON nativo
  - Mapeamento de tags HTML → React Native / Flutter
  - Animações embutidas no payload JSON
  - Lazy loading marcado no output
"""

import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from renderiz import BaseComponent, H, MobileRenderer


class ProductCard(BaseComponent):
    def Render(self):
        Name = self.Props.get("Name", "")
        Price = self.Props.get("Price", 0.0)
        Category = self.Props.get("Category", "")
        return H(
            "div",
            {"animation": "ZoomIn", "lazy": True},
            H("h3", {}, Name),
            H("p", {"style": {"color": "#6b7280"}}, Category),
            H(
                "span",
                {"style": {"font-weight": "bold", "color": "#6366f1"}},
                f"R$ {Price:.2f}",
            ),
        )


class ProductList(BaseComponent):
    def Render(self):
        Products = self.Props.get("Products", [])
        return H(
            "ul",
            {"style": {"padding": "16px", "gap": "12px"}},
            *[ProductCard(P) for P in Products],
        )


class SearchBar(BaseComponent):
    def Render(self):
        Placeholder = self.Props.get("Placeholder", "Buscar...")
        return H(
            "div",
            {"style": {"padding": "12px 16px", "background": "#f1f5f9"}},
            H(
                "input",
                {
                    "type": "text",
                    "placeholder": Placeholder,
                    "style": {
                        "width": "100%",
                        "padding": "10px 14px",
                        "border-radius": "8px",
                        "border": "1px solid #e2e8f0",
                    },
                },
            ),
        )


class MobileApp(BaseComponent):
    def Render(self):
        Products = [
            {"Name": "Tênis Pro Runner", "Price": 349.90, "Category": "Esportes"},
            {"Name": "Mochila Urbana", "Price": 189.00, "Category": "Acessórios"},
            {"Name": "Fone Bluetooth", "Price": 279.50, "Category": "Eletrônicos"},
            {"Name": "Camisa Dry-Fit", "Price": 89.90, "Category": "Roupas"},
        ]

        return H(
            "main",
            {"animation": "FadeIn"},
            H(
                "header",
                {"style": {"padding": "20px 16px 8px"}},
                H("h1", {"style": {"font-size": "22px", "font-weight": "700"}}, "Loja Mobile"),
            ),
            SearchBar({"Placeholder": "Buscar produtos..."}),
            ProductList({"Products": Products}),
        )


if __name__ == "__main__":
    print("=== React Native ===")
    RN_Renderer = MobileRenderer(Platform="react-native")
    RN_Output = RN_Renderer.Render(MobileApp())
    print(RN_Output)

    print("\n=== Flutter ===")
    Flutter_Renderer = MobileRenderer(Platform="flutter")
    Flutter_Output = Flutter_Renderer.Render(MobileApp())
    print(Flutter_Output)

    OutPath = os.path.join(os.path.dirname(__file__), "mobile_output.json")
    with open(OutPath, "w", encoding="utf-8") as F:
        F.write(RN_Output)
    print(f"\n[OK] JSON salvo em: {OutPath}")
