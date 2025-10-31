# 🤖 REGRAS OBRIGATÓRIAS PARA AGENTES - SCRIPTS E COMMITS

**Data:** 27/10/2025  
**Versão:** 1.0  
**Aplicável:** TODOS os agentes de IA que trabalham com Notion  
**Repositório:** https://github.com/LucasBiason/notion-automation-scripts

---

## ⚠️ **REGRA DE OURO**

**TODO SCRIPT CRIADO OU MODIFICADO DEVE SER COMMITADO E PUSHED IMEDIATAMENTE!**

---

## 📁 **ORGANIZAÇÃO DE SCRIPTS**

### **Estrutura Obrigatória**

```
notion-automation-scripts/
├── core/                    # Motor e engines (NÃO MEXER sem autorização)
├── models/                  # Templates e modelos
├── examples/                # Exemplos de uso
├── scripts/
│   ├── Personal/           # Scripts da base PERSONAL
│   ├── Studies/            # Scripts da base STUDIES
│   ├── Work/               # Scripts da base WORK
│   └── Youtuber/           # Scripts da base YOUTUBER
└── [utilitários gerais]    # Apenas scripts multi-base
```

---

## 🎯 **ONDE COLOCAR CADA SCRIPT**

### **Regra de Identificação**

1. **Script acessa APENAS base Personal?**
   → `scripts/Personal/nome_do_script.py`

2. **Script acessa APENAS base Studies?**
   → `scripts/Studies/nome_do_script.py`

3. **Script acessa APENAS base Work?**
   → `scripts/Work/nome_do_script.py`

4. **Script acessa APENAS base Youtuber?**
   → `scripts/Youtuber/nome_do_script.py`

5. **Script acessa MÚLTIPLAS bases OU é utilitário geral?**
   → Raiz do projeto (ex: `check_overdue_tasks.py`)

---

## 📝 **NOMENCLATURA DE SCRIPTS**

### **Padrões Obrigatórios**

| Tipo | Padrão | Exemplo |
|------|--------|---------|
| **Criação** | `create_*.py` | `create_weekly_cards.py` |
| **Atualização** | `update_*.py` | `update_progress.py` |
| **Correção** | `fix_*.py` | `fix_dates.py` |
| **Verificação** | `check_*.py` ou `verificar_*.py` | `check_properties.py` |
| **Limpeza** | `delete_*.py` | `delete_old_cards.py` |
| **Reorganização** | `reorganizar_*.py` | `reorganizar_cronograma.py` |
| **Teste** | `test_*.py` | `test_creation.py` |

---

## 🔧 **ESTRUTURA DE SCRIPT**

### **Template Obrigatório**

Todo script DEVE ter no topo:

```python
#!/usr/bin/env python3
"""
[Nome Descritivo do Script]

Descrição: [O que o script faz em 1-2 linhas]
Base Acessada: [PERSONAL|STUDIES|WORK|YOUTUBER|MULTIPLAS]
Autor: [Nome do Agente ou Humano]
Data: [DD/MM/YYYY]
Versão: [X.Y]
"""

import os
from dotenv import load_dotenv

# Carregar variáveis
load_dotenv()

# Constantes
TOKEN = os.getenv('NOTION_API_TOKEN')
BASE_ID = os.getenv('[BASE]_DB_ID')  # Específico para base

# [Resto do código]
```

---

## 📦 **WORKFLOW DE COMMIT**

### **SEMPRE que criar ou modificar script:**

#### **Passo 1: Organizar**
```bash
# Colocar script na pasta correta
mv meu_script.py scripts/[Base]/meu_script.py
```

#### **Passo 2: Testar**
```bash
# Executar para validar
python3 scripts/[Base]/meu_script.py
```

#### **Passo 3: Git Add**
```bash
cd /home/lucas-biason/Projetos/Automações/notion-automations/notion-automation-scripts
git add .
```

#### **Passo 4: Commit**
```bash
git commit -m "feat([base]): [descrição do script]

- [O que foi adicionado/modificado]
- [Por que foi necessário]
- [Resultado esperado]"
```

**Exemplos de mensagens:**
```bash
# Script novo
git commit -m "feat(personal): Criar cards semanais automaticamente

- Script create_weekly_cards.py
- Cria planejamento, pagamento e tratamento
- Automação para segundas-feiras"

# Correção
git commit -m "fix(studies): Corrigir timezone em cronogramas

- Ajustado para GMT-3 em todos os scripts
- Fix em cronograma_cursos.py
- Alinhado com regras do sistema"

# Atualização
git commit -m "refactor(youtuber): Reorganizar scripts YouTube

- Movidos 3 scripts para scripts/Youtuber/
- Criado README.md
- Estrutura organizada"
```

#### **Passo 5: Push**
```bash
git push origin main
```

---

## 🚨 **COMMITS OBRIGATÓRIOS**

### **SEMPRE commitar quando:**

1. ✅ Criar script novo
2. ✅ Modificar script existente
3. ✅ Corrigir bug em script
4. ✅ Adicionar funcionalidade
5. ✅ Refatorar código
6. ✅ Atualizar documentação
7. ✅ Reorganizar arquivos
8. ✅ Deletar scripts obsoletos

### **NUNCA esquecer de:**

1. ❌ Testar antes de commitar
2. ❌ Validar que funciona
3. ❌ Escrever mensagem clara
4. ❌ Fazer push (senão fica só local!)

---

## 📋 **CHECKLIST PÓS-CRIAÇÃO**

Quando criar qualquer script:

