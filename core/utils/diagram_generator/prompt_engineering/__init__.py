"""
Prompt Engineering Module

Este módulo contém ferramentas e templates para engenharia de prompts,
seguindo as melhores práticas para projetos Generative AI.

Estrutura:
- templates/ - Templates de prompts específicos
- chainer.py - Encadeamento de prompts
- few_shot.py - Exemplos few-shot
- base.py - Classes base e utilitários
"""

from .base import PromptTemplate, BaseTemplate
from .chainer import PromptChainer
from .few_shot import FewShotExamples

__all__ = [
    "PromptTemplate",
    "BaseTemplate",
    "PromptChainer",
    "FewShotExamples",
]


