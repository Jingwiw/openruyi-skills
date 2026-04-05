#!/bin/sh
set -eu

if [ "$#" -lt 4 ]; then
  echo "usage: $0 <project> <repository> <arch> <package ...>" >&2
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

for pkg in "$@"; do
  curl -sS --netrc-file "$OBS_NETRC_FILE" -X POST \
    "${obs_base_url}/build/${project}?cmd=wipe&package=${pkg}&repository=${repository}&arch=${arch}" >/dev/null

  curl -sS --netrc-file "$OBS_NETRC_FILE" -X POST \
    "${obs_base_url}/build/${project}?cmd=rebuild&package=${pkg}&repository=${repository}&arch=${arch}" >/dev/null

  printf 'WIPED+QUEUED %s\n' "$pkg"
done
