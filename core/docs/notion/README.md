# Notion Documentation - Índice

**Última atualização:** 2025-12-08

---

## 📚 estrutura de documentação

esta pasta contém documentação completa sobre o sistema notion.

### organização

```
core/docs/notion/
├── README.md                    # este arquivo (índice)
└── Manual_Notion/              # manual completo passo a passo
    ├── README.md               # índice do manual
    ├── 01_ESTRUTURA_BASES.md
    ├── 02_REGRAS_CRIACAO_CARDS.md
    ├── 03_NOTION_ENGINE_GUIA.md
    ├── 04_EXEMPLOS_PRATICOS.md
    ├── 05_STATUS_E_PROPRIEDADES.md
    ├── 06_TROUBLESHOOTING.md
    └── 07_WORKFLOWS_COMPLETOS.md
```

---

## 🎯 como usar esta documentação

### para agentes

1. **sempre consultar** `core/agents/notion-agent.mdc` primeiro (regras gerais)
2. **consultar** `core/agents/general-context.mdc` (contexto compartilhado)
3. **referenciar** `config/notion/` para regras específicas
4. **usar** `Manual_Notion/` para exemplos e workflows completos

### para desenvolvedores

1. **ler** o manual completo em `Manual_Notion/`
2. **seguir** os exemplos práticos
3. **consultar** troubleshooting quando necessário

---

## 📖 documentos disponíveis

### manual completo

**localização:** `Manual_Notion/README.md`

**conteúdo:**
- estrutura detalhada das 4 bases
- regras obrigatórias de criação
- guia do notion engine
- exemplos práticos de código
- status e propriedades por base
- troubleshooting completo
- workflows end-to-end

**quando usar:**
- quando precisar entender como criar cards
- quando precisar de exemplos de código
- quando tiver problemas ou dúvidas

---

## 🔗 referências rápidas

### regras gerais (públicas)
- **notion-agent.mdc** → `core/agents/notion-agent.mdc`
- **general-context.mdc** → `core/agents/general-context.mdc`

### regras específicas (privadas)
- **timezone** → `config/notion/timezone.md`
- **status** → `config/notion/status.md`
- **verificação** → `config/notion/verification.md`
- **youtube logic** → `config/notion/youtube-logic.md`
- **properties** → `config/notion/properties.md`
- **workflows** → `config/notion/workflows.md`
- **templates** → `config/notion/templates.md`

### guia completo
- **manual notion** → `Manual_Notion/README.md`

---

## 🚀 início rápido

### criar card simples
1. ler: `Manual_Notion/02_REGRAS_CRIACAO_CARDS.md`
2. consultar: `config/notion/timezone.md` (sempre GMT-3)
3. consultar: `config/notion/status.md` (status válidos)
4. usar: `Manual_Notion/04_EXEMPLOS_PRATICOS.md`

### verificar tarefas
1. ler: `config/notion/verification.md`
2. consultar: `config/notion/status.md` (status ignorados)
3. se youtube: `config/notion/youtube-logic.md`

### troubleshooting
1. consultar: `Manual_Notion/06_TROUBLESHOOTING.md`
2. verificar: `Manual_Notion/05_STATUS_E_PROPRIEDADES.md`

---

## 📊 hierarquia de documentação

```
1. core/agents/notion-agent.mdc (regras gerais obrigatórias)
   ↓
2. core/agents/general-context.mdc (contexto compartilhado)
   ↓
3. config/notion/ (regras específicas privadas)
   ↓
4. Manual_Notion/ (guia completo e exemplos)
```

---

## ✅ princípios fundamentais

### timezone
- sempre GMT-3
- nunca UTC
- validar em toda operação

### status
- ignorar finalizados
- ignorar realocados
- ignorar publicados (YouTube)

### duplicações
- sempre verificar antes de criar
- comparar título + data + cliente/projeto

### validação
- verificar schema antes de usar propriedades
- validar status por base
- validar datas (GMT-3)

---

**última atualização:** 2025-12-08


