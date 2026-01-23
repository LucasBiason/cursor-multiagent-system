#!/usr/bin/env python3
"""
Script CLI para geração de diagramas ilustrativos usando APIs de IA.

Uso:
    python -m core.utils.diagram_generator.main \
        --prompt "Crie um diagrama..." \
        --output-filename diagram.png \
        --api-provider nano_banana
"""

import argparse
import logging
import sys
from pathlib import Path

from core.utils.diagram_generator import DiagramGenerator, DiagramConfig

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main() -> None:
    """Função principal do CLI."""
    parser = argparse.ArgumentParser(
        description="Gera diagramas ilustrativos usando APIs de IA"
    )
    
    parser.add_argument(
        "--prompt",
        type=str,
        help="Prompt para geração de imagem"
    )
    
    parser.add_argument(
        "--prompt-file",
        type=str,
        help="Arquivo contendo o prompt"
    )
    
    parser.add_argument(
        "--output-dir",
        type=str,
        help="Diretório de saída (sobrescreve configuração padrão)"
    )
    
    parser.add_argument(
        "--api-provider",
        type=str,
        choices=["nano_banana", "openai_dalle"],
        help="Provedor de API (sobrescreve configuração padrão)"
    )
    
    parser.add_argument(
        "--width",
        type=int,
        help="Largura da imagem (sobrescreve configuração padrão)"
    )
    
    parser.add_argument(
        "--height",
        type=int,
        help="Altura da imagem (sobrescreve configuração padrão)"
    )
    
    parser.add_argument(
        "--output-filename",
        type=str,
        default="diagram.png",
        help="Nome do arquivo de saída (padrão: diagram.png)"
    )
    
    args = parser.parse_args()
    
    # Criar configuração
    config = DiagramConfig.from_env(provider=args.api_provider)
    
    # Aplicar argumentos da linha de comando
    if args.output_dir:
        config.output_dir = Path(args.output_dir)
    
    if args.api_provider:
        config.api_provider = args.api_provider
    
    if args.width:
        config.width = args.width
    
    if args.height:
        config.height = args.height
    
    # Obter prompt
    prompt = None
    if args.prompt:
        prompt = args.prompt
    elif args.prompt_file:
        prompt_path = Path(args.prompt_file)
        if not prompt_path.exists():
            logger.error(f"Arquivo de prompt não encontrado: {prompt_path}")
            sys.exit(1)
        prompt = prompt_path.read_text(encoding='utf-8')
    else:
        parser.print_help()
        logger.error("É necessário fornecer --prompt ou --prompt-file")
        sys.exit(1)
    
    # Criar gerador
    try:
        generator = DiagramGenerator(config)
    except Exception as e:
        logger.error(f"Erro ao criar gerador: {e}")
        sys.exit(1)
    
    # Gerar diagrama
    logger.info("Gerando diagrama...")
    result = generator.generate_from_prompt(prompt, args.output_filename)
    success = result is not None
    
    if success:
        logger.info(f"✅ Diagrama gerado: {result}")
    else:
        logger.error("❌ Falha ao gerar diagrama")
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
