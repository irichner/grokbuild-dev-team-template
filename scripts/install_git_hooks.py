#!/usr/bin/env python3
"""Install GrokForge git hooks (pre-commit metrics) into a repo.

Usage:
  python scripts/install_git_hooks.py
  python scripts/install_git_hooks.py --root C:\\path\\to\\project
  python scripts/install_git_hooks.py --root . --dry-run
  python scripts/install_git_hooks.py --force   # overwrite existing after backup
"""

from __future__ import annotations

import argparse
import shutil
import stat
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def default_root() -> Path:
    return Path(__file__).resolve().parent.parent


def is_git_repo(path: Path) -> bool:
    try:
        r = subprocess.run(
            ["git", "-C", str(path), "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        return r.returncode == 0
    except (OSError, subprocess.TimeoutExpired):
        return False


def _timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")


def install_hooks(root: Path, *, dry_run: bool = False, force: bool = False) -> int:
    root = root.resolve()
    if not is_git_repo(root):
        print(f"ERROR: not a git repo: {root}", file=sys.stderr)
        return 1

    src = root / "scripts" / "githooks" / "pre-commit"
    if not src.is_file():
        # When installing into another project, hooks may live under source template;
        # caller should copy scripts/ first. Try relative to this file.
        alt = Path(__file__).resolve().parent / "githooks" / "pre-commit"
        if alt.is_file():
            src = alt
        else:
            print(f"ERROR: hook source missing: {src}", file=sys.stderr)
            return 1

    hooks_dir = root / ".git" / "hooks"
    dest = hooks_dir / "pre-commit"
    print(f"Install pre-commit hook: {dest}")

    if dest.is_file() and not force:
        # Identical content → ok without --force
        try:
            if dest.read_bytes() == src.read_bytes():
                print("Hook already installed (identical); nothing to do.")
                return 0
        except OSError:
            pass
        print(
            f"ERROR: existing pre-commit hook at {dest}\n"
            "  Refusing to overwrite without --force (creates pre-commit.bak.<timestamp>).\n"
            "  Merge manually if you use Husky/pre-commit framework/lint-staged.",
            file=sys.stderr,
        )
        return 1

    if dry_run:
        if dest.is_file() and force:
            print(f"Would backup existing hook to pre-commit.bak.{_timestamp()}")
        print(f"Would install from {src}")
        return 0

    hooks_dir.mkdir(parents=True, exist_ok=True)
    if dest.is_file() and force:
        bak = hooks_dir / f"pre-commit.bak.{_timestamp()}"
        shutil.copy2(dest, bak)
        print(f"Backed up existing hook → {bak}")

    shutil.copy2(src, dest)
    # Ensure executable bit on Unix; on Windows git still runs with sh.
    mode = dest.stat().st_mode
    dest.chmod(mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    # Ensure prepare script exists
    prep = root / "scripts" / "prepare_commit_metrics.py"
    if not prep.is_file():
        print(
            "WARNING: scripts/prepare_commit_metrics.py not in target; "
            "copy scripts/ from the template for the hook to work.",
            file=sys.stderr,
        )
    print("Done. Every commit will update VERSION + docs/metrics/token-ledger.md")
    print("Provide tokens via env, pending-commit.env, or --unmeasured (see docs/metrics/README.md)")
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Install GrokForge commit metrics git hooks")
    p.add_argument("--root", type=Path, default=None, help="Git repo root")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing pre-commit after timestamped backup",
    )
    args = p.parse_args(argv)
    return install_hooks(args.root or default_root(), dry_run=args.dry_run, force=args.force)


if __name__ == "__main__":
    sys.exit(main())
