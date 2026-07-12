"""Minimal CLI for TaskBoard (smoke / demo)."""

from __future__ import annotations

import argparse
import sys

from taskboard.board import TaskBoard
from taskboard.models import TaskStatus


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="taskboard", description="Minimal task board CLI")
    sub = p.add_subparsers(dest="cmd", required=True)

    add = sub.add_parser("add", help="Add a task")
    add.add_argument("title")
    add.add_argument("--priority", type=int, default=0)
    add.add_argument("--description", default="")

    sub.add_parser("list", help="List tasks")

    done = sub.add_parser("done", help="Mark task done by id prefix")
    done.add_argument("task_id")

    return p


def main(argv: list[str] | None = None) -> int:
    # Demo CLI keeps an ephemeral board; useful for smoke only.
    args = build_parser().parse_args(argv)
    board = TaskBoard()

    if args.cmd == "add":
        t = board.add(args.title, description=args.description, priority=args.priority)
        print(f"{t.id} {t.title} p={t.priority}")
        return 0

    if args.cmd == "list":
        for t in board.list():
            print(f"{t.id[:8]} [{t.status.value}] p={t.priority} {t.title}")
        return 0

    if args.cmd == "done":
        # Empty board in this process — demonstrate arg path only
        try:
            board.set_status(args.task_id, TaskStatus.DONE)
        except KeyError:
            print(f"task not found: {args.task_id}", file=sys.stderr)
            return 1
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
