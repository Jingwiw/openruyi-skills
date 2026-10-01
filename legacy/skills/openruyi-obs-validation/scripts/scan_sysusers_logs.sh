#!/bin/sh
set -eu

if [ "$#" -lt 3 ]; then
  echo "usage: $0 <project> <repository> <arch> [package ...]" >&2
  exit 1
fi

project="$1"
repository="$2"
arch="$3"
shift 3

if [ -z "${OBS_NETRC_FILE:-}" ]; then
  echo "OBS_NETRC_FILE is required" >&2
  exit 1
fi

obs_base_url="${OBS_BASE_URL:-https://obs.example.invalid}"
tmpdir=$(mktemp -d)
trap 'rm -rf "$tmpdir"' EXIT INT TERM

list_packages() {
  curl -sS --netrc-file "$OBS_NETRC_FILE" \
    "${obs_base_url}/source/${project}" |
    awk -F'"' '/<entry name=/{print $2}' |
    sort -u
}

if [ "$#" -gt 0 ]; then
  packages="$*"
else
  packages="$(list_packages)"
fi

if [ -z "$packages" ]; then
  echo "no packages to scan" >&2
  exit 1
fi

had_match=0
issue_pattern='Conflict with earlier configuration|earlier configuration for user|earlier configuration for group|Suggested (user|group) ID .* already used|warning: (group|user) .* does not exist|Failed to resolve (user|group) |useradd.*(already exists|invalid)|groupadd.*(already exists|invalid)|user .* already exists|group .* already exists'

for pkg in $packages; do
  log_path="${tmpdir}/${pkg}.log"

  if ! curl -fsS --netrc-file "$OBS_NETRC_FILE" \
    "${obs_base_url}/build/${project}/${repository}/${arch}/${pkg}/_log?start=0" \
    >"$log_path" 2>/dev/null; then
    printf 'SKIP %s\n' "$pkg"
    continue
  fi

  matches=$(grep -Eni "$issue_pattern" "$log_path" || true)

  if [ -n "$matches" ]; then
    had_match=1
    printf '=== %s ===\n' "$pkg"
    printf '%s\n' "$matches"
  fi
done

if [ "$had_match" -eq 0 ]; then
  echo "no sysusers-related warnings, conflicts, or unresolved users/groups found"
fi
