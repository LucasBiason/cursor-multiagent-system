# Cursor Multiagent System - Documentação

**Versão:** 1.1.0  
**Status:** Desenvolvimento Ativo

---

## 📖 sobre o projeto

**Cursor Multiagent System** é um framework de produção para sistemas coordenados de agentes de IA no Cursor IDE 2.0.

### objetivo

Fornecer uma arquitetura modular para criar e gerenciar múltiplos agentes de IA especializados que trabalham juntos para:
- Automatizar workflows
- Gerenciar tarefas
- Melhorar produtividade
- Coordenar ações entre agentes

---

## 🏗️ arquitetura

O sistema consiste em 4 agentes especializados principais:

1. **Personal Assistant** - Ponto de entrada, gerencia agenda, tarefas e workspace Notion
2. **Studies Assistant** - Ensino, orientação de projetos, expertise em programação para aprendizado
3. **Work Assistant** - Co-programação, code review, testes, automação de deploy
4. **Social Media Assistant** - Estratégia de conteúdo para StuffsCode (Instagram + YouTube)

### características principais

- **Contexto Unificado:** Todos os agentes compartilham conhecimento e estado
- **Integração Notion:** Integração profunda com workspace Notion
- **Automação de Workflows:** Tarefas em background e jobs agendados
- **Design Modular:** Fácil de estender e customizar
- **Privacidade Primeiro:** Separação clara entre dados públicos e privados

---

## 📁 estrutura do projeto

```
cursor-multiagent-system/
├── core/                    # Framework público (reutilizável)
│   ├── agents/             # Definições de agentes (.mdc)
│   ├── templates/          # Templates
│   ├── docs/               # Documentação técnica
│   │   ├── programming/    # Guias de programação
│   │   └── notion/        # Documentação Notion
│   └── utils/              # Scripts utilitários
│
├── config/                  # Configurações privadas (submódulo git)
│   ├── agents/             # Definições de agentes privados
│   ├── notion/             # Regras específicas Notion
│   ├── work/               # Contexto de trabalho
│   ├── studies/            # Contexto de estudos
│   └── system/             # Configurações do sistema
│
├── docs/                    # Documentação do projeto
│   ├── README.md           # Este arquivo
│   └── assets/             # Imagens e recursos
│
├── scripts/                 # Scripts utilitários
└── tests/                   # Suite de testes
```

---

## 🚀 início rápido

### pré-requisitos

- Cursor IDE 2.0+
- Python 3.11+
- Acesso à API Notion (se usar integração Notion)

### instalação

```bash
# 1. Clonar repositório
git clone https://github.com/LucasBiason/cursor-multiagent-system.git
cd cursor-multiagent-system

# 2. Inicializar submódulo privado
git submodule update --init --recursive

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Configurar variáveis de ambiente
cp core/config/.env.example core/config/.env.passwords
# Editar core/config/.env.passwords com suas credenciais
```

**documentação completa:** Ver [README.md](../README.md) na raiz do projeto.

---

## 📚 documentação

### documentação técnica

- **Programação:** `core/docs/programming/` - Guias completos de Python, TypeScript, APIs, etc.
- **Notion:** `core/docs/notion/` - Documentação completa do sistema Notion
- **Agentes:** `core/agents/` - Definições e regras dos agentes

### guias práticos

- **README Principal:** `../README.md` - Guia completo de instalação e uso
- **Versionamento:** `../CHANGELOG.md` - Histórico de mudanças
- **Contribuindo:** `../CONTRIBUTING.md` - Guia de contribuição

---

## 🤖 agentes

### 1. Personal Assistant

Ponto de entrada para todas as interações. Gerencia:
- Agenda diária e horários
- Workspace Notion (4 bases: Personal, Studies, Work, YouTube)
- Criação e atualização de tarefas
- Calendário e timeboxes
- Coordenação com outros agentes

### 2. Studies Assistant

Ensino e orientação de projetos:
- Conceitos de IA/ML e tutoriais
- Aprendizado baseado em projetos
- Code reviews para projetos de aprendizado
- Gerenciamento de cronograma de estudos
- Assistência com coursework FIAP

### 3. Work Assistant

Suporte ao desenvolvimento profissional:
- Sessões de co-programação
- Code review e testes
- Automação de deploy
- Gerenciamento de workflow Git
- Suporte ao projeto ExpenseIQ

### 4. Social Media Assistant

Estratégia e gerenciamento de conteúdo para DOIS canais:

**The Crazy Fox** (YouTube):
- Canal de gaming com uploads diários
- Gerenciamento de séries e produção
- Otimização de cronograma de gravação
- Base YOUTUBER (exclusiva)

**StuffsCode** (Instagram):
- Conteúdo de programação e tutoriais
- Imagens de posts geradas por IA
- Calendário de conteúdo e automação
- Base STUDIES (temporária)

---

## 🔒 privacidade e segurança

Todos os dados sensíveis são:
- Armazenados em `config/` (submódulo privado)
- Ignorados pelo git (ver `.gitignore`)
- Nunca commitados no repositório público
- Fazer backup separadamente

Repositório público contém apenas:
- Templates genéricos
- Documentação
- Utilitários reutilizáveis
- Configurações de exemplo

---

## 🛠️ desenvolvimento

### workflow

```bash
# 1. Fazer mudanças
# 2. Testar localmente
./scripts/validate.sh

# 3. Commit e push
git add -A
git commit -m "tipo: descrição da mudança"
git push origin main
```

### testes

```bash
# Executar todos os testes
pytest tests/

# Validar configurações
./scripts/validate.sh
```

---

## 📝 versionamento

Este projeto segue [Semantic Versioning 2.0.0](https://semver.org/):
- **MAJOR** (X.0.0): Mudanças incompatíveis na API
- **MINOR** (x.Y.0): Novas funcionalidades compatíveis
- **PATCH** (x.y.Z): Correções de bugs compatíveis

---

## 🤝 contribuindo

Contribuições para melhorar o framework são bem-vindas!

1. Fork o repositório
2. Crie uma branch de feature
3. Faça suas mudanças
4. Teste completamente
5. Envie um pull request

Ver [CONTRIBUTING.md](../CONTRIBUTING.md) para diretrizes detalhadas.

---

## 📄 licença

MIT License - Ver arquivo LICENSE para detalhes

---

## 👤 autor

**Lucas Biason**  
GitHub: [@lucasbiason](https://github.com/lucasbiason)

---

## 🙏 agradecimentos

- Construído para Cursor IDE 2.0
- Inspirado em sistemas multi-agente e padrões de IA agêntica
- Notion API para integração de workspace

---

**Última Atualização:** 2025-12-08  
**Versão:** 1.1.0  
**Repositório:** https://github.com/LucasBiason/cursor-multiagent-system


