"""
Gerador de imagens usando OpenAI DALL-E API.
"""

import requests
from pathlib import Path
import logging

from .base import ImageGenerator
from scripts.diagram_generator.config import DiagramConfig

logger = logging.getLogger(__name__)


class OpenAIDALLEGenerator(ImageGenerator):
    """Gerador usando OpenAI DALL-E API."""
    
    def __init__(self, config: DiagramConfig):
        super().__init__(config)
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=config.api_key)
        except ImportError:
            logger.error("Biblioteca openai não instalada. Execute: pip install openai")
            self.client = None
    
    def generate(self, prompt: str, output_path: Path) -> bool:
        """Gera imagem usando OpenAI DALL-E."""
        if not self.validate_config() or not self.client:
            return False
        
        try:
            logger.info("Gerando imagem com DALL-E...")
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size=f"{self.config.width}x{self.config.height}",
                quality="hd" if self.config.quality == "high" else "standard",
                n=1
            )
            
            image_url = response.data[0].url
            
            # Download da imagem
            img_response = requests.get(image_url)
            img_response.raise_for_status()
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_bytes(img_response.content)
            
            logger.info(f"✅ Imagem salva em: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao gerar imagem: {e}")
            return False

