# Diagram Generator

Sistema para geração de diagramas ilustrativos usando APIs de IA (OpenAI DALL-E e Google Gemini).

## 📋 Visão Geral

Este módulo fornece uma interface unificada para gerar diagramas ilustrativos usando APIs de geração de imagens. É útil para criar diagramas conceituais, ilustrações de algoritmos, fluxos visuais e outros diagramas que não se encaixam em formatos técnicos como Mermaid ou PlantUML.

## 🚀 Instalação

### Dependências

```bash
# Para OpenAI DALL-E
pip install openai requests

# Para Google Gemini
pip install google-genai requests
```

### Variáveis de Ambiente

```bash
# Para Gemini (Nano Banana)
export GEMINI_API_KEY="sua-chave-aqui"

# Para OpenAI DALL-E
export OPENAI_API_KEY="sua-chave-aqui"

# Opcional: Configurar diretório de saída
export DIAGRAM_OUTPUT_DIR="./output"
export DIAGRAM_API_PROVIDER="nano_banana"  # ou "openai_dalle"
```

## 💻 Uso

### Uso Programático

```python
from core.utils.diagram_generator import DiagramGenerator, DiagramConfig
from pathlib import Path

# Criar configuração
config = DiagramConfig.from_env(provider="nano_banana")
config.output_dir = Path("./diagrams")
config.width = 1920
config.height = 1080

# Criar gerador
generator = DiagramGenerator(config)

# Gerar diagrama
result = generator.generate_from_prompt(
    "Diagrama ilustrativo de algoritmo de ordenação bubble sort. "
    "Mostre bolhas subindo, estilo minimalista, cores vibrantes.",
    "bubble_sort.png"
)

if result:
    print(f"✅ Diagrama salvo em: {result}")
```

### Uso via CLI

```bash
# Usando Gemini
python -m core.utils.diagram_generator.main \
    --prompt "Diagrama ilustrativo de algoritmo de ordenação" \
    --output-filename diagram.png \
    --api-provider nano_banana

# Usando OpenAI DALL-E
python -m core.utils.diagram_generator.main \
    --prompt "Diagrama ilustrativo de algoritmo de ordenação" \
    --output-filename diagram.png \
    --api-provider openai_dalle
```

## 📝 Estrutura

```
core/utils/diagram_generator/
├── __init__.py              # Exports principais
├── config.py                # DiagramConfig
├── generators/
│   ├── __init__.py
│   ├── base.py              # ImageGenerator (classe abstrata)
│   ├── gemini.py            # GeminiImageGenerator
│   ├── openai_dalle.py      # OpenAIDALLEGenerator
│   └── diagram_generator.py # DiagramGenerator (orquestrador)
└── README.md                # Esta documentação
```

## 🎨 Provedores Suportados

### Google Gemini (Nano Banana)

- **Modelo:** `gemini-2.5-flash-image`
- **Variável de ambiente:** `GEMINI_API_KEY`
- **Vantagens:** Gratuito (com limites), rápido, boa qualidade
- **Limitações:** Tamanhos de imagem podem variar

### OpenAI DALL-E

- **Modelo:** `dall-e-3`
- **Variável de ambiente:** `OPENAI_API_KEY`
- **Vantagens:** Alta qualidade, tamanhos consistentes
- **Limitações:** Pago, tamanhos limitados (1024x1024, 1792x1024, 1024x1792)

## 📚 Exemplos de Prompts

### Algoritmos de Ordenação

```
"Diagrama ilustrativo de algoritmo bubble sort. Mostre bolhas subindo, 
estilo minimalista, cores vibrantes, fundo branco."
```

### Arquitetura de Sistema

```
"Diagrama ilustrativo de arquitetura de microsserviços. Mostre serviços 
conectados, estilo flat design, cores modernas."
```

### Fluxo de Dados

```
"Diagrama ilustrativo de fluxo de dados ETL. Mostre funil recebendo dados, 
transformando e enviando para banco, estilo infográfico."
```

## 🔧 Configuração Avançada

```python
from core.utils.diagram_generator import DiagramConfig, DiagramGenerator

config = DiagramConfig(
    output_dir=Path("./output"),
    api_provider="nano_banana",
    width=1920,
    height=1080,
    format="png",
    quality="high"
)

generator = DiagramGenerator(config)
```

## ⚠️ Limitações

1. **Custos:** APIs de geração de imagens podem ter custos associados
2. **Tamanhos:** DALL-E tem tamanhos limitados
3. **Qualidade:** Resultados podem variar dependendo do prompt
4. **Rate Limits:** APIs têm limites de requisições

## 📖 Referências

- **Skill:** `skills/documentation/diagram-generation/SKILL.md`
- **OpenAI DALL-E:** https://platform.openai.com/docs/guides/images
- **Google Gemini:** https://ai.google.dev/docs
