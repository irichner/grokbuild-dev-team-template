# GrokForge Agentic Dev Team Template

**Template version:** 1.5

Bootstrap config for a Grok-native agentic software team (accuracy, tests, coverage, plan-quality loops), plus a **TaskBoard** sample app used to exercise the team.

## Install into another project

Copy the agentic team config (not TaskBoard product code) into a new or existing git repo:

```bash
# from this template repo root
python scripts/install_agentic_team.py C:\path\to\project
python scripts/install_agentic_team.py C:\path\to\project --dry-run
python scripts/install_agentic_team.py C:\path\to\project --write-handoff --verify
python scripts/install_agentic_team.py C:\path\to\project --force   # overwrite diverged template files (with backup)
```

| Flag | Effect |
|------|--------|
| `--dry-run` | Print actions only |
| `--force` | Overwrite conflicting `.grok`/fixture files (timestamped backup) |
| `--write-handoff` | Write `docs/plans/agentic-team-install-handoff.md` in the target |
| `--verify` | Check required tree; run `grok inspect` if CLI available |
| `--no-scan` | Leave Project Test Commands as TODO |
| `--skip-agents` / `--agents-only` | Control `AGENTS.md` generation |

**Installs:** `.grok/`, `docs/waivers/README.md`, acceptance fixtures, generated `AGENTS.md` (scanned build/test commands).

**Does not install:** TaskBoard `src/` / template `tests/` / `pyproject.toml`, or this repo’s plan history.

**Existing product rules:** If the target has `CLAUDE.md` (or similar), it is left unchanged and referenced from `AGENTS.md`. Existing `AGENTS.md` is backed up before rewrite.

**Git:** Full protocol (`/review` local mode, worktrees) needs a git root. Non-git targets install in degraded mode.

Optional Grok skill: `/install-agentic-team` (runs the same script).

## What's in this repo

| Path | Purpose |
|------|---------|
| `AGENTS.md` | Lead rules, gates, Project Test Commands |
| `.grok/` | Personas, skills, auto-loaded rules, reference docs |
| `scripts/install_agentic_team.py` | Install config into another project |
| `docs/plans/` | Plans + bootstrap verification artifacts |
| `docs/waivers/` | Durable gate waivers |
| `fixtures/agentic-template-acceptance/` | Acceptance fixtures A/B/C (+ optional D) |
| `src/taskboard/` | **Test application** for agents to extend |
| `tests/` | Pytest suite |

## TaskBoard (test application)

Minimal in-memory task board library:

```bash
# install dev deps
python -m pip install -e ".[dev]"

# unit tests
python -m pytest tests/ -q

# coverage
python -m pytest tests/ --cov=taskboard --cov-report=term-missing

# lint
python -m ruff check src tests
```

### Feature for agents to build

See `docs/plans/taskboard-tags-feature.md` — add **tags** to tasks with normalization, filtering, and tests.

Suggested agent pipeline:

1. `/plan-review-loop` or `/cold-review` on the tags plan (hard gates; max 2 revise passes)  
2. `/implement` (or spawn `gf-backend` with prepended instructions; green targeted tests before Ready)  
3. `/post-change-accuracy-protocol` (targeted → review → regression → check-work; max 3 cycles)  

v1.5 strengthens plan hard gates (`.grok/docs/plan-quality-standards.md`), fix→re-test loops in QA skills, and implementer done criteria.

## Bootstrap status

See `docs/plans/bootstrap-handoff.md`.
