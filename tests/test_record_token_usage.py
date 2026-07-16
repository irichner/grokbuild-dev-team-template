"""Tests for scripts/record_token_usage.py."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "record_token_usage.py"


def load_mod():
    spec = importlib.util.spec_from_file_location("record_token_usage", SCRIPT)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["record_token_usage"] = mod
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def mod():
    return load_mod()


def test_record_appends_and_totals(mod, tmp_path: Path) -> None:
    root = tmp_path / "proj"
    root.mkdir()
    (root / "VERSION").write_text("1.7\n", encoding="utf-8")
    ledger = root / "docs" / "metrics" / "token-ledger.md"
    # Create empty via helper
    text = mod.render_ledger("1.7", [], "2026-07-15")
    ledger.parent.mkdir(parents=True)
    ledger.write_text(text, encoding="utf-8")

    rc = mod.main(
        [
            "--root",
            str(root),
            "--model",
            "grok-build",
            "--input",
            "100",
            "--output",
            "40",
            "--note",
            "unit test",
            "--session",
            "s1",
            "--date",
            "2026-07-15",
        ]
    )
    assert rc == 0
    body = ledger.read_text(encoding="utf-8")
    assert "grok-build" in body
    assert "| Total tokens (measured) | 140 |" in body
    assert "unit test" in body

    rc2 = mod.main(
        [
            "--root",
            str(root),
            "--model",
            "grok-build",
            "--input",
            "10",
            "--output",
            "5",
            "--note",
            "second",
            "--date",
            "2026-07-16",
        ]
    )
    assert rc2 == 0
    body2 = ledger.read_text(encoding="utf-8")
    assert "| Total tokens (measured) | 155 |" in body2
    assert "| Measured entries | 2 |" in body2

    rc3 = mod.main(
        [
            "--root",
            str(root),
            "--unmeasured",
            "--note",
            "no stats",
            "--date",
            "2026-07-17",
        ]
    )
    assert rc3 == 0
    body3 = ledger.read_text(encoding="utf-8")
    # Unmeasured must not inflate totals
    assert "| Total tokens (measured) | 155 |" in body3
    assert "unmeasured" in body3.lower()


def test_rejects_negative(mod, tmp_path: Path) -> None:
    root = tmp_path / "proj"
    root.mkdir()
    (root / "VERSION").write_text("1.7.0\n", encoding="utf-8")
    rc = mod.main(
        [
            "--root",
            str(root),
            "--model",
            "x",
            "--input",
            "-1",
            "--output",
            "0",
        ]
    )
    assert rc == 2
