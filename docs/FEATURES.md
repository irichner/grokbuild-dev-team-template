# Feature Map — GrokForge Agentic Dev Team

Surfaces this template installs and uses for accuracy-first agentic development.  
**Primary stack: Grok.** Installer: `scripts/install_agentic_team.py`.

> **Optional sibling:** Claude Code (`.claude/`, hooks, `/ship`) may be present in the monorepo for dual-stack work. It is **not** part of the Grok install package. Prefer `AGENTS.md` + this map when Grok is Lead.

---

## Surfaces

### 1. Project memory — `AGENTS.md`

Loaded as Lead policy: pipeline, implement/review de-dupe, severity map, loop caps, personas, secrets/waivers, **Project Test Commands** (REAL / NONE / TODO+waiver).

Companion product rules (e.g. `CLAUDE.md`) may remain in the target and are referenced, not overwritten, by the installer.

### 2. Auto-loaded rules — `.grok/rules/`

| File | Purpose |
|------|---------|
| `accuracy-coverage.md` | Merge/done gates, severity, max cycles |
| `spawn.md` | Lead-only spawn, prepend, capability_mode, tags UI-only |

### 3. Personas — `.grok/personas/`

| Name | Instructions | Typical capability |
|------|--------------|--------------------|
| `gf-backend` | `instructions/gf-backend.md` | `all` |
| `gf-frontend` | `instructions/gf-frontend.md` | `all` (+ UI standards) |
| `gf-qa` | `instructions/gf-qa.md` | `execute` / `all` |
| `gf-plan-reviewer` | `instructions/gf-plan-reviewer.md` | `read-only` |

Roles under `.grok/roles/*.toml` are **catalog metadata only** — not spawn binding. Always prepend instruction files.

### 4. Project skills — `.grok/skills/`

| Skill | Purpose |
|-------|---------|
| `plan-review-loop` | Default plan critique; max 2 passes; Lead writes review files |
| `targeted-unit-test-loop` | Changed-code tests + lint + coverage + accuracy |
| `regression-test-loop` | Quick/Extended phase before merge |
| `post-change-accuracy-protocol` | Full done bar; host skill probe; UI report |
| `parallel-fullstack-feature` | Contract-first parallel BE/FE worktrees |
| `install-agentic-team` | Runs installer script |

All use `disable-model-invocation: true` (slash / Lead re-enactment).

### 5. Standards docs — `.grok/docs/`

- `plan-quality-standards.md` — hard gates 1–8  
- `test-accuracy-standards.md` — circular/happy-path blockers  
- `coverage-policy.md` — ≥80%, vacuous UNMEASURED, compare-branch  
- `ui-design-standards.md` — design blockers → gap  
- `privacy-safety.md` — secrets guidance  

### 6. Host / bundled skills (not vendored)

Expected from Grok host: `/implement`, `/review`, `/check-work`, often `security-auditor`.  
Protocol records `HOST_SKILLS=OK` or `PARTIAL` with non-silent fallback.

### 7. Metrics

- `VERSION` patch-bumped every commit  
- `docs/metrics/token-ledger.md`  
- `scripts/prepare_commit_metrics.py`, `record_token_usage.py`, `install_git_hooks.py`  
- Feature train label: installer `TEMPLATE_VERSION` (e.g. `1.7`) vs per-commit `VERSION` (e.g. `1.7.x`) — intentional dual scheme  

### 8. Acceptance fixtures

`fixtures/agentic-template-acceptance/` — A–E (bad plan, seeded bug, coverage, accuracy, UI).

### 9. Sample product (template repo only)

TaskBoard under `src/taskboard/` + `tests/` — **not** copied by installer. Used to exercise the team in this repo.

---

## Extension points

1. Fill Project Test Commands (or durable waivers) for target languages.  
2. Add project skills under `.grok/skills/<name>/SKILL.md` via `/create-skill`.  
3. Add durable waivers under `docs/waivers/`.  
4. Optional: keep Claude stack for dual tooling; do not let it override Grok Lead policy when both load.

---

## What is intentionally not automated

- Persona auto-bind from tags (platform cannot; prepend required)  
- Stop-hook equivalent for Grok (protocol + metrics hook instead)  
- Full reimplementation of host `/implement` / `/review` / `/check-work`
