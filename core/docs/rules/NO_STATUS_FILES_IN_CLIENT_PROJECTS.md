# ❌ PROIBIDO: Arquivos de Status/Feedback em Projetos de Cliente

**Versão**: 1.0  
**Data**: 05/Dez/2025  
**Prioridade**: CRÍTICA

---

## ⚠️ REGRA DE OURO

**NUNCA criar arquivos de status, feedback, resumo ou tutoriais no diretório do projeto do cliente.**

---

## ❌ PROIBIDO CRIAR

### Arquivos de Status/Resumo
- `STATUS-*.md`
- `RESUMO-*.md`
- `ENTREGA-*.md`
- `SISTEMA-*.md`
- `CORRECAO-*.md`
- `CORREÇÕES-*.md`
- `FINAL-*.md`
- `COMPLETO-*.md`
- `PRONTO-*.md`

### Arquivos de Tutorial/Guia
- `LEIA-ME-*.md`
- `PROXIMAS-ACOES.md`
- `COMO-*.md`
- `GUIA-*.md`
- `TUTORIAL-*.md`

### Arquivos de Planejamento
- `PLANEJAMENTO-*.md`
- `TODO-*.md`
- `CHECKLIST-*.md`

### Arquivos de Custo/Métrica
- `CUSTOS-*.md`
- `TEMPO-*.md`
- `ORCAMENTO-*.md`

---

## ✅ ONDE COLOCAR CONTEXTO

### Contexto do Agente
**Local**: `/home/lucas-biason/Projetos/Infraestrutura/cursor-multiagent-system/config/`

### Estrutura por Domínio
```
config/
├── work/
│   └── {ClienteName}/
│       ├── 00-context.md       # Contexto geral do projeto
│       ├── 01-planning.md      # Planejamento atual
│       └── 02-knowledge.md     # Conhecimento acumulado
├── studies/
│   └── {Course}/
│       └── ... (mesma estrutura)
├── personal/
│   └── {Project}/
│       └── ... (mesma estrutura)
└── system/
    ├── planning/               # Planejamentos temporários
    └── sessions/               # Resumos de sessões
```

### Exemplo Correto
```
❌ ERRADO:
/home/lucas-biason/Projetos/Trabalho/Freelancers/KPIs/RESUMO-FINAL.md

✅ CORRETO:
/home/lucas-biason/Projetos/Infraestrutura/cursor-multiagent-system/config/work/KPI-Comunita/02-knowledge.md
```

---

## 📝 COMO COMUNICAR PROGRESSO

### ✅ Permitido
1. **Via Chat**: Comunicar diretamente com o usuário
2. **Comments no código**: Apenas quando necessário para entendimento
3. **Docstrings**: Em funções/classes complexas
4. **README do projeto**: Se solicitado explicitamente

### ❌ Proibido
1. **Arquivos .md avulsos** no projeto
2. **Arquivos de status** no projeto
3. **Resumos executivos** no projeto
4. **Documentação excessiva** não solicitada

---

## 🎯 PRINCÍPIOS

### Menos é Mais
- Comunicar via chat é mais eficiente
- Arquivos devem ser APENAS código e configuração
- Contexto vai para `cursor-multiagent-system/config/`

### Foco no Código
- Projeto do cliente = apenas código funcional
- Sem poluição de arquivos auxiliares
- Estrutura limpa e profissional

### Contexto Centralizado
- Todo contexto em `cursor-multiagent-system/config/`
- Organizado por domínio e projeto
- Versionado em repositório privado

---

## 🔍 VALIDAÇÃO

### Antes de Criar Arquivo .md
Pergunte-se:
1. **É código funcional?** → Crie no projeto
2. **É configuração necessária?** → Crie no projeto
3. **É documentação solicitada?** → Crie no projeto
4. **É contexto/status/resumo?** → `cursor-multiagent-system/config/`

### Checklist
- [ ] Arquivo é necessário para o sistema funcionar?
- [ ] Foi explicitamente solicitado pelo usuário?
- [ ] Faz parte da entrega do projeto?

**Se todas as respostas forem NÃO** → Não criar ou mover para `config/`

---

## 🚫 VIOLAÇÕES COMUNS

### ❌ Exemplo 1: Status de Entrega
```markdown
# ❌ ERRADO
/projeto-cliente/ENTREGA-FINAL-COMPLETA.md
/projeto-cliente/STATUS-PARA-CLIENTE.md

# ✅ CORRETO
Via chat: "Sistema pronto! Tudo funcionando."
```

### ❌ Exemplo 2: Custos
```markdown
# ❌ ERRADO
/projeto-cliente/CUSTOS-PROJETO.md

# ✅ CORRETO
config/work/ClienteName/02-knowledge.md (seção de custos)
```

### ❌ Exemplo 3: Tutoriais
```markdown
# ❌ ERRADO
/projeto-cliente/COMO-USAR.md
/projeto-cliente/LEIA-ME-PRIMEIRO.md

# ✅ CORRETO
Via chat ou README.md (se solicitado)
```

---

## 📚 EXCEÇÕES

### ✅ Arquivos Permitidos no Projeto

**Documentação Funcional** (se solicitada):
- `README.md` - Overview do projeto
- `CONTRIBUTING.md` - Guia de contribuição
- `CHANGELOG.md` - Histórico de versões
- `API.md` - Documentação de API

**Configuração**:
- `.env.example` - Template de variáveis
- `requirements.txt`, `package.json` - Dependências
- `.gitignore`, `.dockerignore` - Configuração de versionamento

**Licença**:
- `LICENSE` - Licença do código

---

## 🎯 RESUMO

### Proibido
❌ Arquivos de status/feedback no projeto do cliente  
❌ Documentação não solicitada  
❌ Resumos executivos  
❌ Tutoriais não pedidos  
❌ Planejamentos temporários  

### Permitido
✅ Código funcional  
✅ Configurações necessárias  
✅ README (se solicitado)  
✅ Documentação de API (se solicitada)  
✅ Comentários no código (quando necessário)  

### Obrigatório
✅ Contexto em `cursor-multiagent-system/config/`  
✅ Comunicação via chat  
✅ Estrutura limpa no projeto do cliente  

---

## 📞 REFERÊNCIAS

- Regras de organização: `cursor-multiagent-system/.cursorrules`
- Mapeamento de arquivos: `config/system/MAPEAMENTO_ASSUNTOS.md`
- Estrutura de projetos: `config/README.md`

---

**PROJETO DO CLIENTE = SÓ CÓDIGO. CONTEXTO = cursor-multiagent-system/config/**

