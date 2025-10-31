# Rules Configuration

This directory contains rule definitions for the multiagent system.

## Structure

```
rules/
├── public-*.md          # Public, shareable rules
├── private-*.md         # Private rules (gitignored)
└── README.md            # This file
```

## Public Rules

Generic rules that can be shared:
- Timezone handling
- Status management
- Task verification logic
- Agent coordination protocols

See `core/docs/RULES_SYSTEM.md` for public rules.

## Private Rules

User-specific rules (not in git):
- Personal schedule details
- Medical appointments specifics
- Work client information
- Private workflow configurations

## Usage

Agents load rules from both:
1. Public rules (from `core/docs/`)
2. Private rules (from `config/rules/private-*.md`)

Combined rules create the complete ruleset for each agent.

---

Note: All `private-*.md` files are gitignored to protect sensitive information.

