"""
Classe principal para geração de diagramas.
Orquestra diferentes geradores de imagens.
"""

from pathlib import Path
from typing import Optional
import logging

from .base import ImageGenerator
from .gemini import GeminiImageGenerator
from .openai_dalle import OpenAIDALLEGenerator
from scripts.diagram_generator.config import DiagramConfig

logger = logging.getLogger(__name__)


class DiagramGenerator:
    """Classe principal para geração de diagramas."""
    
    def __init__(self, config: Optional[DiagramConfig] = None):
        self.config = config or DiagramConfig.from_env()
        self.generator = self._create_generator()
    
    def _create_generator(self) -> ImageGenerator:
        """Cria o gerador apropriado baseado na configuração."""
        provider = self.config.api_provider.lower()
        
        if provider in ["nano_banana", "gemini"]:
            return GeminiImageGenerator(self.config)
        elif provider == "openai_dalle":
            return OpenAIDALLEGenerator(self.config)
        else:
            raise ValueError(f"Provedor não suportado: {provider}")
    
    def generate_from_prompt(
        self,
        prompt: str,
        output_filename: str,
    ) -> Optional[Path]:
        """
        Gera diagrama a partir de um prompt fornecido.
        
        Args:
            prompt: Texto do prompt para geração
            output_filename: Nome do arquivo de saída
            
        Returns:
            Caminho do arquivo gerado ou None se falhar
        """
        try:
            output_path = self.config.output_dir / output_filename
            
            logger.info(f"Gerando diagrama: {output_filename}...")
            success = self.generator.generate(prompt, output_path)
            
            if success:
                return output_path
            else:
                logger.error(f"Falha ao gerar diagrama: {output_filename}")
                return None
                
        except Exception as e:
            logger.error(f"Erro ao gerar diagrama: {e}")
            return None

