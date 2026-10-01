#!/bin/sh
set -eu

if [ "$#" -lt 3 ] || [ "$#" -gt 4 ]; then
  echo "usage: $0 <github-user> <git-revision> <package> [auto|yes|no]" >&2
  exit 1
fi

github_user="$1"
git_revision="$2"
package="$3"
download_assets="${4:-auto}"

case "$download_assets" in
  auto)
    # On this OBS instance the generic template is more reliable when
    # download_assets is enabled by default, even for some packages that
    # only extract local spec-side sources.
    download_assets=yes
    ;;
  yes|no)
    ;;
  *)
    echo "invalid download_assets mode: ${download_assets}" >&2
    exit 1
    ;;
esac

cat <<EOF
<services>
  <service name="obs_scm" mode="trylocal">
    <param name="scm">git</param>
    <param name="url">https://${GIT_HOST}/${github_user}/${DISTRO_REPO_NAME}/</param>
    <param name="revision">${git_revision}</param>
    <param name="exclude">*</param>
    <param name="extract">SPECS/${package}/*</param>
  </service>
EOF

if [ "$download_assets" = yes ]; then
  cat <<EOF
  <service name="download_assets" mode="trylocal"></service>
EOF
fi

cat <<EOF
</services>
EOF
