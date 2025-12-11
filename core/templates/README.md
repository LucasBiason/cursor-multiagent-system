# Agent Templates

This directory contains templates for creating new agents.

## Available Templates

### Agent Template
- **`agent-template.mdc`** - Base template for creating new agent definitions

## Usage

1. Copy the template:
   ```bash
   cp agent-template.mdc ../agents/my-new-agent.mdc
   ```

2. Fill in the template with:
   - Agent name and role
   - Core responsibilities
   - Configuration details
   - Rules and best practices
   - Capabilities and triggers
   - Integration points

3. Reference mandatory files:
   - `core/agents/programming.mdc` - For any code-related work
   - `core/agents/notion.mdc` - For Notion operations

## Agent Naming Convention

- Use `-assistant.mdc` suffix (not `-coach.mdc`)
- Examples: `personal-assistant.mdc`, `work-assistant.mdc`, `studies-assistant.mdc`

## Important Notes

- All agents should reference `programming.mdc` when working with code
- All agents should reference `notion.mdc` when working with Notion
- Sensitive information should be in `config/` (private submodule)
- Non-sensitive rules and processes go in agent `.mdc` files

---

**Last Updated:** 2025-12-08
