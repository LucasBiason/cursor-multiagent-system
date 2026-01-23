"""
Classe principal para geração de diagramas ilustrativos.

Este módulo orquestra diferentes geradores de imagens (OpenAI DALL-E, Google Gemini)
para criar diagramas ilustrativos usando APIs de IA.
"""

from pathlib import Path
from typing import Optional
import logging

from .base import ImageGenerator
from .gemini import GeminiImageGenerator
from .openai_dalle import OpenAIDALLEGenerator
from core.utils.diagram_generator.config import DiagramConfig

logger = logging.getLogger(__name__)


class DiagramGenerator:
    """
    Classe principal para geração de diagramas ilustrativos.
    
    Esta classe orquestra diferentes provedores de API (OpenAI DALL-E, Google Gemini)
    para gerar diagramas a partir de prompts textuais.
    
    Exemplo:
        ```python
        from core.utils.diagram_generator import DiagramGenerator, DiagramConfig
        
        config = DiagramConfig.from_env(provider="nano_banana")
        generator = DiagramGenerator(config)
        
        result = generator.generate_from_prompt(
            "Diagrama ilustrativo de algoritmo de ordenação bubble sort",
            "bubble_sort.png"
        )
        ```
    """
    
    def __init__(self, config: Optional[DiagramConfig] = None) -> None:
        """
        Inicializa o gerador de diagramas.
        
        Args:
            config: Configuração para geração. Se None, usa DiagramConfig.from_env()
        """
        self.config = config or DiagramConfig.from_env()
        self.generator = self._create_generator()
    
    def _create_generator(self) -> ImageGenerator:
        """
        Cria o gerador apropriado baseado na configuração.
        
        Returns:
            Instância do gerador (GeminiImageGenerator ou OpenAIDALLEGenerator)
            
        Raises:
            ValueError: Se o provedor não for suportado
        """
        provider = self.config.api_provider.lower()
        
        if provider in ["nano_banana", "gemini"]:
            return GeminiImageGenerator(self.config)
        elif provider == "openai_dalle":
            return OpenAIDALLEGenerator(self.config)
        else:
            raise ValueError(
                f"Provedor não suportado: {provider}. "
                "Use 'nano_banana' ou 'openai_dalle'"
            )
    
    def generate_from_prompt(
        self,
        prompt: str,
        output_filename: str,
    ) -> Optional[Path]:
        """
        Gera diagrama a partir de um prompt fornecido.
        
        Args:
            prompt: Texto descritivo do diagrama a ser gerado
            output_filename: Nome do arquivo de saída (ex: "diagram.png")
            
        Returns:
            Caminho do arquivo gerado ou None se falhar
        """
        try:
            output_path = self.config.output_dir / output_filename
            
            logger.info(f"Gerando diagrama: {output_filename}...")
            success = self.generator.generate(prompt, output_path)
            
            if success:
                logger.info(f"✅ Diagrama gerado com sucesso: {output_path}")
                return output_path
            else:
                logger.error(f"❌ Falha ao gerar diagrama: {output_filename}")
                return None
                
        except Exception as e:
            logger.error(f"Erro ao gerar diagrama: {e}", exc_info=True)
            return None
