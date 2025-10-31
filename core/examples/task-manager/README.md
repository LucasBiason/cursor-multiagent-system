# Task Manager Example

Complete example of a task management agent system.

## Overview

This example demonstrates how to create a coordinated multi-agent system for task management using:
- Coordinator agent (entry point)
- Task agent (CRUD operations)
- Calendar agent (scheduling)
- Report agent (analytics)

## Agents

### 1. Task Coordinator

Entry point that delegates to specialist agents.

See: `coordinator-agent.mdc`

### 2. Task Manager

Handles task CRUD operations.

See: `task-agent.mdc`

### 3. Calendar Manager

Manages scheduling and conflicts.

See: `calendar-agent.mdc`

### 4. Report Generator

Creates task reports and analytics.

See: `report-agent.mdc`

## Usage

### Basic Commands

```
"Show my tasks for today"
"Create task: Review PR tomorrow at 14:00"
"Mark task X as complete"
"Generate weekly report"
```

### Advanced

```
"Plan my week"
→ Coordinator delegates to:
  - Calendar: Find available slots
  - Task: List pending tasks
  - Report: Generate priorities

Result: Organized week plan
```

## Setup

1. Copy agent files to your config/agents/
2. Edit with your specific needs
3. Register in config.json
4. Test with Cursor Composer

## Customization

Modify agents to fit your workflow:
- Change task properties
- Adjust scheduling rules
- Customize reports
- Add integrations

## Integration

Can integrate with:
- Notion
- Google Calendar
- Todoist
- Linear
- Jira

See integration examples in each agent file.

---

Version: 1.0

