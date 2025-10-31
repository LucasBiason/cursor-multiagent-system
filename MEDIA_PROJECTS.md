# 📺📱 Projetos de Mídia Social - Referência Rápida

Este documento diferencia claramente os dois projetos de mídia social gerenciados pelo Social Media Coach.

---

## 🦊 THE CRAZY FOX (YouTube)

### Informações Básicas
- **Nome:** The Crazy Fox
- **Plataforma:** YouTube
- **Tipo:** Canal de Gaming
- **Base Notion:** YOUTUBER (exclusiva para este canal)
- **Status:** Ativo

### Conteúdo
- Séries longas de RPGs (15-20+ episódios)
- Séries curtas de jogos diversos
- Reviews ao final de cada série
- Futuro: Notícias e outros formatos (quando automatizado)

### Produção
- **Frequência:** Diário (2 vídeos/dia)
- **Horários:** 12:00 e 18:00 (às vezes 15:00)
- **Séries Simultâneas:** Máximo 4 (intercaladas em 2 slots)
- **Gravação:** Noturna (21:00-00:00) + Sprint fim de semana

### Documentação
**Localização:** `config/private/youtube/`

Arquivos principais:
- `README.md` - Visão geral do canal
- `LOGICA_PRODUCAO.md` - Sistema completo de produção
- `SERIES_TEMPLATE.md` - Como criar novas séries
- `scripts/` - Scripts de automação

### Workflow
1. Criar série + episódios no Notion (Base YOUTUBER)
2. Gravar piloto (decidir se continua)
3. Produção em lote (fim de semana)
4. Edições distribuídas (durante semana)
5. Publicações automáticas (horários fixos)

### Campos Notion Importantes
- **Periodo:** Data/hora de GRAVAÇÃO
- **Data de Lançamento:** Data/hora de PUBLICAÇÃO
- **item_principal:** Vínculo episódio → série
- **Status:** Para Gravar → Gravando → Para Edição → Editando → Editado → Publicado

---

## 🎨 STUFFSCODE (Instagram)

### Informações Básicas
- **Nome:** StuffsCode
- **Plataforma:** Instagram
- **Tipo:** Conteúdo de Programação
- **Base Notion:** STUDIES (projeto temporário)
- **Futuro:** Terá base própria "STUFFSCODE"
- **Status:** Em Desenvolvimento

### Conteúdo
- Posts estáticos (carrosséis de código)
- Reels/vídeos curtos (planejado)
- Stories (compartilhamento de posts)
- Imagens geradas por IA

### Produção
- **Frequência:** 2-4 posts/semana (início: 2, depois expandir)
- **Horários:** A definir (pesquisar melhor horário)
- **Agendamento:** Automático (planejado)
- **Criação:** IA generativa para imagens

### Documentação
**Localização:** `config/private/social/stuffscode/`

Estrutura completa (28 documentos):
- `01_Planejamento/` - Análises e estratégias
- `02_Identidade_Visual/` - Cores, logo, prompts
- `03_Conteudo/` - Ideias, hashtags, exemplos
- `04_Automacao/` - API Instagram, ferramentas
- `05_GitHub/` - Organização do repositório

### Workflow
1. Criar card de post no Notion (Base STUDIES)
2. Gerar imagem com IA (Gemini)
3. Preparar legenda e hashtags
4. Agendar publicação
5. Monitorar engagement

---

## 🎯 DIFERENÇAS PRINCIPAIS

| Aspecto | The Crazy Fox | StuffsCode |
|---------|---------------|------------|
| **Plataforma** | YouTube | Instagram |
| **Base Notion** | YOUTUBER | STUDIES* |
| **Tipo** | Gaming | Programação |
| **Frequência** | 2/dia (diário) | 2-4/semana |
| **Horários** | 12h, 18h fixos | A definir |
| **Conteúdo** | Vídeos longos (séries) | Posts/Carrosséis |
| **Produção** | Manual (gravação) | IA generativa |
| **Automação** | Agendamento | IA + Agendamento |
| **Status** | Ativo há tempo | Projeto novo |
| **Documentação** | `youtube/` | `social/stuffscode/` |

\* StuffsCode terá base própria no futuro quando estrutura estiver completa

---

## 📋 TRIGGERS DE ATIVAÇÃO

### Para The Crazy Fox:
- "gravar", "gravação", "episódio"
- "youtube", "crazy fox"
- "série", "lançamento"
- "o que gravar", "fim de semana"
- "status gravações"

### Para StuffsCode:
- "stuffscode", "instagram"
- "post", "carrossel"
- "programação", "tutorial"
- "agendar post"

---

## ⚠️ REGRAS CRÍTICAS

### NUNCA Confundir!
- The Crazy Fox ≠ StuffsCode
- Base YOUTUBER ≠ Base STUDIES
- Gravação de vídeo ≠ Post de Instagram
- Episódio ≠ Post

### Sempre Verificar
- Qual projeto está sendo discutido?
- Qual base Notion usar?
- Qual documentação consultar?
- Qual workflow seguir?

---

## 📁 ORGANIZAÇÃO DE ARQUIVOS

### The Crazy Fox
```
config/private/youtube/
├── README.md
├── LOGICA_PRODUCAO.md
├── SERIES_TEMPLATE.md
└── scripts/
    └── [scripts temporários]
```

### StuffsCode
```
config/private/social/stuffscode/
├── README.md
├── 01_Planejamento/
├── 02_Identidade_Visual/
├── 03_Conteudo/
├── 04_Automacao/
└── 05_GitHub/
```

---

## 🚀 PRÓXIMOS PASSOS

### The Crazy Fox
- ✅ Sistema de produção funcionando
- ✅ Workflow definido
- ⏳ Possível automação de roteiros

### StuffsCode
- ⏳ Primeiros posts
- ⏳ Teste de horários
- ⏳ Automação completa
- ⏳ Base própria no Notion (quando pronto)

---

**Última Atualização:** 2025-10-31  
**Versão:** 1.0  
**Gerenciado por:** Social Media Coach Agent

