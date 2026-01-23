"""
Templates de prompts base para geração de diagramas.

DEPRECATED: Este módulo está sendo migrado para prompt_engineering/.
Use prompt_engineering.base.BaseTemplate e prompt_engineering.templates.diagram_base.DiagramBaseTemplate
"""

from prompt_engineering.base import BaseTemplate, PromptTemplate
from prompt_engineering.templates.diagram_base import DiagramBaseTemplate

# Manter compatibilidade com código existente
__all__ = [
    "PromptTemplate",
    "BaseTemplate",
    "DiagramBaseTemplate",
    "BASE_TEMPLATE_STRUCTURE",
]

# Alias para compatibilidade
BASE_TEMPLATE_STRUCTURE = BaseTemplate.TEMPLATE_STRUCTURE

