#!/usr/bin/env bash
# Install the jawdrop skill into every AI coding agent found on this machine.
#
#   curl -fsSL https://raw.githubusercontent.com/AryanAliPro/jawdrop/main/install.sh | bash
#
# Options (after "bash -s --" when piping, or directly from a clone):
#   --agent <id>    Install only into this agent (repeatable). Ids: claude-code,
#                   codex, cursor, antigravity, gemini-cli, windsurf,
#                   github-copilot, opencode, kiro, trae, roo, agents
#   --list          Show detected agents and where jawdrop would go, install nothing
#   --uninstall     Remove jawdrop from every agent
#   -h, --help      Show this help
#
# An existing jawdrop folder is moved to ~/.jawdrop-backups/<timestamp>/ first,
# so nothing is lost. Needs curl and tar (or a local clone of the repo).

set -euo pipefail

REPO="AryanAliPro/jawdrop"
BRANCH="${JAWDROP_BRANCH:-main}"
SKILL="jawdrop"

# id | folder that shows the agent is installed | global skills folder
AGENTS=(
  "claude-code|$HOME/.claude|$HOME/.claude/skills"
  "codex|$HOME/.codex|$HOME/.agents/skills"
  "cursor|$HOME/.cursor|$HOME/.cursor/skills"
  "antigravity|$HOME/.gemini/antigravity|$HOME/.gemini/antigravity/skills"
  "gemini-cli|$HOME/.gemini|$HOME/.gemini/skills"
  "windsurf|$HOME/.codeium/windsurf|$HOME/.codeium/windsurf/skills"
  "github-copilot|$HOME/.copilot|$HOME/.copilot/skills"
  "opencode|$HOME/.config/opencode|$HOME/.config/opencode/skills"
  "kiro|$HOME/.kiro|$HOME/.kiro/skills"
  "trae|$HOME/.trae|$HOME/.trae/skills"
  "roo|$HOME/.roo|$HOME/.roo/skills"
  "agents|$HOME/.agents|$HOME/.agents/skills"
)
# Used when no agent is detected at all.
FALLBACK=("claude-code" "agents")

mode=install
wanted=()
while [[ $# -gt 0 ]]; do
  case "$1" in
    --agent)     [[ $# -ge 2 ]] || { echo "error: --agent needs an id" >&2; exit 2; }
                 wanted+=("$2"); shift ;;
    --list)      mode=list ;;
    --uninstall) mode=uninstall ;;
    -h|--help)   cat <<EOF
Install the jawdrop skill into every AI coding agent found on this machine.

  --agent <id>   Install only into this agent (repeatable): claude-code, codex, cursor,
                 antigravity, gemini-cli, windsurf, github-copilot, opencode, kiro, trae, roo, agents
  --list         Show detected agents and where jawdrop would go, install nothing
  --uninstall    Remove jawdrop from every agent

More: https://github.com/$REPO#install
EOF
                 exit 0 ;;
    *)           echo "error: unknown option $1 (try --help)" >&2; exit 2 ;;
  esac
  shift
done

agent_field() { # agent_field <id> <1|2|3>
  local entry
  for entry in "${AGENTS[@]}"; do
    [[ ${entry%%|*} == "$1" ]] && { echo "$entry" | cut -d'|' -f"$2"; return 0; }
  done
  return 1
}

# Pick target agents: the ones asked for, else the ones installed, else a fallback.
targets=()
if [[ ${#wanted[@]} -gt 0 ]]; then
  for id in "${wanted[@]}"; do
    agent_field "$id" 1 >/dev/null || { echo "error: unknown agent '$id'" >&2; exit 2; }
    targets+=("$id")
  done
else
  for entry in "${AGENTS[@]}"; do
    id="${entry%%|*}"
    [[ -d "$(agent_field "$id" 2)" ]] && targets+=("$id")
  done
  [[ ${#targets[@]} -gt 0 ]] || targets=("${FALLBACK[@]}")
fi

if [[ $mode == list ]]; then
  for id in "${targets[@]}"; do printf '%-15s %s/%s\n' "$id" "$(agent_field "$id" 3)" "$SKILL"; done
  exit 0
fi

if [[ $mode == uninstall ]]; then
  for entry in "${AGENTS[@]}"; do
    dest="$(echo "$entry" | cut -d'|' -f3)/$SKILL"
    if [[ -L $dest ]] || grep -qs "^name: $SKILL\$" "$dest/SKILL.md"; then
      rm -rf "$dest" && echo "removed    $dest"
    fi
  done
  exit 0
fi

# Find the skill: a local clone next to this script, or a fresh download.
src=""
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]:-.}")" 2>/dev/null && pwd || true)"
if [[ -n $script_dir && -f "$script_dir/skills/$SKILL/SKILL.md" ]]; then
  src="$script_dir/skills/$SKILL"
else
  command -v curl >/dev/null || { echo "error: curl is required" >&2; exit 1; }
  command -v tar >/dev/null || { echo "error: tar is required" >&2; exit 1; }
  tmp="$(mktemp -d)"
  trap 'rm -rf "$tmp"' EXIT
  echo "Downloading $REPO ($BRANCH)..."
  curl -fsSL "https://codeload.github.com/$REPO/tar.gz/refs/heads/$BRANCH" | tar -xz -C "$tmp"
  for candidate in "$tmp"/*/skills/"$SKILL"; do
    [[ -f "$candidate/SKILL.md" ]] && src="$candidate"
  done
  [[ -n $src ]] || { echo "error: skills/$SKILL not found in the download" >&2; exit 1; }
fi

stamp="$(date +%Y%m%d-%H%M%S)"
done_dirs=" "
for id in "${targets[@]}"; do
  dir="$(agent_field "$id" 3)"
  # Several agents share ~/.agents/skills; install there once.
  [[ $done_dirs == *" $dir "* ]] && { echo "installed  $id (shares $dir)"; continue; }
  done_dirs+="$dir "

  mkdir -p "$dir"
  dest="$dir/$SKILL"
  if [[ -L $dest ]]; then
    rm "$dest"
  elif [[ -e $dest ]]; then
    backup="$HOME/.jawdrop-backups/$stamp/$id"
    mkdir -p "$backup"
    mv "$dest" "$backup/"
    echo "backed up  previous $dest -> $backup/$SKILL"
  fi
  cp -R "$src" "$dest"
  echo "installed  $id -> $dest"
done

echo
echo "Done. Restart your agent, then ask it to build a website, for example:"
echo "  Build website for a family-run roofing company in Denver"
echo "In Claude Code you can also type: /jawdrop Build website for ..."
