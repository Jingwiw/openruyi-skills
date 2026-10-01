#!/bin/sh
set -eu

if [ "$#" -lt 3 ]; then
  echo "usage: $0 <project> <github-user> <git-revision> [package ...]" >&2
  exit 1
fi

project="$1"
github_user="$2"
git_revision="$3"
shift 3

if [ -z "${OBS_NETRC_FILE:-}" ]; then
  echo "OBS_NETRC_FILE is required" >&2
  exit 1
fi

obs_base_url="${OBS_BASE_URL:-https://obs.example.invalid}"
script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
tmpdir=$(mktemp -d)
trap 'rm -rf "$tmpdir"' EXIT INT TERM

render_meta="${script_dir}/render_package_meta.sh"
render_service="${script_dir}/render_service.sh"

if [ ! -x "$render_meta" ] || [ ! -x "$render_service" ]; then
  echo "required helper scripts are missing in ${script_dir}" >&2
  exit 1
fi

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
  echo "no packages to sync" >&2
  exit 1
fi

branch_name="${project##*:}"
description="Validation package for ${branch_name} at ${git_revision}"

for pkg in $packages; do
  meta_path="${tmpdir}/${pkg}.meta"
  service_path="${tmpdir}/${pkg}.service"

  "$render_meta" "$project" "$pkg" "$description" >"$meta_path"
  "$render_service" "$github_user" "$git_revision" "$pkg" >"$service_path"

  curl -sS --netrc-file "$OBS_NETRC_FILE" -X PUT \
    -H 'Content-Type: application/xml' \
    --data-binary @"$meta_path" \
    "${obs_base_url}/source/${project}/${pkg}/_meta" >/dev/null

  curl -sS --netrc-file "$OBS_NETRC_FILE" -X PUT \
    -H 'Content-Type: application/xml' \
    --data-binary @"$service_path" \
    "${obs_base_url}/source/${project}/${pkg}/_service" >/dev/null

  curl -sS --netrc-file "$OBS_NETRC_FILE" -X POST \
    "${obs_base_url}/source/${project}/${pkg}?cmd=runservice" >/dev/null

  printf 'SYNCED %s\n' "$pkg"
done
