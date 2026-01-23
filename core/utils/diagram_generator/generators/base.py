"""
Classe abstrata base para geradores de imagens.

Este módulo define a interface comum para todos os geradores de imagens
usando APIs de IA (OpenAI DALL-E, Google Gemini, etc.).
"""

from abc import ABC, abstractmethod
from pathlib import Path
import logging

from core.utils.diagram_generator.config import DiagramConfig

logger = logging.getLogger(__name__)


class ImageGenerator(ABC):
    """
    Classe abstrata base para geradores de imagens.
    
    Todas as implementações de geradores devem herdar desta classe
    e implementar o método `generate()`.
    """
    
    def __init__(self, config: DiagramConfig) -> None:
        """
        Inicializa o gerador com a configuração fornecida.
        
        Args:
            config: Configuração para geração de diagramas
        """
        self.config = config
    
    @abstractmethod
    def generate(self, prompt: str, output_path: Path) -> bool:
        """
        Gera uma imagem a partir de um prompt.
        
        Args:
            prompt: Texto descritivo da imagem a ser gerada
            output_path: Caminho onde salvar a imagem gerada
            
        Returns:
            True se a geração foi bem-sucedida, False caso contrário
        """
        pass
    
    def validate_config(self) -> bool:
        """
        Valida se a configuração está correta.
        
        Returns:
            True se a configuração é válida, False caso contrário
        """
        if not self.config.api_key:
            logger.error("API key não configurada. Configure GEMINI_API_KEY ou OPENAI_API_KEY")
            return False
        return True
