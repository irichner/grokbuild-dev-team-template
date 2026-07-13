# Plan: Install GrokForge Agentic Dev Team into target projects

**Date:** 2026-07-12  
**Template version:** 1.4  
**Status:** Draft for approval  
**Goal:** Reusable installer that copies agentic team config into a new or existing repo, then validate by installing into `C:\Users\israe\Projects\SPM_ICM`.

## Decisions (confirmed)

| Decision | Choice |
|----------|--------|
| Scope | Installer tooling in this template **+** install into SPM_ICM |
| Existing product rules | Create root `AGENTS.md`; **keep** `CLAUDE.md` (and similar) intact; reference them from AGENTS |
| Product code | **Never** copy TaskBoard (`src/`, `tests/`, `pyproject.toml`) or bootstrap history docs |
| Config root | `.grok/` only (no `.grokbuild/`) |

## Problem

This repo is both:

1. A **working sample** (TaskBoard + full agentic config), and  
2. The **source of truth** for the agentic team (`.grok/`, AGENTS pipeline, fixtures, waivers).

There is a long bootstrap markdown, but no turnkey way to land the config in another git project (e.g. SPM_ICM) without re-running the multi-phase bootstrap by hand.

SPM_ICM today:

- Git repo; has `CLAUDE.md` product invariants; **no** `AGENTS.md` or `.grok/`
- Tests: `uv run --project backend pytest tests` (from root)
- Lint: `uv run --project backend ruff check backend tests scripts`
- Frontend build: `cd frontend && npm run build`
- No pytest-cov in backend deps → Coverage likely `NONE — no tool in repo` unless we add tooling (out of scope for installer; durable waiver path exists)

## Non-goals

- Replacing product code, CI YAML, or CLAUDE.md  
- Installing coverage tools into every language  
- Full Phase 4 behavioral Fixture A inside the target during silent install (optional `--verify` / post-install checklist)  
- Shipping TaskBoard as part of install  
- Auto-merging foreign `AGENTS.md` body into a single mega-file  

## Design

### Install surface (what gets copied)

**Always install (template-owned paths):**

```
.grok/                          # entire tree (rules, personas, skills, roles, docs, workflows, README)
docs/waivers/README.md          # create dir; do not wipe existing waivers
fixtures/agentic-template-acceptance/   # acceptance fixtures A notes
```

**Generate (not blind copy of template AGENTS):**

```
AGENTS.md   # pipeline + gates + personas + Project Test Commands filled for TARGET
```

**Optional / create-if-missing dirs:**

```
docs/plans/     # mkdir only if missing (do not clobber existing plans)
docs/waivers/   # ensure exists
```

**Never install:**

- `src/`, `tests/`, `pyproject.toml`, TaskBoard egg-info  
- `docs/plans/*` content from the template (bootstrap history, taskboard plans)  
- Root bootstrap markdown / review artifacts  
- `.git`, caches, `.coverage`

### Installer CLI

**Path:** `scripts/install_agentic_team.py` (Python 3.11+, stdlib-only — no install deps)

```text
python scripts/install_agentic_team.py <target> [options]

Options:
  --dry-run          Print actions only
  --force            Overwrite template-owned files even if changed in target
  --skip-agents      Do not write/update AGENTS.md
  --agents-only      Only (re)write AGENTS Project Test Commands section helper
  --no-scan          Leave Project Test Commands as TODO placeholders (still requires note in handoff)
  --write-handoff    Write docs/plans/agentic-team-install-handoff.md in target
  --verify           After copy: check tree + list expected skill names (no grok CLI required);
                     if `grok` on PATH, optionally run grok inspect from target cwd
```

**Default source root:** parent of `scripts/` (this template repo). Override: `--source <path>`.

### Conflict policy

