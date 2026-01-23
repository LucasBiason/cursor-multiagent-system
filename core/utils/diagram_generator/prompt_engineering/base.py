"""
Classes base para templates de prompts.
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class PromptTemplate:
    """Template base para prompts de geração."""
    
    algorithm_name: str
    algorithm_emoji: str
    colors: Dict[str, str]
    base_prompt: str
    
    def render(self, **kwargs) -> str:
        """Renderiza o template com os parâmetros fornecidos."""
        prompt = self.base_prompt.format(
            algorithm_name=self.algorithm_name,
            algorithm_emoji=self.algorithm_emoji,
            **self.colors,
            **kwargs
        )
        return prompt


class BaseTemplate:
    """Template base comum para todos os algoritmos."""
    
    TEMPLATE_STRUCTURE = """
Crie um diagrama visual simples e claro para o algoritmo {algorithm_name} ({algorithm_emoji}).

ESTILO VISUAL:
- Design limpo e minimalista, adequado para notebooks Jupyter
- Não muito elaborado, sem elementos decorativos excessivos
- Foco na clareza e didática
- Estilo técnico profissional

PALETA DE CORES:
- Cor principal: {primary}
- Cor secundária: {secondary}
- Cor de destaque: {accent}
- Cor de sucesso/ordenado: {success}
- Fundo: {background}

ESPECIFICAÇÕES TÉCNICAS:
- Resolução: 1920x1080px
- Formato: PNG
- Qualidade: Alta
- Sem marca d'água
- Sem elementos de branding externo
- Otimizado para exibição em notebooks

{content_specific}
"""
    
    @classmethod
    def render(cls, algorithm_name: str, algorithm_emoji: str, colors: Dict[str, str], content_specific: str) -> str:
        """Renderiza o template base com os parâmetros fornecidos."""
        return cls.TEMPLATE_STRUCTURE.format(
            algorithm_name=algorithm_name,
            algorithm_emoji=algorithm_emoji,
            primary=colors.get("primary", "#3B82F6"),
            secondary=colors.get("secondary", "#10B981"),
            accent=colors.get("accent", "#F59E0B"),
            success=colors.get("success", "#10B981"),
            background=colors.get("background", "#FFFFFF"),
            content_specific=content_specific
        )


