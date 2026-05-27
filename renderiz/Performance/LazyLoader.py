from __future__ import annotations

from typing import Optional

from ..Core.VNode import VNode


class LazyLoader:
    _LazyAttr = "data-lazy"
    _PlaceholderClass = "rz-lazy-placeholder"
    _LoadedClass = "rz-lazy-loaded"

    def MarkLazy(self, Node: VNode, Placeholder: Optional[str] = None) -> VNode:
        Clone = Node.Clone()
        Clone.Props[self._LazyAttr] = "true"
        if Placeholder:
            Clone.Props["data-placeholder"] = Placeholder
        return Clone

    def GenerateScript(self) -> str:
        return (
            "(function() {\n"
            "  var lazies = document.querySelectorAll('[data-lazy]');\n"
            "  if (!lazies.length) return;\n"
            "  var observer = new IntersectionObserver(function(entries) {\n"
            "    entries.forEach(function(entry) {\n"
            "      if (!entry.isIntersecting) return;\n"
            "      var el = entry.target;\n"
            "      el.classList.add('rz-lazy-loaded');\n"
            "      el.classList.remove('rz-lazy-placeholder');\n"
            "      el.removeAttribute('data-lazy');\n"
            "      observer.unobserve(el);\n"
            "    });\n"
            "  }, { threshold: 0.1, rootMargin: '50px' });\n"
            "  lazies.forEach(function(el) {\n"
            "    el.classList.add('rz-lazy-placeholder');\n"
            "    observer.observe(el);\n"
            "  });\n"
            "})();"
        )

    def GenerateStyles(self) -> str:
        return (
            ".rz-lazy-placeholder {\n"
            "  opacity: 0;\n"
            "  transform: translateY(12px);\n"
            "  transition: opacity 0.4s ease, transform 0.4s ease;\n"
            "}\n"
            ".rz-lazy-loaded {\n"
            "  opacity: 1;\n"
            "  transform: translateY(0);\n"
            "}"
        )
