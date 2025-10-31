# Cursor Multiagent System

A production-ready framework for coordinated AI agent systems in Cursor IDE 2.0.

## Overview

This project provides a modular architecture for creating and managing multiple specialized AI agents that work together to automate workflows, manage tasks, and improve productivity.

## Project Status

**Version:** 1.0.0 (Pilot Phase)  
**Phase:** November 2024 - Testing & Refinement  
**Status:** Active Development

## Architecture

The system consists of 4 main specialized agents:

1. **Personal Assistant** - Entry point, manages agenda, tasks, and Notion workspace
2. **Studies Coach** - Teaching, project guidance, senior programming expertise for learning
3. **Work Coach** - Co-programming, code review, testing, deployment automation
4. **Social Media Coach** - Content strategy for StuffsCode (Instagram + YouTube)

All agents:
- Monitor and update Notion databases
- Check calendar and timeboxes
- Create/update cards automatically
- Respect schedule impacts

## Directory Structure

```
cursor-multiagent-system/
├── core/                    # Public framework (reusable)
│   ├── templates/          # Agent templates
│   ├── schemas/            # Configuration schemas
│   ├── docs/              # Documentation
│   ├── utils/             # Utility scripts
│   └── examples/          # Usage examples
│
├── config/                 # Private configurations
│   ├── agents/            # Agent definitions
│   ├── workflows/         # Workflow definitions
│   ├── rules/             # Business rules
│   └── private/           # Sensitive data
│
├── scripts/               # Utility scripts
├── tests/                 # Test suite
└── .cursor/              # Cursor IDE configs
```

## Key Features

- **Unified Context**: All agents share knowledge and state
- **Notion Integration**: Deep integration with Notion workspace
- **Workflow Automation**: Background tasks and scheduled jobs
- **Modular Design**: Easy to extend and customize
- **Privacy First**: Clear separation between public and private data

## Quick Start

### Prerequisites

- Cursor IDE 2.0+
- Python 3.11+
- Notion API access

### Installation

```bash
# Clone or navigate to project
cd /home/lucas-biason/Projetos/Infraestrutura/cursor-multiagent-system

# Install dependencies
pip install -r requirements.txt

# Setup configuration
./scripts/setup.sh

# Validate setup
./scripts/validate.sh
```

### Configuration

1. Copy example configurations:
```bash
cp config/agents/template-personal-assistant.mdc config/agents/personal-assistant.mdc
```

2. Edit with your specific data (Notion IDs, preferences, etc.)

3. Configure Cursor:
```bash
ln -s $(pwd)/config/agents ~/.cursor/agents
```

## Documentation

- [Architecture Overview](core/docs/ARCHITECTURE.md)
- [Agent Creation Guide](core/docs/AGENT_CREATION.md)
- [Notion Integration](core/docs/NOTION_INTEGRATION.md)
- [Workflows Guide](core/docs/WORKFLOWS.md)
- [Rules System](core/docs/RULES.md)

## Agents

### 1. Personal Assistant

Entry point for all interactions. Manages:
- Daily agenda and schedule
- Notion workspace (4 bases: Personal, Studies, Work, YouTube)
- Task creation and updates
- Calendar and timeboxes
- Coordination with other agents

### 2. Studies Coach

Teaching and project guidance:
- IA/ML concepts and tutorials
- Project-based learning
- Code reviews for learning projects
- Study schedule management
- FIAP coursework assistance

### 3. Work Coach

Professional development support:
- Co-programming sessions
- Code review and testing
- Deployment automation
- Git workflow management
- ExpenseIQ project support

### 4. Social Media Coach

Content strategy and management:
- StuffsCode Instagram content
- YouTube channel planning
- Content calendar
- Episode planning and tracking

## Pilot Phase (November 2024)

Goals:
- Validate productivity improvements
- Refine agent interactions
- Optimize workflows
- Document best practices
- Measure time savings

## Privacy & Security

All sensitive data is:
- Stored in `config/private/`
- Ignored by git (see `.gitignore`)
- Never committed to repository
- Backed up separately

Public repository contains only:
- Generic templates
- Documentation
- Reusable utilities
- Example configurations

## Development

### Adding a New Agent

```bash
# Generate from template
python core/utils/generator.py create-agent \
  --name "my-agent" \
  --role "specialist" \
  --output config/agents/
```

### Testing

```bash
# Run all tests
pytest tests/

# Validate configurations
./scripts/validate.sh
```

## Contributing

This is a personal productivity system, but the core framework is designed to be reusable. Contributions to the public framework are welcome.

## License

MIT License - See LICENSE file for details

## Author

Lucas Biason  
GitHub: [@lucasbiason](https://github.com/lucasbiason)

## Acknowledgments

- Built for Cursor IDE 2.0
- Inspired by multi-agent systems and agentic AI patterns
- Notion API for workspace integration

---

Last Updated: 2024-11-01  
Version: 1.0.0  
Status: Pilot Phase



