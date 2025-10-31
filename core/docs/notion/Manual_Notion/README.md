# 📚 Manual Completo - Notion Automation

**Data:** 11/10/2025  
**Versão:** 1.0  
**Autor:** Guardião do Notion v3.0  
**Status:** Documentação completa e testada

---

## 🎯 OBJETIVO DESTE MANUAL

Este manual documenta **TUDO** que você precisa saber para trabalhar com as 4 bases do Notion do Lucas Biason, incluindo:

1. **Estrutura das bases** - Campos, propriedades, tipos de dados
2. **Regras de criação** - Como criar cards corretamente
3. **Padrões e convenções** - Emojis, status, timezone, hierarquias
4. **Scripts e automação** - Como usar o NotionEngine
5. **Exemplos práticos** - Código funcional para cada base
6. **Troubleshooting** - Erros comuns e soluções

---

## 📁 ESTRUTURA DESTE MANUAL

```
Manual_Notion/
├── README.md                           # Este arquivo (índice)
├── 01_ESTRUTURA_BASES.md              # Estrutura detalhada das 4 bases
├── 02_REGRAS_CRIACAO_CARDS.md         # Regras obrigatórias
├── 03_NOTION_ENGINE_GUIA.md           # Como usar o motor
├── 04_EXEMPLOS_PRATICOS.md            # Exemplos de código
├── 05_STATUS_E_PROPRIEDADES.md        # Status válidos por base
├── 06_TROUBLESHOOTING.md              # Erros comuns e soluções
└── 07_WORKFLOWS_COMPLETOS.md          # Workflows end-to-end
```

---

## 🚀 INÍCIO RÁPIDO

### Para Criar Cards Rapidamente:

```python
from core.notion_engine import NotionEngine

# Inicializar motor
TOKEN = 'ntn_YOUR_NOTION_TOKEN_HERE'
engine = NotionEngine(TOKEN)

# Criar card simples
card_id = engine.create_card('WORK', {
    'title': 'Minha Tarefa',
    'status': 'Não iniciado',
    'cliente': 'Astracode',
    'projeto': 'ExpenseIQ',
    'priority': 'Normal'
})

print(f'Card criado: https://www.notion.so/{card_id}')
```

---

## 📊 AS 4 BASES DO NOTION

### 1. BASE TRABALHO (WORK)
- **ID:** `1f9962a7-693c-80a3-b947-c471a975acb0`
- **Campo Título:** `Nome do projeto`
- **Campo Relação:** `item principal`
- **Status Padrão:** `Não iniciado`
- **Uso:** Projetos profissionais da Astracode

### 2. BASE PESSOAL (PERSONAL)
- **ID:** `1fa962a7-693c-8032-8996-dd9cd2607dbf`
- **Campo Título:** `Nome da tarefa`
- **Campo Relação:** `tarefa principal`
- **Status Padrão:** `Não iniciado`
- **Uso:** Tarefas pessoais e organizacionais

### 3. BASE CURSOS (STUDIES)
- **ID:** `1fa962a7-693c-80de-b90b-eaa513dcf9d1`
- **Campo Título:** `Project name`
- **Campo Relação:** `Parent item`
- **Status Padrão:** `Para Fazer`
- **Uso:** Cursos, formações e estudos

### 4. BASE YOUTUBE (YOUTUBER)
- **ID:** `1fa962a7-693c-80ce-9f1d-ff86223d6bda`
- **Campo Título:** `Nome do projeto`
- **Campo Relação:** `item principal`
- **Status Padrão:** `Não iniciado`
- **Uso:** Séries e episódios do canal

---

## 🔑 REGRAS CRÍTICAS

### 1. Timezone
- **SEMPRE GMT-3** (São Paulo)
- **NUNCA UTC** em cards visíveis
- Formato: `YYYY-MM-DDTHH:MM:SS-03:00`

### 2. Ícones
- **SEMPRE** como ícone da página (`icon` property)
- **NUNCA** no título do card
- Usar emojis relevantes ao contexto

### 3. Hierarquias
- **WORK:** Use `item_principal` para linkar sub-itens
- **PERSONAL:** Use `tarefa_principal` para linkar subtarefas
- **STUDIES:** Use `parent_item` para linkar aulas/seções
- **YOUTUBER:** Use `item_principal` para linkar episódios à série

### 4. Prioridades
- **WORK:** Padrão `Normal`
- **STUDIES:** Padrão `Normal`
- **PERSONAL:** Sem campo de prioridade

