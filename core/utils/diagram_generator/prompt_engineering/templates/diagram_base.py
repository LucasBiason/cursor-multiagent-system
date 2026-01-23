"""
Template base para geração de diagramas de algoritmos.
"""

from typing import Dict, Any
from ..base import BaseTemplate


class DiagramBaseTemplate:
    """Template base para diagramas de algoritmos."""
    
    @staticmethod
    def create_prompt(
        algorithm_name: str,
        algorithm_emoji: str,
        colors: Dict[str, str],
        content_specific: str
    ) -> str:
        """
        Cria um prompt completo para geração de diagrama.
        
        Args:
            algorithm_name: Nome do algoritmo
            algorithm_emoji: Emoji representativo
            colors: Dicionário com cores (primary, secondary, accent, success, background)
            content_specific: Conteúdo específico do algoritmo
        
        Returns:
            Prompt formatado completo
        """
        return BaseTemplate.render(
            algorithm_name=algorithm_name,
            algorithm_emoji=algorithm_emoji,
            colors=colors,
            content_specific=content_specific
        )
    
    @staticmethod
    def get_default_colors() -> Dict[str, str]:
        """Retorna paleta de cores padrão."""
        return {
            "primary": "#3B82F6",      # Azul
            "secondary": "#10B981",     # Verde
            "accent": "#F59E0B",       # Laranja
            "success": "#10B981",      # Verde (sucesso)
            "background": "#FFFFFF"     # Branco
        }

