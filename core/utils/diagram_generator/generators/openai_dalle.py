"""
Gerador de imagens usando OpenAI DALL-E API.

Este módulo implementa a geração de diagramas ilustrativos usando
a API do OpenAI DALL-E 3.
"""

import requests
from pathlib import Path
import logging
from typing import Optional, Any

from .base import ImageGenerator
from core.utils.diagram_generator.config import DiagramConfig

logger = logging.getLogger(__name__)


class OpenAIDALLEGenerator(ImageGenerator):
    """
    Gerador de imagens usando OpenAI DALL-E API.
    
    Requer a biblioteca `openai` instalada:
        pip install openai
    """
    
    def __init__(self, config: DiagramConfig) -> None:
        """
        Inicializa o gerador DALL-E.
        
        Args:
            config: Configuração para geração de diagramas
        """
        super().__init__(config)
        self.client: Optional[Any] = None
        self._initialize_client()
    
    def _initialize_client(self) -> None:
        """Inicializa o cliente OpenAI."""
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=self.config.api_key)
        except ImportError:
            logger.error(
                "Biblioteca openai não instalada. "
                "Execute: pip install openai"
            )
            self.client = None
        except Exception as e:
            logger.error(f"Erro ao inicializar cliente OpenAI: {e}")
            self.client = None
    
    def generate(self, prompt: str, output_path: Path) -> bool:
        """
        Gera imagem usando OpenAI DALL-E.
        
        Args:
            prompt: Texto descritivo da imagem
            output_path: Caminho onde salvar a imagem
            
        Returns:
            True se a geração foi bem-sucedida, False caso contrário
        """
        if not self.validate_config() or not self.client:
            return False
        
        try:
            logger.info("Gerando imagem com DALL-E 3...")
            
            # DALL-E 3 suporta apenas tamanhos específicos
            size = self._get_dalle_size()
            
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size=size,
                quality="hd" if self.config.quality == "high" else "standard",
                n=1
            )
            
            image_url = response.data[0].url
            
            # Download da imagem
            img_response = requests.get(image_url, timeout=30)
            img_response.raise_for_status()
            
            # Criar diretório se não existir
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_bytes(img_response.content)
            
            logger.info(f"✅ Imagem salva em: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao gerar imagem com DALL-E: {e}")
            return False
    
    def _get_dalle_size(self) -> str:
        """
        Converte dimensões para tamanhos suportados pelo DALL-E 3.
        
        DALL-E 3 suporta apenas: "1024x1024", "1792x1024", "1024x1792"
        
        Returns:
            Tamanho suportado mais próximo
        """
        width, height = self.config.width, self.config.height
        
        # DALL-E 3 tamanhos suportados
        supported_sizes = [
            "1024x1024",
            "1792x1024",  # Landscape
            "1024x1792",  # Portrait
        ]
        
        # Se for exatamente um tamanho suportado, usar
        size_str = f"{width}x{height}"
        if size_str in supported_sizes:
            return size_str
        
        # Caso contrário, usar o mais próximo
        # Preferir 1024x1024 para quadrados
        if abs(width - height) < 100:
            return "1024x1024"
        # Landscape
        elif width > height:
            return "1792x1024"
        # Portrait
        else:
            return "1024x1792"