| Target state | Behavior |
|--------------|----------|
| Missing path | Create |
| Existing file, identical content | Skip (idempotent) |
| Existing file, different content, template-owned path under `.grok/` or fixtures | Skip + warn unless `--force` (then backup `*.bak-agentic-YYYYMMDD-HHMMSS` then overwrite) |
| Existing `docs/waivers/*` other than README | Never delete |
| Existing `AGENTS.md` | Timestamped backup `AGENTS.md.bak-before-agentic-template-YYYYMMDD`; write new AGENTS with pipeline; if old body was non-template, include a short "Preserved notes" pointer to backup path |
| Existing `CLAUDE.md` / `GEMINI.md` / etc. | Leave untouched; AGENTS.md adds: **Also follow** `CLAUDE.md` (list detected companion rule files) |
| Non-git target | Warn; continue with `git_mode: degraded` in handoff (mirror bootstrap Phase 0) |

### AGENTS.md generation

1. Start from **template skeleton** (same structure as current `AGENTS.md`: pipeline, gates, personas, waivers).  
2. Replace **Project Test Commands** via scan of target (Phase 3 closed outcomes: REAL / NONE / TODO).  
3. If companion files exist (`CLAUDE.md`), insert under Harness or a **Project-specific rules** section:

```markdown
## Project-specific rules

Also follow these existing contributor files (do not ignore product invariants):

- `CLAUDE.md`
```

4. Do **not** copy TaskBoard-specific command comments.

### Manifest scan (Project Test Commands)

Heuristic, evidence-based (good enough for SPM_ICM + common stacks):

| Command | Detection order |
|---------|-----------------|
| Build | `uv` + `backend/pyproject.toml` → note backend env; `frontend/package.json` scripts.build → `npm run build` (document both lines if monorepo); else root `package.json` / `pip install -e` |
| Unit tests | README / CI / `pytest.ini` / `pyproject` → prefer documented root command e.g. `uv run --project backend pytest tests -q` |
| Coverage | `pytest-cov` / `--cov` in CI or pyproject tool config; else `NONE — no tool in repo` |
| Regression | Same as unit if single suite; if CI has extra e2e/determinism jobs, list primary full suite + note extended |
| Lint | ruff/eslint/mypy from CI or package scripts |

Write a short HTML comment block in AGENTS with scan evidence paths.

For **SPM_ICM expected fill:**

- **Build:** `uv sync --project backend` (or document compose) + `cd frontend && npm run build`  
- **Unit tests:** `uv run --project backend pytest tests -q`  
- **Coverage:** `NONE — no tool in repo` (no pytest-cov in backend dev deps) → handoff notes waiver-or-add-tooling  
- **Regression:** `uv run --project backend pytest tests -q` (full suite; optional extended: e2e/Playwright noted)  
- **Lint:** `uv run --project backend ruff check backend tests scripts` + frontend `npm run typecheck`

### Packaging the template source

Keep source-of-truth as the live `.grok/` tree in this repo (not re-embed bootstrap megadoc).

Add:

- `scripts/install_agentic_team.py` — main installer  
- `scripts/template_manifest.json` (optional) — explicit file list if we want freeze control; otherwise walk `.grok/`, `fixtures/agentic-template-acceptance/`, `docs/waivers/README.md`  
- `templates/AGENTS.md.skeleton` — AGENTS without product-specific Project Test Commands (placeholders)  
  - *Alternative:* generate skeleton by reading root `AGENTS.md` and replacing the Project Test Commands section via markers `<!-- BEGIN PROJECT_TEST_COMMANDS -->` … `<!-- END PROJECT_TEST_COMMANDS -->`

**Prefer markers** in current `AGENTS.md` so one file stays authoritative for pipeline text.

### Docs

Update root `README.md`:

```markdown
## Install into another project

python scripts/install_agentic_team.py C:\path\to\project
python scripts/install_agentic_team.py C:\path\to\project --dry-run
python scripts/install_agentic_team.py C:\path\to\project --force --write-handoff
```

Document: new vs existing, CLAUDE.md coexistence, git required for full protocol, post-install checklist (V8-style skill names, optional Fixture A).

### Grok skill (light)

Add project skill `.grok/skills/install-agentic-team/SKILL.md`:

- When user says "install this template into X"  
- Run the Python script with execute capability  
- Then summarize handoff / next steps  
- Does not reimplement bootstrap Phases as free-form file writes

