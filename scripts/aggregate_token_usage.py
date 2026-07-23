#!/usr/bin/env python3
"""Aggregate per-project Claude Code token usage from local session transcripts.

Source of truth: the JSONL transcripts Claude Code writes under
``~/.claude/projects/<slug>/<session-id>.jsonl`` (plus nested
``<session-id>/subagents/**/agent-*.jsonl`` for subagent threads). Every
assistant record carries the real project path in a top-level ``cwd`` field and
per-response token counts in ``message.usage`` (``input_tokens``,
``output_tokens``, ``cache_read_input_tokens``, ``cache_creation_input_tokens``).

We group usage by the normalized ``cwd`` field, never by the folder slug: the
slug is not a reliable function of the path (the same drive shows up as both
``c--Users-...`` and ``C--Users-...`` depending on how the session was
launched). We also dedupe by ``message.id`` (falling back to ``requestId``,
then a usage fingerprint): streaming responses repeat byte-identical ``usage``
blocks across several consecutive JSONL lines, so summing naively
triple-counts.

Stdlib only. Cross-platform.

Usage (from repo root):
  python scripts/aggregate_token_usage.py
      Full scan of ~/.claude/projects -> writes docs/metrics/token-usage.json.

  python scripts/aggregate_token_usage.py --print
      Full scan; render a human-readable table to stdout. Writes nothing.

  python scripts/aggregate_token_usage.py --transcript path/to/session.jsonl
      Aggregate a single transcript file; print its totals as JSON.

  python scripts/aggregate_token_usage.py --transcript path/to/session.jsonl --append-project-log
      Same, and also append one summary line to that project's
      .claude/logs/token-usage.jsonl (used by the SessionEnd hook).

  python scripts/aggregate_token_usage.py --project "C:\\Users\\me\\Projects\\foo"
      Filter to a single project (compared after cwd normalization).

  python scripts/aggregate_token_usage.py --projects-dir /tmp/fixture-projects
      Override the transcripts root (used by tests).
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Iterator, Optional

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
DEFAULT_PROJECTS_DIR = Path.home() / ".claude" / "projects"
DEFAULT_OUTPUT_PATH = REPO_ROOT / "docs" / "metrics" / "token-usage.json"


def normalize_cwd(cwd: Optional[str]) -> Optional[str]:
    """Normalize a raw ``cwd`` field for stable grouping across sessions.

    Lowercases a leading Windows drive letter and unifies path separators, so
    that the same project reached via a differently-cased drive letter (a
    quirk of how the Claude Code project-slug folders get named) collapses
    into one row. POSIX-looking paths are left with forward slashes.
    """
    if not cwd:
        return cwd
    normalized = cwd.strip()
    is_windows_path = len(normalized) >= 2 and normalized[1] == ":" and normalized[0].isalpha()
    if is_windows_path:
        normalized = normalized[0].lower() + normalized[1:]
        normalized = normalized.replace("/", "\\")
        sep = "\\"
    else:
        normalized = normalized.replace("\\", "/")
        sep = "/"
    while sep * 2 in normalized:
        normalized = normalized.replace(sep * 2, sep)
    if len(normalized) > 3 and normalized.endswith(sep):
        normalized = normalized[:-1]
    return normalized


def iter_transcript_files(projects_dir: Path) -> Iterator[Path]:
    """Yield every transcript JSONL file under *projects_dir*.

    A plain recursive glob naturally picks up nested subagent transcripts
    (``<session>/subagents/**/agent-*.jsonl``) alongside top-level session
    transcripts -- no special-casing needed to include them.
    """
    if not projects_dir.exists():
        return
    yield from sorted(projects_dir.rglob("*.jsonl"))


def iter_assistant_records(path: Path) -> Iterator[dict]:
    """Yield well-formed assistant usage records from one transcript file.

    Defensive against schema drift and the many non-assistant record kinds a
    transcript can contain (queue operations, user turns, attachments,
    summaries, ...): skips blank lines, invalid JSON, non-dict records,
    records that aren't ``type == "assistant"``, and records missing either
    ``message.usage`` or a top-level ``cwd``. Never raises.
    """
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError:
        return
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(record, dict) or record.get("type") != "assistant":
            continue
        message = record.get("message")
        if not isinstance(message, dict):
            continue
        usage = message.get("usage")
        if not isinstance(usage, dict):
            continue
        if not record.get("cwd"):
            continue
        yield record


def dedupe_key(record: dict) -> str:
    """A stable per-API-response key: message.id, else requestId, else a
    usage fingerprint. Streaming emits several JSONL lines per response with
    byte-identical usage, so this key is what collapses them to one count."""
    message = record.get("message") or {}
    message_id = message.get("id")
    if message_id:
        return f"id:{message_id}"
    request_id = record.get("requestId")
    if request_id:
        return f"req:{request_id}"
    usage = message.get("usage") or {}
    fingerprint = json.dumps(usage, sort_keys=True)
    return f"fp:{record.get('sessionId', '')}:{fingerprint}"


def _new_model_bucket() -> dict:
    return {
        "input_tokens": 0,
        "output_tokens": 0,
        "cache_read_tokens": 0,
        "cache_creation_tokens": 0,
        "total_tokens": 0,
    }


def _new_project_bucket() -> dict:
    return {
        "sessions": set(),
        "input_tokens": 0,
        "output_tokens": 0,
        "cache_read_tokens": 0,
        "cache_creation_tokens": 0,
        "total_tokens": 0,
        "by_model": defaultdict(_new_model_bucket),
    }


def aggregate_records(records: Iterable[dict]) -> dict:
    """Aggregate raw assistant records into per-project totals.

    Dedupes (by ``dedupe_key``) across the whole iterable, so callers can feed
    it records pulled from many transcript files -- including nested subagent
    transcripts -- without double-counting repeated streaming lines. Returns
    a dict keyed by normalized cwd, values holding raw accumulators (a
    ``sessions`` set and a ``by_model`` defaultdict) -- pass through
    ``build_report`` to get the committed JSON shape.
    """
    projects: dict = defaultdict(_new_project_bucket)
    seen: set = set()
    for record in records:
        key = dedupe_key(record)
        if key in seen:
            continue
        seen.add(key)

        cwd = normalize_cwd(record.get("cwd"))
        message = record.get("message") or {}
        usage = message.get("usage") or {}
        model = message.get("model") or "unknown"

        input_tokens = int(usage.get("input_tokens") or 0)
        output_tokens = int(usage.get("output_tokens") or 0)
        cache_read = int(usage.get("cache_read_input_tokens") or 0)
        cache_creation = int(usage.get("cache_creation_input_tokens") or 0)
        total = input_tokens + output_tokens + cache_read + cache_creation

        bucket = projects[cwd]
        session_id = record.get("sessionId")
        if session_id:
            bucket["sessions"].add(session_id)
        bucket["input_tokens"] += input_tokens
        bucket["output_tokens"] += output_tokens
        bucket["cache_read_tokens"] += cache_read
        bucket["cache_creation_tokens"] += cache_creation
        bucket["total_tokens"] += total

        model_bucket = bucket["by_model"][model]
        model_bucket["input_tokens"] += input_tokens
        model_bucket["output_tokens"] += output_tokens
        model_bucket["cache_read_tokens"] += cache_read
        model_bucket["cache_creation_tokens"] += cache_creation
        model_bucket["total_tokens"] += total

    return projects


def scan_projects(projects_dir: Path, project_filter: Optional[str] = None) -> dict:
    """Scan every transcript under *projects_dir* and aggregate by project."""
    records: list = []
    for path in iter_transcript_files(projects_dir):
        records.extend(iter_assistant_records(path))
    projects = aggregate_records(records)
    if project_filter:
        norm_filter = normalize_cwd(project_filter)
        projects = {k: v for k, v in projects.items() if k == norm_filter}
    return projects


def build_report(projects: dict) -> dict:
    """Convert the internal aggregation (sets/defaultdicts) into the
    committed JSON shape: {cwd: {sessions, input_tokens, ..., by_model, last_updated}}."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    report = {}
    for cwd, bucket in sorted(projects.items()):
        report[cwd] = {
            "sessions": len(bucket["sessions"]),
            "input_tokens": bucket["input_tokens"],
            "output_tokens": bucket["output_tokens"],
            "cache_read_tokens": bucket["cache_read_tokens"],
            "cache_creation_tokens": bucket["cache_creation_tokens"],
            "total_tokens": bucket["total_tokens"],
            "by_model": {model: dict(vals) for model, vals in sorted(bucket["by_model"].items())},
            "last_updated": now,
        }
    return report


