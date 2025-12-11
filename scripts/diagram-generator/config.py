"""
Configurações base para geração de diagramas.
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, field


@dataclass
class DiagramConfig:
    """Configurações base para geração de diagramas."""
    
    # Diretórios
    # output_dir pode ser definido via variável de ambiente DIAGRAM_OUTPUT_DIR
    # ou será definido dinamicamente no __post_init__
    output_dir: Path = None
    templates_dir: Path = Path(__file__).parent / "templates"
    
    # API Configuration
    api_provider: str = "nano_banana"  # nano_banana (Gemini 2.5 Flash Image), openai_dalle, stable_diffusion
    api_key: str = field(default_factory=lambda: os.getenv("GEMINI_API_KEY", os.getenv("NANO_BANANA_API_KEY", "")))
    api_url: str = field(default_factory=lambda: os.getenv("NANO_BANANA_API_URL", "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent"))
    
    # Image Specifications
    width: int = 1920
    height: int = 1080
    format: str = "png"
    quality: str = "high"
    
    # Generation Parameters
    num_variations: int = 1
    seed: Optional[int] = None
    
    def __post_init__(self):
        """Inicializa valores padrão se não fornecidos."""
        if self.output_dir is None:
            # Tenta pegar do env, senão usa diretório atual relativo ao script
            env_dir = os.getenv("DIAGRAM_OUTPUT_DIR")
            if env_dir:
                self.output_dir = Path(env_dir)
            else:
                # Usa diretório de output relativo ao script
                script_dir = Path(__file__).resolve().parent
                self.output_dir = script_dir / "output"
        
        if self.templates_dir is None:
            self.templates_dir = Path(__file__).parent / "templates"
        
        # Garantir que são Path objects
        if isinstance(self.output_dir, str):
            self.output_dir = Path(self.output_dir)
        if isinstance(self.templates_dir, str):
            self.templates_dir = Path(self.templates_dir)
    
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
    def from_env(cls) -> "DiagramConfig":
        """Cria configuração a partir de variáveis de ambiente."""
        config = cls()
        
        # Override com variáveis de ambiente se existirem
        if os.getenv("DIAGRAM_OUTPUT_DIR"):
            config.output_dir = Path(os.getenv("DIAGRAM_OUTPUT_DIR"))
        
        if os.getenv("DIAGRAM_API_PROVIDER"):
            config.api_provider = os.getenv("DIAGRAM_API_PROVIDER")
        
        if os.getenv("DIAGRAM_WIDTH"):
            config.width = int(os.getenv("DIAGRAM_WIDTH"))
        
        if os.getenv("DIAGRAM_HEIGHT"):
            config.height = int(os.getenv("DIAGRAM_HEIGHT"))
        
        return config


