"""Tests for scripts/install_agentic_team.py (loaded via importlib)."""

from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "install_agentic_team.py"


def load_installer():
    spec = importlib.util.spec_from_file_location("install_agentic_team", SCRIPT)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["install_agentic_team"] = mod
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def inst():
    return load_installer()


def _git_init(path: Path) -> None:
    subprocess.run(["git", "init"], cwd=path, check=True, capture_output=True)
    subprocess.run(
        ["git", "config", "user.email", "test@example.com"],
        cwd=path,
        check=True,
        capture_output=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Test"],
        cwd=path,
        check=True,
        capture_output=True,
    )


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_dry_run_creates_no_files(inst, tmp_path: Path) -> None:
    target = tmp_path / "proj"
    target.mkdir()
    _git_init(target)
    report = inst.install(REPO_ROOT, target, dry_run=True, write_handoff_flag=True)
    assert not report.errors
    assert not (target / ".grok").exists()
    assert not (target / "AGENTS.md").exists()
    assert any(a.kind == "create" for a in report.actions)


def test_install_empty_git_repo_creates_tree(inst, tmp_path: Path) -> None:
    target = tmp_path / "proj"
    target.mkdir()
    _git_init(target)
    report = inst.install(REPO_ROOT, target, write_handoff_flag=True, verify=True)
    assert not report.errors
    assert (target / ".grok" / "skills" / "plan-review-loop" / "SKILL.md").is_file()
    assert (target / ".grok" / "rules" / "accuracy-coverage.md").is_file()
    assert (target / "docs" / "waivers" / "README.md").is_file()
    assert (target / "fixtures" / "agentic-template-acceptance" / "bad-plan.md").is_file()
    assert (target / "AGENTS.md").is_file()
    assert (target / "docs" / "plans" / "agentic-team-install-handoff.md").is_file()
    assert report.verify_ok is True
    # Never copy TaskBoard product
    assert not (target / "src" / "taskboard").exists()
    assert not (target / "pyproject.toml").exists()


def test_second_install_idempotent(inst, tmp_path: Path) -> None:
    target = tmp_path / "proj"
    target.mkdir()
    _git_init(target)
    inst.install(REPO_ROOT, target)
    report2 = inst.install(REPO_ROOT, target)
    assert not report2.errors
    # All template files should be skip_identical; AGENTS may be skip_identical too
    conflicts = [a for a in report2.actions if a.kind == "skip_conflict"]
    assert not conflicts
    creates = [a for a in report2.actions if a.kind in {"create", "update"}]
    # mkdir skip or skip_identical only expected
    assert not creates, f"unexpected writes on reinstall: {creates}"


def test_divergent_file_preserved_without_force(inst, tmp_path: Path) -> None:
    target = tmp_path / "proj"
    target.mkdir()
    _git_init(target)
    inst.install(REPO_ROOT, target)
    custom = target / ".grok" / "rules" / "accuracy-coverage.md"
    custom.write_text("# customized locally\n", encoding="utf-8")
    report = inst.install(REPO_ROOT, target, force=False)
    assert custom.read_text(encoding="utf-8") == "# customized locally\n"
    assert any(a.kind == "skip_conflict" and "accuracy-coverage" in a.path for a in report.actions)
    assert report.warnings


def test_force_overwrites_with_backup(inst, tmp_path: Path) -> None:
    target = tmp_path / "proj"
    target.mkdir()
    _git_init(target)
    inst.install(REPO_ROOT, target)
    custom = target / ".grok" / "rules" / "accuracy-coverage.md"
    custom.write_text("# customized\n", encoding="utf-8")
    report = inst.install(REPO_ROOT, target, force=True)
    assert "# customized" not in custom.read_text(encoding="utf-8")
    backups = list((target / ".grok" / "rules").glob("accuracy-coverage.md.bak-agentic-*"))
    assert backups
    assert any(a.kind == "backup" for a in report.actions)


def test_claude_md_referenced_and_unchanged(inst, tmp_path: Path) -> None:
    target = tmp_path / "proj"
    target.mkdir()
    _git_init(target)
    claude_body = "# Product invariants\n\nNo float on calc path.\n"
    _write(target / "CLAUDE.md", claude_body)
    report = inst.install(REPO_ROOT, target)
    assert report.companion_rules == ["CLAUDE.md"]
    assert (target / "CLAUDE.md").read_text(encoding="utf-8") == claude_body
    agents = (target / "AGENTS.md").read_text(encoding="utf-8")
    assert "CLAUDE.md" in agents
    assert "Project-specific rules" in agents


