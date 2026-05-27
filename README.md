# Renderiz

Framework Python para renderização de alta performance em **Web** e **Mobile**.

Crie interfaces com componentes reutilizáveis, Virtual DOM, lazy loading, animações e transições; tudo em Python puro.

---

## Índice

- [Instalação](#instalação)
- [Conceitos básicos](#conceitos-básicos)
- [Componentes](#componentes)
- [Props e State](#props-e-state)
- [Lifecycle hooks](#lifecycle-hooks)
- [Renderização Web](#renderização-web)
- [Renderização Mobile](#renderização-mobile)
- [Animações](#animações)
- [Transições](#transições)
- [Lazy Loading](#lazy-loading)
- [CSSBuilder](#cssbuilder)
- [Easing](#easing)
- [Exemplo completo](#exemplo-completo)

---

## Instalação

```bash
pip install .
```

Requer **Python 3.10+**.

---

## Conceitos básicos

### A função `H()`

`H()` (alias de `CreateElement`) é a função principal para criar nós da árvore virtual:

```python
H(tag, props, *children)
```

```python
from renderiz import H

# Elemento simples
H("p", {}, "Olá mundo")

# Com estilo inline
H("div", {"style": {"color": "#333", "padding": "16px"}}, "conteúdo")

# Aninhado
H("div", {},
    H("h1", {}, "Título"),
    H("p", {}, "Parágrafo"),
)
```

| Parâmetro  | Tipo               | Descrição                                      |
|------------|--------------------|------------------------------------------------|
| `tag`      | `str`              | Tag HTML (`"div"`, `"p"`, `"span"`, etc.)      |
| `props`    | `dict`             | Atributos e estilos do elemento                |
| `*children`| `VNode` ou `str`   | Filhos: outros nós ou texto puro               |

---

## Componentes

Todo componente herda de `BaseComponent` e deve implementar o método `Render()`, que retorna um `VNode`.

**Nomenclatura obrigatória:** nomes de componentes e Props em **PascalCase**.

```python
from renderiz import BaseComponent, H

class Cartao(BaseComponent):
    def Render(self):
        Titulo = self.Props.get("Titulo", "")
        Descricao = self.Props.get("Descricao", "")

        return H(
            "div",
            {"style": {"padding": "24px", "border-radius": "12px", "background": "#fff"}},
            H("h3", {}, Titulo),
            H("p", {"style": {"color": "#6b7280"}}, Descricao),
        )
```

Para usar um componente dentro de outro, instancie-o passando as Props como dicionário:

```python
class App(BaseComponent):
    def Render(self):
        return H(
            "div",
            {},
            Cartao({"Titulo": "Bem-vindo", "Descricao": "Isso é o Renderiz."}),
        )
```

---

## Props e State

### Props

Acessadas via `self.Props.get("NomeDaProp", valorPadrao)`:

```python
class Botao(BaseComponent):
    def Render(self):
        Label = self.Props.get("Label", "Clique")
        Variante = self.Props.get("Variante", "primary")

        Cores = {"primary": "#6366f1", "danger": "#ef4444"}
        Bg = Cores.get(Variante, "#6366f1")

        return H("button", {"style": {"background": Bg, "color": "#fff"}}, Label)
```

### State

Use `SetState()` para atualizar e `GetState()` para ler:

```python
class Contador(BaseComponent):
    def OnMount(self):
        self.SetState({"Count": 0})

    def Render(self):
        Count = self.GetState("Count", 0)
        return H("p", {}, f"Contagem: {Count}")
```

---

## Lifecycle hooks

Sobrescreva os métodos abaixo quando precisar reagir a eventos do ciclo de vida:

| Método                              | Quando é chamado                        |
|-------------------------------------|-----------------------------------------|
| `OnMount()`                         | Logo após o componente ser montado      |
| `OnUpdate(PrevProps, PrevState)`    | Após qualquer atualização de state      |
| `OnUnmount()`                       | Antes do componente ser destruído       |

```python
class MeuComponente(BaseComponent):
    def OnMount(self):
        self.SetState({"Ativo": True})

    def OnUpdate(self, PrevProps, PrevState):
        print(f"State anterior: {PrevState}")

    def OnUnmount(self):
        print("Componente removido")

    def Render(self):
        return H("div", {}, "conteúdo")
```

---

## Renderização Web

`WebRenderer` transforma a árvore de componentes em um arquivo **HTML completo** com CSS e JavaScript embutidos.

```python
from renderiz import WebRenderer

renderer = WebRenderer(Title="Minha Página")
html = renderer.Render(MinhaApp())

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
```

O HTML gerado já inclui:
- Estilos globais e reset básico
- CSS das animações utilizadas
- JavaScript do lazy loading via `IntersectionObserver`

---

## Renderização Mobile

`MobileRenderer` gera um **payload JSON** com a estrutura de componentes, pronto para ser consumido por aplicações React Native ou Flutter.

```python
from renderiz import MobileRenderer

# React Native
rn = MobileRenderer(Platform="react-native")
print(rn.Render(MinhaApp()))

# Flutter
fl = MobileRenderer(Platform="flutter")
print(fl.Render(MinhaApp()))
```

As tags HTML são mapeadas automaticamente para os equivalentes nativos de cada plataforma. Animações e lazy loading são incluídos no JSON como metadados.

---

## Animações

Aplique animações adicionando o atributo `"animation"` a qualquer nó. No `WebRenderer`, os keyframes CSS são gerados automaticamente.

```python
H("div", {"animation": "FadeIn"}, "Aparece suavemente")
H("div", {"animation": "SlideInUp"}, "Sobe da base")
H("div", {"animation": "ZoomIn"}, "Zoom de entrada")
```

### Presets disponíveis

| Preset         | Efeito                        |
|----------------|-------------------------------|
| `FadeIn`       | Aparece gradualmente          |
| `FadeOut`      | Desaparece gradualmente       |
| `SlideInUp`    | Entra subindo                 |
| `SlideInDown`  | Entra descendo                |
| `SlideInLeft`  | Entra pela esquerda           |
| `SlideInRight` | Entra pela direita            |
| `ZoomIn`       | Zoom de entrada               |
| `Pulse`        | Pulsação contínua             |
| `Shake`        | Agitação (erro, atenção)      |
| `Spin`         | Rotação contínua              |
| `HeartBeat`    | Batida de coração             |

### Configuração avançada com `AnimationEngine`

```python
from renderiz import AnimationEngine

Engine = AnimationEngine()
Config = Engine.BuildConfig(
    Preset="SlideInUp",
    Duration=0.6,
    EasingName="EaseOutCubic",
    Delay=0.2,
)
print(Config.ToStyle())
```

---

## Transições

`Transition` gera strings CSS de transição com easing matemático.

```python
from renderiz import Transition

# Rápida (0.15s)
css = Transition.Fast(["background", "transform"]).ToCss()

# Suave (0.3s, padrão)
css = Transition.Smooth(["opacity", "transform"]).ToCss()

# Lenta (0.6s)
css = Transition.Slow().ToCss()

# Todas as propriedades
css = Transition.All(Duration=0.4).ToCss()

# Personalizada
from renderiz import Transition
t = Transition()
t.Add("background", Duration=0.2, EasingName="EaseOut")
t.Add("transform", Duration=0.3, EasingName="EaseInOut", Delay=0.05)
css = t.ToCss()
```

Aplique o resultado no estilo do elemento:

```python
H("a", {"style": {"transition": Transition.Fast(["background"]).ToCss()}}, "link")
```

---

## Lazy Loading

Qualquer nó com `"lazy": True` é carregado sob demanda usando `IntersectionObserver`. O elemento só se torna visível quando entra na viewport.

```python
H("div", {"lazy": True}, "Carregado ao aparecer na tela")

# Combinar com animação
H("div", {"lazy": True, "animation": "SlideInUp"}, conteudo)
```

> Funciona automaticamente no `WebRenderer`. No `MobileRenderer`, o atributo é incluído no JSON para tratamento nativo.

---

## CSSBuilder

Utilitário para construir folhas de estilo programaticamente.

```python
from renderiz import CSSBuilder

css = CSSBuilder()

css.Var("primary", "#6366f1")
css.Var("radius", "12px")

css.Rule(".card") \
    .Set("background", "#fff") \
    .Set("border-radius", "var(--radius)") \
    .Set("padding", "24px")

css.Rule(".card:hover") \
    .Set("box-shadow", "0 4px 20px rgba(0,0,0,0.1)")

css.MediaQuery("(max-width: 768px)", ".card { padding: 16px; }")

print(css.Build())
```

### Helpers estáticos

```python
CSSBuilder.Px(16)       # "16px"
CSSBuilder.Rem(1.5)     # "1.5rem"
CSSBuilder.Pct(100)     # "100%"

CSSBuilder.DictToInline({"color": "red", "font-weight": "bold"})
# "color: red; font-weight: bold"

CSSBuilder.Merge({"color": "red"}, {"padding": "8px"})
# {"color": "red", "padding": "8px"}
```

---

## Easing

Funções de easing matemático para uso em animações e interpolações.

```python
from renderiz import Easing

# Interpolar entre dois valores
valor = Easing.Interpolate(Start=0, End=100, T=0.5, Fn=Easing.EaseInOut)

# Usar diretamente
progresso = Easing.EaseOutCubic(0.75)
```

### Funções disponíveis

| Função            | Característica                        |
|-------------------|---------------------------------------|
| `Linear`          | Velocidade constante                  |
| `EaseIn`          | Começa devagar, acelera               |
| `EaseOut`         | Começa rápido, desacelera             |
| `EaseInOut`       | Suave nos dois extremos               |
| `EaseInCubic`     | EaseIn mais pronunciado               |
| `EaseOutCubic`    | EaseOut mais pronunciado              |
| `EaseInOutCubic`  | EaseInOut cúbico                      |
| `EaseInQuart`     | Aceleração muito forte                |
| `EaseOutQuart`    | Desaceleração muito forte             |
| `EaseInElastic`   | Elástico na entrada                   |
| `EaseOutElastic`  | Elástico na saída                     |
| `EaseOutBounce`   | Quicada na chegada                    |
| `Spring`          | Mola física (Stiffness + Damping)     |

---

## Exemplo completo

```python
from renderiz import BaseComponent, H, WebRenderer, Transition
import os

class Badge(BaseComponent):
    def Render(self):
        Label = self.Props.get("Label", "")
        return H(
            "span",
            {"style": {"background": "#6366f1", "color": "#fff",
                       "padding": "2px 10px", "border-radius": "999px"}},
            Label,
        )

class Cartao(BaseComponent):
    def Render(self):
        Titulo = self.Props.get("Titulo", "")
        Descricao = self.Props.get("Descricao", "")
        Tag = self.Props.get("Tag", None)

        Filhos = [
            H("h3", {}, Titulo),
            H("p", {"style": {"color": "#6b7280"}}, Descricao),
        ]
        if Tag:
            Filhos.append(Badge({"Label": Tag}))

        return H(
            "div",
            {"lazy": True, "animation": "SlideInUp",
             "style": {"background": "#fff", "border-radius": "12px", "padding": "24px"}},
            *Filhos,
        )

class App(BaseComponent):
    def Render(self):
        return H(
            "div",
            {"style": {"padding": "40px", "background": "#f8fafc", "min-height": "100vh"}},
            H("h1", {"animation": "FadeIn", "style": {"color": "#1e1e2e"}}, "Renderiz"),
            Cartao({"Titulo": "Virtual DOM", "Descricao": "Diffing eficiente.", "Tag": "Core"}),
            Cartao({"Titulo": "Animações",   "Descricao": "11 presets prontos.", "Tag": "Animation"}),
        )

renderer = WebRenderer(Title="Demo Renderiz")
html = renderer.Render(App())

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("HTML gerado: index.html")
```

---

## Estrutura do projeto

```
renderiz/
├── Core/           # VNode, VirtualDOM, DiffPatcher, Renderer base
├── Components/     # BaseComponent, Props, Lifecycle, Registry
├── Animation/      # AnimationEngine, Keyframe, Transition, Easing
├── Performance/    # LazyLoader, Scheduler, Memoizer
├── Platform/       # WebRenderer, MobileRenderer
└── Utils/          # CSSBuilder, EventEmitter
examples/
├── WebExample.py   # Exemplo completo para Web
└── MobileExample.py # Exemplo completo para Mobile
```

---

## Licença

MIT
