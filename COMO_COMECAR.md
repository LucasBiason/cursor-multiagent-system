# Como Comecar a Usar

Guia pratico para comecar a usar o sistema multiagente hoje mesmo.

## Configuracao Inicial (5 min)

### Passo 1: Validar Estrutura

```bash
cd /home/lucas-biason/Projetos/Infraestrutura/cursor-multiagent-system
./scripts/validate.sh
```

Se aparecer "VALIDATION PASSED": Continuar  
Se aparecer erros: Verificar o que falta

---

### Passo 2: Configurar Notion API

```bash
# Adicionar ao .zshrc
echo 'export NOTION_API_KEY="secret_xyz..."' >> ~/.zshrc
source ~/.zshrc

# Verificar
echo $NOTION_API_KEY
```

---

### Passo 3: Testar Primeiro Comando

Abrir Cursor neste diretorio:

```bash
cursor .
```

No Cursor, abrir chat e testar:

```
"Bom dia, qual meu status?"
```

**Se Personal Assistant responder:** Sistema funcionando!

---

## Usando os Agentes

### Personal Assistant (Sempre Ativo)

Use para:
- Verificar agenda
- Criar cards no Notion
- Gerar relatorios
- Coordenar outros agentes

Comandos:
```
"Bom dia, meu status"
"Qual minha agenda de hoje?"
"Criar card: [descricao]"
"Verificar tarefas atrasadas"
"Gerar relatorio semanal"
"Prepare minha semana"
```

---

### Studies Coach (Estudos)

Use para:
- Estudar conceitos de IA/ML
- Guia em projetos de aprendizado
- Revisoes de aulas
- Reorganizar cronograma

Comandos:
```
"Retomar projeto ML Spam Classifier"
"Criar revisao da Aula 10"
"Como funciona LoRA?"
"Explica fine tuning"
"Reorganizar cronograma FIAP"
```

---

### Work Coach (Trabalho)

Use para:
- Programacao profissional
- Bug fixes
- Code review
- Deploy e testes

Comandos:
```
"Bug no ExpenseIQ, user_service"
"Implementar filtro de data"
"Code review deste arquivo"
"Deploy user service"
"Rodar testes"
```

---

### Social Media Coach (Conteudo)

Use para:
- Planejar gravacoes
- Organizar series
- Agendar lancamentos
- Instagram StuffsCode

Comandos:
```
"Status das gravacoes"
"O que gravar hoje?"
"Planejar fim de semana"
"Proximos lancamentos"
"Criar serie nova: [nome]"
```

---

## Fluxo de Trabalho Diario

### Manha (07:00)

```
"Bom dia, meu status de hoje"
```

Recebe:
- Agenda do dia
- Tarefas pendentes
- Proximos compromissos
- Prioridades

---

### Durante o Dia

**Trabalhando:**
```
"Bug no ExpenseIQ"
→ Work Coach ativa

[Corrige bug]

"Pronto, volta pro contexto anterior"
→ Retoma o que estava fazendo
```

**Estudando:**
```
"Retomar ML Spam"
→ Studies Coach ativa
→ Guia passo a passo

[Faz uma parte]

"Pausa aqui, preciso gravar"
→ Social Media Coach ativa
→ Studies Coach pausa (salva contexto)
```

**Criando Cards:**
```
"Criar lembrete: ligar banco 14h"
→ Personal Assistant cria card
→ Continua contexto anterior
```

---

### Noite (23:00)

```
"Resumo do dia"
```

Recebe:
- O que foi feito
- XP ganho
- Pendencias
- Plano para amanha

---

### Domingo (23:00)

```
"Maestro, prepare minha semana"
```

Sistema:
1. Cria 3 cards semanais
2. Verifica atrasos
3. Gera relatorio
4. Mostra plano da semana

---

## Trocar Entre Agentes

### Sem Perder Contexto

```
Voce: "Retomar ML Spam"
Studies Coach: [Guiando projeto...]

Voce: "Espera, bug urgente"
Work Coach: [Ativa, Studies pausa]

Voce: "Pronto, volta"
Studies Coach: [Retoma exatamente onde parou]
```

**Contexto nunca se perde!**

---

## Primeiros Testes Recomendados

### Teste 1: Status

```
"Qual meu status atual?"
```

Deve mostrar: agenda, tarefas, proximos eventos

---

### Teste 2: Criar Card

```
"Criar card: Teste do sistema, amanha 10h"
```

Deve:
- Criar no Notion (base Personal)
- Confirmar criacao
- Mostrar link

---

### Teste 3: Trocar Contexto

```
"Retomar projeto ML Spam"
→ Studies Coach ativa

"Criar card: lembrete teste"
→ Personal Assistant cria (Studies continua)

"Como estou no projeto?"
→ Studies Coach responde contexto
```

---

### Teste 4: Verificar Atrasos

```
"Verificar tarefas atrasadas"
```

Deve:
- Buscar em todas as bases
- Ignorar status corretos
- Reportar apenas realmente atrasadas

---

## Troubleshooting

### Agente nao ativa

Verificar:
- Arquivo .mdc existe
- Registrado em config.json
- Triggers corretos
- Cursor Composer habilitado

### Notion nao atualiza

Verificar:
- NOTION_API_KEY configurada
- IDs do Notion corretos
- Permissoes da API
- Timezone GMT-3

### Contexto nao compartilha

Verificar:
- Cursor 2.0 instalado
- context_sharing: true
- unified_history: true
- Mesma conversa (nao tabs separadas)

---

## Dicas de Uso

1. **Seja natural:** Fale normalmente, sistema entende
2. **Confie na delegacao:** Sistema escolhe agente certo
3. **Troque livremente:** Mude contexto quando quiser
4. **Verifique sempre:** Pergunte status/agenda
5. **Use background:** Configure automacoes

---

## Roadmap do Piloto

### Semana 1 (01-03/11)
- Setup e primeiros testes
- Validar agentes basicos
- Coletar feedback inicial

### Semana 2 (04-10/11)
- Uso diario intensivo
- Refinar triggers
- Otimizar respostas

### Semana 3 (11-17/11)
- Automacoes background
- Workflows avancados
- Metricas de produtividade

### Semana 4 (18-24/11)
- Funcionalidades avancadas
- Edge cases
- Estabilidade

### Semana 5 (25-30/11)
- Avaliacao final
- Metricas consolidadas
- Decisao: open source?

---

## Metricas a Acompanhar

Registrar diariamente em `logs/pilot-daily.md`:

- Quantas vezes usou sistema
- Quais agentes ativou
- Tempo economizado (estimativa)
- Problemas encontrados
- Sugestoes de melhoria

---

## Objetivo do Piloto

Validar:
- 20% ganho de produtividade
- Uso diario consistente
- Sistema estavel
- Documentacao adequada
- Pronto para compartilhar

---

## Comece Agora

```bash
# 1. Validar
./scripts/validate.sh

# 2. Abrir Cursor
cursor .

# 3. Testar
"Bom dia, qual meu status?"

# 4. Usar!
```

**Sistema pronto para uso!**

---

Last Updated: 2024-11-01  
Version: 1.0.0  
Phase: Pilot Started



