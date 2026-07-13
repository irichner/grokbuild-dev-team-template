#!/usr/bin/env python3
"""Install GrokForge Agentic Dev Team config into a new or existing project.

Stdlib only. Copies .grok/, fixtures, docs/waivers README; generates AGENTS.md
with Project Test Commands scanned from the target. Never copies product code
(TaskBoard src/tests/pyproject).

Usage:
  python scripts/install_agentic_team.py <target> [--dry-run] [--force] ...
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

TEMPLATE_VERSION = "1.5"

EXPECTED_SKILLS = (
    "plan-review-loop",
    "targeted-unit-test-loop",
    "regression-test-loop",
    "post-change-accuracy-protocol",
    "parallel-fullstack-feature",
    "install-agentic-team",
)

# Reference docs that must land with the harness (under .grok/docs/).
EXPECTED_DOCS = (
    "test-accuracy-standards.md",
    "coverage-policy.md",
    "privacy-safety.md",
    "plan-quality-standards.md",
)

# Relative paths under source that are always installable (walked as trees or files).
INSTALL_TREES = (
    ".grok",
    "fixtures/agentic-template-acceptance",
)
INSTALL_FILES = (
    "docs/waivers/README.md",
)

COMPANION_RULE_FILES = (
    "CLAUDE.md",
    "GEMINI.md",
    "CODEX.md",
    "CURSOR.md",
    ".cursorrules",
)

BEGIN_PTC = "<!-- BEGIN PROJECT_TEST_COMMANDS -->"
END_PTC = "<!-- END PROJECT_TEST_COMMANDS -->"
BEGIN_PSR = "<!-- BEGIN PROJECT_SPECIFIC_RULES -->"
END_PSR = "<!-- END PROJECT_SPECIFIC_RULES -->"


@dataclass
class CommandRow:
    name: str
    value: str
    status: str  # REAL | NONE | TODO
    evidence: list[str] = field(default_factory=list)


@dataclass
class ScanResult:
    rows: list[CommandRow] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def by_name(self, name: str) -> CommandRow | None:
        for r in self.rows:
            if r.name == name:
                return r
        return None


@dataclass
class Action:
    kind: str  # create | update | skip_identical | skip_conflict | mkdir | backup
    path: str
    detail: str = ""


@dataclass
class InstallReport:
    actions: list[Action] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    git_mode: str = "full"  # full | degraded
    scan: ScanResult | None = None
    companion_rules: list[str] = field(default_factory=list)
    verify_ok: bool | None = None

    def add(self, kind: str, path: str, detail: str = "") -> None:
        self.actions.append(Action(kind=kind, path=path, detail=detail))


def default_source_root() -> Path:
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


def timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str, dry_run: bool) -> None:
    if dry_run:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def backup_file(
    path: Path,
    dry_run: bool,
    report: InstallReport,
    suffix: str,
    *,
    root: Path | None = None,
) -> Path | None:
    if not path.is_file():
        return None
    bak = path.with_name(f"{path.name}{suffix}")
    # Avoid clobbering an existing backup: add seconds if needed.
    if bak.exists():
        bak = path.with_name(f"{path.name}{suffix}-{timestamp()}")
    shown = rel_str(bak, root) if root else str(bak)
    report.add("backup", shown, f"from {path.name}")
    if not dry_run:
        shutil.copy2(path, bak)
    return bak


def rel_str(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def iter_install_files(source: Path) -> list[Path]:
    files: list[Path] = []
    for tree in INSTALL_TREES:
        root = source / tree
        if not root.exists():
            continue
        if root.is_file():
            files.append(root)
            continue
        for p in sorted(root.rglob("*")):
            if p.is_file():
                # Skip bytecode / caches if any slipped in
                if any(part in {"__pycache__", ".pytest_cache", ".ruff_cache"} for part in p.parts):
                    continue
                if p.suffix in {".pyc", ".pyo"}:
                    continue
                files.append(p)
    for rel in INSTALL_FILES:
        p = source / rel
        if p.is_file():
            files.append(p)
    return files


def install_file(
    src: Path,
    dest: Path,
    *,
    force: bool,
    dry_run: bool,
    report: InstallReport,
    target_root: Path,
) -> None:
    rel = rel_str(dest, target_root)
    if not dest.exists():
        report.add("create", rel)
        if not dry_run:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)
        return

    src_bytes = src.read_bytes()
    dest_bytes = dest.read_bytes()
    if src_bytes == dest_bytes:
        report.add("skip_identical", rel)
        return

    if not force:
        report.add("skip_conflict", rel, "use --force to overwrite (with backup)")
        report.warnings.append(f"Conflict (left unchanged): {rel}")
        return

    backup_file(
        dest, dry_run, report, f".bak-agentic-{timestamp()}", root=target_root
    )
    report.add("update", rel)
    if not dry_run:
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)


def ensure_dirs(target: Path, dry_run: bool, report: InstallReport) -> None:
    for rel in ("docs/plans", "docs/waivers"):
        d = target / rel
        if d.is_dir():
            report.add("skip_identical", rel + "/", "directory exists")
            continue
        report.add("mkdir", rel + "/")
        if not dry_run:
            d.mkdir(parents=True, exist_ok=True)


def find_companion_rules(target: Path) -> list[str]:
    found: list[str] = []
    for name in COMPANION_RULE_FILES:
        if (target / name).is_file():
            found.append(name)
    return found


def _read_if(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def _load_json(path: Path) -> dict | list | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def _first_match(patterns: Iterable[str], text: str) -> str | None:
    for pat in patterns:
        m = re.search(pat, text, flags=re.MULTILINE)
        if m:
            return m.group(0).strip()
    return None


def scan_project_commands(target: Path) -> ScanResult:
    """Heuristic scan of manifests / README / CI for Project Test Commands."""
    result = ScanResult()
    evidence_hits: list[str] = []

    readme = _read_if(target / "README.md")
    claude = _read_if(target / "CLAUDE.md")
    pytest_ini = _read_if(target / "pytest.ini")
    root_pyproject = _read_if(target / "pyproject.toml")
    backend_pyproject = _read_if(target / "backend" / "pyproject.toml")
    frontend_pkg = _load_json(target / "frontend" / "package.json")
    root_pkg = _load_json(target / "package.json")

    ci_text = ""
    ci_dir = target / ".github" / "workflows"
    if ci_dir.is_dir():
        for wf in sorted(ci_dir.glob("*.yml")) + sorted(ci_dir.glob("*.yaml")):
            ci_text += "\n" + _read_if(wf)
            evidence_hits.append(rel_str(wf, target))

    combined = "\n".join([readme, claude, pytest_ini, root_pyproject, backend_pyproject, ci_text])

    # --- Build ---
    build_parts: list[str] = []
    build_ev: list[str] = []

    if (target / "backend" / "pyproject.toml").is_file() and (
        "uv" in combined or (target / "backend" / "uv.lock").is_file()
    ):
        build_parts.append("`uv sync --project backend`")
        build_ev.append("backend/pyproject.toml")
    elif (target / "pyproject.toml").is_file():
        if re.search(r'\[project\.optional-dependencies\][\s\S]*?dev\s*=', root_pyproject) or '".[dev]"' in root_pyproject:
            build_parts.append('`python -m pip install -e ".[dev]"`')
        else:
            build_parts.append("`python -m pip install -e .`")
        build_ev.append("pyproject.toml")

    if isinstance(frontend_pkg, dict) and isinstance(frontend_pkg.get("scripts"), dict):
        scripts = frontend_pkg["scripts"]
        if "build" in scripts:
            build_parts.append("`cd frontend && npm run build`")
            build_ev.append("frontend/package.json")
    elif isinstance(root_pkg, dict) and isinstance(root_pkg.get("scripts"), dict):
        if "build" in root_pkg["scripts"]:
            build_parts.append("`npm run build`")
            build_ev.append("package.json")

    if "docker compose" in readme.lower() or "docker-compose" in readme.lower():
        if not build_parts:
            build_parts.append("`docker compose up --build`")
            build_ev.append("README.md")

    if build_parts:
        result.rows.append(
            CommandRow("Build", " · ".join(build_parts), "REAL", build_ev or evidence_hits[:1])
        )
    else:
        result.rows.append(
            CommandRow("Build", "TODO — user must fill", "TODO", [])
        )

    # --- Unit tests ---
    unit_cmd: str | None = None
    unit_ev: list[str] = []

    # Prefer README-documented commands (often monorepo-correct).
    m = re.search(
        r"^(uv run --project \S+ pytest\b[^\n`]*)",
        readme + "\n" + claude,
        flags=re.MULTILINE,
    )
    if m:
        unit_cmd = m.group(1).strip()
        unit_ev.append("README.md" if m.group(1) in readme else "CLAUDE.md")
    else:
        m2 = _first_match(
            [
                r"uv run --project \S+ pytest[^\n]*",
                r"python -m pytest[^\n]*",
                r"pytest tests[^\n]*",
                r"npm test\b[^\n]*",
                r"npm run test\b[^\n]*",
                r"cargo test\b[^\n]*",
                r"go test\b[^\n]*",
            ],
            combined,
        )
        if m2:
            unit_cmd = m2.rstrip("\\").strip()
            unit_ev.append("manifest/CI scan")

    if unit_cmd is None and (target / "pytest.ini").is_file() and (target / "backend" / "pyproject.toml").is_file():
        unit_cmd = "uv run --project backend pytest tests -q"
        unit_ev.append("pytest.ini + backend/pyproject.toml")
    elif unit_cmd is None and (target / "tests").is_dir() and (target / "pyproject.toml").is_file():
        unit_cmd = "python -m pytest tests/ -q"
        unit_ev.append("tests/ + pyproject.toml")

    if unit_cmd:
        # Normalize trailing noise from markdown fences / inline comments before flags
        unit_cmd = unit_cmd.strip().strip("`").split("#")[0].strip()
        if " -q" not in unit_cmd and " -x" not in unit_cmd and "pytest" in unit_cmd:
            unit_cmd = unit_cmd + " -q"
        result.rows.append(CommandRow("Unit tests", f"`{unit_cmd}`", "REAL", unit_ev))
    else:
        result.rows.append(CommandRow("Unit tests", "NONE — no tool in repo", "NONE", []))

    # --- Coverage ---
    cov_cmd: str | None = None
    cov_ev: list[str] = []
    has_cov = (
        "pytest-cov" in combined
        or "--cov" in combined
        or "[tool.coverage" in root_pyproject
        or "[tool.coverage" in backend_pyproject
    )
    if has_cov:
        m = re.search(r"(python -m pytest[^\n]*--cov[^\n]*)", combined)
        if m:
            cov_cmd = m.group(1).strip().strip("`")
            cov_ev.append("scan")
        elif unit_cmd and "pytest" in unit_cmd:
            # Best-effort: append cov flags if package name guessable
            cov_cmd = unit_cmd
            if "--cov" not in cov_cmd:
                # leave as-is with note — better NONE than wrong package
                if "taskboard" in root_pyproject:
                    cov_cmd = (
                        'python -m pytest tests/ --cov=taskboard --cov-report=term-missing'
                    )
                    cov_ev.append("pyproject.toml (taskboard)")
                else:
                    cov_cmd = None
        if cov_cmd:
            result.rows.append(
                CommandRow(
                    "Coverage",
                    f"`{cov_cmd}` (whole-package % is proxy for changed-line when diff-cover not installed)",
                    "REAL",
                    cov_ev,
                )
            )
        else:
            result.rows.append(
                CommandRow(
                    "Coverage",
                    "NONE — no tool in repo",
                    "NONE",
                    ["pytest-cov signals found but command not reconstructable"],
                )
            )
    else:
        result.rows.append(
            CommandRow("Coverage", "NONE — no tool in repo", "NONE", ["no pytest-cov / --cov in scan"])
        )

    # --- Regression ---
    unit_row = result.by_name("Unit tests")
    if unit_row and unit_row.status == "REAL":
        reg = unit_row.value
        notes = []
        if "tests/e2e" in combined or (target / "tests" / "e2e").is_dir():
            notes.append("extended: e2e under tests/e2e")
        if (target / "frontend" / "e2e").is_dir() or "playwright" in combined.lower():
            notes.append("extended: frontend Playwright e2e")
        if "tests/determinism" in combined:
            notes.append("extended: tests/determinism")
        suffix = f" ({'; '.join(notes)})" if notes else ""
        result.rows.append(
            CommandRow(
                "Regression / full suite",
                f"{reg}{suffix}",
                "REAL",
                unit_row.evidence,
            )
        )
    else:
        result.rows.append(
            CommandRow("Regression / full suite", "NONE — no tool in repo", "NONE", [])
        )

    # --- Lint / typecheck ---
    lint_parts: list[str] = []
    lint_ev: list[str] = []

    m = re.search(
        r"^(uv run --project \S+ ruff check[^\n`]*)",
        readme + "\n" + claude,
        flags=re.MULTILINE,
    )
    if m:
        lint_cmd = m.group(1).strip().strip("`").split("#")[0].strip()
        lint_parts.append(f"`{lint_cmd}`")
        lint_ev.append("README/CLAUDE")
    else:
        m2 = _first_match(
            [
                r"uv run --project \S+ ruff check[^\n]*",
                r"python -m ruff check[^\n]*",
                r"ruff check[^\n]*",
            ],
            combined,
        )
        if m2:
            lint_parts.append(f"`{m2.strip().strip('`').split('#')[0].strip()}`")
            lint_ev.append("scan")
        elif "ruff" in backend_pyproject or "ruff" in root_pyproject:
            if (target / "backend" / "pyproject.toml").is_file():
                lint_parts.append("`uv run --project backend ruff check backend tests`")
            else:
                lint_parts.append("`python -m ruff check .`")
            lint_ev.append("pyproject ruff config")

    if isinstance(frontend_pkg, dict) and isinstance(frontend_pkg.get("scripts"), dict):
        fs = frontend_pkg["scripts"]
        if "typecheck" in fs:
            lint_parts.append("`cd frontend && npm run typecheck`")
            lint_ev.append("frontend/package.json")
        elif "lint" in fs:
            lint_parts.append("`cd frontend && npm run lint`")
            lint_ev.append("frontend/package.json")

    if lint_parts:
        result.rows.append(
            CommandRow("Lint / typecheck", " · ".join(lint_parts), "REAL", lint_ev)
        )
    else:
        result.rows.append(
            CommandRow("Lint / typecheck", "NONE — no tool in repo", "NONE", [])
        )

    return result


def format_project_test_commands(scan: ScanResult, *, no_scan: bool) -> str:
    if no_scan:
        lines = [
            BEGIN_PTC,
            "<!-- Installer: --no-scan; fill or write docs/waivers/bootstrap-test-commands.md -->",
            "",
            "- **Build:** `TODO — user must fill`",
            "- **Unit tests:** `TODO — user must fill`",
            "- **Coverage:** `TODO — user must fill`",
            "- **Regression / full suite:** `TODO — user must fill`",
            "- **Lint / typecheck:** `TODO — user must fill`",
            END_PTC,
        ]
        return "\n".join(lines)

    evidence_bits: list[str] = []
    for row in scan.rows:
        if row.evidence:
            evidence_bits.extend(row.evidence)
    uniq = sorted(set(evidence_bits))
    comment = (
        f"<!-- Filled by install_agentic_team.py from: {', '.join(uniq) if uniq else 'scan'} -->"
    )
    lines = [BEGIN_PTC, comment, ""]
    for row in scan.rows:
        lines.append(f"- **{row.name}:** {row.value}")
    lines.append(END_PTC)
    return "\n".join(lines)


def format_project_specific_rules(companions: list[str]) -> str:
    if not companions:
        return f"{BEGIN_PSR}\n{END_PSR}"
    lines = [
        BEGIN_PSR,
        "## Project-specific rules",
        "",
        "Also follow these existing contributor files (do not ignore product invariants):",
        "",
    ]
    for name in companions:
        lines.append(f"- `{name}`")
    lines.append(END_PSR)
    return "\n".join(lines)


def replace_marked_section(text: str, begin: str, end: str, replacement: str) -> str:
    if begin not in text or end not in text:
        raise ValueError(f"Missing markers {begin!r} / {end!r} in AGENTS skeleton")
    pre, rest = text.split(begin, 1)
    _, post = rest.split(end, 1)
    # replacement already includes begin/end
    return pre + replacement + post


def build_agents_md(
    source_agents: str,
    scan: ScanResult,
    companions: list[str],
    *,
    no_scan: bool,
    previous_agents_backup: str | None,
) -> str:
    text = source_agents
    text = replace_marked_section(
        text, BEGIN_PSR, END_PSR, format_project_specific_rules(companions)
    )
    text = replace_marked_section(
        text, BEGIN_PTC, END_PTC, format_project_test_commands(scan, no_scan=no_scan)
    )
    if previous_agents_backup:
        note = (
            "\n## Preserved notes\n\n"
            f"A previous root `AGENTS.md` was backed up to `{previous_agents_backup}` "
            "before this install. Merge any project-specific lead rules from that backup if needed.\n"
        )
        # Insert before Project Test Commands heading if possible
        anchor = "## Project Test Commands"
        if anchor in text and "## Preserved notes" not in text:
            text = text.replace(anchor, note + anchor, 1)
    return text


def write_agents(
    source: Path,
    target: Path,
    scan: ScanResult,
    companions: list[str],
    *,
    force: bool,
    dry_run: bool,
    no_scan: bool,
    report: InstallReport,
) -> None:
    src_agents = source / "AGENTS.md"
    if not src_agents.is_file():
        report.errors.append(f"Source AGENTS.md missing: {src_agents}")
        return

    dest = target / "AGENTS.md"
    backup_rel: str | None = None
    if dest.is_file():
        # Always backup existing AGENTS before rewrite (even if force) when content would change
        new_body = build_agents_md(
            read_text(src_agents),
            scan,
            companions,
            no_scan=no_scan,
            previous_agents_backup=None,
        )
        if dest.read_text(encoding="utf-8") == new_body:
            report.add("skip_identical", "AGENTS.md")
            return
        # If existing is different and not force and existing is non-template? Plan says always backup and write new AGENTS
        # For AGENTS we always update (it's generated), with backup.
        day = datetime.now(timezone.utc).strftime("%Y%m%d")
        bak = dest.with_name(f"AGENTS.md.bak-before-agentic-template-{day}")
        if bak.exists():
            bak = dest.with_name(
                f"AGENTS.md.bak-before-agentic-template-{day}-{timestamp()}"
            )
        report.add("backup", rel_str(bak, target), "from AGENTS.md")
        if not dry_run:
            shutil.copy2(dest, bak)
        backup_rel = rel_str(bak, target)

    body = build_agents_md(
        read_text(src_agents),
        scan,
        companions,
        no_scan=no_scan,
        previous_agents_backup=backup_rel,
    )
    if dest.is_file() and not force:
        # Still write AGENTS — plan: generate AGENTS for target. Existing always backed up.
        pass
    report.add("update" if dest.exists() else "create", "AGENTS.md")
    write_text(dest, body, dry_run)


def write_handoff(
    target: Path,
    report: InstallReport,
    *,
    dry_run: bool,
) -> None:
    path = target / "docs" / "plans" / "agentic-team-install-handoff.md"
    lines = [
        "# Agentic team install handoff",
        "",
        f"- **Date:** {datetime.now(timezone.utc).strftime('%Y-%m-%d')}",
        f"- **Template version:** {TEMPLATE_VERSION}",
        f"- **git_mode:** {report.git_mode}",
        f"- **Companion rules (unchanged):** {', '.join(report.companion_rules) or 'none'}",
        "",
        "## Project Test Commands status",
        "",
    ]
    if report.scan:
        for row in report.scan.rows:
            ev = f" (evidence: {', '.join(row.evidence)})" if row.evidence else ""
            lines.append(f"- **{row.name}:** {row.status} — {row.value}{ev}")
    else:
        lines.append("- (no scan)")

    lines.extend(
        [
            "",
            "## Actions",
            "",
        ]
    )
    for a in report.actions:
        detail = f" — {a.detail}" if a.detail else ""
        lines.append(f"- `{a.kind}` `{a.path}`{detail}")

    if report.warnings:
        lines.extend(["", "## Warnings", ""])
        for w in report.warnings:
            lines.append(f"- {w}")

    if report.errors:
        lines.extend(["", "## Errors", ""])
        for e in report.errors:
            lines.append(f"- {e}")

    lines.extend(
        [
            "",
            "## Next steps",
            "",
            "1. Confirm Project Test Commands in root `AGENTS.md` (fill TODOs or write durable waivers).",
            "2. If Coverage is NONE: add tooling or `docs/waivers/` before merge claims coverage gate.",
            "3. Optional: `grok inspect --json` and confirm project skills.",
            "4. Optional: Fixture A — copy `fixtures/agentic-template-acceptance/bad-plan.md` → `docs/plans/acceptance-bad-plan.md` and run `/plan-review-loop` or `/cold-review`.",
            "5. Prefer bundled `/review`, `/check-work`, `/implement` for product work.",
            "",
            "## Reminders",
            "",
            "- Prepend persona instruction files on every spawn; tags are UI-only.",
            "- Always set `capability_mode` on spawn (QA: execute/all).",
            "- Lead-only spawn (depth 1).",
            "",
        ]
    )
    report.add("create" if not path.exists() else "update", rel_str(path, target))
    write_text(path, "\n".join(lines), dry_run)


def verify_install(target: Path, report: InstallReport) -> bool:
    ok = True
    for skill in EXPECTED_SKILLS:
        # install-agentic-team may not exist in older sources — only require core five always
        if skill == "install-agentic-team":
            p = target / ".grok" / "skills" / skill / "SKILL.md"
            if not p.is_file():
                report.warnings.append(f"Optional skill missing: {skill}")
            continue
        p = target / ".grok" / "skills" / skill / "SKILL.md"
        if not p.is_file():
            report.errors.append(f"Missing skill: {skill}")
            ok = False
    for rel in (
        ".grok/rules/accuracy-coverage.md",
        ".grok/personas/gf-qa.toml",
        "docs/waivers/README.md",
        "AGENTS.md",
    ):
        if not (target / rel).is_file():
            report.errors.append(f"Missing required path: {rel}")
            ok = False

    for doc in EXPECTED_DOCS:
        p = target / ".grok" / "docs" / doc
        if not p.is_file():
            report.errors.append(f"Missing required doc: .grok/docs/{doc}")
            ok = False

    for persona in (
        "gf-qa.md",
        "gf-plan-reviewer.md",
        "gf-backend.md",
        "gf-frontend.md",
    ):
        p = target / ".grok" / "personas" / "instructions" / persona
        if not p.is_file():
            report.errors.append(f"Missing persona instructions: {persona}")
            ok = False

    # Optional grok inspect
    try:
        r = subprocess.run(
            ["grok", "inspect", "--json"],
            cwd=str(target),
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
        if r.returncode == 0 and r.stdout.strip():
            try:
                json.loads(r.stdout)
                report.warnings.append("grok inspect ran successfully (see CLI for skill list)")
            except json.JSONDecodeError:
                report.warnings.append("grok inspect returned non-JSON; skipped parse")
        else:
            report.warnings.append("grok inspect not available or failed; tree checks only")
    except (OSError, subprocess.TimeoutExpired):
        report.warnings.append("grok CLI not available; tree checks only")

    report.verify_ok = ok
    return ok


def install(
    source: Path,
    target: Path,
    *,
    dry_run: bool = False,
    force: bool = False,
    skip_agents: bool = False,
    agents_only: bool = False,
    no_scan: bool = False,
    write_handoff_flag: bool = False,
    verify: bool = False,
) -> InstallReport:
    report = InstallReport()
    source = source.resolve()
    target = target.resolve()

    if not source.is_dir():
        report.errors.append(f"Source is not a directory: {source}")
        return report
    if not target.is_dir():
        report.errors.append(f"Target is not a directory: {target}")
        return report
    if source == target:
        report.errors.append("Source and target are the same path; refusing self-install")
        return report

    if not is_git_repo(target):
        report.git_mode = "degraded"
        report.warnings.append(
            "Target is not a git repository. Grok projectRoot may be null; "
            "/review, worktrees, and git-diff test selection are degraded."
        )
    else:
        report.git_mode = "full"

    report.companion_rules = find_companion_rules(target)
    report.scan = (
        ScanResult(
            rows=[
                CommandRow(n, "TODO — user must fill", "TODO")
                for n in (
                    "Build",
                    "Unit tests",
                    "Coverage",
                    "Regression / full suite",
                    "Lint / typecheck",
                )
            ]
        )
        if no_scan
        else scan_project_commands(target)
    )

    if not agents_only:
        ensure_dirs(target, dry_run, report)
        for src_file in iter_install_files(source):
            rel = rel_str(src_file, source)
            dest = target / rel
            install_file(
                src_file,
                dest,
                force=force,
                dry_run=dry_run,
                report=report,
                target_root=target,
            )

    if not skip_agents:
        write_agents(
            source,
            target,
            report.scan,
            report.companion_rules,
            force=force,
            dry_run=dry_run,
            no_scan=no_scan,
            report=report,
        )

    if write_handoff_flag:
        if not dry_run:
            (target / "docs" / "plans").mkdir(parents=True, exist_ok=True)
        write_handoff(target, report, dry_run=dry_run)

    if verify and not dry_run:
        verify_install(target, report)
    elif verify and dry_run:
        report.warnings.append("--verify skipped during --dry-run")

    return report


def print_report(report: InstallReport) -> None:
    print(f"git_mode: {report.git_mode}")
    if report.companion_rules:
        print(f"companion_rules: {', '.join(report.companion_rules)}")
    if report.scan:
        print("Project Test Commands:")
        for row in report.scan.rows:
            print(f"  [{row.status}] {row.name}: {row.value}")
    print("Actions:")
    for a in report.actions:
        detail = f" ({a.detail})" if a.detail else ""
        print(f"  {a.kind:16} {a.path}{detail}")
    for w in report.warnings:
        print(f"WARNING: {w}", file=sys.stderr)
    for e in report.errors:
        print(f"ERROR: {e}", file=sys.stderr)
    if report.verify_ok is not None:
        print(f"verify: {'PASS' if report.verify_ok else 'FAIL'}")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Install GrokForge Agentic Dev Team template config into a project.",
    )
    p.add_argument("target", type=Path, help="Target project root directory")
    p.add_argument(
        "--source",
        type=Path,
        default=None,
        help="Template source root (default: parent of scripts/)",
    )
    p.add_argument("--dry-run", action="store_true", help="Print actions only")
    p.add_argument(
        "--force",
        action="store_true",
        help="Overwrite conflicting template-owned files (with backup)",
    )
    p.add_argument("--skip-agents", action="store_true", help="Do not write AGENTS.md")
    p.add_argument(
        "--agents-only",
        action="store_true",
        help="Only (re)generate AGENTS.md",
    )
    p.add_argument(
        "--no-scan",
        action="store_true",
        help="Leave Project Test Commands as TODO placeholders",
    )
    p.add_argument(
        "--write-handoff",
        action="store_true",
        help="Write docs/plans/agentic-team-install-handoff.md in target",
    )
    p.add_argument(
        "--verify",
        action="store_true",
        help="After install, check required tree (and grok inspect if available)",
    )
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    source = (args.source or default_source_root()).resolve()
    target = args.target.resolve()
    report = install(
        source,
        target,
        dry_run=args.dry_run,
        force=args.force,
        skip_agents=args.skip_agents,
        agents_only=args.agents_only,
        no_scan=args.no_scan,
        write_handoff_flag=args.write_handoff,
        verify=args.verify,
    )
    print_report(report)
    return 1 if report.errors else 0


if __name__ == "__main__":
    sys.exit(main())
