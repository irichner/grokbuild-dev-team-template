"""Tests for scripts/prepare_commit_metrics.py."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "prepare_commit_metrics.py"


def load_mod():
    # Ensure sibling record_token_usage is importable
    scripts = str(REPO_ROOT / "scripts")
    if scripts not in sys.path:
        sys.path.insert(0, scripts)
    spec = importlib.util.spec_from_file_location("prepare_commit_metrics", SCRIPT)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["prepare_commit_metrics"] = mod
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def mod():
    return load_mod()


def test_prepare_bumps_version_and_records(mod, tmp_path: Path) -> None:
    root = tmp_path / "proj"
    root.mkdir()
    (root / "VERSION").write_text("1.7.0\n", encoding="utf-8")
    (root / "docs" / "metrics").mkdir(parents=True)

    rc = mod.main(
        [
            "--root",
            str(root),
            "--model",
            "grok-build",
            "--input",
            "50",
            "--output",
            "10",
            "--note",
            "test commit",
            "--no-bump",  # first assert no-bump path separately
        ]
    )
    # Wait - we want to test bump. Re-run without no-bump on fresh state
    assert rc == 0
    assert (root / "VERSION").read_text(encoding="utf-8").strip() == "1.7.0"
    ledger = (root / "docs" / "metrics" / "token-ledger.md").read_text(encoding="utf-8")
    assert "50" in ledger and "grok-build" in ledger

    rc2 = mod.main(
        [
            "--root",
            str(root),
            "--model",
            "grok-build",
            "--input",
            "1",
            "--output",
            "1",
            "--note",
            "bump me",
        ]
    )
    assert rc2 == 0
    assert (root / "VERSION").read_text(encoding="utf-8").strip() == "1.7.1"
    assert "1.7.1" in (root / "docs" / "metrics" / "token-ledger.md").read_text(encoding="utf-8")


def test_prepare_unmeasured(mod, tmp_path: Path) -> None:
    root = tmp_path / "proj"
    root.mkdir()
    (root / "VERSION").write_text("0.1.0\n", encoding="utf-8")
    rc = mod.main(
        [
            "--root",
            str(root),
            "--unmeasured",
            "--note",
            "no host stats",
        ]
    )
    assert rc == 0
    assert (root / "VERSION").read_text(encoding="utf-8").strip() == "0.1.1"
    body = (root / "docs" / "metrics" / "token-ledger.md").read_text(encoding="utf-8")
    assert "| Total tokens (measured) | 0 |" in body
    assert "unmeasured" in body.lower()


def test_prepare_from_env_falls_back_unmeasured(mod, tmp_path: Path) -> None:
    """GUI commits with no env should not fail hard; unmeasured stamp is OK."""
    root = tmp_path / "proj"
    root.mkdir()
    (root / "VERSION").write_text("0.1.0\n", encoding="utf-8")
    rc = mod.main(["--root", str(root), "--from-env"])
    assert rc == 0
    assert (root / "VERSION").read_text(encoding="utf-8").strip() == "0.1.1"
    body = (root / "docs" / "metrics" / "token-ledger.md").read_text(encoding="utf-8")
    assert "unmeasured" in body.lower()


def test_prepare_requires_metrics_without_fallback(mod, tmp_path: Path) -> None:
    root = tmp_path / "proj"
    root.mkdir()
    (root / "VERSION").write_text("0.1.0\n", encoding="utf-8")
    with pytest.raises(SystemExit):
        mod.main(["--root", str(root)])  # no --from-env, no metrics


def test_prepare_bad_token_env_exits_clearly(mod, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    root = tmp_path / "proj"
    root.mkdir()
    (root / "VERSION").write_text("0.1.0\n", encoding="utf-8")
    monkeypatch.setenv("GROK_MODEL", "grok-build")
    monkeypatch.setenv("GROK_INPUT_TOKENS", "abc")
    monkeypatch.setenv("GROK_OUTPUT_TOKENS", "10")
    with pytest.raises(SystemExit) as ei:
        mod.main(["--root", str(root), "--from-env"])
    msg = str(ei.value)
    assert "invalid integer" in msg.lower() or "INPUT" in msg or "abc" in msg


def test_unmeasured_ignores_garbage_token_env(mod, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    root = tmp_path / "proj"
    root.mkdir()
    (root / "VERSION").write_text("0.1.0\n", encoding="utf-8")
    monkeypatch.setenv("GROK_INPUT_TOKENS", "abc")
    monkeypatch.setenv("GROK_OUTPUT_TOKENS", "xyz")
    rc = mod.main(["--root", str(root), "--unmeasured", "--note", "ignore garbage"])
    assert rc == 0


def test_prepare_bad_pending_file_int(mod, tmp_path: Path) -> None:
    root = tmp_path / "proj"
    root.mkdir()
    (root / "VERSION").write_text("0.1.0\n", encoding="utf-8")
    metrics = root / "docs" / "metrics"
    metrics.mkdir(parents=True)
    (metrics / "pending-commit.env").write_text(
        "MODEL=grok-build\nINPUT=not-a-number\nOUTPUT=5\n",
        encoding="utf-8",
    )
    with pytest.raises(SystemExit) as ei:
        mod.main(["--root", str(root), "--from-env"])
    assert "invalid integer" in str(ei.value).lower() or "not-a-number" in str(ei.value)


def test_bump_patch_helpers() -> None:
    scripts = str(REPO_ROOT / "scripts")
    if scripts not in sys.path:
        sys.path.insert(0, scripts)
    import record_token_usage as rtu

    assert rtu.bump_patch("1.7") == "1.7.1"
    assert rtu.bump_patch("1.7.0") == "1.7.1"
    assert rtu.bump_patch("1.7.9") == "1.7.10"
