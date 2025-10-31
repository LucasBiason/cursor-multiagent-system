# 🏠 TEMPLATES PESSOAIS - GUIA COMPLETO

**Data:** 22/10/2025  
**Versão:** 1.0  
**Status:** Implementado e Funcionando  
**Script:** `/Projetos/Automações/notion-automations/notion-automation-scripts/models/personal_templates.py`

---

## 🎯 OBJETIVO

Sistema de templates para criar cards pessoais padronizados no Notion, onde apenas **data e hora** mudam.

---

## 📋 TEMPLATES DISPONÍVEIS

### 1. 📝 Planejamento Semanal
```python
{
    "title": "Planejamento Semanal",
    "emoji": "📝",
    "atividade": "Gestão",
    "description": "Revisão do planejamento de tarefas para a semana."
}
```

**Quando:** Segunda-feira (semanal)

---

### 2. 💰 Pagamento Hamilton (Médico)
```python
{
    "title": "Pagamento Hamilton (Médico)",
    "emoji": "💰",
    "atividade": "Finanças",
    "description": "Realizar a transferência bancária e o envio do comprovante"
}
```

**Quando:** Segunda-feira (semanal)

---

### 3. 🏥 Tratamento Médico
```python
{
    "title": "Tratamento Médico",
    "emoji": "🏥",
    "atividade": "Saúde",
    "description": "Sessão de tratamento sempre as terças das 16:00 as 18:00"
}
```

**Quando:** Terça-feira 16:00-18:00 (semanal)

---

### 4. 📊 Revisão Financeira - Recebimentos
```python
{
    "title": "Revisão Financeira - Recebimento e Pagamentos",
    "emoji": "📊",
    "atividade": "Finanças",
    "description": "Revisão Financeira dos gastos até o momento no mês. Atualizar a Planilha de Controle."
}
```

**Quando:** Dia 15 de cada mês

---

### 5. 📊 Revisão Financeira - Fechamento
```python
{
    "title": "Revisão Financeira - Fechamento do Mês",
    "emoji": "📊",
    "atividade": "Finanças",
    "description": "Revisão Financeira dos gastos até o momento no mês. Atualizar a Planilha de Controle."
}
```

**Quando:** Último dia do mês

---

### 6. 💸 Pagamento Contadora e Impostos
```python
{
    "title": "Pagamento Contadora e Impostos",
    "emoji": "💸",
    "atividade": "Finanças",
    "description": "Verificar impostos na plataforma\nLink: https://app.contabilizei.com.br/\nVerificar valores e atualizar na planilha de controle contábil"
}
```

**Quando:** Dia 15 de cada mês

---

### 7. 📄 Emissão de Nota Fiscal Astracode
```python
{
    "title": "Emissão de Nota Fiscal Astracode",
    "emoji": "📄",
    "atividade": "Finanças",
    "description": "Emitir Nota Fiscal para Astracode"
}
```

**Quando:** Dia 25 de cada mês

---

### 8. 🏥 Consulta Médica (DINÂMICO)
```python
{
    "title": "Consulta Médica: <Médico> <Especialidade>",
    "emoji": "🏥",
    "atividade": "Saúde",
    "description": "Consulta médica com especialista"
}
```

**Quando:** Conforme agendamento  
**Especial:** Título personalizável com nome do médico e especialidade

---

## 💻 COMO USAR

### Instalação
```python
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'models'))

from personal_templates import PersonalTemplates
```

### Inicialização
```python
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('NOTION_API_TOKEN')

templates = PersonalTemplates(TOKEN)
```

---

## 🔨 MÉTODOS DISPONÍVEIS

### 1. create_card_from_template()

**Uso Simples:**
```python
# Criar Planejamento Semanal
card_id = templates.create_card_from_template(
    template_name="planejamento_semanal",
    date="2025-10-28",
    status="Não iniciado"
)
```

**Com Dados Customizados:**
```python
# Sobrescrever campos
card_id = templates.create_card_from_template(
    template_name="planejamento_semanal",
    date="2025-10-28",
    status="Em andamento",
    custom_data={"description": "Descrição personalizada"}
)
```

---

### 2. create_consulta_medica()

