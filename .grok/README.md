# GrokForge project template (v1.7)

Grok-native paths only. Optimized for **accuracy + coverage + UI design quality** with explicit revise/retry loops.

## What loads automatically

| Path | Loaded by Grok? |
|------|-----------------|
| Root `AGENTS.md` | Yes (project rules) |
| `.grok/rules/*.md` | Yes (incl. spawn checklist + accuracy gates) |
| `.grok/skills/*/SKILL.md` | Yes (skills / slash commands) |
| `.grok/personas/*.toml` | Yes (persona **catalog only**; spawn needs instruction **prepend**) |
| `.grok/roles/*.toml` | Catalog defaults only — **not spawn binding**; skills still set `capability_mode` + prepend |
| `.grok/docs/*`, `.grok/workflows/*` | **No** — reference only (mandatory `read_file` for reviewers/QA/frontend) |

## Two primary skills (agent owners)

| Skill | Path | Owns agents |
|-------|------|-------------|
| **`/plan`** | `.grok/skills/plan/SKILL.md` | Lead (author) + `gf-plan-reviewer` |
| **`/implement`** | `.grok/skills/implement/SKILL.md` | `gf-backend`, `gf-frontend`, `gf-qa`, `gf-reviewer`, `gf-debugger` |
| `/install-agentic-team` | `.grok/skills/install-agentic-team/SKILL.md` | Meta-install only (not an SDLC agent owner) |

**Spawn rule:** `gf-*` personas only while re-enacting `/plan` or `/implement` (see `.grok/rules/spawn.md`).

### Deprecated skill aliases (stubs only)

`plan-review-loop`, `targeted-unit-test-loop`, `regression-test-loop`, `post-change-accuracy-protocol`, `parallel-fullstack-feature` — redirect to `/plan` or `/implement`. Do not treat stubs as full procedures.

## Personas (project catalog)

| Persona | Owned by | Role | Typical capability |
|---------|----------|------|--------------------|
| `gf-plan-reviewer` | `/plan` | Plan hard-gate critique | `read-only` |
| `gf-backend` | `/implement` | Backend implementer | `all` |
| `gf-frontend` | `/implement` | Frontend implementer + UI design bar | `all` |
| `gf-qa` | `/implement` | Tests, coverage, accuracy | `execute` / `all` |
| `gf-reviewer` | `/implement` | Thin local code review (host `/review` fallback) | `read-only` |
| `gf-debugger` | `/implement` | Root-cause debug + regression test | `all` |

Spawn requires **prepend** of instruction files + explicit `capability_mode`. Tags are UI-only. Do not shadow bundled names `reviewer` / `implementer` / `test-writer` / `security-auditor`.

## Host skills (probe; not vendored)

Project `/plan` and `/implement` are **template-authoritative** for GrokForge work. Host may also expose skills with similar names; for this template, re-enact **project** `.grok/skills/plan` and `.grok/skills/implement`.

| Host skill | Status | Role under `/implement` |
|------------|--------|-------------------------|
| `/review` | Assumed for review step | Prefer over `gf-reviewer` when present |
| `/check-work` | Assumed for final verify | Session VERDICT |
| `security-auditor` | Optional conditional | Auth/secrets/payments/untrusted input |
| `/code-review` | Optional | Stricter maintainability |
| `/cold-review` | Optional | Only if `grok inspect` lists it; plan-phase adversarial |

Missing `/review` or `/check-work` → `HOST_SKILLS=PARTIAL` + non-silent fallback (never silent-skip).

## Accuracy loops

| Phase | Skill | Cap |
|-------|-------|-----|
| Plan critique | `/plan` Phase C | 2 passes |
| Targeted unit | `/implement` accuracy | 3 full suite runs |
| Regression | `/implement` accuracy | 3 full phase runs |
| Full accuracy protocol | `/implement` Phase 2 | 3 cycles |

## Metrics (every commit)

- `VERSION` patch-bumps on each commit  
- Token / model usage: `docs/metrics/token-ledger.md` via `scripts/prepare_commit_metrics.py`  
- Git hook: `python scripts/install_git_hooks.py`

## Git required for full protocol

`/review` local mode, worktrees, and git-diff coverage need a git repo. Without git: degraded protocol.

## Deprecated

`.grokbuild/` (v1.1) — not discovered.