### 5. Cliente e Projeto (WORK)
- **Cliente padrão:** `Astracode`
- **Projetos válidos:** `ExpenseIQ`, `HubTravel`, `Avulso`
- Agentes específicos sempre usam seus projetos

---

## 📖 LEIA PRIMEIRO

### Se você vai criar cards:
👉 Leia: `04_EXEMPLOS_PRATICOS.md`

### Se você quer entender as bases:
👉 Leia: `01_ESTRUTURA_BASES.md`

### Se você precisa saber regras:
👉 Leia: `02_REGRAS_CRIACAO_CARDS.md`

### Se você teve um erro:
👉 Leia: `06_TROUBLESHOOTING.md`

---

## 🛠️ FERRAMENTAS DISPONÍVEIS

### NotionEngine
**Localização:** `/home/user/Projetos/Automações/notion-automations/notion-automation-scripts/core/notion_engine.py`

**Métodos principais:**
- `create_card(base, data)` - Cria um card
- `create_subitems_only(base, parent_id, subitems)` - Cria múltiplos sub-itens

### Scripts Úteis
**Localização:** `/home/user/Projetos/Automações/notion-automations/notion-automation-scripts/scripts/`

- `Personal/` - Scripts para base pessoal
- `Work/` - Scripts para base de trabalho
- `Studies/` - Scripts para base de cursos
- `Youtuber/` - Scripts para base YouTube

---

## 🎓 APRENDIZADOS IMPORTANTES

### 1. Cada Base é Diferente
- Campos de título diferentes
- Campos de relação diferentes
- Status disponíveis diferentes
- Propriedades específicas de cada uma

### 2. Vínculos São Críticos
- Sub-itens DEVEM ter o campo de relação preenchido
- O campo de relação é diferente em cada base
- Sem vínculo = sub-item não aparece

### 3. Ícones vs Títulos
- Ícones vão na propriedade `icon` da página
- Títulos devem ser limpos (sem emojis)
- Usar `emoji` no payload do NotionEngine

### 4. Datas e Horários
- STUDIES: Aulas COM horário, Seções/Cursos SEM horário
- YOUTUBER: Episódios com período de gravação E data de lançamento
- WORK/PERSONAL: Usar campo `Periodo` ou `Data` conforme a base

---

## 📞 CREDENCIAIS E IDS

### Token Notion
```
ntn_YOUR_NOTION_TOKEN_HERE
```

### Database IDs
```python
BASES = {
    'WORK': '1f9962a7-693c-80a3-b947-c471a975acb0',
    'PERSONAL': '1fa962a7-693c-8032-8996-dd9cd2607dbf',
    'STUDIES': '1fa962a7-693c-80de-b90b-eaa513dcf9d1',
    'YOUTUBER': '1fa962a7-693c-80ce-9f1d-ff86223d6bda'
}
```

---

## ✅ VALIDAÇÃO

Este manual foi **testado completamente** em 11/10/2025 com:
- ✅ Criação de cards em todas as 4 bases
- ✅ Criação de sub-itens com vínculos corretos
- ✅ Validação de ícones, status e propriedades
- ✅ Verificação de hierarquias funcionando

**Todos os exemplos de código neste manual FUNCIONAM!**

---

## 🎯 PRÓXIMOS PASSOS

1. Leia o arquivo que mais se aplica à sua necessidade
2. Copie os exemplos de código
3. Adapte para seu caso específico
4. Execute e valide no Notion

---

**Qualquer pessoa que ler este manual conseguirá criar cards corretamente no Notion!**

---

## 🆕 ATUALIZAÇÕES RECENTES (22/10/2025)

### ✅ Novos Recursos
1. **Templates Pessoais** - Sistema de modelos reutilizáveis
   - Ver: `../Templates/TEMPLATES_PESSOAIS_GUIA.md`
   
2. **Verificação Inteligente** - Sistema de detecção de tarefas atrasadas
   - Ver: `../Regras/REGRAS_VERIFICACAO_TAREFAS.md`
   
3. **Lógica YouTube** - Regras especiais para Data de Lançamento
   - Ver: `../Regras/REGRAS_YOUTUBE_LOGICA_ESPECIAL.md`

### ✅ Regras Atualizadas
- Status ignorados em verificações
- Lógica especial para YouTube
- Templates de consulta médica customizável

---

**Última Atualização:** 22/10/2025  
**Versão:** 2.0 (Atualizada)  
**Status:** ✅ Completo com Novas Funcionalidades


