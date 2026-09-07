#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
export GOMODCACHE="${GOMODCACHE:-${REPO_ROOT}/.cache/gomod}"
export GOCACHE="${GOCACHE:-${REPO_ROOT}/.cache/go-build}"

mkdir -p "${GOMODCACHE}" "${GOCACHE}"

go mod download github.com/oer-particle-physics/hugo-styles >/dev/null
MODULE_DIR="$(go list -m -f '{{.Dir}}' github.com/oer-particle-physics/hugo-styles)"

if [[ -z "${MODULE_DIR}" ]]; then
  echo "Error: could not resolve github.com/oer-particle-physics/hugo-styles module directory" >&2
  exit 1
fi

UPSTREAM_SYNC_SCRIPT="${MODULE_DIR}/scripts/sync-template-files.sh"

if [[ -f "${UPSTREAM_SYNC_SCRIPT}" ]]; then
  bash "${UPSTREAM_SYNC_SCRIPT}" "${REPO_ROOT}"
  exit 0
fi

echo "Pinned hugo-styles module does not yet provide scripts/sync-template-files.sh; falling back to legacy shared-file sync" >&2

LEGACY_SHARED_FILES=(
  "scripts/build-versioned-site.py|scripts/build-versioned-site.py|0755"
  "lychee.toml|lychee.toml|0644"
)

for entry in "${LEGACY_SHARED_FILES[@]}"; do
  IFS='|' read -r source_rel target_rel mode <<<"${entry}"
  source_path="${MODULE_DIR}/${source_rel}"
  target_path="${REPO_ROOT}/${target_rel}"

  if [[ ! -f "${source_path}" ]]; then
    if [[ -f "${target_path}" ]]; then
      echo "Pinned hugo-styles module does not provide ${source_rel}; leaving committed ${target_rel} unchanged"
      continue
    fi
    echo "Error: expected source file not found at ${source_path}" >&2
    exit 1
  fi

  install -m "${mode}" "${source_path}" "${target_path}"
  echo "Synced ${target_rel} from ${source_rel}"
done