**Uso:**
```python
card_id = templates.create_consulta_medica(
    medico="Doutora Andrea",
    especialidade="Endocrino",
    date="2025-10-14",
    hora_inicio="8:00",
    hora_fim="10:20",
    status="Concluído"
)
```

**Resultado:**
- Título: `Consulta Médica: Doutora Andrea Endocrino`
- Descrição: `Consulta médica com Doutora Andrea - Endocrino\nHorário: 8:00 às 10:20`
- Emoji: 🏥
- Status: Concluído

---

### 3. create_weekly_cards()

**Uso:**
```python
from datetime import datetime, timezone, timedelta

# Próxima segunda-feira
SAO_PAULO_TZ = timezone(timedelta(hours=-3))
proxima_segunda = datetime(2025, 10, 28, tzinfo=SAO_PAULO_TZ)

# Status de cada card
status_map = {
    "planejamento_semanal": "Não iniciado",
    "pagamento_hamilton": "Não iniciado",
    "tratamento_medico": "Não iniciado"
}

# Criar cards
card_ids = templates.create_weekly_cards(proxima_segunda, status_map)
```

**Resultado:**
- Planejamento Semanal (Segunda)
- Pagamento Hamilton (Segunda)
- Tratamento Médico (Terça)

---

### 4. create_monthly_cards()

**Uso:**
```python
from datetime import datetime, timezone, timedelta

# Mês atual
SAO_PAULO_TZ = timezone(timedelta(hours=-3))
mes_ref = datetime(2025, 10, 1, tzinfo=SAO_PAULO_TZ)

# Status de cada card
status_map = {
    "revisao_financeira_recebimentos": "Não iniciado",
    "pagamento_contadora_impostos": "Não iniciado",
    "nota_fiscal_astracode": "Não iniciado",
    "revisao_financeira_fechamento": "Não iniciado"
}

# Criar cards
card_ids = templates.create_monthly_cards(mes_ref, status_map)
```

**Resultado:**
- Dia 15: Revisão Financeira - Recebimentos
- Dia 15: Pagamento Contadora e Impostos
- Dia 25: Emissão de Nota Fiscal
- Dia 30: Revisão Financeira - Fechamento

---

## 📅 CALENDÁRIO DE RECORRÊNCIAS

### Eventos Semanais

| Dia | Evento | Horário | Template |
|-----|--------|---------|----------|
| Segunda | Planejamento Semanal | Manhã | `planejamento_semanal` |
| Segunda | Pagamento Hamilton | Manhã | `pagamento_hamilton` |
| Terça | Tratamento Médico | 16:00-18:00 | `tratamento_medico` |

---

### Eventos Mensais

| Dia | Evento | Template |
|-----|--------|----------|
| 15 | Revisão Financeira | `revisao_financeira_recebimentos` |
| 15 | Pagamento Impostos | `pagamento_contadora_impostos` |
| 25 | Nota Fiscal | `nota_fiscal_astracode` |
| 30 | Fechamento Mensal | `revisao_financeira_fechamento` |

---

## 🔧 EXEMPLOS PRÁTICOS

### Criar Cards da Semana
```python
#!/usr/bin/env python3
from models.personal_templates import PersonalTemplates
from datetime import datetime, timezone, timedelta
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('NOTION_API_TOKEN')

templates = PersonalTemplates(TOKEN)
SAO_PAULO_TZ = timezone(timedelta(hours=-3))

# Próxima segunda
hoje = datetime.now(SAO_PAULO_TZ)
dias_ate_segunda = (7 - hoje.weekday()) % 7 or 7
proxima_segunda = hoje + timedelta(days=dias_ate_segunda)

# Cards semanais
status_map = {
    "planejamento_semanal": "Não iniciado",
    "pagamento_hamilton": "Não iniciado",
    "tratamento_medico": "Não iniciado"
}

card_ids = templates.create_weekly_cards(proxima_segunda, status_map)

print(f"✅ {len(card_ids)} cards semanais criados!")
```

---

### Criar Consulta Médica Emergencial
```python
#!/usr/bin/env python3
from models.personal_templates import PersonalTemplates
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('NOTION_API_TOKEN')

templates = PersonalTemplates(TOKEN)

# Consulta emergencial
card_id = templates.create_consulta_medica(
    medico="Doutor Mario",
    especialidade="Otorino",
    date="2025-10-21",
    status="Concluído"
)

print(f"✅ Consulta médica criada: {card_id}")
```

