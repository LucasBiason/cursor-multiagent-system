# Changelog - Refatoração para Script Genérico

## Mudanças Realizadas

### 1. Removidos Paths Hardcoded
- ✅ `output_dir` agora é opcional e pode ser passado no construtor ou via env
- ✅ Usa `Path.cwd() / "output"` como padrão se não especificado
- ✅ Suporta `DIAGRAM_OUTPUT_DIR` via variável de ambiente

### 2. Configurações Específicas Movidas
- ✅ `ALGORITHM_COLORS` movido para `config/studies/01-Knowledge-Bases/programming-kb/diagram_config.py`
- ✅ Templates específicos movidos para `config/studies/01-Knowledge-Bases/programming-kb/diagram_prompts.py`
- ✅ Script genérico agora apenas contém integração e prompts base

### 3. Atualização para Gemini API
- ✅ Usa `GEMINI_API_KEY` (mesma chave do Gemini)
- ✅ Classe renomeada de `NanoBananaGenerator` para `GeminiImageGenerator`
- ✅ Usa biblioteca `google-genai` oficial
- ✅ Modelo padrão: `gemini-2.5-flash-image`

### 4. Estrutura Genérica
- ✅ `config.py`: Apenas configurações genéricas
- ✅ `prompt_templates.py`: Apenas estrutura base de templates
- ✅ `generators.py`: Apenas integração com APIs
- ✅ Configurações específicas em arquivos externos

## Como Usar

### Script Genérico (qualquer projeto)
```python
from scripts.diagram_generator import DiagramConfig, DiagramGenerator

config = DiagramConfig(
    output_dir=Path("./meu_output"),  # Dinâmico!
    api_provider="gemini"
)

generator = DiagramGenerator(config)
generator.generator.generate("meu prompt", Path("./imagem.png"))
```

### Script Específico do Projeto
```bash
cd config/studies/01-Knowledge-Bases/programming-kb
python generate_diagrams.py
```

## Arquivos Criados

1. `config/studies/01-Knowledge-Bases/programming-kb/diagram_config.py` - Cores e paths específicos
2. `config/studies/01-Knowledge-Bases/programming-kb/diagram_prompts.py` - Templates específicos
3. `config/studies/01-Knowledge-Bases/programming-kb/generate_diagrams.py` - Script wrapper do projeto


