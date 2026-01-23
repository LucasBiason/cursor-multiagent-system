"""
Diagram Generator - Geração de diagramas ilustrativos usando APIs de IA.

Este módulo fornece ferramentas para gerar diagramas ilustrativos usando
OpenAI DALL-E ou Google Gemini (Nano Banana).

Uso básico:
    ```python
    from core.utils.diagram_generator import DiagramGenerator, DiagramConfig
    
    config = DiagramConfig.from_env(provider="nano_banana")
    generator = DiagramGenerator(config)
    
    result = generator.generate_from_prompt(
        "Diagrama ilustrativo de algoritmo de ordenação",
        "diagram.png"
    )
    ```
"""

from core.utils.diagram_generator.config import DiagramConfig
from core.utils.diagram_generator.generators import DiagramGenerator

__all__ = [
    "DiagramConfig",
    "DiagramGenerator",
]
