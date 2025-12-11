"""
Gerador de imagens usando Gemini API (Nano Banana / Gemini 2.5 Flash Image).
"""

import base64
import requests
from pathlib import Path
import logging

from .base import ImageGenerator
from scripts.diagram_generator.config import DiagramConfig

logger = logging.getLogger(__name__)


class GeminiImageGenerator(ImageGenerator):
    """Gerador usando Gemini API (Nano Banana / Gemini 2.5 Flash Image)."""
    
    def __init__(self, config: DiagramConfig):
        super().__init__(config)
        self.api_key = config.api_key
        self.model = config.model
        
        # Tentar importar biblioteca do Gemini
        try:
            from google import genai
            from google.genai import types
            self.genai = genai
            self.types = types
            self.client = None
        except ImportError:
            logger.error("Biblioteca google-genai não instalada. Execute: pip install google-genai")
            self.genai = None
            self.types = None
            self.client = None
    
    def _initialize_client(self):
        """Inicializa cliente Gemini."""
        if self.genai is None:
            return False
        
        try:
            self.client = self.genai.Client(api_key=self.api_key)
            return True
        except Exception as e:
            logger.error(f"Erro ao inicializar cliente Gemini: {e}")
            return False
    
    def generate(self, prompt: str, output_path: Path) -> bool:
        """Gera imagem usando Gemini API."""
        if not self.validate_config():
            return False
        
        if self.genai is None or self.types is None:
            logger.error("Biblioteca Gemini não disponível")
            return False
        
        try:
            if self.client is None:
                if not self._initialize_client():
                    return False
            
            logger.info(f"Gerando imagem com Gemini ({self.model})...")
            
            # Configuração para geração de imagens
            generate_config = self.types.GenerateContentConfig(
                temperature=0.7,
                top_p=0.95,
                max_output_tokens=8192,
                response_modalities=["IMAGE"],  # Solicitar imagem como resposta
            )
            
            # Gerar conteúdo (imagem)
            response = self.client.models.generate_content(
                model=self.model,
                contents=[prompt],
                config=generate_config,
            )
            
            # Extrair imagem da resposta
            if hasattr(response, 'candidates') and response.candidates:
                candidate = response.candidates[0]
                if hasattr(candidate, 'content') and candidate.content:
                    parts = candidate.content.parts
                    for part in parts:
                        if hasattr(part, 'inline_data'):
                            # Imagem em base64
                            image_data = base64.b64decode(part.inline_data.data)
                            output_path.parent.mkdir(parents=True, exist_ok=True)
                            output_path.write_bytes(image_data)
                            logger.info(f"✅ Imagem salva em: {output_path}")
                            return True
                        elif hasattr(part, 'file_data'):
                            # URL da imagem
                            file_uri = part.file_data.file_uri
                            img_response = requests.get(file_uri)
                            img_response.raise_for_status()
                            output_path.parent.mkdir(parents=True, exist_ok=True)
                            output_path.write_bytes(img_response.content)
                            logger.info(f"✅ Imagem salva em: {output_path}")
                            return True
            
            logger.error("Resposta da API não contém imagem")
            return False
            
        except Exception as e:
            logger.error(f"Erro ao gerar imagem: {e}")
            return False

