# User Guide — GrokForge Agentic Dev Team

How to install and use this template day to day.  
**Primary stack: Grok** (`.grok/` + root `AGENTS.md`).  
For *why* the accuracy loop exists, see `docs/WORKFLOW.md`. For surfaces, see `docs/FEATURES.md`.

> **Optional sibling:** This repo may also contain a Claude Code tree (`.claude/`, `CLAUDE.md`).  
> That path is **not** what `install_agentic_team.py` installs. When using Grok as Lead, follow this guide and `AGENTS.md` first.

---

## Contents

1. [What you're installing](#1-what-youre-installing)
2. [Prerequisites](#2-prerequisites)
3. [Install in 5 minutes](#3-install-in-5-minutes)
4. [Confirm it works](#4-confirm-it-works)
5. [Your first task](#5-your-first-task)
6. [Commands and skills](#6-commands-and-skills)
7. [Accuracy pipeline](#7-accuracy-pipeline)
8. [Personas and spawn](#8-personas-and-spawn)
9. [Metrics and commits](#9-metrics-and-commits)
10. [Acceptance fixtures](#10-acceptance-fixtures)
11. [Troubleshooting](#11-troubleshooting)

---

## 1. What you're installing

A **GrokForge** agentic team config:

| Surface | Path | Role |
|---------|------|------|
| Lead rules | `AGENTS.md` | Pipeline, gates, Project Test Commands |
| Auto-loaded rules | `.grok/rules/` | Spawn checklist, accuracy/coverage |
| Skills | `.grok/skills/*/SKILL.md` | Plan review, targeted/regression loops, post-change protocol, install |
| Personas | `.grok/personas/instructions/` | `gf-backend`, `gf-frontend`, `gf-qa`, `gf-plan-reviewer` |
| Standards | `.grok/docs/` | Plan quality, test accuracy, coverage, UI design |
| Fixtures | `fixtures/agentic-template-acceptance/` | Acceptance A–E |
| Metrics | `scripts/prepare_commit_metrics.py` + ledger | Every-commit VERSION + tokens |

**Does not install:** TaskBoard product sample, template plan history, or the Claude `.claude/` tree.

---

## 2. Prerequisites

- **Grok / Grok Build** (or host that loads `AGENTS.md` + `.grok/`)
- **Git** for full protocol (worktrees, `/review` local mode)
- **Python 3.11+** for the installer and (in this template repo) TaskBoard tests
- Host skills when available: `/implement`, `/review`, `/check-work` (bundled; not vendored). If missing, protocol records `HOST_SKILLS=PARTIAL` and must not silent-skip — see post-change skill.

---

## 3. Install in 5 minutes

From this **template** repo root into a target project:

```bash
python scripts/install_agentic_team.py C:\path\to\project --dry-run
python scripts/install_agentic_team.py C:\path\to\project --write-handoff --verify
```

| Flag | Effect |
|------|--------|
| `--dry-run` | Print actions only |
| `--force` | Overwrite diverged template files (timestamped backup) |
| `--write-handoff` | Write `docs/plans/agentic-team-install-handoff.md` |
| `--verify` | Check required tree; optional `grok inspect` |
| `--no-scan` | Leave Project Test Commands as TODO |

Also installs metrics scripts + pre-commit hook. Divergent existing hooks are **not** overwritten unless install uses `--force` (creates `pre-commit.bak.<timestamp>` first).

Optional skill: `/install-agentic-team` (same script).

---

## 4. Confirm it works

1. Target has `.grok/skills/post-change-accuracy-protocol/SKILL.md` and root `AGENTS.md`.  
2. Project Test Commands are REAL, NONE, or TODO+waiver (no silent forever TODO).  
3. Optional Fixture A: copy `fixtures/agentic-template-acceptance/bad-plan.md` → `docs/plans/acceptance-bad-plan.md`, run `/plan-review-loop` → must **not** Approve.  
4. If host has `grok inspect`, confirm project skills appear. Missing `/review` or `/check-work` → treat protocol as `HOST_SKILLS=PARTIAL`.

---

## 5. Your first task

1. Plan (Plan Mode / durable `docs/plans/<name>.md`).  
2. `/plan-review-loop` (max 2 passes).  
3. `/implement` or spawn `gf-backend` / `gf-frontend` with **prepended** instruction files.  
4. `/post-change-accuracy-protocol`.  
5. Commit with `python scripts/prepare_commit_metrics.py --model … --input N --output M` (or `--unmeasured`).

---

## 6. Commands and skills

### Project skills (this template)

| Skill | When |
|-------|------|
| `/plan-review-loop` | Before implement; hard gates 1–8 |
| `/targeted-unit-test-loop` | After code change; accuracy + coverage + lint |
| `/regression-test-loop` | Before merge |
| `/post-change-accuracy-protocol` | Full done bar after non-trivial code change |
| `/parallel-fullstack-feature` | Contract-first parallel BE/FE |
| `/install-agentic-team` | Install into another repo |

### Host / bundled (expected)

| Skill | When |
|-------|------|
| `/implement` | Non-trivial coding |
| `/review` | Diff review (de-dupe may skip only if bugs=0 **and** gaps=0) |
| `/check-work` | Session adequacy VERDICT |
| `security-auditor` | Auth/secrets/payments/untrusted input |

Lead may **re-enact** project `SKILL.md` files when slash UI is unavailable.

---

## 7. Accuracy pipeline

```
Plan → plan-review-loop (max 2)
  → implement
  → post-change-accuracy-protocol (max 3 cycles)
       1. targeted unit loop (max 3; WAITING_ON_PRODUCT pauses budget)
       2. /review or de-dupe + conditional security
       3. regression loop
       4. UI verification (if UI) + UI Verification Report
       5. /check-work
  → merge only if gates pass or durable waiver
  → prepare_commit_metrics every commit
```

Gates: tests, coverage ≥80% (or waiver / honest UNMEASURED), test accuracy, review, lint, UI when applicable. Details: `AGENTS.md` and `.grok/rules/accuracy-coverage.md`.

---

## 8. Personas and spawn

| Persona | Use |
|---------|-----|
| `gf-backend` | Backend implementation |
| `gf-frontend` | Frontend (+ UI design standards) |
| `gf-qa` | Tests, coverage, accuracy |
| `gf-plan-reviewer` | Plan critique |

**Always:** Lead-only spawn; prepend full `.grok/personas/instructions/<name>.md`; set `capability_mode` explicitly; tags like `[gf-qa]` are **UI labels only**. See `.grok/rules/spawn.md`.

---

## 9. Metrics and commits

Every git commit must bump `VERSION` and append `docs/metrics/token-ledger.md`:

```bash
python scripts/prepare_commit_metrics.py --model grok-build --input N --output M --note "..."
# or
python scripts/prepare_commit_metrics.py --unmeasured --note "host did not report usage"
```

Never invent token counts. Install hook: `python scripts/install_git_hooks.py`.

---

## 10. Acceptance fixtures

See `fixtures/agentic-template-acceptance/README.md` (A bad plan, B seeded bug, C coverage, D accuracy, E UI).

---

## 11. Troubleshooting

| Symptom | Check |
|---------|--------|
| Gates always NO-GO | Project Test Commands still TODO without waiver |
| Spawn ignores persona rules | Instruction file not prepended (tags alone do nothing) |
| Protocol incomplete | `HOST_SKILLS=PARTIAL` — run thin review / degraded check-work; do not silent-skip |
| Hook overwrote existing pre-commit | Restored from `pre-commit.bak.*`; re-install with backup-aware script |
| Wrong stack docs | Prefer this guide + `AGENTS.md` over Claude-only sections |

---

## Quick reference

| Goal | Action |
|------|--------|
| Install | `python scripts/install_agentic_team.py <target> --write-handoff --verify` |
| Critique plan | `/plan-review-loop` |
| After code change | `/post-change-accuracy-protocol` |
| Commit metrics | `prepare_commit_metrics.py` |
| Lead policy | `AGENTS.md` |
