---
name: todo-skill
description: Govern project execution backlog and action logs for engineering work. Use at the beginning of every coding session, after requirement changes, and at milestone completion to update `docs/TASKS.md` and `docs/ACTION_HISTORY.md`, reprioritize P0/P1/P2, and define the next 1-3 executable steps.
---

# Todo Skill

## Objective
Keep planning artifacts current and decision-ready so implementation always starts from the highest-value next step.

## Required Inputs
- Current user request and acceptance constraints.
- Existing `docs/TASKS.md` and `docs/ACTION_HISTORY.md`.
- Current repository state, blockers, and unfinished items.

## Workflow
1. Read `docs/TASKS.md` and `docs/ACTION_HISTORY.md`. If missing, create them using `references/task-doc-templates.md`.
2. Reconcile backlog with the latest request; delete stale tasks, split oversized tasks, and restate ambiguous tasks as verifiable outcomes.
3. Reassign priority:
   - `P0`: blocks current delivery or correctness.
   - `P1`: important but can follow current delivery.
   - `P2`: future optimization.
4. Declare the next 1-3 concrete steps before code edits.
5. After each milestone, append a dated action-history entry with what changed, why, and boundary impact.
6. End with explicit next-step recommendation and pending risks.

## Output Contract
- `docs/TASKS.md` contains prioritized and testable tasks with clear done conditions.
- `docs/ACTION_HISTORY.md` contains chronological and factual milestones.
- Final handoff includes immediate next actions.

## Quality Gates
- Avoid generic tasks without measurable checks.
- Keep backlog minimal; each task must map to current project goals.
- Record blockers immediately with recovery options.

## References
- Read `references/task-doc-templates.md` when creating or normalizing task documents.
