#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
SRC_ROOT=${CODEX_SKILLS_ROOT:-"$HOME/.codex/skills"}
SOURCE_LOCAL_HOME_PATTERN=${SOURCE_LOCAL_HOME_PATTERN:-/Users/example-user}
SOURCE_LOCAL_USER_PATTERN=${SOURCE_LOCAL_USER_PATTERN:-example-user}
SOURCE_OBS_BASE_URL_PATTERN=${SOURCE_OBS_BASE_URL_PATTERN:-https://build.example.invalid}
SOURCE_OBS_HOST_PATTERN=${SOURCE_OBS_HOST_PATTERN:-build.example.invalid}
SOURCE_OBS_HOME_PROJECT_PATTERN=${SOURCE_OBS_HOME_PROJECT_PATTERN:-home:example-user:example-branch}
SOURCE_SYNC_EXAMPLE_PATTERN=${SOURCE_SYNC_EXAMPLE_PATTERN:-example-user <commit> pkg-a pkg-b pkg-c}
SOURCE_REBUILD_EXAMPLE_PATTERN=${SOURCE_REBUILD_EXAMPLE_PATTERN:-x86_64 x86_64 pkg-d pkg-e}

require_file() {
  if [ ! -f "$1" ]; then
    echo "missing source file: $1" >&2
    exit 1
  fi
}

prepare_dir() {
  dst_dir="$1"
  mkdir -p "$dst_dir"
}

common_sanitize() {
  sed \
    -e "s|${SOURCE_LOCAL_HOME_PATTERN}|\\\${LOCAL_HOME}|g" \
    -e "s|${SOURCE_LOCAL_USER_PATTERN}|\\\${LOCAL_USER}|g"
}

obs_sanitize() {
  common_sanitize | \
  sed \
    -e "s|${SOURCE_OBS_BASE_URL_PATTERN}|\\\${OBS_BASE_URL}|g" \
    -e "s|${SOURCE_OBS_HOST_PATTERN}|\\\${OBS_HOST}|g" \
    -e "s|${SOURCE_OBS_HOME_PROJECT_PATTERN}|\\\${OBS_HOME_PROJECT}|g" \
    -e "s|${SOURCE_SYNC_EXAMPLE_PATTERN}|\\\${GIT_FORK_USER} \\\${GIT_REVISION} \\\${VALIDATION_PACKAGES}|g" \
    -e "s|${SOURCE_REBUILD_EXAMPLE_PATTERN}|x86_64 x86_64 \\\${DOWNSTREAM_PACKAGES}|g" \
    -e 's|home:<user>:<branch>|${OBS_HOME_PROJECT}|g' \
    -e 's|openruyi/x86_64|${OBS_RELEASE_REPO_X86_64}|g' \
    -e 's|openruyi/riscv64|${OBS_RELEASE_REPO_RISCV64}|g' \
    -e 's|https://github\.com/<user>/openRuyi/|https://${GIT_HOST}/<user>/${DISTRO_REPO_NAME}/|g' \
    -e 's|https://github\.com/\${github_user}/openRuyi/|https://${GIT_HOST}/${github_user}/${DISTRO_REPO_NAME}/|g' \
    -e 's|obs_base_url="[^"]*"|obs_base_url="${OBS_BASE_URL:-https://obs.example.invalid}"|g'
}

copy_with_filter() {
  src="$1"
  dst="$2"
  mode="$3"

  require_file "$src"
  prepare_dir "$(dirname "$dst")"

  case "$mode" in
    common)
      common_sanitize < "$src" > "$dst"
      ;;
    obs)
      obs_sanitize < "$src" > "$dst"
      ;;
    raw)
      cat "$src" > "$dst"
      ;;
    *)
      echo "unknown sanitize mode: $mode" >&2
      exit 1
      ;;
  esac
}

copy_exec() {
  src="$1"
  dst="$2"
  mode="$3"
  copy_with_filter "$src" "$dst" "$mode"
  chmod 0755 "$dst"
}

copy_skill_tree() {
  skill="$1"
  mode="$2"
  shift 2

  for rel in "$@"; do
    copy_with_filter \
      "$SRC_ROOT/$skill/$rel" \
      "$ROOT/skills/$skill/$rel" \
      "$mode"
  done
}

copy_skill_exec_tree() {
  skill="$1"
  mode="$2"
  shift 2

  for rel in "$@"; do
    copy_exec \
      "$SRC_ROOT/$skill/$rel" \
      "$ROOT/skills/$skill/$rel" \
      "$mode"
  done
}

rm -rf "$ROOT/skills/openruyi-obs-validation" \
       "$ROOT/skills/distro-analysis-skill" \
       "$ROOT/skills/todo-skill" \
       "$ROOT/skills/commit-spec-skill" \
       "$ROOT/skills/rust-dev-lead-skill"

copy_skill_tree openruyi-obs-validation obs \
  SKILL.md

copy_skill_exec_tree openruyi-obs-validation obs \
  scripts/render_package_meta.sh \
  scripts/render_service.sh \
  scripts/scan_sysusers_logs.sh \
  scripts/sync_project.sh \
  scripts/wipe_rebuild.sh

copy_skill_tree distro-analysis-skill common \
  SKILL.md \
  agents/openai.yaml \
  references/distro-source-playbook.md

copy_skill_tree todo-skill common \
  SKILL.md \
  agents/openai.yaml \
  references/task-doc-templates.md

copy_skill_tree commit-spec-skill common \
  SKILL.md \
  agents/openai.yaml \
  references/commit-templates.md

copy_skill_tree rust-dev-lead-skill common \
  SKILL.md \
  agents/openai.yaml \
  references/rust-quality-checklist.md

echo "Exported sanitized skills into $ROOT/skills"
