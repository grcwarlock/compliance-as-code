#!/usr/bin/env bash
set -euo pipefail

# Symlink each skill (and agent, when present) into a user-supplied target
# directory so a compatible agent runtime can discover them.
#
# This script does not assume any default install location. Set --target to
# wherever your agent runtime expects to read skills from.

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

TARGET=""
DRY_RUN=0
FORCE=0

usage() {
  cat <<EOF
Usage: $0 --target <path> [--dry-run] [--force]

Symlinks every skill in skills/ (and every agent in agents/, when present)
into <path>/<name>/ so a compatible agent runtime can discover them.

  --target <path>  Required. Directory your agent runtime reads skills from.
  --dry-run        Print what would happen without changing anything.
  --force          Replace an existing symlink at the target.
  -h, --help       Show this message.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --target)
      TARGET="${2:-}"
      shift 2
      ;;
    --target=*)
      TARGET="${1#*=}"
      shift
      ;;
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    --force)
      FORCE=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

if [[ -z "$TARGET" ]]; then
  echo "ERROR: --target is required (no default install location is assumed)." >&2
  usage >&2
  exit 2
fi

mkdir -p "$TARGET"
TARGET="$(cd "$TARGET" && pwd)"

link_one() {
  local src="$1"
  local name
  name="$(basename "$src")"
  local dest="$TARGET/$name"

  if [[ -e "$dest" || -L "$dest" ]]; then
    if [[ "$FORCE" -eq 1 ]]; then
      if [[ "$DRY_RUN" -eq 1 ]]; then
        echo "would replace: $dest"
      else
        rm -rf "$dest"
        ln -s "$src" "$dest"
        echo "replaced:      $src -> $dest"
      fi
    else
      echo "skip (exists): $dest" >&2
    fi
    return 0
  fi

  if [[ "$DRY_RUN" -eq 1 ]]; then
    echo "would link:    $src -> $dest"
  else
    ln -s "$src" "$dest"
    echo "linked:        $src -> $dest"
  fi
}

processed=0

if [[ -d "$REPO_ROOT/skills" ]]; then
  for skill in "$REPO_ROOT"/skills/*/; do
    [[ -d "$skill" ]] || continue
    link_one "${skill%/}"
    processed=$((processed + 1))
  done
fi

if [[ -d "$REPO_ROOT/agents" ]]; then
  for agent in "$REPO_ROOT"/agents/*/; do
    [[ -d "$agent" ]] || continue
    link_one "${agent%/}"
    processed=$((processed + 1))
  done
fi

echo
echo "Done. Processed $processed item(s) into $TARGET."
