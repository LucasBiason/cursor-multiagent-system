# Architecture Overview

## System Design

### High-Level Architecture

```
User Interaction
       |
       v
+-----------------+
| Cursor IDE 2.0  |
|   Composer      |
+-----------------+
       |
       v
+-----------------+
| Personal        |
| Assistant       | <-- Entry Point (Always Active)
| (Coordinator)   |
+-----------------+
       |
       +-- Delegates --> Specialist Agents
       |
       +-------------------+-------------------+-------------------+
       |                   |                   |                   |
       v                   v                   v                   v
+-------------+    +-------------+    +-------------+    +-------------+
| Studies     |    | Work        |    | Social      |    | Gaming      |
| Coach       |    | Coach       |    | Media Coach |    | Manager     |
| (Specialist)|    | (Specialist)|    | (Specialist)|    | (Specialist)|
+-------------+    +-------------+    +-------------+    +-------------+
       |                   |                   |                   |
       +-------------------+-------------------+-------------------+
                           |
                           v
                  +----------------+
                  | Shared Context |
                  | Knowledge Base |
                  +----------------+
                           |
                           v
                  +----------------+
                  | Notion API     |
                  | Integration    |
                  +----------------+
```

## Components

### 1. Personal Assistant (Coordinator)

**Purpose:** Entry point and traffic controller

**Responsibilities:**
- Receive all user requests
- Analyze intent
- Delegate to appropriate specialist
- Consolidate results
- Maintain conversation continuity

**When Active:** Always (default agent)

### 2. Studies Coach (Specialist)

**Purpose:** Teaching and learning project guidance

**Responsibilities:**
- Explain concepts
- Guide through projects
- Create lesson reviews
- Manage study schedule
- Educational code review

**When Active:** Study-related requests

### 3. Work Coach (Specialist)

**Purpose:** Professional development support

**Responsibilities:**
- Co-programming
- Code review
- Testing
- Deployment
- Git workflows

**When Active:** Work-related requests

### 4. Social Media Coach (Specialist)

**Purpose:** Content strategy and production

**Responsibilities:**
- Content planning
- Recording schedule
- Launch coordination
- Series management
- Platform strategy (YouTube + Instagram)

**When Active:** Content-related requests

### 5. Gaming Manager (Specialist)

**Purpose:** Gamification system

**Responsibilities:**
- XP calculations
- Badge checks
- Streak tracking
- Reward management

**When Active:** Gamification requests

## Data Flow

### Request Processing

```
1. User sends message
   |
   v
2. Personal Assistant receives
   |
   v
3. Analyze intent + context
   |
   v
4. Decision: Handle self OR delegate
   |
   +-- Self: Execute directly
   |
   +-- Delegate:
       |
       v
       Select specialist agent(s)
       |
       v
       Pass context + request
       |
       v
       Specialist executes
       |
       v
       Return results
       |
       v
       Consolidate
       |
       v
       Update shared context
       |
       v
       Respond to user
```

### Context Sharing

All agents share access to:
- Conversation history
- Notion database states
- User preferences and rules
- Recent actions and changes
- Active tasks and projects

Updated in real-time through Cursor's unified context.

## Agent Communication

### Delegation Protocol

```json
{
  "from": "personal-assistant",
  "to": "studies-coach",
  "action": "guide_project",
  "context": {
    "project": "ML Spam Classifier",
    "status": "in_progress",
    "last_session": "2025-10-31",
    "current_file": "02_model_training.ipynb"
  },
  "priority": "high"
}
```

### Response Protocol

```json
{
  "from": "studies-coach",
  "to": "personal-assistant",
  "status": "completed",
  "result": {
    "action": "guided_through_step_1",
    "next_step": "step_2",
    "updates_needed": [
      {
        "database": "studies",
        "card": "ML Spam Classifier",
        "property": "Progress",
        "value": "Step 1 Complete"
      }
    ]
  }
}
```

## Notion Integration

### Database Operations

All agents can:
- Query databases
- Create pages
- Update pages
- Search content

Following rules:
- GMT-3 timezone always
- Duplicate checking
- Property validation
- Status verification

### Update Strategy

1. Read current state
2. Validate changes
3. Apply updates
4. Verify success
5. Log action

## State Management

### Shared Knowledge Base

Stored in:
- Cursor's unified context (automatic)
- Optional: `/tmp/multiagent_state.json` (for Python scripts)

Contains:
- Active sessions
- Recent actions
- Pending decisions
- Agent states
- User preferences

### Persistence

- Notion: Source of truth (persistent)
- Local state: Temporary (session-based)
- Cursor context: Automatic (IDE-managed)

## Scalability

### Adding New Agents

1. Create agent file: `config/agents/new-agent.mdc`
2. Define role and capabilities
3. Set triggers
4. Add to `config.json`
5. Test integration

### Adding New Workflows

1. Define workflow in `config/workflows/`
2. Specify agent sequence
3. Define success criteria
4. Test execution
5. Document

## Security

### Sensitive Data

Never commit:
- API keys and tokens
- Notion database IDs
- Personal information
- Medical details
- Work client data

Protected via:
- `.gitignore` rules
- `config/private/` directory
- Environment variables

### Public Repository

Contains only:
- Generic templates
- Framework code
- Documentation
- Example configurations

## Performance

### Optimization Strategies

1. **Parallel Execution:** Run independent agents simultaneously
2. **Caching:** Cache Notion queries when appropriate
3. **Lazy Loading:** Load context only when needed
4. **Batch Operations:** Group similar operations

### Monitoring

Track:
- Response times
- Success rates
- Error frequencies
- User satisfaction

## Future Enhancements

### Phase 2 (After November pilot)
- Enhanced context persistence
- Advanced workflow engine
- Metrics and analytics
- Mobile notifications

### Phase 3 (Long-term)
- Gmail integration
- Google Calendar sync
- Dashboard visualization
- Team collaboration features

---

Version: 1.0  
Last Updated: 2024-11-01  
Status: Pilot Phase



