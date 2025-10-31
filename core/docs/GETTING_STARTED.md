# Getting Started

## Overview

This framework enables coordinated multi-agent systems in Cursor IDE 2.0.

## Prerequisites

- Cursor IDE 2.0 or higher
- Python 3.11+
- Notion API access (if using Notion integration)

## Installation

### 1. Clone or Download

```bash
git clone https://github.com/lucasbiason/cursor-multiagent-framework
cd cursor-multiagent-framework
```

### 2. Run Setup

```bash
chmod +x scripts/*.sh
./scripts/setup.sh
```

### 3. Configure

Edit configuration files in `config/`:

```bash
# Edit your user context
nano config/private/user-context.md

# Edit your Notion IDs (if using Notion)
nano config/private/notion-ids.json

# Set environment variables
export NOTION_API_KEY="your_notion_api_key"
```

### 4. Validate

```bash
./scripts/validate.sh
```

## Creating Your First Agent

### Step 1: Generate from Template

```bash
cp core/templates/agent-template.mdc config/agents/my-agent.mdc
```

### Step 2: Edit Agent File

```markdown
# My Agent

## Role
You are a [description]

## Triggers
- "keyword1", "keyword2"

## Examples
[Add examples]
```

### Step 3: Register in Config

Edit `config/config.json`:

```json
{
  "agents": {
    "agents_list": [
      {
        "id": "my-agent",
        "name": "My Agent",
        "file": "config/agents/my-agent.mdc",
        "triggers": ["keyword1", "keyword2"]
      }
    ]
  }
}
```

### Step 4: Test

In Cursor, try:
```
"keyword1 test request"
```

Agent should activate automatically via Composer.

## Using the System

### Basic Usage

Simply talk to Cursor naturally:

```
"Show my agenda for today"
"Help me with this project"
"Create a task for tomorrow"
"What should I work on next?"
```

Cursor Composer will:
1. Analyze your request
2. Activate appropriate agent(s)
3. Execute actions
4. Return consolidated results

### Specific Agent

Call a specific agent:

```
@my-agent specific request
```

### Background Tasks

Configure in `config.json`:

```json
{
  "background_agents": {
    "enabled": true,
    "schedule": {
      "my-agent": {
        "daily_check": "0 8 * * *"
      }
    }
  }
}
```

## Examples

### Example 1: Task Management

```
You: "Create task: Review code tomorrow at 14:00"

System:
- Activates Personal Assistant
- Creates task in Notion
- Sets reminder
- Confirms creation
```

### Example 2: Multi-Agent Coordination

```
You: "Prepare my week"

System:
- Activates Personal Assistant
- Delegates to multiple agents:
  - Create weekly cards
  - Check for overdue tasks
  - Generate weekly report
- Consolidates results
- Shows summary
```

### Example 3: Context Switching

```
You: "Help with ML project"
→ Studies Coach activated

You: "Hold on, fix this bug first"
→ Work Coach activated (Studies Coach paused)

You: "OK, back to ML"
→ Studies Coach resumed (exactly where you left off)
```

## Troubleshooting

### Agents Not Activating

Check:
- Agent file exists in config/agents/
- Registered in config.json
- Triggers are correct
- Cursor Composer is enabled

### Context Not Shared

Verify:
- `context_sharing: true` in config.json
- Cursor 2.0 or higher
- Unified history enabled

### Notion Integration Issues

Check:
- NOTION_API_KEY is set
- Database IDs are correct
- Timezone is GMT-3
- API key has proper permissions

## Next Steps

1. Read [Architecture Overview](../ARCHITECTURE.md)
2. Review [Rules System](RULES_SYSTEM.md)
3. Explore [Examples](../examples/)
4. Create your custom agents
5. Configure workflows

## Support

For issues or questions:
- Check documentation in `core/docs/`
- Review examples in `core/examples/`
- Open an issue on GitHub

---

Version: 1.0  
Last Updated: 2024-11-01