def test_scan_detects_uv_pytest_ruff(inst, tmp_path: Path) -> None:
    target = tmp_path / "proj"
    target.mkdir()
    _git_init(target)
    _write(
        target / "README.md",
        """# Demo
```bash
uv sync --project backend
uv run --project backend pytest tests
uv run --project backend ruff check backend tests scripts
cd frontend && npm run build
```
""",
    )
    _write(target / "backend" / "pyproject.toml", '[project]\nname = "demo"\n')
    _write(target / "backend" / "uv.lock", "# lock\n")
    _write(target / "pytest.ini", "[pytest]\ntestpaths = tests\n")
    _write(
        target / "frontend" / "package.json",
        '{"name":"ui","scripts":{"build":"vite build","typecheck":"tsc --noEmit"}}\n',
    )
    scan = inst.scan_project_commands(target)
    unit = scan.by_name("Unit tests")
    assert unit and unit.status == "REAL"
    assert "uv run --project backend pytest" in unit.value
    build = scan.by_name("Build")
    assert build and build.status == "REAL"
    assert "uv sync" in build.value
    assert "npm run build" in build.value
    cov = scan.by_name("Coverage")
    assert cov and cov.status == "NONE"
    lint = scan.by_name("Lint / typecheck")
    assert lint and lint.status == "REAL"
    assert "ruff" in lint.value
    assert "typecheck" in lint.value


def test_never_copies_taskboard_on_full_install(inst, tmp_path: Path) -> None:
    target = tmp_path / "proj"
    target.mkdir()
    _git_init(target)
    inst.install(REPO_ROOT, target)
    assert not any(target.rglob("board.py"))
    assert not (target / "tests" / "test_board.py").exists()


def test_self_install_refused(inst) -> None:
    report = inst.install(REPO_ROOT, REPO_ROOT)
    assert report.errors
    assert "same path" in report.errors[0].lower() or "self-install" in report.errors[0].lower()


def test_agents_backup_on_existing(inst, tmp_path: Path) -> None:
    target = tmp_path / "proj"
    target.mkdir()
    _git_init(target)
    _write(target / "AGENTS.md", "# Old agents\n\ncustom lead rules\n")
    inst.install(REPO_ROOT, target)
    agents = (target / "AGENTS.md").read_text(encoding="utf-8")
    assert "GrokForge" in agents
    assert "Preserved notes" in agents
    backups = list(target.glob("AGENTS.md.bak-before-agentic-template-*"))
    assert backups
    assert "custom lead rules" in backups[0].read_text(encoding="utf-8")


def test_template_version_is_1_5(inst) -> None:
    assert inst.TEMPLATE_VERSION == "1.5"
    agents = (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8")
    assert "Template Version:** 1.5" in agents


def test_install_includes_plan_quality_and_loop_assets(inst, tmp_path: Path) -> None:
    target = tmp_path / "proj"
    target.mkdir()
    _git_init(target)
    report = inst.install(REPO_ROOT, target, verify=True)
    assert not report.errors
    assert report.verify_ok is True
    assert (target / ".grok" / "docs" / "plan-quality-standards.md").is_file()
    assert (target / ".grok" / "docs" / "test-accuracy-standards.md").is_file()
    for name in ("gf-qa.md", "gf-plan-reviewer.md", "gf-backend.md", "gf-frontend.md"):
        assert (target / ".grok" / "personas" / "instructions" / name).is_file()
    plan_skill = (
        target / ".grok" / "skills" / "plan-review-loop" / "SKILL.md"
    ).read_text(encoding="utf-8")
    assert "Hard gates" in plan_skill or "hard gates" in plan_skill.lower()
    assert "Max review passes" in plan_skill or "max 2" in plan_skill.lower()
    targeted = (
        target / ".grok" / "skills" / "targeted-unit-test-loop" / "SKILL.md"
    ).read_text(encoding="utf-8")
    assert "MAX = 3" in targeted or "max 3" in targeted.lower()
    agents = (target / "AGENTS.md").read_text(encoding="utf-8")
    assert "Loop policy" in agents
    assert "plan-quality-standards.md" in agents


def test_verify_fails_when_plan_quality_doc_missing(inst, tmp_path: Path) -> None:
    target = tmp_path / "proj"
    target.mkdir()
    _git_init(target)
    inst.install(REPO_ROOT, target)
    missing = target / ".grok" / "docs" / "plan-quality-standards.md"
    missing.unlink()
    report = inst.InstallReport()
    ok = inst.verify_install(target, report)
    assert ok is False
    assert any("plan-quality-standards.md" in e for e in report.errors)
