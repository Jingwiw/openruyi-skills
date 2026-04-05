---
name: commit-spec-skill
description: Standardize commit content for engineering traceability and review quality. Use whenever preparing commits or summarizing commit-ready changes so each commit contains clear motivation, scoped changes, verification evidence, and impact notes.
---

# Commit Spec Skill

## Objective
Produce consistent and reviewable commit content that documents intent, implementation boundary, and verification results.

## Required Inputs
- Final code diff and touched boundaries.
- Validation results (tests, build, lint, or manual checks).
- Known risks, compatibility changes, and follow-up work.

## Workflow
1. Group changes into coherent commit units.
2. Generate subject using `type(scope): summary`.
3. Fill structured body using template in `references/commit-templates.md`.
4. Ensure body includes `Why`, `What`, `Validation`, and `Impact`.
5. If multiple commits are needed, provide ordered commit list with rationale.
6. Keep wording factual and concise; do not call out AI process.

## Output Contract
- Commit subject and body are directly usable.
- Validation evidence is explicit and reproducible.
- Risk and migration notes are visible to reviewers.

## Quality Gates
- One commit should represent one coherent intent.
- Avoid vague subjects such as "update" or "improve".
- Do not hide failed or skipped validation.

## References
- Read `references/commit-templates.md` before writing commit text.