---

### Criar Cards Retroativos
```python
#!/usr/bin/env python3
from models.personal_templates import PersonalTemplates
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('NOTION_API_TOKEN')

templates = PersonalTemplates(TOKEN)

# Planejamento já concluído
templates.create_card_from_template(
    "planejamento_semanal",
    "2025-10-20",
    status="Concluído"
)

# Pagamento já concluído
templates.create_card_from_template(
    "pagamento_hamilton",
    "2025-10-20",
    status="Concluído"
)

# Consulta médica emergencial
templates.create_consulta_medica(
    "Doutor Mario",
    "Otorino",
    "2025-10-21",
    status="Concluído"
)

print("✅ Cards retroativos criados!")
```

---

## 🎯 PERSONALIZAÇÃO

### Adicionar Novo Template
```python
# Em personal_templates.py
self.templates["novo_template"] = {
    "title": "Nome do Template",
    "emoji": "🎯",
    "atividade": "Categoria",
    "description": "Descrição do template"
}
```

### Usar Novo Template
```python
card_id = templates.create_card_from_template(
    "novo_template",
    "2025-10-25",
    status="Não iniciado"
)
```

---

## 📊 ESTRUTURA DA CLASSE

```python
class PersonalTemplates:
    def __init__(self, token: str)
        # Inicializa com token do Notion
        
    def get_template(self, template_name: str) -> dict
        # Retorna dados do template
        
    def create_card_from_template(
        self, 
        template_name: str, 
        date: str, 
        status: str = "Não iniciado", 
        custom_data: dict = None
    ) -> str
        # Cria card a partir de template
        
    def create_consulta_medica(
        self,
        medico: str,
        especialidade: str,
        date: str,
        hora_inicio: str = "",
        hora_fim: str = "",
        status: str = "Não iniciado"
    ) -> str
        # Cria consulta médica personalizada
        
    def create_weekly_cards(
        self,
        start_date: datetime,
        status_map: dict
    ) -> list
        # Cria cards semanais recorrentes
        
    def create_monthly_cards(
        self,
        month_date: datetime,
        status_map: dict
    ) -> list
        # Cria cards mensais recorrentes
```

---

## ✅ VALIDAÇÕES AUTOMÁTICAS

### O que a Classe Valida
- ✅ Template existe
- ✅ Data no formato correto (YYYY-MM-DD)
- ✅ Status válido
- ✅ Emoji aplicado corretamente
- ✅ Descrição completa

### O que NÃO Valida
- ❌ Duplicação de cards (responsabilidade do sistema)
- ❌ Conflitos de horário (responsabilidade do Monitor Integrado)

---

## 🔄 INTEGRAÇÃO COM OUTROS SISTEMAS

### Com NotionEngine
```python
# PersonalTemplates usa NotionEngine internamente
self.engine = NotionEngine(token)
card_id = self.engine.create_card("PERSONAL", card_data)
```

### Com Agente 1 (Gerenciador de Cards Semanais)
```python
# Agente 1 pode usar PersonalTemplates
from models.personal_templates import PersonalTemplates

templates = PersonalTemplates(TOKEN)
card_ids = templates.create_weekly_cards(proxima_segunda, status_map)
```

---

## 📝 EXEMPLO COMPLETO DE USO

