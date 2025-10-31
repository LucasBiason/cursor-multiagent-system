# 🎨 Templates - Sistema de Modelos Reutilizáveis

**Data:** 22/10/2025  
**Versão:** 1.0  
**Status:** Em Expansão

---

## 🎯 OBJETIVO

Esta pasta contém **templates e modelos reutilizáveis** para criação de cards no Notion.

---

## 📚 TEMPLATES DISPONÍVEIS

### 1. TEMPLATES_PESSOAIS_GUIA.md 🏠
**Conteúdo:** Templates para cards pessoais recorrentes  
**Implementação:** `models/personal_templates.py`

**Templates Inclusos:**
- Planejamento Semanal
- Pagamento Hamilton (Médico)
- Tratamento Médico
- Revisão Financeira (2 tipos)
- Pagamento Contadora e Impostos
- Emissão de Nota Fiscal
- Consulta Médica (customizável)

**Quando usar:** Para criar cards pessoais padronizados

---

## 🚀 INÍCIO RÁPIDO

### Usar Template Pessoal
```python
from models.personal_templates import PersonalTemplates

templates = PersonalTemplates(TOKEN)

# Criar card de template
card_id = templates.create_card_from_template(
    "planejamento_semanal",
    "2025-10-28"
)
```

### Consulta Médica Customizada
```python
# Título dinâmico com médico e especialidade
card_id = templates.create_consulta_medica(
    "Doutora Andrea",
    "Endocrino",
    "2025-10-14",
    "8:00",
    "10:20"
)
# Título: "Consulta Médica: Doutora Andrea Endocrino"
```

---

## 📋 TEMPLATES PLANEJADOS

### Templates de Trabalho (Futuro)
- Sprint de desenvolvimento
- Reunião semanal
- Code review
- Deploy de serviço

### Templates de Estudo (Futuro)
- Aula teórica
- Aula prática
- Revisão de módulo
- Projeto prático

### Templates de YouTube (Futuro)
- Episódio regular
- Episódio especial
- Livestream
- Trailer

---

## 🎯 PRINCÍPIOS DOS TEMPLATES

### 1. Reutilização
- ✅ Definir uma vez
- ✅ Usar múltiplas vezes
- ✅ Manter consistência

### 2. Customização
- ✅ Campos variáveis (data, hora)
- ✅ Campos opcionais (descrição extra)
- ✅ Títulos dinâmicos (consulta médica)

### 3. Validação
- ✅ Templates validados
- ✅ Dados consistentes
- ✅ Emojis corretos

---

## 📊 ESTRUTURA RECOMENDADA

### Template Básico
```python
{
    "title": "Nome do Template",
    "emoji": "🎯",
    "atividade": "Categoria",  # Para PERSONAL
    "description": "Descrição padrão do template",
    
    # Campos variáveis passados na criação:
    # - date
    # - status
    # - custom_data (opcional)
}
```

### Template com Customização
```python
def create_custom_card(self, custom_param, date, status):
    """Template com parâmetro customizável"""
    
    title = f"Padrão: {custom_param}"
    description = f"Descrição com {custom_param}"
    
    custom_data = {
        "title": title,
        "description": description
    }
    
    return self.create_card_from_template(
        "template_base",
        date,
        status,
        custom_data
    )
```

---

## 💡 EXEMPLOS DE USO

### Criar Cards da Semana
```python
from models.personal_templates import PersonalTemplates
from datetime import datetime, timezone, timedelta

templates = PersonalTemplates(TOKEN)
SAO_PAULO_TZ = timezone(timedelta(hours=-3))

# Segunda-feira
segunda = datetime(2025, 10, 28, tzinfo=SAO_PAULO_TZ)

# Cards com status diferentes
status_map = {
    "planejamento_semanal": "Concluído",      # Já feito
    "pagamento_hamilton": "Em andamento",     # Fazendo agora
    "tratamento_medico": "Não iniciado"       # Ainda não
}

card_ids = templates.create_weekly_cards(segunda, status_map)
```

---

## 🔧 COMO CRIAR NOVO TEMPLATE

### Passo 1: Definir Template
```python
# Em personal_templates.py
self.templates["novo_evento"] = {
    "title": "Título do Evento",
    "emoji": "🎯",
    "atividade": "Categoria",
    "description": "Descrição do evento"
}
```

### Passo 2: Usar Template
```python
card_id = templates.create_card_from_template(
    "novo_evento",
    "2025-11-01",
    status="Não iniciado"
)
```

### Passo 3: Documentar
- Adicionar ao guia `TEMPLATES_PESSOAIS_GUIA.md`
- Atualizar README.md
- Fazer commit

---

## ✅ VANTAGENS

### 1. Consistência
- Todos os cards seguem mesmo padrão
- Emojis corretos
- Descrições padronizadas

### 2. Produtividade
- Criação rápida
- Menos erros
- Automação simples

### 3. Manutenção
- Um lugar para atualizar
- Mudanças propagam automaticamente
- Código organizado

---

## 📈 ESTATÍSTICAS

### Templates Pessoais
- Templates ativos: 8
- Cards criados: 15+ (desde implementação)
- Taxa de sucesso: 100%

### Testes Realizados
- ✅ Planejamento Semanal
- ✅ Pagamento Hamilton
- ✅ Tratamento Médico
- ✅ Consulta Médica (2 testes)
- ✅ Cards retroativos (5 cards)

---

## 🔗 LINKS

### Código
- **PersonalTemplates:** `/Projetos/Automações/notion-automations/notion-automation-scripts/models/personal_templates.py`
- **GitHub:** https://github.com/LucasBiason/notion-automation-scripts

### Documentação
- **Guia Completo:** `TEMPLATES_PESSOAIS_GUIA.md`
- **Manual Notion:** `../Manual_Notion/`

---

**Última Atualização:** 22/10/2025  
**Templates Disponíveis:** 1 (Personal)  
**Planejados:** 3 (Work, Studies, YouTube)













