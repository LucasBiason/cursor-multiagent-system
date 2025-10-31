# Agent Configurations

This directory contains agent definition files.

## Structure

Each agent is defined in a `.mdc` (Markdown Context) file:

```
agents/
├── personal-assistant.mdc    # Entry point coordinator
├── studies-coach.mdc         # Teaching specialist
├── work-coach.mdc            # Development specialist
├── social-media-coach.mdc    # Content specialist
└── template-*.mdc            # Public templates
```

## Agent File Format

See `core/templates/agent-template.mdc` for the standard template.

Each agent file must include:
- Role definition
- Responsibilities
- Configuration
- Rules
- Capabilities
- Triggers
- Examples
- Integration points

## Privacy

Agent files containing sensitive information:
- Are gitignored (see .gitignore)
- Contain actual Notion IDs, tokens, personal data
- Should be backed up separately

Public template files:
- Are committed to git
- Contain no sensitive data
- Serve as examples for others

## Creating a New Agent

1. Copy template:
```bash
cp ../core/templates/agent-template.mdc new-agent.mdc
```

2. Edit with your agent's specifics

3. Register in config.json

4. Test activation

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

Last Updated: 2024-11-01




