"""
Configurações base para geração de diagramas ilustrativos usando APIs de IA.

Este módulo fornece a classe DiagramConfig para configurar a geração de diagramas
usando OpenAI DALL-E ou Google Gemini (Nano Banana).
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, field


@dataclass
class DiagramConfig:
    """
    Configurações para geração de diagramas ilustrativos.
    
    Attributes:
        output_dir: Diretório onde salvar os diagramas gerados
        api_provider: Provedor de API ("nano_banana" ou "openai_dalle")
        api_key: Chave de API (carregada automaticamente de variáveis de ambiente)
        width: Largura da imagem em pixels (padrão: 1024)
        height: Altura da imagem em pixels (padrão: 1024)
        format: Formato da imagem ("png" ou "jpg")
        quality: Qualidade da imagem ("high" ou "standard")
    """
    
    # Diretórios
    output_dir: Optional[Path] = None
    
    # API Configuration
    api_provider: str = "nano_banana"  # "nano_banana" ou "openai_dalle"
    api_key: str = ""
    
    # Image Specifications
    width: int = 1024
    height: int = 1024
    format: str = "png"
    quality: str = "standard"
    
    def __post_init__(self) -> None:
        """Inicializa valores padrão se não fornecidos."""
        self.refresh_api_key()
        
        if self.output_dir is None:
            env_dir = os.getenv("DIAGRAM_OUTPUT_DIR")
            if env_dir:
                self.output_dir = Path(env_dir)
            else:
                # Usar diretório atual/output como padrão
                self.output_dir = Path.cwd() / "output"
        
        if isinstance(self.output_dir, str):
            self.output_dir = Path(self.output_dir)
    
    def refresh_api_key(self) -> None:
        """Atualiza a chave de API baseada no provedor atual."""
        provider = self.api_provider.lower()
        if provider in ["nano_banana", "gemini"]:
            self.api_key = os.getenv("GEMINI_API_KEY") or os.getenv("NANO_BANANA_API_KEY", "")
        elif provider == "openai_dalle":
            self.api_key = os.getenv("OPENAI_API_KEY", "")

    def to_dict(self) -> Dict[str, Any]:
        """Converte configuração para dicionário."""
        return {
            "output_dir": str(self.output_dir),
            "api_provider": self.api_provider,
            "width": self.width,
            "height": self.height,
            "format": self.format,
            "quality": self.quality,
        }
    
    @classmethod
    def from_env(cls, provider: Optional[str] = None) -> "DiagramConfig":
        """
        Cria configuração a partir de variáveis de ambiente.
        
        Args:
            provider: Provedor de API ("nano_banana" ou "openai_dalle").
                     Se None, usa DIAGRAM_API_PROVIDER ou "nano_banana" como padrão.
        
        Returns:
            DiagramConfig configurado com valores do ambiente.
        """
        if provider is None:
            provider = os.getenv("DIAGRAM_API_PROVIDER", "nano_banana")
        
        config = cls(api_provider=provider)
        
        if os.getenv("DIAGRAM_OUTPUT_DIR"):
            config.output_dir = Path(os.getenv("DIAGRAM_OUTPUT_DIR"))
        
        if os.getenv("DIAGRAM_WIDTH"):
            config.width = int(os.getenv("DIAGRAM_WIDTH"))
        
        if os.getenv("DIAGRAM_HEIGHT"):
            config.height = int(os.getenv("DIAGRAM_HEIGHT"))
        
        return config
