# Configuration Directory

This directory contains all configuration files for your multiagent system.

## Structure

```
config/
├── agents/              # Agent definition files
├── workflows/           # Workflow definitions
├── rules/              # Business rules
├── private/            # Private data (gitignored)
├── config.json         # Main configuration
└── README.md           # This file
```

## Privacy

Files in `config/private/` and personal agent files are gitignored to protect sensitive information.

### What Goes in Private

- Notion database IDs
- API keys and tokens
- Personal schedule details
- Medical information
- Work client data
- Specific project details

### What's Public

- Generic agent templates
- Rule frameworks
- Configuration schemas
- Documentation

## Configuration Files

### config.json

Main system configuration:
- Agent definitions
- System settings
- Background jobs
- Integration configs

### agents/

Agent definition files (.mdc format):
- personal-assistant.mdc
- studies-coach.mdc
- work-coach.mdc
- social-media-coach.mdc

### workflows/

Workflow definitions (.yml format):
- morning-routine.yml
- weekly-planning.yml
- recording-sprint.yml

### rules/

Business rule definitions:
- Public rules (shareable)
- Private rules (gitignored)

### private/

Sensitive data:
- notion-ids.json (database IDs)
- user-context.md (personal details)
- work-context.md (work specifics)
- youtube-context.md (series data)

## Backup Strategy

Private configs should be backed up separately:

1. Local backup:
```bash
tar -czf ~/backups/multiagent-config-$(date +%Y%m%d).tar.gz config/private/
```

2. Private git repo (recommended):
```bash
cd config/private
git init
git add .
git commit -m "Backup config"
git remote add origin [your-private-repo]
git push origin main
```

## Usage

Agents automatically load:
1. Public rules from core/docs/
2. Private rules from config/rules/private-*
3. Personal context from config/private/
4. System config from config.json

Combined to create complete agent context.

## Validation

Before using:

```bash
./scripts/validate.sh
```

Checks:
- Required files exist
- JSON syntax is valid
- No sensitive data in public files
- Environment variables set

---

Last Updated: 2024-11-01




