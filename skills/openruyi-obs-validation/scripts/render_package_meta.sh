#!/bin/sh
set -eu

if [ "$#" -ne 3 ]; then
  echo "usage: $0 <project> <package> <description>" >&2
  exit 1
fi

project="$1"
package="$2"
description="$3"

cat <<EOF
<package name="${package}" project="${project}">
  <title>${package}</title>
  <description>${description}</description>
</package>
EOF
