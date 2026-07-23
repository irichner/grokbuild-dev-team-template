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
    assert (target / ".grok" / "skills" / "plan" / "SKILL.md").is_file()
    assert (target / ".grok" / "skills" / "implement" / "SKILL.md").is_file()
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
    lint = scan.by_name("Lint")
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


def test_template_version_is_1_7(inst) -> None:
    assert inst.TEMPLATE_VERSION == "1.7"
    agents = (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8")
    assert "VERSION" in agents
    assert "every" in agents.lower() and "commit" in agents.lower()
    version = (REPO_ROOT / "VERSION").read_text(encoding="utf-8").strip()
    assert version.startswith("1.7")
    assert (REPO_ROOT / "scripts" / "prepare_commit_metrics.py").is_file()
    assert (REPO_ROOT / "scripts" / "githooks" / "pre-commit").is_file()


def test_scan_python_package_emits_diff_cover(inst, tmp_path: Path) -> None:
    target = tmp_path / "proj"
    target.mkdir()
    _git_init(target)
    _write(
        target / "pyproject.toml",
        """
[project]
name = "widget"
version = "0.1.0"

[project.optional-dependencies]
dev = ["pytest>=8", "pytest-cov>=5", "diff-cover>=9", "ruff>=0.6"]

[tool.coverage.run]
source = ["widget"]
""",
    )
    (target / "tests").mkdir()
    scan = inst.scan_project_commands(target)
    cov = scan.by_name("Coverage")
    assert cov and cov.status == "REAL"
    assert "--cov=widget" in cov.value
    assert "diff_cover" in cov.value or "diff-cover" in cov.value
    assert "origin/main" in cov.value
    lint = scan.by_name("Lint")
    assert lint is not None


def test_install_seeds_metrics_and_preserves_ledger(inst, tmp_path: Path) -> None:
    target = tmp_path / "proj"
    target.mkdir()
    _git_init(target)
    report = inst.install(REPO_ROOT, target, verify=True)
    assert not report.errors
    assert report.verify_ok is True
    assert (target / ".grok" / "rules" / "spawn.md").is_file()
    assert (target / "docs" / "metrics" / "README.md").is_file()
    ledger = target / "docs" / "metrics" / "token-ledger.md"
    assert ledger.is_file()
    custom = "# Token & model usage ledger\n\n**Template version:** 1.7\n\n## Entries\n\n| Date (UTC) | Session / label | Model | Input | Output | Total | Notes |\n|---|---|---|---:|---:|---:|---|\n| 2026-01-01 | s1 | grok-build | 10 | 5 | 15 | keep me |\n"
    ledger.write_text(custom, encoding="utf-8")
    report2 = inst.install(REPO_ROOT, target, force=True)
    assert not report2.errors
    assert "keep me" in ledger.read_text(encoding="utf-8")
    for role in (
        "gf-backend.toml",
        "gf-frontend.toml",
        "gf-qa.toml",
        "gf-plan-reviewer.toml",
        "gf-reviewer.toml",
        "gf-debugger.toml",
    ):
        assert (target / ".grok" / "roles" / role).is_file()
    assert (target / "fixtures" / "agentic-template-acceptance" / "sample-ui" / "index.html").is_file()
    assert (target / "scripts" / "prepare_commit_metrics.py").is_file()
    assert (target / "scripts" / "githooks" / "pre-commit").is_file()
    assert (target / "VERSION").is_file()


def test_install_includes_plan_quality_and_loop_assets(inst, tmp_path: Path) -> None:
    target = tmp_path / "proj"
    target.mkdir()
    _git_init(target)
    report = inst.install(REPO_ROOT, target, verify=True)
    assert not report.errors
    assert report.verify_ok is True
    assert (target / ".grok" / "docs" / "plan-quality-standards.md").is_file()
    assert (target / ".grok" / "docs" / "test-accuracy-standards.md").is_file()
    assert (target / ".grok" / "docs" / "ui-design-standards.md").is_file()
    for name in (
        "gf-qa.md",
        "gf-plan-reviewer.md",
        "gf-backend.md",
        "gf-frontend.md",
        "gf-reviewer.md",
        "gf-debugger.md",
    ):
        assert (target / ".grok" / "personas" / "instructions" / name).is_file()
    plan_skill = (target / ".grok" / "skills" / "plan" / "SKILL.md").read_text(
        encoding="utf-8"
    )
    assert "Hard gates" in plan_skill or "hard gates" in plan_skill.lower()
    assert "max 2" in plan_skill.lower() or "pass <= 2" in plan_skill
    assert "gf-plan-reviewer" in plan_skill
    implement_skill = (
        target / ".grok" / "skills" / "implement" / "SKILL.md"
    ).read_text(encoding="utf-8")
    assert "MAX = 3" in implement_skill or "max 3" in implement_skill.lower()
    assert "gf-qa" in implement_skill
    assert "gf-backend" in implement_skill
    # Deprecated stubs redirect only (no dual source of truth)
    plan_stub = (
        target / ".grok" / "skills" / "plan-review-loop" / "SKILL.md"
    ).read_text(encoding="utf-8")
    assert "Deprecated" in plan_stub or "DEPRECATED" in plan_stub
    agents = (target / "AGENTS.md").read_text(encoding="utf-8")
    assert "Loop policy" in agents
    assert "plan-quality-standards.md" in agents
    assert "/plan" in agents and "/implement" in agents


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


def test_install_includes_ui_design_assets(inst, tmp_path: Path) -> None:
    target = tmp_path / "proj"
    target.mkdir()
    _git_init(target)
    report = inst.install(REPO_ROOT, target, verify=True)
    assert not report.errors
    ui_doc = target / ".grok" / "docs" / "ui-design-standards.md"
    assert ui_doc.is_file()
    assert "Blockers" in ui_doc.read_text(encoding="utf-8")
    fixture_e = (
        target / "fixtures" / "agentic-template-acceptance" / "seeded-design-defect-notes.md"
    )
    assert fixture_e.is_file()
    frontend = (
        target / ".grok" / "personas" / "instructions" / "gf-frontend.md"
    ).read_text(encoding="utf-8")
    assert "ui-design-standards.md" in frontend
    implement_skill = (
        target / ".grok" / "skills" / "implement" / "SKILL.md"
    ).read_text(encoding="utf-8")
    assert "UI verification" in implement_skill
    protocol_stub = (
        target / ".grok" / "skills" / "post-change-accuracy-protocol" / "SKILL.md"
    ).read_text(encoding="utf-8")
    assert "Deprecated" in protocol_stub or "DEPRECATED" in protocol_stub
    plan_std = (
        target / ".grok" / "docs" / "plan-quality-standards.md"
    ).read_text(encoding="utf-8")
    assert "UI/UX design" in plan_std
    agents = (target / "AGENTS.md").read_text(encoding="utf-8")
    assert "ui-design-standards.md" in agents


def test_verify_fails_when_ui_design_doc_missing(inst, tmp_path: Path) -> None:
    target = tmp_path / "proj"
    target.mkdir()
    _git_init(target)
    inst.install(REPO_ROOT, target)
    (target / ".grok" / "docs" / "ui-design-standards.md").unlink()
    report = inst.InstallReport()
    ok = inst.verify_install(target, report)
    assert ok is False
    assert any("ui-design-standards.md" in e for e in report.errors)
