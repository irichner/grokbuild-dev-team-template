"""Tests for scripts/install_git_hooks.py."""

from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "install_git_hooks.py"


def load_mod():
    spec = importlib.util.spec_from_file_location("install_git_hooks", SCRIPT)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["install_git_hooks"] = mod
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def mod():
    return load_mod()


def _init_git(root: Path) -> None:
    subprocess.run(
        ["git", "init"],
        cwd=str(root),
        check=True,
        capture_output=True,
    )


def _seed_hook_source(root: Path, body: str = "#!/bin/sh\necho grok-metrics\n") -> Path:
    hooks = root / "scripts" / "githooks"
    hooks.mkdir(parents=True)
    src = hooks / "pre-commit"
    src.write_text(body, encoding="utf-8", newline="\n")
    (root / "scripts" / "prepare_commit_metrics.py").write_text("# stub\n", encoding="utf-8")
    return src


def test_not_git_repo(mod, tmp_path: Path) -> None:
    root = tmp_path / "nogit"
    root.mkdir()
    assert mod.install_hooks(root) == 1


def test_install_fresh_hook(mod, tmp_path: Path) -> None:
    root = tmp_path / "repo"
    root.mkdir()
    _init_git(root)
    _seed_hook_source(root)
    assert mod.install_hooks(root) == 0
    dest = root / ".git" / "hooks" / "pre-commit"
    assert dest.is_file()
    assert "grok-metrics" in dest.read_text(encoding="utf-8")


def test_identical_hook_is_noop(mod, tmp_path: Path) -> None:
    root = tmp_path / "repo"
    root.mkdir()
    _init_git(root)
    src = _seed_hook_source(root)
    dest = root / ".git" / "hooks"
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "pre-commit").write_bytes(src.read_bytes())
    assert mod.install_hooks(root) == 0


def test_refuse_overwrite_without_force(mod, tmp_path: Path) -> None:
    root = tmp_path / "repo"
    root.mkdir()
    _init_git(root)
    _seed_hook_source(root)
    hooks = root / ".git" / "hooks"
    hooks.mkdir(parents=True, exist_ok=True)
    (hooks / "pre-commit").write_text("#!/bin/sh\necho other\n", encoding="utf-8")
    assert mod.install_hooks(root, force=False) == 1
    assert "other" in (hooks / "pre-commit").read_text(encoding="utf-8")


def test_force_backs_up_existing(mod, tmp_path: Path) -> None:
    root = tmp_path / "repo"
    root.mkdir()
    _init_git(root)
    _seed_hook_source(root)
    hooks = root / ".git" / "hooks"
    hooks.mkdir(parents=True, exist_ok=True)
    (hooks / "pre-commit").write_text("#!/bin/sh\necho other\n", encoding="utf-8")
    assert mod.install_hooks(root, force=True) == 0
    assert "grok-metrics" in (hooks / "pre-commit").read_text(encoding="utf-8")
    backups = list(hooks.glob("pre-commit.bak.*"))
    assert len(backups) == 1
    assert "other" in backups[0].read_text(encoding="utf-8")


def test_dry_run_no_write(mod, tmp_path: Path) -> None:
    root = tmp_path / "repo"
    root.mkdir()
    _init_git(root)
    _seed_hook_source(root)
    assert mod.install_hooks(root, dry_run=True) == 0
    assert not (root / ".git" / "hooks" / "pre-commit").exists()
