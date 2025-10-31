# Rules System

Core rules that all agents must follow.

## Timezone Rules

### Rule: ALWAYS GMT-3

All dates and times must use GMT-3 timezone (Sao Paulo, Brazil).

```python
from datetime import datetime, timezone, timedelta

SAO_PAULO_TZ = timezone(timedelta(hours=-3))
dt = datetime(2025, 11, 1, 19, 0, 0, tzinfo=SAO_PAULO_TZ)
formatted = dt.isoformat()
```

**Format:** `2025-11-01T19:00:00-03:00`

**NEVER use:**
- UTC (Z or +00:00)
- No timezone
- Other timezones

---

## Status Rules

### Ignored Statuses (Task Checking)

These statuses indicate tasks that should be ignored in overdue checks:

```python
IGNORED_STATUSES = [
    "Concluido",
    "Completo",
    "Done",
    "Cancelado",
    "Realocada",
    "Descartado",
    "Publicado"
]
```

**Reason:** These tasks are either completed, cancelled, or no longer user's responsibility.

---

## Notion Integration Rules

### Card Creation

1. **Icons:** Set via page icon property (not in title)
2. **Timezone:** Always GMT-3
3. **Validation:** Check for duplicates before creating
4. **Properties:** Use exact property names from schema

### Card Updates

1. **Verify existence** before updating
2. **Preserve** unmodified properties
3. **Validate** dates and statuses
4. **Log** all changes

---

## Schedule Rules

### Study Hours

**Monday, Wednesday, Thursday, Friday:**
- 19:00-21:00 (2 hours)

**Tuesday:**
- 19:30-21:00 (1.5 hours - after medical treatment)

**Hard Limit:** 21:00 (NEVER exceed)

**Overflow:** Move to next available day

### Work Hours

**Monday-Friday:**
- 08:00-17:00

**Tuesday:**
- 08:00-16:00 (medical treatment 16:00-19:00)

### Content Creation

**Daily:**
- 21:00-00:00 (recording/editing)

**Weekends:**
- Flexible (sprint recording sessions)

---

## YouTube Production Rules

### Core Principle

**Focus on LAUNCH DATE, not recording date.**

### Goal

**Always have episodes RECORDED for the entire week.**

### Weekend Strategy

1. Record fastest series first (complete 100%)
2. Then record longer series (complete 100%)
3. If time remains: Pull episodes from following week

### Priorities

1. **Urgent:** Launch in 0-3 days
2. **Important:** Launch in 4-7 days
3. **Planned:** Launch in 8+ days

### Episode Statuses

- **Publicado:** Completed (ignore)
- **Para Edicao:** Recorded, needs editing
- **Gravando:** In progress
- **Para Gravar:** Not recorded yet

---

## Task Verification Rules

### General

Check if task is overdue by comparing:
- Date/Period property vs current date
- Ignore tasks with ignored statuses

### YouTube Special Logic

For editing statuses (Para Edicao, Editando, Revisao):
- Check **Launch Date** field (not Period)
- Only overdue if Launch Date < Today
- Period is when it was/will be recorded

---

## Data Privacy Rules

### Public vs Private

**Public (can be shared):**
- Generic rules
- Templates
- Architecture
- Examples
- Documentation

**Private (never share):**
- Notion database IDs
- API tokens
- Personal schedules
- Medical information
- Work details
- Specific workflows

### .gitignore Strategy

All private configurations in:
- `config/private/`
- `config/agents/*-personal.mdc`
- `config/agents/*-work.mdc`
- `config/config.json`

---

## Agent Coordination Rules

### All Agents Must

1. **Monitor Notion:** Check databases regularly
2. **Update Cards:** Create/update when needed
3. **Check Calendar:** Verify timeboxes and conflicts
4. **Respect Schedule:** Never exceed time limits
5. **Share Context:** Update shared knowledge base

### Inter-Agent Communication

1. **Delegation:** Coordinator delegates to specialists
2. **Context Passing:** Full context shared between agents
3. **Result Reporting:** All agents report back
4. **Error Handling:** Failures are logged and reported

---

## Validation Rules

### Before Creating Cards

- [ ] Timezone is GMT-3
- [ ] No duplicate cards
- [ ] All required properties present
- [ ] Status is valid
- [ ] Dates are properly formatted

### Before Scheduling

- [ ] Time slot is available
- [ ] No conflicts with existing tasks
- [ ] Within working hours
- [ ] Respects hard limits (21:00 for studies)

---

## Best Practices

1. **Be Explicit:** Clear communication with user
2. **Validate First:** Check before executing
3. **Log Everything:** Maintain audit trail
4. **Error Gracefully:** Handle failures properly
5. **Stay in Sync:** Keep Notion updated
6. **Respect Privacy:** Never expose sensitive data

---

Last Updated: 2024-11-01  
Version: 1.0




