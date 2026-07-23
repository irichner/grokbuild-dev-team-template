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
| Skills | `.grok/skills/*/SKILL.md` | **`/plan`** + **`/implement`** (agent owners), install; deprecated stubs redirect |
| Personas | `.grok/personas/instructions/` | Owned by `/plan` or `/implement` — see spawn table below |
| Standards | `.grok/docs/` | Plan quality, test accuracy, coverage, UI design |
| Fixtures | `fixtures/agentic-template-acceptance/` | Acceptance A–E |
| Metrics | `scripts/prepare_commit_metrics.py` + ledger | Every-commit VERSION + tokens |

**Does not install:** TaskBoard product sample, template plan history, or the Claude `.claude/` tree.

---

## 2. Prerequisites

- **Grok / Grok Build** (or host that loads `AGENTS.md` + `.grok/`)
- **Git** for full protocol (worktrees, `/review` local mode)
- **Python 3.11+** for the installer and (in this template repo) TaskBoard tests
- Project skills: **`/plan`** and **`/implement`** (template-authoritative agent owners). Host skills used *inside* `/implement`: `/review`, `/check-work` (assumed); optional `security-auditor`, `/code-review`, `/cold-review` (only if `grok inspect` lists it). If host review/check-work missing → `HOST_SKILLS=PARTIAL` + non-silent fallback (`gf-reviewer`); see [Pure-Grok agent map](FEATURES.md#pure-grok-agent-map).

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

1. Target has `.grok/skills/plan/SKILL.md`, `.grok/skills/implement/SKILL.md`, and root `AGENTS.md`.  
2. Project Test Commands are REAL, NONE, or TODO+waiver (no silent forever TODO).  
3. Optional Fixture A: copy `fixtures/agentic-template-acceptance/bad-plan.md` → `docs/plans/acceptance-bad-plan.md`, run **`/plan`** → critique must **not** Approve.  
4. If host has `grok inspect`, confirm project skills appear. Missing host `/review` or `/check-work` → treat `/implement` protocol as `HOST_SKILLS=PARTIAL`.

---

## 5. Your first task

1. **`/plan`** — durable `docs/plans/<name>.md` + critique with `gf-plan-reviewer` (max 2 passes). Copy session Plan Mode `plan.md` into `docs/plans/` if needed.  
2. **`/implement`** — only after Approve or durable waiver: code change + accuracy protocol (targeted → review → regression → UI → check-work).  
3. Commit with `python scripts/prepare_commit_metrics.py --model … --input N --output M` (or `--unmeasured`).

---

## 6. Commands and skills

### Project skills (this template)

| Skill | When |
|-------|------|
| **`/plan`** | Explore, durable plan, plan critique (hard gates 1–8) |
| **`/implement`** | Code change + full accuracy protocol (all implement-phase agents) |
| `/install-agentic-team` | Install into another repo |

**Deprecated aliases** (redirect stubs only): `/plan-review-loop`, `/targeted-unit-test-loop`, `/regression-test-loop`, `/post-change-accuracy-protocol`, `/parallel-fullstack-feature` → open `/plan` or `/implement` instead.

### Host / bundled (used inside `/implement`; not vendored)

| Skill | Status | When |
|-------|--------|------|
| `/review` | **Assumed** | Diff review (de-dupe may skip only if bugs=0 **and** gaps=0) |
| `/check-work` | **Assumed** | Session adequacy VERDICT |
| `security-auditor` | **Optional** (conditional) | Auth/secrets/payments/untrusted input |
| `/code-review` | **Optional** | Stricter maintainability if host lists it |
| `/cold-review` | **Optional** | Only if `grok inspect` lists it (not shipped); from `/plan` |

Missing assumed host skills → `HOST_SKILLS=PARTIAL`: thin local review or spawn **`gf-reviewer`**; degraded check-work with recorded note. Never silent-skip. Full map: `docs/FEATURES.md` (Pure-Grok agent map).

Lead may **re-enact** project `SKILL.md` files when slash UI is unavailable.

**Claude `.claude/agents/`** are **not** installed by `install_agentic_team.py`. When Grok is Lead they are optional helpers only and must not override `AGENTS.md`.

---

## 7. Accuracy pipeline

```
/plan (explore + durable MD + critique, max 2)
  → /implement
       Phase 1: feature | bugfix | parallel-fullstack
       Phase 2 accuracy (max 3 cycles):
         1. targeted unit (gf-qa; max 3; WAITING_ON_PRODUCT pauses budget)
         2. /review or gf-reviewer or de-dupe + conditional security
         3. regression (gf-qa)
         4. UI verification (if UI)
         5. /check-work
  → merge only if gates pass or durable waiver
  → prepare_commit_metrics every commit
```

Gates: tests, coverage ≥80% (or waiver / honest UNMEASURED), test accuracy, review, lint, UI when applicable. Details: `AGENTS.md` and `.grok/rules/accuracy-coverage.md`.

**Escape hatches:** docs/typo trivial path; separate **spike/prototype mode** only with explicit user approval + time box + durable note (`docs/plans/` or `docs/waivers/spike-<name>.md`). Spike work is not production merge-ready until normal gates re-enter. See `AGENTS.md`.

---

## 8. Personas and spawn

| Persona | Owned by | Use | Typical `capability_mode` |
|---------|----------|-----|---------------------------|
| `gf-plan-reviewer` | `/plan` | Plan critique | `read-only` |
| `gf-backend` | `/implement` | Backend implementation | `all` |
| `gf-frontend` | `/implement` | Frontend (+ UI design standards) | `all` |
| `gf-qa` | `/implement` | Tests, coverage, accuracy | `execute` / `all` |
| `gf-reviewer` | `/implement` | Thin local code review (`HOST_SKILLS=PARTIAL`) | `read-only` |
| `gf-debugger` | `/implement` | Root-cause debug + regression test | `all` |

**Always:** Lead-only spawn **while re-enacting `/plan` or `/implement`**; prepend full `.grok/personas/instructions/<name>.md`; set `capability_mode` explicitly; tags like `[gf-qa]` are **UI labels only**. See `.grok/rules/spawn.md`.

Do **not** redefine bundled names `reviewer`, `implementer`, `test-writer`, `security-auditor` — use the `gf-*` project names above.

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
| Protocol incomplete | `HOST_SKILLS=PARTIAL` — thin local review or spawn `gf-reviewer` / degraded check-work; do not silent-skip |
| Hook overwrote existing pre-commit | Restored from `pre-commit.bak.*`; re-install with backup-aware script |
| Wrong stack docs | Prefer this guide + `AGENTS.md` over Claude-only sections |

---

## Quick reference

| Goal | Action |
|------|--------|
| Install | `python scripts/install_agentic_team.py <target> --write-handoff --verify` |
| Plan + critique | `/plan` |
| Implement + accuracy | `/implement` |
| Commit metrics | `prepare_commit_metrics.py` |
| Lead policy | `AGENTS.md` |
