---
name: distro-analysis-skill
description: Convert distro packaging requirements into implementable engineering constraints. Use when defining features, evaluating architecture, or validating roadmap choices for RPM-based and cross-distro targets, including Fedora, Debian, Nix, Guix, Arch Linux, openSUSE, and openRuyi.
---

# Distro Analysis Skill

## Objective
Translate policy and packaging rules into concrete tasks, acceptance gates, and architecture constraints that keep the project useful for distro maintainers.

## Required Inputs
- Current feature request and project goals.
- Local norms from project docs and openRuyi-related specs.
- Official distro documentation and upstream packaging references.

## Workflow
1. Extract requirement intent, scope, and explicit non-goals.
2. Read local constraints first (`docs/`, packaging conventions, existing spec behavior).
3. Query official distro docs relevant to the request and collect source URLs.
4. Build a constraint matrix with fields: `constraint`, `source`, `impact`, `required action`, `priority`.
5. Separate facts from inference and state confidence when inference is used.
6. Convert constraints into backlog entries in `docs/TASKS.md` with acceptance criteria.
7. Provide implementation guidance without role self-labeling.

## Output Contract
- Requirement summary with non-goals.
- Constraint matrix with traceable sources.
- Recommended implementation path and explicit tradeoffs.
- `P0/P1/P2` backlog updates aligned with distro value.

## Quality Gates
- Prefer official documentation over secondary summaries.
- Do not keep requirements that cannot be traced to a source or local policy.
- State unresolved questions as blocking assumptions.

## References
- Read `references/distro-source-playbook.md` before external research.
