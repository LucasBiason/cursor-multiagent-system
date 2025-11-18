# Quick Start Guide

Get up and running with the Cursor Multiagent System in 10 minutes.

## Step 1: Setup (2 min)

```bash
cd /path/to/cursor-multiagent-system
./scripts/setup.sh
```

## Step 2: Configure (5 min)

### Edit User Context

```bash
git submodule update --init config
nano config/user-context.md
```

Add your:
- Name and timezone
- Work schedule
- Study hours
- Preferences

### Configure Notion IDs

```bash
nano config/notion-ids.json
```

Add your Notion database IDs.

### Set Environment Variables

```bash
export NOTION_API_KEY="your_notion_api_key_here"
```

Add to your `.zshrc` or `.bashrc` to persist.

## Step 3: Validate (1 min)

```bash
./scripts/validate.sh
```

Should show: "VALIDATION PASSED"

## Step 4: Test Agents (2 min)

Open Cursor and try:

```
"Bom dia, qual meu status?"
```

Personal Assistant should respond with your agenda.

```
"Retomar projeto X"
```

Studies Coach should activate for project guidance.

## Step 5: Use Daily

### Morning

```
"Bom dia, meu status de hoje"
```

### During Day

```
"Criar card: [task description]"
"Retomar projeto X"
"Bug no [project]"
"O que gravar hoje?"
```

### Evening

```
"Resumo do dia"
"Prepare minha semana" (Sundays)
```

## Common Commands

### Personal Assistant
- "Qual minha agenda?"
- "Criar card: [description]"
- "Verificar tarefas atrasadas"
- "Gerar relatorio semanal"

### Studies Coach
- "Retomar projeto [name]"
- "Criar revisao da Aula X"
- "Como funciona [concept]?"
- "Reorganizar cronograma"

### Work Coach
- "Bug no [project]"
- "Implementar [feature]"
- "Code review"
- "Deploy"

### Social Media Coach
- "Status das gravacoes"
- "O que gravar hoje?"
- "Planejar fim de semana"
- "Proximos lancamentos"

## Tips

1. **Be Natural:** Talk normally, Composer understands context
2. **Trust Delegation:** System picks right agent automatically
3. **Switch Freely:** Can change context anytime
4. **Check Status:** Ask for status/agenda anytime
5. **Validate First:** System validates before executing

## Troubleshooting

### Agent Not Activating

Check triggers in agent file match your request keywords.

### Notion Errors

Verify:
- API key is valid
- Database IDs are correct
- Permissions are granted

### Timezone Issues

Ensure all dates use GMT-3 (or your timezone in config).

## Next Steps

- Read [Architecture](ARCHITECTURE.md)
- Explore [Examples](core/examples/)
- Customize agents for your needs
- Set up background automation

---

Ready to boost your productivity!

Last Updated: 2024-11-01