```python
#!/usr/bin/env python3
"""
Exemplo completo de uso dos templates pessoais
"""

import os
import sys
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

# Setup
sys.path.append(os.path.join(os.path.dirname(__file__), 'models'))
from personal_templates import PersonalTemplates

load_dotenv()
TOKEN = os.getenv('NOTION_API_TOKEN')
SAO_PAULO_TZ = timezone(timedelta(hours=-3))

# Inicializar
templates = PersonalTemplates(TOKEN)

# 1. Criar cards semanais
print("📅 Criando cards semanais...")
proxima_segunda = datetime(2025, 10, 28, tzinfo=SAO_PAULO_TZ)

status_map_semanal = {
    "planejamento_semanal": "Não iniciado",
    "pagamento_hamilton": "Não iniciado",
    "tratamento_medico": "Não iniciado"
}

weekly_ids = templates.create_weekly_cards(proxima_segunda, status_map_semanal)
print(f"✅ {len(weekly_ids)} cards semanais criados")

# 2. Criar cards mensais
print("\n💰 Criando cards mensais...")
mes_ref = datetime(2025, 10, 1, tzinfo=SAO_PAULO_TZ)

status_map_mensal = {
    "revisao_financeira_recebimentos": "Não iniciado",
    "pagamento_contadora_impostos": "Não iniciado",
    "nota_fiscal_astracode": "Não iniciado",
    "revisao_financeira_fechamento": "Não iniciado"
}

monthly_ids = templates.create_monthly_cards(mes_ref, status_map_mensal)
print(f"✅ {len(monthly_ids)} cards mensais criados")

# 3. Criar consulta médica personalizada
print("\n🏥 Criando consulta médica...")
consulta_id = templates.create_consulta_medica(
    medico="Doutora Andrea",
    especialidade="Endocrino",
    date="2025-11-05",
    hora_inicio="8:00",
    hora_fim="10:20",
    status="Não iniciado"
)
print(f"✅ Consulta médica criada: {consulta_id}")

print("\n🎉 Todos os cards criados com sucesso!")
```

---

## 🎨 CUSTOMIZAÇÃO DE TÍTULO (Consulta Médica)

### Formato do Título
```
Consulta Médica: <Médico> <Especialidade>
```

### Exemplos
```python
# Exemplo 1
create_consulta_medica("Doutora Andrea", "Endocrino", "2025-10-14")
# Título: "Consulta Médica: Doutora Andrea Endocrino"

# Exemplo 2
create_consulta_medica("Doutor Mario", "Otorino", "2025-10-21")
# Título: "Consulta Médica: Doutor Mario Otorino"

# Exemplo 3
create_consulta_medica("Dr. João Silva", "Cardiologista", "2025-11-05")
# Título: "Consulta Médica: Dr. João Silva Cardiologista"
```

---

## 📊 TESTES REALIZADOS

### Teste 1: Planejamento Semanal ✅
- Data: 20/10/2025
- Status: Concluído
- Resultado: Card criado com sucesso

### Teste 2: Pagamento Hamilton ✅
- Data: 20/10/2025
- Status: Concluído
- Resultado: Card criado com sucesso

### Teste 3: Consulta Médica ✅
- Médico: Doutora Andrea
- Especialidade: Endocrino
- Data: 14/10/2025
- Horário: 8:00-10:20
- Resultado: Card criado com título personalizado ✅

### Teste 4: Consulta Emergencial ✅
- Médico: Doutor Mario
- Especialidade: Otorino
- Data: 21/10/2025
- Resultado: Card criado para emergência ✅

---

## 🔗 ARQUIVOS RELACIONADOS

### Código
- **Principal:** `/Projetos/Automações/notion-automations/notion-automation-scripts/models/personal_templates.py`
- **Exemplo:** `/Projetos/Automações/notion-automations/notion-automation-scripts/examples/use_personal_templates.py`

### Testes
- **Teste Consulta:** `/Projetos/Automações/notion-automations/notion-automation-scripts/test_consulta_medica.py`
- **Teste Retroativo:** `/Projetos/Automações/notion-automations/notion-automation-scripts/create_retroactive_cards.py`

### Documentação
- **GitHub:** https://github.com/LucasBiason/notion-automation-scripts
- **Commit:** `409a944` (feat: criar classe PersonalTemplates)

---

## ✅ BENEFÍCIOS

### 1. Reutilização
- ✅ Templates definidos uma vez
- ✅ Usados múltiplas vezes
- ✅ Consistência garantida

### 2. Manutenção
- ✅ Centralizado em um arquivo
- ✅ Fácil de atualizar
- ✅ Uma mudança afeta todos os usos

### 3. Produtividade
- ✅ Criação rápida de cards
- ✅ Menos erros
- ✅ Padronização automática

---

## 🎯 PRÓXIMAS EXPANSÕES

### Templates Planejados
- Template de reunião
- Template de backup
- Template de compras
- Template de viagem

### Funcionalidades Futuras
- Validação de duplicação
- Agendamento automático
- Notificações de vencimento
- Integração com Agente 1

---

**Última Atualização:** 22/10/2025  
**Versão:** 1.0  
**Status:** ✅ Implementado e Testado













