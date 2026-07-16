# GrokForge Agentic Dev Team Template

**Template version:** see [`VERSION`](VERSION) (patch bumps on **every commit**)

Bootstrap config for a Grok-native agentic software team (accuracy, tests, coverage, plan-quality loops, UI design gates), plus a **TaskBoard** sample app used to exercise the team.

**Metrics (every commit):** [`docs/metrics/token-ledger.md`](docs/metrics/token-ledger.md) + `VERSION` via  
`python scripts/prepare_commit_metrics.py --model … --input N --output M`  
(or `--unmeasured`). Install hook: `python scripts/install_git_hooks.py`. Never invent counts.

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

**Installs:** `.grok/`, `docs/waivers/README.md`, `docs/metrics/` (README + seed ledger if missing), acceptance fixtures, generated `AGENTS.md` (scanned build/test commands).

**Does not install:** TaskBoard `src/` / template `tests/` / `pyproject.toml`, or this repo’s plan history. **Never overwrites** an existing token ledger.

**Existing product rules:** If the target has `CLAUDE.md` (or similar), it is left unchanged and referenced from `AGENTS.md`. Existing `AGENTS.md` is backed up before rewrite.

**Git:** Full protocol (`/review` local mode, worktrees) needs a git root. Non-git targets install in degraded mode.

Optional Grok skill: `/install-agentic-team` (runs the same script).

## What's in this repo

| Path | Purpose |
|------|---------|
| `VERSION` | Semver; **patch bumps on every commit** |
| `AGENTS.md` | Lead rules, gates, Project Test Commands |
| `.grok/` | Personas, skills, auto-loaded rules, reference docs |
| `scripts/install_agentic_team.py` | Install config into another project |
| `scripts/prepare_commit_metrics.py` | **Required every commit:** bump VERSION + ledger entry |
| `scripts/install_git_hooks.py` | Install pre-commit metrics hook |
| `scripts/record_token_usage.py` | Optional mid-session ledger append (no version bump) |
| `docs/metrics/` | Token ledger + metrics README |
| `docs/plans/` | Plans + bootstrap verification artifacts |
| `docs/waivers/` | Durable gate waivers |
| `fixtures/agentic-template-acceptance/` | Acceptance fixtures A–E (+ sample UI for E) |
| `src/taskboard/` | **Test application** for agents to extend |
| `tests/` | Pytest suite |
| `.github/workflows/ci.yml` | Unit + lint + coverage + diff-cover |

## TaskBoard (test application)

Minimal in-memory task board library:

```bash
# install dev deps
python -m pip install -e ".[dev]"

# unit tests
python -m pytest tests/ -q

# coverage (whole-package + changed-line)
python -m pytest tests/ --cov=taskboard --cov-report=term-missing --cov-report=xml
python -m diff_cover.diff_cover_tool coverage.xml --compare-branch=origin/main --fail-under=80
# fallback compare-branch: main (if origin/main missing)
# vacuous "no lines in this diff" => UNMEASURED / no changed lines — not 100%

# lint
python -m ruff check src tests scripts
```

### Feature for agents to build

See `docs/plans/taskboard-tags-feature.md` — add **tags** to tasks with normalization, filtering, and tests.

Suggested agent pipeline:

1. `/plan-review-loop` on the tags plan (hard gates; max 2 revise passes). Optional `/cold-review` only if present in `grok inspect`.  
2. `/implement` (or spawn `gf-backend` with prepended instructions; green targeted tests before Ready)  
3. `/post-change-accuracy-protocol` (targeted → review → regression → check-work; max 3 cycles)  
4. Before commit: `prepare_commit_metrics.py` with measured tokens (or `--unmeasured`)  

### Sample UI (Fixture E)

`fixtures/agentic-template-acceptance/sample-ui/` — small HTML UI with design tokens and state inventory, used to exercise the UI design gate without a full frontend app.

## Version history (short)

- **v1.7** — Coverage alignment, installer diff-cover, vacuous-diff policy, spawn checklist, full roles, plan-review default, parallel-fullstack CLI path, Lint gate, CI, sample UI, **per-commit VERSION + token ledger** (`prepare_commit_metrics` + git hook).  
- **v1.6** — UI design pillar, gate 8, UI verification, Fixture E notes, lint gate, diff-cover ladder, QA independence, conditional security.  
- **v1.5** — Plan hard gates, fix→re-test loops, implementer done criteria.

## Bootstrap status

See `docs/plans/bootstrap-handoff.md` (historical + current snapshot).
