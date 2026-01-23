"""
Gerador de imagens usando Google Gemini API (Gemini 2.5 Flash Image).

Este módulo implementa a geração de diagramas ilustrativos usando
a API do Google Gemini para geração de imagens.
"""

import base64
import requests
from pathlib import Path
import logging
from typing import Optional, Any

from .base import ImageGenerator
from core.utils.diagram_generator.config import DiagramConfig

logger = logging.getLogger(__name__)


class GeminiImageGenerator(ImageGenerator):
    """
    Gerador de imagens usando Google Gemini API.
    
    Requer a biblioteca `google-genai` instalada:
        pip install google-genai
    """
    
    def __init__(self, config: DiagramConfig) -> None:
        """
        Inicializa o gerador Gemini.
        
        Args:
            config: Configuração para geração de diagramas
        """
        super().__init__(config)
        self.api_key = config.api_key
        self.model = config.model if hasattr(config, 'model') else "gemini-2.5-flash-image"
        
        # Tentar importar biblioteca do Gemini
        self.genai: Optional[Any] = None
        self.types: Optional[Any] = None
        self.client: Optional[Any] = None
        self._initialize_library()
    
    def _initialize_library(self) -> None:
        """Inicializa a biblioteca do Gemini."""
        try:
            from google import genai
            from google.genai import types
            self.genai = genai
            self.types = types
        except ImportError:
            logger.error(
                "Biblioteca google-genai não instalada. "
                "Execute: pip install google-genai"
            )
            self.genai = None
            self.types = None
    
    def _initialize_client(self) -> bool:
        """
        Inicializa cliente Gemini.
        
        Returns:
            True se inicializado com sucesso, False caso contrário
        """
        if self.genai is None:
            return False
        
        try:
            self.client = self.genai.Client(api_key=self.api_key)
            return True
        except Exception as e:
            logger.error(f"Erro ao inicializar cliente Gemini: {e}")
            return False
    
    def generate(self, prompt: str, output_path: Path) -> bool:
        """
        Gera imagem usando Gemini API.
        
        Args:
            prompt: Texto descritivo da imagem
            output_path: Caminho onde salvar a imagem
            
        Returns:
            True se a geração foi bem-sucedida, False caso contrário
        """
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
                response_modalities=["IMAGE"],
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
                        # Imagem em base64 ou bytes
                        if hasattr(part, 'inline_data'):
                            data = part.inline_data.data
                            if isinstance(data, str):
                                image_data = base64.b64decode(data)
                            else:
                                image_data = data
                            
                            output_path.parent.mkdir(parents=True, exist_ok=True)
                            output_path.write_bytes(image_data)
                            logger.info(f"✅ Imagem salva em: {output_path}")
                            return True
                        
                        # URL da imagem
                        elif hasattr(part, 'file_data'):
                            file_uri = part.file_data.file_uri
                            img_response = requests.get(file_uri, timeout=30)
                            img_response.raise_for_status()
                            output_path.parent.mkdir(parents=True, exist_ok=True)
                            output_path.write_bytes(img_response.content)
                            logger.info(f"✅ Imagem salva em: {output_path}")
                            return True
            
            logger.error("Resposta da API não contém imagem")
            return False
            
        except Exception as e:
            logger.error(f"Erro ao gerar imagem com Gemini: {e}")
            return False
