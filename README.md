# Cursor Multiagent System

A production-ready framework for coordinated AI agent systems in Cursor IDE 2.0.

## Overview

This project provides a modular architecture for creating and managing multiple specialized AI agents that work together to automate workflows, manage tasks, and improve productivity.

## Project Status

**Version:** 1.1.0  
**Repository:** [github.com/LucasBiason/cursor-multiagent-system](https://github.com/LucasBiason/cursor-multiagent-system)  
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
# Clone the repository
git clone https://github.com/LucasBiason/cursor-multiagent-system.git
cd cursor-multiagent-system

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

### Getting Started
- [Quick Start Guide](QUICK_START.md)
- [Como Começar (PT-BR)](COMO_COMECAR.md)
- [Architecture Overview](ARCHITECTURE.md)
- [Project Summary](PROJECT_SUMMARY.md)

### Development
- [Versioning Guide](docs/VERSIONING_GUIDE.md)
- [Contributing Guidelines](CONTRIBUTING.md)
- [Changelog](CHANGELOG.md)

### Core Framework
- [Getting Started](core/docs/GETTING_STARTED.md)
- [Rules System](core/docs/RULES_SYSTEM.md)
- [Task Manager Example](core/examples/task-manager/README.md)

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

### Workflow

```bash
# 1. Make your changes
# 2. Test locally
./scripts/validate.sh

# 3. Commit and push (automated script)
./scripts/commit-and-push.sh "feat: add new feature"
```

### Testing

```bash
# Run all tests
pytest tests/

# Validate configurations
./scripts/validate.sh
```

## Contributing

Contributions to improve the framework are welcome! Please read the [Contributing Guidelines](CONTRIBUTING.md) and [Versioning Guide](docs/VERSIONING_GUIDE.md) first.

### Quick Contribution Guide

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

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

**Last Updated:** 2025-10-31  
**Version:** 1.1.0  
**Repository:** https://github.com/LucasBiason/cursor-multiagent-system



