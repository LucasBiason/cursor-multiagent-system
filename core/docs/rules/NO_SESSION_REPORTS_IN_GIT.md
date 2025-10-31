# RULE: No Session Reports in Git

**Priority:** CRITICAL  
**Applies to:** ALL agents  
**Status:** MANDATORY

---

## The Rule

**NEVER commit to git:**
- Session reports
- Interaction feedback
- Daily logs
- Agent conversation summaries
- User feedback documents
- Meeting notes
- Analysis reports
- Recovery plans
- Status reports from conversations

## Why

These documents:
- Are byproducts of agent interactions
- Contain no reusable code or configs
- Clutter the repository
- Are not part of the framework
- Are personal/temporary in nature

## What Goes in Git

ONLY commit:
- Framework code
- Agent configurations (generic parts)
- Documentation (how-to, architecture)
- Templates (reusable)
- Examples (educational)
- Tests
- Utilities

## What Does NOT Go in Git

NEVER commit:
- RESUMO_SESSAO_*.md
- RELATORIO_*.md
- FEEDBACK_*.md
- ANALISE_*.md
- PLANO_RECOVERY_*.md
- STATUS_*.md (from sessions)
- Daily logs
- Interaction reports

## Where These Files Go

If needed for reference:
- Local directory: `docs/pilot/daily-logs/` (gitignored)
- Or: Don't create them at all
- Or: Separate private notes repo

## Implementation

### In .gitignore

```gitignore
# SESSION REPORTS (NEVER COMMIT)
**/RESUMO_SESSAO*.md
**/RELATORIO*.md
**/FEEDBACK*.md
**/ANALISE_AGENDA*.md
**/STATUS_*.md
docs/pilot/daily-logs/**
logs/**
```

### In Agent Instructions

All agents must:
1. NOT create session reports in project directory
2. NOT create interaction summaries
3. NOT create feedback documents
4. If user requests summary, provide in chat only
5. If documentation needed, ask where to save (outside git)

## Correct Behavior

User: "Me de um resumo da sessao"
Agent: [Provides summary in CHAT, does not create file]

User: "Documente isso"
Agent: "Onde deseja salvar? (Sugiro fora deste repositorio para nao poluir o Git)"

## Exceptions

Project-level documentation that CAN be committed:
- CHANGELOG.md (version history)
- PROJECT_SUMMARY.md (one-time project overview)
- ARCHITECTURE.md (system design)
- Pilot plan (PILOT_PLAN.md) - template for pilot, not session logs

## Enforcement

Before any git commit:
1. Check for session report files
2. Remove if found
3. Add to .gitignore if pattern missing
4. Commit only framework-related changes

---

**This is a CRITICAL rule. All agents MUST follow.**

Last Updated: 2024-11-01  
Version: 1.0  
Priority: CRITICAL




