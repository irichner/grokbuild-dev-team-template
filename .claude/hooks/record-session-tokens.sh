#!/usr/bin/env bash
# SessionEnd: aggregate this session's token usage from its transcript and
# append one summary line to the project's own usage log
# (.claude/logs/token-usage.jsonl). The central aggregator (scripts/
# aggregate_token_usage.py, run standalone) remains the canonical source --
# this hook is just a convenience per-project mirror. Best-effort and async;
# never blocks or fails the session.
set -uo pipefail

INPUT="$(cat)"

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-}"
[ -z "$PROJECT_DIR" ] && exit 0

AGGREGATOR="$PROJECT_DIR/scripts/aggregate_token_usage.py"
[ -f "$AGGREGATOR" ] || exit 0

PYTHON_BIN="$(command -v python || command -v python3 || true)"
[ -z "$PYTHON_BIN" ] && exit 0

json_get() {
  if command -v jq >/dev/null 2>&1; then
    printf '%s' "$INPUT" | jq -r "$1 // empty" 2>/dev/null || true
  else
    printf '%s' "$INPUT" | "$PYTHON_BIN" -c 'import sys,json
d=json.load(sys.stdin)
cur=d
for k in sys.argv[1].lstrip(".").split("."):
    cur=cur.get(k) if isinstance(cur,dict) else None
    if cur is None: break
print(cur if isinstance(cur,str) else "")' "$1" 2>/dev/null || true
  fi
}

TRANSCRIPT="$(json_get .transcript_path)"
[ -z "$TRANSCRIPT" ] && exit 0
[ -f "$TRANSCRIPT" ] || exit 0

# --project-dir pins the log write to this project, rather than trusting the
# transcript's recorded cwd for the destination.
"$PYTHON_BIN" "$AGGREGATOR" --transcript "$TRANSCRIPT" --append-project-log --project-dir "$PROJECT_DIR" >/dev/null 2>&1 || true
exit 0