- [ ] Script está na pasta correta?
- [ ] Nome segue padrão?
- [ ] Tem docstring no topo?
- [ ] Foi testado e funciona?
- [ ] README da pasta atualizado? (se relevante)
- [ ] Git add executado?
- [ ] Commit com mensagem clara?
- [ ] Push para GitHub?
- [ ] Card do Notion atualizado? (se aplicável)

---

## 🎯 **RESPONSABILIDADES POR AGENTE**

### **Agente Organizador (Principal)**
- ✅ Garantir organização de scripts
- ✅ Mover scripts mal posicionados
- ✅ Atualizar READMEs
- ✅ Fazer commits de reorganização

### **Agente de Programação**
- ✅ Criar scripts bem estruturados
- ✅ Colocar na pasta correta IMEDIATAMENTE
- ✅ Commitar após criação
- ✅ Documentar no código

### **Agente de Estudos**
- ✅ Scripts em `scripts/Studies/`
- ✅ Nomear adequadamente
- ✅ Commitar sempre
- ✅ Atualizar card do Notion

### **Assistente Pessoal (Este Agente)**
- ✅ Scripts em `scripts/Personal/`
- ✅ Garantir organização geral
- ✅ Revisar commits dos outros
- ✅ Manter tudo sincronizado

---

## 🔗 **INTEGRAÇÃO COM NOTION**

### **Após Commit, SEMPRE:**

1. **Buscar card relacionado** no Notion
2. **Atualizar descrição** com link do commit
3. **Adicionar** na seção "Commits Relacionados":

```markdown
## 📦 Commits Relacionados

- [2a4e758](https://github.com/LucasBiason/notion-automation-scripts/commit/2a4e758) - Organização scripts (27/10/2025)
- [Novo hash] - [Descrição] ([Data])
```

---

## 🎯 **EXEMPLOS PRÁTICOS**

### **Exemplo 1: Criar Script Personal**

```bash
# 1. Criar script
vim scripts/Personal/create_duolingo_monthly.py

# 2. Desenvolver código
# [código aqui]

# 3. Testar
python3 scripts/Personal/create_duolingo_monthly.py

# 4. Commit
git add scripts/Personal/create_duolingo_monthly.py
git commit -m "feat(personal): Script mensal Duolingo tracking

- Cria card mensal com checkboxes diários
- XP, streaks e conquistas
- Template reutilizável"

# 5. Push
git push origin main

# 6. Atualizar Notion (card Duolingo)
# Adicionar link do commit na descrição
```

---

### **Exemplo 2: Reorganizar Scripts**

```bash
# 1. Identificar scripts fora do lugar
# (scripts Studies na raiz)

# 2. Mover
mv cronograma_*.py scripts/Studies/

# 3. Commit
git add -A
git commit -m "refactor(studies): Mover scripts de cronograma

- Movidos 4 scripts para scripts/Studies/
- Estrutura organizada por base
- Facilita manutenção"

# 4. Push
git push origin main
```

---

### **Exemplo 3: Correção de Bug**

```bash
# 1. Identificar e corrigir bug
vim scripts/Personal/create_weekly_cards.py

# 2. Testar correção
python3 scripts/Personal/create_weekly_cards.py

# 3. Commit
git add scripts/Personal/create_weekly_cards.py
git commit -m "fix(personal): Corrigir timezone em cards semanais

- Alterado de UTC para GMT-3
- Alinhado com REGRAS_TIMEZONE.md
- Testado e validado"

# 4. Push
git push origin main
```

---

## 🚫 **O QUE NÃO FAZER**

### **NUNCA:**

1. ❌ Criar script na raiz se for específico de uma base
2. ❌ Modificar sem commitar
3. ❌ Commitar sem testar
4. ❌ Push sem mensagem clara
5. ❌ Esquecer de fazer push (fica só local!)
6. ❌ Duplicar scripts
7. ❌ Deixar scripts temporários commitados
8. ❌ Modificar `core/` sem autorização

---

## 📊 **MONITORAMENTO**

### **Checklist Semanal (Agente Organizador)**

Todo domingo 23:00:

- [ ] Verificar se há scripts na raiz que deveriam estar em pastas
- [ ] Verificar se há commits pendentes (local mas não pushed)
- [ ] Verificar se READMEs estão atualizados
- [ ] Verificar se há duplicados
- [ ] Fazer limpeza se necessário
- [ ] Commitar reorganização

---

## ✅ **ÚLTIMA REORGANIZAÇÃO**

**Data:** 27/10/2025  
**Commit:** `2a4e758`  
**Ação:** Organização completa de 54 scripts  
**Status:** ✅ Sistema Organizado

**Próxima Revisão:** 03/11/2025

---

## 📞 **EM CASO DE DÚVIDA**

**"Onde eu coloco este script?"**
1. Pergunta: Qual base ele acessa PRINCIPALMENTE?
2. Resposta: Essa é a pasta!
3. Se múltiplas: Raiz (utilitário geral)

**"Posso modificar sem commitar?"**
- ❌ NÃO! Sempre commitar!

**"E se esquecer de push?"**
- ⚠️ Código fica só local (perdido se der problema)
- ✅ Sempre fazer push IMEDIATAMENTE

---

**REGRA FUNDAMENTAL:** Código só existe se estiver no GitHub! 🚀

---

**Gerado por:** AI Notion Manager  
**Data:** 27/10/2025  
**Status:** ✅ Regra Oficial do Sistema  
**Aplicável:** TODOS os agentes

