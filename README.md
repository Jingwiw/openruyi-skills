# Sanitized Codex Skills For Distro Work

This project is a sanitized export of selected local Codex skills used for distro-oriented engineering work. It is scoped to reusable planning, backlog, review, Rust architecture, and OBS validation workflows.

The export keeps the skill structure intact where it matters:

- `skills/*/SKILL.md`
- `skills/*/references/*`
- `skills/*/agents/openai.yaml`
- `skills/openruyi-obs-validation/scripts/*`

The export intentionally removes or replaces instance-specific details:

- local usernames and absolute home paths
- concrete OBS instance URLs and home project names
- concrete GitHub fork users and branch examples
- branch-specific validation examples tied to one personal workflow

See [MACROS.md](./MACROS.md) for the placeholder catalog and intended substitutions.

## Included Skills

- `openruyi-obs-validation`
- `distro-analysis-skill`
- `todo-skill`
- `commit-spec-skill`
- `rust-dev-lead-skill`

## Regeneration

Run:

```sh
./tools/export_from_codex.sh
```

By default the script reads from `~/.codex/skills`. Override the source root with:

```sh
CODEX_SKILLS_ROOT=/path/to/skills ./tools/export_from_codex.sh
```

If the original local skill set contains private usernames, OBS project names, or instance URLs, pass the original values explicitly through `SOURCE_*_PATTERN` variables so the exporter can match and replace them without hardcoding those values into this repository:

```sh
SOURCE_LOCAL_HOME_PATTERN=/path/to/private/home \
SOURCE_LOCAL_USER_PATTERN=private-user \
SOURCE_OBS_BASE_URL_PATTERN=https://private-obs.example \
SOURCE_OBS_HOST_PATTERN=private-obs.example \
SOURCE_OBS_HOME_PROJECT_PATTERN=home:private-user:private-branch \
./tools/export_from_codex.sh
```

## Notes

- This project is a sanitized working bundle, not a legal redistribution statement for the original local environment.
- Review [NOTICE.md](./NOTICE.md) before publishing outside the current trust boundary.
