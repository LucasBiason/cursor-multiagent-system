# Agent Configurations

This directory contains agent definition files.

## Structure

Each agent is defined in a `.mdc` (Markdown Context) file:

```
agents/
├── personal-assistant.mdc    # Entry point coordinator
├── studies-assistant.mdc         # Teaching specialist
├── work-assistant.mdc            # Development specialist
├── social-media-assistant.mdc    # Content specialist
├── cicd-agent.mdc            # CI/CD and deployment specialist
├── programming.mdc           # Programming rules (ALL AGENTS - MANDATORY)
└── README.md                 # This file
```

## Technical Rules

**ALL agents must follow `programming.mdc`** which contains:
- REST API Best Practices (MANDATORY)
- Architecture Patterns (Django, FastAPI)
- Code Standards (Python, TypeScript)
- Testing Requirements
- Security Best Practices
- Git Workflow
- Deployment Standards
- React/TypeScript Best Practices

## Agent File Format

Each agent file must include:
- Role definition
- Responsibilities
- Configuration (without sensitive data)
- Rules (reference programming.mdc)
- Capabilities
- Triggers
- Examples (without sensitive data)
- Integration points

## Privacy and Security

### Sensitive Information
- **NEVER** include in agent files:
  - IP addresses
  - Passwords or credentials
  - Client names
  - Project names (use generic descriptions)
  - Email addresses
  - API keys or tokens
  - Server hostnames with IPs

### Where to Store Sensitive Data
- Credentials: `.env.passwords` (gitignored)
- Project details: `config/CONTEXTO_TRABALHO.md`, `config/CONTEXTO_ESTUDOS.md`
- Deployment configs: `config/cicd/projects/` (without credentials)
- General Context: `core/agents/general-context.mdc` (ALWAYS applies to all agents)
- Notion IDs: No projeto do MCP (`my-local-place/services/external/notion-automation-suite/config/.env` - gitignored)
- Schedule: `config/system/schedule/schedule.md` (official schedule)

### Examples in Agent Files
- Use generic examples (e.g., "project" instead of "ExpenseIQ")
- Use placeholder IPs (e.g., "server.example.com" instead of real IPs)
- Use placeholder credentials ("[From .env.passwords]")

## Updating Agents

When updating agents:
1. **Add technical rules**: Reference `programming.mdc`
2. **Remove sensitive data**: IPs, passwords, client names
3. **Update examples**: Make them generic
4. **Keep structure**: Maintain agent file format
5. **Test triggers**: Ensure agent activates correctly

## Creating a New Agent

1. Copy template:
```bash
cp ../templates/agent-template.mdc new-agent.mdc
```

2. Edit with your agent's specifics
3. Reference `programming.mdc` for technical standards
4. Remove all sensitive information
5. Register in `config.json`
6. Test activation

## Loading Agents in Cursor

Agents are automatically loaded by Cursor from this directory.

Cursor looks for:
- `.mdc` files
- Registered in `config.json`
- Proper trigger keywords

## Testing Agents

Test each agent with its trigger keywords:

```
"[trigger keyword] test request"
```

Agent should activate and respond appropriately.

---

**Last Updated:** 2025-12-08  
**Version:** 2.0