def write_report(report: dict, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def print_report(report: dict) -> None:
    if not report:
        print("No token usage recorded.")
        return
    header = (
        f"{'project':<60} {'sessions':>8} {'input':>10} {'output':>10} "
        f"{'cache_read':>12} {'cache_create':>12} {'total':>12}"
    )
    print(header)
    print("-" * len(header))
    grand_total = 0
    ranked = sorted(report.items(), key=lambda kv: kv[1]["total_tokens"], reverse=True)
    for cwd, entry in ranked:
        print(
            f"{cwd:<60} {entry['sessions']:>8} {entry['input_tokens']:>10} "
            f"{entry['output_tokens']:>10} {entry['cache_read_tokens']:>12} "
            f"{entry['cache_creation_tokens']:>12} {entry['total_tokens']:>12}"
        )
        grand_total += entry["total_tokens"]
    print("-" * len(header))
    print(f"{'TOTAL':<60} {'':>8} {'':>10} {'':>10} {'':>12} {'':>12} {grand_total:>12}")


def append_project_log(cwd: str, entry: dict, session_id: Optional[str], model: str) -> Optional[Path]:
    """Append one summary line to <project>/.claude/logs/token-usage.jsonl.

    Best-effort: if the project directory no longer exists or the log dir
    can't be created/written, returns None without raising.
    """
    project_dir = Path(cwd)
    if not project_dir.exists():
        return None
    log_dir = project_dir / ".claude" / "logs"
    try:
        log_dir.mkdir(parents=True, exist_ok=True)
    except OSError:
        return None
    log_path = log_dir / "token-usage.jsonl"
    line = {
        "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "session_id": session_id,
        "model": model,
        "input": entry["input_tokens"],
        "output": entry["output_tokens"],
        "cache_read": entry["cache_read_tokens"],
        "cache_create": entry["cache_creation_tokens"],
        "total": entry["total_tokens"],
    }
    try:
        with log_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(line, sort_keys=True) + "\n")
    except OSError:
        return None
    return log_path