### Validation: SPM_ICM install

After script is ready (from this template repo):

```powershell
python scripts/install_agentic_team.py C:\Users\israe\Projects\SPM_ICM --write-handoff
```

Verify:

1. `C:\Users\israe\Projects\SPM_ICM\.grok\skills\*\SKILL.md` exist (5 skills)  
2. `AGENTS.md` exists; `CLAUDE.md` unchanged  
3. `docs/waivers/README.md` exists; existing `docs/plans/*` intact  
4. Project Test Commands match SPM_ICM reality  
5. No TaskBoard paths under SPM_ICM  
6. Optional: `grok inspect --json` from SPM_ICM if CLI available  

**Note:** Installing into SPM_ICM modifies a sibling repo. Confirm once before running non-dry-run (user already chose this slice).

### Tests for the installer (this template repo)

Minimal unit tests under `tests/test_install_agentic_team.py` (or `tests/scripts/`):

- Dry-run on a temp dir creates no files  
- Install into empty temp git repo creates expected tree  
- Second install is idempotent (no spurious backups if identical)  
- Existing divergent `.grok/rules/foo.md` is preserved without `--force`  
- `CLAUDE.md` present → AGENTS references it; CLAUDE bytes unchanged  
- Scan detects pytest/ruff from a fake pyproject fixture  
- Never copies `src/taskboard`

Keep coverage gate honest: either put install module under a package path covered by pytest, or document tests for the script via `importlib` loading from `scripts/`.

**Preferred layout for testability:**

```
src/grokforge_template/
  __init__.py
  install.py          # library logic
scripts/install_agentic_team.py  # thin CLI wrapper
```

But adding a second package alongside taskboard may be heavier. **Simpler approach:** keep single module at `scripts/install_agentic_team.py` and load it in tests via path insert — acceptable for tooling scripts.

Or put logic in `src/taskboard` — **no**, wrong domain.

**Decision:** `scripts/install_agentic_team.py` self-contained + tests import via `importlib.util.spec_from_file_location`.

### Accuracy protocol for this change

1. Plan (this doc) → optional cold-review if large  
2. Implement installer + tests in template repo  
3. `/targeted-unit-test-loop` on install tests  
4. `/review` (manual implement path)  
5. Regression full pytest  
6. Run installer against SPM_ICM (user-approved sibling write)  
7. Handoff file in SPM_ICM  

### Implementation steps

1. Add section markers to `AGENTS.md` around Project Test Commands  
2. Implement `scripts/install_agentic_team.py` (copy, scan, AGENTS gen, backups, dry-run, force)  
3. Unit tests for installer behavior on temp dirs  
4. README install section + skill `install-agentic-team`  
5. Run installer on SPM_ICM with `--write-handoff`  
6. Spot-check SPM_ICM tree; fix scanner if commands wrong  
7. Template-repo pytest green; record install handoff  

### Risks

| Risk | Mitigation |
|------|------------|
| Overwrite custom `.grok` in target | Default skip-on-diff; `--force` + backup |
| Wrong test commands | Prefer README/CI strings; print evidence; handoff lists REAL/NONE |
| SPM_ICM coverage NONE blocks "operational gates" | Honest NONE + handoff; user can waive or add pytest-cov later |
| Sibling repo surprise writes | Explicit path in CLI; dry-run first in docs; confirm before live install |
| AGENTS replaces product invariants | Reference CLAUDE.md; never delete CLAUDE.md |

### Success criteria

- `python scripts/install_agentic_team.py <target>` works for empty and existing projects  
- SPM_ICM has discoverable project skills under `.grok/skills/` and an AGENTS.md that points at real `uv`/`npm` commands  
- CLAUDE.md untouched  
- Installer tests pass in template repo  
- Docs explain new vs existing install  

## Open follow-ups (not this slice)

- Fixture A behavioral run inside SPM_ICM  
- Adding pytest-cov to SPM_ICM  
- PowerShell one-liner wrapper (optional; Python is enough on Windows if `python` on PATH)  
- Publishing template as a pip entry point  
