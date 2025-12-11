# Diagram Generator

Script estruturado para geração de diagramas de algoritmos de ordenação usando APIs de geração de imagens.

## 📋 Estrutura

```
diagram-generator/
├── __init__.py          # Módulo principal
├── config.py            # Configurações base
├── prompt_templates.py  # Templates de prompts
├── generators.py        # Classes geradoras
├── main.py             # Script principal
└── README.md           # Esta documentação
```

## 🚀 Uso

### Configuração

1. **Variáveis de Ambiente (arquivo .env):**
   ```bash
   GEMINI_API_KEY=sua-chave-gemini-aqui
   ```
   
   **Nota:** A chave do Gemini é a mesma para Nano Banana (Gemini 2.5 Flash Image)

2. **Ou usar OpenAI DALL-E:**
   ```bash
   export OPENAI_API_KEY="sua-chave-aqui"
   ```

### Execução

**Script Genérico (qualquer projeto):**
```bash
python -m scripts.diagram-generator.main \
    --algorithm bubble_sort \
    --output-dir ./meu_output \
    --api-provider gemini
```

**Script Específico do Projeto (programming-kb):**
```bash
cd config/studies/01-Knowledge-Bases/programming-kb
python generate_diagrams.py
```

**Nota:** O script genérico não contém templates específicos. Use o script do projeto ou forneça seus próprios templates.

## 📝 Templates de Prompts

Os templates estão baseados nos prompts ultra enxutos criados anteriormente e incluem:

- **Bubble Sort**: Tema "Bolhas Subindo"
- **Selection Sort**: Tema "Seleção e Troca"
- **Insertion Sort**: Tema "Inserção e Deslocamento"
- **Merge Sort**: Tema "Divisão e Conquista"
- **Quick Sort**: Tema "Particionamento Rápido"
- **Comparativo**: Comparação de todos os algoritmos

## ⚙️ Configurações

### DiagramConfig

Classe de configuração com parâmetros:

- `output_dir`: Diretório de saída
- `api_provider`: Provedor (nano_banana, openai_dalle)
- `width` / `height`: Dimensões da imagem
- `format`: Formato (png, jpg)
- `quality`: Qualidade (high, standard)
- `style`: Estilo (notebook_friendly, infographic, minimal)
- `color_scheme`: Esquema de cores

### Cores por Algoritmo

Cada algoritmo tem uma paleta de cores específica definida em `ALGORITHM_COLORS`.

## 🔧 Extensibilidade

### Adicionar Novo Provedor

1. Criar classe herdando de `ImageGenerator`
2. Implementar método `generate()`
3. Adicionar ao `_create_generator()` em `DiagramGenerator`

### Adicionar Novo Template

1. Criar `PromptTemplate` em `prompt_templates.py`
2. Adicionar ao dicionário `TEMPLATES`

## 📦 Dependências

```bash
pip install requests
# Para OpenAI DALL-E:
pip install openai
```

## 🎯 Exemplos de Uso Programático

```python
from scripts.diagram_generator import DiagramGenerator, DiagramConfig

# Criar configuração
config = DiagramConfig(
    output_dir=Path("./output"),
    api_provider="nano_banana",
    width=1920,
    height=1080
)

# Criar gerador
generator = DiagramGenerator(config)

# Gerar diagrama
result = generator.generate_algorithm_diagram("bubble_sort")
print(f"Diagrama salvo em: {result}")
```

## 📚 Referências

- Prompts base: `config/studies/01-Knowledge-Bases/programming-kb/PROMPTS_ULTRA_ENXUTOS.md`
- Notebooks: `Projetos/programming-knowledge-base/Sorting-Algorithms/`