def _combine_entries(report: dict) -> Optional[dict]:
    """Collapse a (normally single-project) transcript report into one entry."""
    entries = list(report.values())
    if not entries:
        return None
    combined = {
        "sessions": sum(e.get("sessions", 0) for e in entries),
        "input_tokens": sum(e.get("input_tokens", 0) for e in entries),
        "output_tokens": sum(e.get("output_tokens", 0) for e in entries),
        "cache_read_tokens": sum(e.get("cache_read_tokens", 0) for e in entries),
        "cache_creation_tokens": sum(e.get("cache_creation_tokens", 0) for e in entries),
        "total_tokens": sum(e.get("total_tokens", 0) for e in entries),
        "by_model": {},
    }
    for e in entries:
        for model, stats in (e.get("by_model") or {}).items():
            slot = combined["by_model"].setdefault(model, {})
            for key, value in stats.items():
                if isinstance(value, int):
                    slot[key] = slot.get(key, 0) + value
    return combined


def _primary_model(entry: dict) -> str:
    by_model = entry.get("by_model") or {}
    if not by_model:
        return "unknown"
    return max(by_model.items(), key=lambda kv: kv[1]["total_tokens"])[0]


def summarize_transcript(path: Path) -> tuple[dict, list]:
    """Aggregate one transcript file. Returns (report, raw_records)."""
    records = list(iter_assistant_records(path))
    projects = aggregate_records(records)
    return build_report(projects), records


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Aggregate per-project Claude Code token usage from local session transcripts.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--projects-dir",
        type=Path,
        default=DEFAULT_PROJECTS_DIR,
        help="Override the Claude Code projects root (default: ~/.claude/projects). Mainly for tests.",
    )
    parser.add_argument(
        "--print",
        dest="print_table",
        action="store_true",
        help="Render a human-readable table to stdout instead of writing the JSON report.",
    )
    parser.add_argument(
        "--transcript",
        type=Path,
        default=None,
        help="Aggregate a single transcript file instead of scanning --projects-dir.",
    )
    parser.add_argument(
        "--append-project-log",
        action="store_true",
        help=(
            "Append one JSONL summary line to the project's .claude/logs/token-usage.jsonl. "
            "Requires --transcript."
        ),
    )
    parser.add_argument(
        "--project",
        default=None,
        help="Filter to a single project path (compared after cwd normalization).",
    )
    parser.add_argument(
        "--project-dir",
        type=Path,
        default=None,
        help=(
            "With --append-project-log: write the log under this project directory "
            "instead of trusting the transcript's recorded cwd for the destination."
        ),
    )
    return parser


def main(argv: Optional[list] = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)

    if args.append_project_log and not args.transcript:
        parser.error("--append-project-log requires --transcript")

    if args.transcript:
        if not args.transcript.exists():
            print(f"error: transcript not found: {args.transcript}", file=sys.stderr)
            return 1

        report, records = summarize_transcript(args.transcript)

        if args.append_project_log:
            if args.project_dir is not None:
                combined = _combine_entries(report)
                if combined is not None:
                    session_id = next((r.get("sessionId") for r in records if r.get("sessionId")), None)
                    append_project_log(
                        str(args.project_dir), combined, session_id, _primary_model(combined)
                    )
            else:
                for cwd, entry in report.items():
                    session_id = next(
                        (
                            r.get("sessionId")
                            for r in records
                            if normalize_cwd(r.get("cwd")) == cwd and r.get("sessionId")
                        ),
                        None,
                    )
                    append_project_log(cwd, entry, session_id, _primary_model(entry))

        if args.print_table:
            print_report(report)
        else:
            print(json.dumps(report, indent=2, sort_keys=True))
        return 0

    projects = scan_projects(args.projects_dir, project_filter=args.project)
    report = build_report(projects)

    if args.print_table:
        print_report(report)
        return 0

    write_report(report, DEFAULT_OUTPUT_PATH)
    print(f"wrote {len(report)} project(s) to {DEFAULT_OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
