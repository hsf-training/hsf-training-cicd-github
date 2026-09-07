#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "sync-build-versioned-site.sh is deprecated; forwarding to sync-template-files.sh" >&2
"${SCRIPT_DIR}/sync-template-files.sh" "$@"
