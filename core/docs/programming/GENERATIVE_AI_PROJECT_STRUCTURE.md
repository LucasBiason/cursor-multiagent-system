# Estrutura de Projetos Generative AI

**Fonte:** Generative AI Project Structure - Brij Kishore Pandey

Este documento descreve a estrutura recomendada e melhores práticas para projetos de Generative AI, seguindo padrões profissionais de organização e manutenibilidade.

---

## 📁 Estrutura de Diretórios

```
generative_ai_project/
├── config/                      # Configurações separadas do código
│   ├── __init__.py
│   ├── model_config.yaml        # Configurações de modelos
│   ├── prompt_templates.yaml    # Templates de prompts
│   └── logging_config.yaml      # Configurações de logging
│
├── src/                         # Código fonte principal
│   ├── llm/                     # Clientes LLM
│   │   ├── __init__.py
│   │   ├── base.py              # Classe base abstrata
│   │   ├── claude_client.py     # Cliente Claude
│   │   ├── gpt_client.py        # Cliente GPT
│   │   └── utils.py              # Utilitários LLM
│   │
│   ├── prompt_engineering/      # Engenharia de prompts
│   │   ├── __init__.py
│   │   ├── templates.py         # Templates de prompts
│   │   ├── few_shot.py          # Exemplos few-shot
│   │   └── chainer.py           # Encadeamento de prompts
│   │
│   ├── utils/                   # Utilitários gerais
│   │   ├── __init__.py
│   │   ├── rate_limiter.py      # Rate limiting para APIs
│   │   ├── token_counter.py     # Contagem de tokens
│   │   ├── cache.py             # Sistema de cache
│   │   └── logger.py            # Sistema de logging
│   │
│   └── handlers/                # Handlers de erro
│       ├── __init__.py
│       └── error_handler.py     # Tratamento de erros
│
├── data/                        # Dados organizados
│   ├── cache/                   # Cache de respostas
│   ├── prompts/                  # Prompts armazenados
│   ├── outputs/                 # Saídas geradas
│   └── embeddings/               # Embeddings armazenados
│
├── examples/                    # Exemplos de uso
│   ├── basic_completion.py      # Exemplo básico
│   ├── chat_session.py          # Sessão de chat
│   └── chain_prompts.py         # Encadeamento de prompts
│
├── notebooks/                   # Jupyter notebooks
│   ├── prompt_testing.ipynb     # Testes de prompts
│   ├── response_analysis.ipynb  # Análise de respostas
│   └── model_experimentation.ipynb  # Experimentação
│
├── requirements.txt             # Dependências Python
├── setup.py                     # Setup do projeto
├── README.md                    # Documentação principal
└── Dockerfile                   # Containerização
```

---

## 🎯 Componentes Principais

### `config/` - Configurações

**Propósito:** Separar configurações do código, facilitando manutenção e deploy.

**Arquivos:**
- `model_config.yaml`: Configurações de modelos (temperatura, max_tokens, etc.)
- `prompt_templates.yaml`: Templates de prompts reutilizáveis
- `logging_config.yaml`: Configurações de logging

**Benefícios:**
- ✅ Fácil alteração sem modificar código
- ✅ Suporte a múltiplos ambientes (dev, prod)
- ✅ Versionamento de configurações

### `src/` - Código Fonte

**Propósito:** Código modular e organizado por responsabilidade.

#### `llm/` - Clientes LLM

- **`base.py`**: Interface abstrata para todos os clientes LLM
- **`claude_client.py`**: Implementação específica do Claude
- **`gpt_client.py`**: Implementação específica do GPT
- **`utils.py`**: Funções auxiliares (formatação, validação)

**Padrão:** Cada cliente implementa a interface base, garantindo consistência.

#### `prompt_engineering/` - Engenharia de Prompts

- **`templates.py`**: Templates reutilizáveis de prompts
- **`few_shot.py`**: Gerenciamento de exemplos few-shot
- **`chainer.py`**: Encadeamento de prompts para fluxos complexos

**Benefícios:**
- ✅ Reutilização de prompts
- ✅ Consistência na geração
- ✅ Fácil experimentação

#### `utils/` - Utilitários

- **`rate_limiter.py`**: Controle de taxa de requisições
- **`token_counter.py`**: Contagem e otimização de tokens
- **`cache.py`**: Cache de respostas para reduzir custos
- **`logger.py`**: Sistema de logging padronizado

#### `handlers/` - Tratamento de Erros

- **`error_handler.py`**: Tratamento centralizado de erros

### `data/` - Dados

**Organização por tipo:**
- `cache/`: Respostas em cache
- `prompts/`: Prompts salvos
- `outputs/`: Saídas geradas
- `embeddings/`: Embeddings pré-computados

### `examples/` - Exemplos

