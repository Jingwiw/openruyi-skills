---
name: rust-dev-lead-skill
description: Drive Rust architecture and implementation quality for extensible systems. Use when choosing module boundaries, plugin architecture, parser/compiler design, performance strategy, or code quality policy across Rust 1.76 through 1.93.
---

# Rust Dev Lead Skill

## Objective
Keep Rust code minimal, maintainable, and performance-aware while preserving extension points and long-term portability.

## Required Inputs
- Current requirement and acceptance criteria.
- Existing architecture boundaries and plugin contracts.
- Compatibility constraints for Rust 1.76 to 1.93.

## Workflow
1. Read backlog priorities and distro constraints before coding.
2. Define ownership boundaries for each module and keep domain-specific logic out of core.
3. Compare at least two implementation options and document tradeoffs.
4. Choose the minimal design that keeps extension points explicit.
5. Apply quality gates from `references/rust-quality-checklist.md`.
6. Update tasks/history with architecture decisions and follow-up refactors.
7. Keep user-facing language neutral; do not label yourself by role.

## Output Contract
- Chosen design with boundary map.
- Rejected alternatives with reason.
- Compatibility notes for Rust 1.76-1.93.
- Verification plan (build, targeted tests, or static checks).

## Quality Gates
- Use explicit error context and typed boundaries.
- Justify `Arc`, `Box`, arena, and cloning decisions.
- Keep parser/AST span and allocation strategy auditable.
- Avoid introducing complexity without measurable gain.

## References
- Read `references/rust-quality-checklist.md` before implementation or review.
