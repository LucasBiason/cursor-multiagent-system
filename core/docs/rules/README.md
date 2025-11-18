# 📖 Regras do Sistema Notion - Índice

**Data:** 22/10/2025  
**Versão:** 1.0  
**Status:** Documentação Completa

---

## 🎯 VISÃO GERAL

Esta pasta contém **todas as regras obrigatórias** do sistema de automação Notion.

---

## 📚 DOCUMENTOS DISPONÍVEIS

### 1. REGRAS_TIMEZONE.md ⏰
**Conteúdo:** Regras de timezone GMT-3  
**Quando ler:** Sempre que trabalhar com datas

**Regra Principal:**
- SEMPRE GMT-3 (`-03:00`)
- NUNCA UTC

---

### 2. REGRAS_STATUS_IGNORADOS.md 🚫
**Conteúdo:** Status que devem ser ignorados em verificações  
**Quando ler:** Ao implementar verificações de tarefas

**Status Ignorados:**
- Concluído, Cancelado, Realocada, Descartado, Publicado

---

### 3. REGRAS_YOUTUBE_LOGICA_ESPECIAL.md 🎥
**Conteúdo:** Lógica especial para base YouTube  
**Quando ler:** Ao trabalhar com cards de YouTube

**Diferença Chave:**
- Período = Quando GRAVAR
- Data de Lançamento = Quando PUBLICAR
- Cards em edição: verificar Data de Lançamento

---

### 4. REGRAS_VERIFICACAO_TAREFAS.md 🔍
**Conteúdo:** Sistema completo de verificação de atrasos  
**Quando ler:** Ao implementar ou usar verificações

**Características:**
- Lógica por base
- Classificação de urgência
- 100% de precisão

---

### 5. REACT_BEST_PRACTICES.md ⚛️
**Conteúdo:** Regras e boas práticas para desenvolvimento React.js  
**Quando ler:** Ao trabalhar com projetos React.js, Next.js ou frontend

**Regras Principais:**
- Absolute imports obrigatórios (`@/components`, `@/hooks`, etc.)
- React.memo para performance
- useCallback em hooks e handlers
- Error Boundaries obrigatórios
- TypeScript com types completos
- Tailwind CSS exclusivo (sem CSS inline)
- Acessibilidade (a11y) obrigatória

**Referências Base:**
- [React Architecture Pattern and Best Practices (GeeksforGeeks)](https://www.geeksforgeeks.org/reactjs/react-architecture-pattern-and-best-practices/)
- [React Design Patterns and Best Practices for 2025 (Telerik)](https://www.telerik.com/blogs/react-design-patterns-best-practices)

---

## 🚀 INÍCIO RÁPIDO

### Para Criar Cards:
1. Leia: `REGRAS_TIMEZONE.md` primeiro
2. Consulte: `../Manual_Notion/02_REGRAS_CRIACAO_CARDS.md`
3. Use: `../Templates/` para modelos

### Para Verificar Tarefas:
1. Leia: `REGRAS_VERIFICACAO_TAREFAS.md`
2. Leia: `REGRAS_STATUS_IGNORADOS.md`
3. Se for YouTube: `REGRAS_YOUTUBE_LOGICA_ESPECIAL.md`

### Para Desenvolvimento React.js:
1. Leia: `REACT_BEST_PRACTICES.md` **ANTES** de começar
2. Use o checklist de implementação
3. Siga os padrões de código documentados

---

## 📊 HIERARQUIA DE REGRAS

### Regras Notion
```
1. REGRAS_TIMEZONE.md (base de tudo)
   ↓
2. Manual_Notion/02_REGRAS_CRIACAO_CARDS.md (criação)
   ↓
3. REGRAS_STATUS_IGNORADOS.md (verificação)
   ↓
4. REGRAS_YOUTUBE_LOGICA_ESPECIAL.md (caso especial)
   ↓
5. REGRAS_VERIFICACAO_TAREFAS.md (sistema completo)
```

### Regras Desenvolvimento
```
1. REACT_BEST_PRACTICES.md (React.js/Next.js)
   - Absolute imports
   - Performance (memo, useCallback, useMemo)
   - Error Boundaries
   - TypeScript
   - Acessibilidade
```

---

## ✅ PRINCÍPIOS FUNDAMENTAIS

### 1. Timezone
- SEMPRE GMT-3
- NUNCA UTC
- Validar em toda operação

### 2. Status
- Ignorar finalizados
- Ignorar realocados
- Ignorar publicados (YouTube)

### 3. YouTube
- Data de Lançamento para cards em edição
- Período para cards em gravação
- Diferenciação clara

### 4. Precisão
- 100% de acurácia
- Zero falsos positivos
- Zero falsos negativos

---

## 🎯 IMPLEMENTAÇÕES

### Scripts que Usam Estas Regras
1. `check_overdue_tasks.py` - Verificação completa
2. `investigate_youtube_cards.py` - Análise YouTube
3. `models/personal_templates.py` - Templates pessoais
4. `create_retroactive_cards.py` - Criação retroativa

### Agentes que Usam Estas Regras
1. Agent 1 - Gerenciador de Cards Semanais
2. Agent 3 - Finalizador Semanal
3. Agent 4 - Organizador YouTube
4. Agent 7-8-9 - Monitor Integrado
5. **TODOS OS AGENTES** - REACT_BEST_PRACTICES.md (ao trabalhar com React.js)

---

## 📈 EVOLUÇÃO DAS REGRAS

### Versão 1.0 (29/09/2025)
- Regras básicas de timezone
- Status padrões

### Versão 1.5 (01/10/2025)
- Limite 21:00 para estudos
- Hierarquias por base

### Versão 2.0 (22/10/2025)
- Status ignorados
- Lógica especial YouTube
- Templates pessoais
- Sistema de verificação inteligente

### Versão 2.1 (17/11/2025 - ATUAL)
- Adicionado REACT_BEST_PRACTICES.md
- Regras de desenvolvimento React.js/Next.js
- Baseado em artigos GeeksforGeeks e Telerik

---

## 🔗 LINKS RELACIONADOS

### Documentação
- Manual Notion: `../Manual_Notion/README.md`
- Templates: `../Templates/TEMPLATES_PESSOAIS_GUIA.md`
- Configurações: `../Configuracoes/BASES_NOTION_CONTEXTO.md`

### Scripts
- Repositório: https://github.com/LucasBiason/notion-automation-scripts
- Pasta local: `/Projetos/Automações/notion-automations/notion-automation-scripts/`

---

**Última Atualização:** 17/11/2025  
**Total de Regras:** 5 documentos  
**Status:** ✅ Completo e Validado













