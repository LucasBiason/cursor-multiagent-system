"""
Classe abstrata base para geradores de imagens.
"""

from abc import ABC, abstractmethod
from pathlib import Path
import logging

from scripts.diagram_generator.config import DiagramConfig

logger = logging.getLogger(__name__)


class ImageGenerator(ABC):
    """Classe abstrata base para geradores de imagens."""
    
    def __init__(self, config: DiagramConfig):
        self.config = config
    
    @abstractmethod
    def generate(self, prompt: str, output_path: Path) -> bool:
        """
        Gera uma imagem a partir de um prompt.
        
        Args:
            prompt: Texto descritivo da imagem
            output_path: Caminho onde salvar a imagem
            
        Returns:
            True se sucesso, False caso contrário
        """
        pass
    
    def validate_config(self) -> bool:
        """Valida se a configuração está correta."""
        if not self.config.api_key:
            logger.error("API key não configurada")
            return False
        return True