Código de exemplo demonstrando uso do framework:
- Exemplos básicos
- Casos de uso avançados
- Padrões de uso

### `notebooks/` - Experimentação

Jupyter notebooks para:
- Testes de prompts
- Análise de respostas
- Experimentação com modelos

---

## ✅ Melhores Práticas

### 1. Use YAML para Configurações

**Por quê:**
- Fácil de ler e editar
- Suporta estruturas complexas
- Padrão da indústria

**Exemplo:**
```yaml
# model_config.yaml
models:
  gpt4:
    temperature: 0.7
    max_tokens: 2000
  claude:
    temperature: 0.5
    max_tokens: 1500
```

### 2. Implemente Tratamento de Erros Adequado

**Por quê:**
- APIs podem falhar
- Rate limits podem ser atingidos
- Respostas podem ser inválidas

**Exemplo:**
```python
try:
    response = llm_client.generate(prompt)
except RateLimitError:
    # Retry com backoff
except APIError as e:
    # Log e notificar
```

### 3. Use Rate Limiting para APIs

**Por quê:**
- Evita exceder limites da API
- Reduz custos
- Melhora confiabilidade

**Implementação:**
- Decorators para rate limiting
- Filas para requisições
- Retry com backoff exponencial

### 4. Separe Clientes de Modelos

**Por quê:**
- Facilita troca de modelos
- Permite usar múltiplos modelos
- Testes mais fáceis

**Padrão:**
```python
class BaseLLMClient(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        pass

class GPTClient(BaseLLMClient):
    def generate(self, prompt: str) -> str:
        # Implementação GPT
```

### 5. Cache Resultados Apropriadamente

**Por quê:**
- Reduz custos de API
- Melhora performance
- Permite reprocessamento

**Estratégias:**
- Cache por hash do prompt
- TTL configurável
- Invalidação inteligente

### 6. Mantenha Documentação Atualizada

**Por quê:**
- Facilita onboarding
- Reduz perguntas
- Melhora manutenibilidade

**Documentar:**
- README com exemplos
- Docstrings em funções
- Comentários em código complexo

### 7. Use Notebooks para Testes

**Por quê:**
- Experimentação rápida
- Visualização de resultados
- Documentação interativa

---

## 🚀 Como Começar

### Passo 1: Clone o Repositório

```bash
git clone <repository-url>
cd generative_ai_project
```

### Passo 2: Instale Dependências

```bash
pip install -r requirements.txt
```

### Passo 3: Configure Modelos

Edite `config/model_config.yaml` com suas configurações:
- API keys
- Modelos preferidos
- Parâmetros padrão

### Passo 4: Revise Exemplos

Explore `examples/` para entender o uso:
- `basic_completion.py`: Uso básico
- `chat_session.py`: Sessões de chat
- `chain_prompts.py`: Encadeamento

### Passo 5: Comece com Notebooks

Use `notebooks/` para experimentar:
- Testar prompts
- Analisar respostas
- Experimentar modelos

---

## 💡 Dicas de Desenvolvimento

### 1. Siga Design Modular

- Separe responsabilidades
- Use interfaces abstratas
- Facilite testes unitários

### 2. Escreva Testes de Componentes

- Teste cada módulo isoladamente
- Use mocks para APIs externas
- Mantenha cobertura alta

### 3. Use Controle de Versão

- Commits frequentes
- Mensagens descritivas
- Branches para features

### 4. Mantenha Docs Atualizadas

- Atualize README
- Documente mudanças
- Adicione exemplos

### 5. Monitore Uso de API

- Track de custos
- Monitore rate limits
- Analise performance

---

## 📄 Arquivos Principais

### `requirements.txt`

Lista todas as dependências do projeto:
```txt
openai>=1.0.0
anthropic>=0.5.0
pyyaml>=6.0
requests>=2.31.0
```

### `README.md`

Documentação principal do projeto:
- Visão geral
- Instalação
- Exemplos de uso
- Contribuição

### `Dockerfile`

Containerização para deploy:
- Ambiente isolado
- Reproducibilidade
- Facilita deploy

---

## 🔄 Aplicação no Diagram Generator

Esta estrutura foi aplicada no projeto `diagram-generator`:

```
diagram-generator/
├── prompt_engineering/          # ✅ Implementado
│   ├── base.py                 # Classes base
│   ├── chainer.py              # Encadeamento
│   ├── few_shot.py             # Few-shot examples
│   └── templates/             # Templates específicos
│       └── diagram_base.py    # Template base
│
├── generators/                 # Clientes de geração
│   ├── base.py                 # Interface base
│   ├── gemini.py              # Cliente Gemini
│   └── openai_dalle.py        # Cliente DALL-E
│
└── config.py                  # Configurações
```

---

**Última Atualização:** 2025-12-10  
**Fonte:** Generative AI Project Structure - Brij Kishore Pandey

