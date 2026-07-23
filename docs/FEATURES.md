# Feature Map — GrokForge Agentic Dev Team

Surfaces this template installs and uses for accuracy-first agentic development.  
**Primary stack: Grok.** Installer: `scripts/install_agentic_team.py`.

> **Optional sibling:** Claude Code (`.claude/`, hooks, `/ship`) may be present in the monorepo for dual-stack work. It is **not** part of the Grok install package. Prefer `AGENTS.md` + this map when Grok is Lead.

---

## Surfaces

### 1. Project memory — `AGENTS.md`

Loaded as Lead policy: pipeline (`/plan` → `/implement`), implement/review de-dupe, severity map, loop caps, personas, secrets/waivers, **Project Test Commands** (REAL / NONE / TODO+waiver).

Companion product rules (e.g. `CLAUDE.md`) may remain in the target and are referenced, not overwritten, by the installer.

### 2. Auto-loaded rules — `.grok/rules/`

| File | Purpose |
|------|---------|
| `accuracy-coverage.md` | Merge/done gates, severity, max cycles |
| `spawn.md` | Lead-only spawn, skill ownership, prepend, capability_mode, tags UI-only |

### 3. Personas — `.grok/personas/`

| Name | Owned by skill | Instructions | Typical capability |
|------|----------------|--------------|--------------------|
| `gf-plan-reviewer` | `/plan` | `instructions/gf-plan-reviewer.md` | `read-only` |
| `gf-backend` | `/implement` | `instructions/gf-backend.md` | `all` |
| `gf-frontend` | `/implement` | `instructions/gf-frontend.md` | `all` (+ UI standards) |
| `gf-qa` | `/implement` | `instructions/gf-qa.md` | `execute` / `all` |
| `gf-reviewer` | `/implement` | `instructions/gf-reviewer.md` | `read-only` (thin local review) |
| `gf-debugger` | `/implement` | `instructions/gf-debugger.md` | `all` (reproduce + confirm) |

Roles under `.grok/roles/*.toml` are **catalog metadata only** — not spawn binding. Always prepend instruction files.  
Do **not** redefine bundled names `reviewer`, `implementer`, `test-writer`, `security-auditor`.  
**Spawn only while re-enacting `/plan` or `/implement`.**

### 4. Project skills — `.grok/skills/`

| Skill | Purpose |
|-------|---------|
| **`plan`** | **Primary.** Explore + durable plan + `gf-plan-reviewer` critique (max 2) |
| **`implement`** | **Primary.** Code change modes + full accuracy protocol through merge readiness |
| `install-agentic-team` | Runs installer script (meta; not an SDLC agent owner) |

**Deprecated stubs** (redirect only; not dual sources of truth):

| Stub | Redirects to |
|------|----------------|
| `plan-review-loop` | `/plan` Phase C |
| `targeted-unit-test-loop` | `/implement` targeted |
| `regression-test-loop` | `/implement` regression |
| `post-change-accuracy-protocol` | `/implement` Phase 2 accuracy |
| `parallel-fullstack-feature` | `/implement` mode parallel-fullstack |

All use `disable-model-invocation: true` (slash / Lead re-enactment).

### 5. Standards docs — `.grok/docs/`

- `plan-quality-standards.md` — hard gates 1–8  
- `test-accuracy-standards.md` — circular/happy-path blockers  
- `coverage-policy.md` — ≥80%, vacuous UNMEASURED, compare-branch  
- `ui-design-standards.md` — design blockers → gap  
- `privacy-safety.md` — secrets guidance  

### 6. Host / bundled skills (not vendored)

See [Pure-Grok agent map](#pure-grok-agent-map). Project `/plan` and `/implement` are template-authoritative; host skills fill review/security/check-work inside `/implement`.

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

## Pure-Grok agent map

Minimal map when **Grok is Lead** and only this install is present. Claude `.claude/agents/` are **not** installed by `install_agentic_team.py` and are not required for this map.

| Layer | What | SDLC role |
|-------|------|-----------|
| **Lead** | Root `AGENTS.md` | Orchestration, spawn, gates, merge decision |
| **`/plan`** | Project skill | Durable plan + `gf-plan-reviewer` |
| **`/implement`** | Project skill | All implement/QA/review/debug agents + accuracy protocol |
| **`gf-plan-reviewer`** | Persona under `/plan` | Plan hard-gate critique |
| **`gf-backend` / `gf-frontend`** | Personas under `/implement` | Implement product code + tests |
| **`gf-qa`** | Persona under `/implement` | Targeted/regression, coverage, test accuracy |
| **`gf-reviewer`** | Persona under `/implement` | Thin local code review when host `/review` missing |
| **`gf-debugger`** | Persona under `/implement` | Root-cause: reproduce → isolate → fix + regression test |
| **Host skills** | Not vendored | `/review`, `/check-work`, optional security inside `/implement` |

### Host skills: assumed vs optional (used inside `/implement`)

| Skill | Status | Notes |
|-------|--------|-------|
| `/review` | **Assumed** for accuracy review step | De-dupe may skip only when clean implement (bugs=0, gaps=0) |
| `/check-work` | **Assumed** for session VERDICT | Session adequacy; not a substitute for QA GO |
| `security-auditor` | **Optional** (conditional) | When auth/secrets/payments/untrusted input |
| `/code-review` | **Optional** | Stricter maintainability if host lists it |
| `/cold-review` | **Optional** | Only if `grok inspect` lists it; used from `/plan` |

### When host skills are missing (`HOST_SKILLS=PARTIAL`)

| Missing | Required fallback (never silent-skip) |
|---------|----------------------------------------|
| `/review` | Thin local review checklist **or** spawn **`gf-reviewer`** (read-only); open bug/gap still blocks; or NO-GO for merge claims |
| `/check-work` | Lead self-verify against protocol exit criteria; record `check-work: DEGRADED`; merge needs explicit accept or treat incomplete |

Full host present → record `HOST_SKILLS=OK`.

### Not installed by the Grok installer

| Surface | Notes |
|---------|--------|
| Claude `.claude/agents/` | Optional monorepo helpers only; never override Grok Lead policy when both load |
| Host review/check-work/security | Bundled by host, not copied into the target tree |
| TaskBoard product sample | Template-repo only |

---

## Extension points

1. Fill Project Test Commands (or durable waivers) for target languages.  
2. Add project skills under `.grok/skills/<name>/SKILL.md` via `/create-skill` (prefer nesting under `/plan` or `/implement` ownership if they spawn `gf-*`).  
3. Add durable waivers under `docs/waivers/`.  
4. Optional: keep Claude stack for dual tooling; do not let it override Grok Lead policy when both load.

---

## What is intentionally not automated

- Persona auto-bind from tags (platform cannot; prepend required)  
- Stop-hook equivalent for Grok (protocol + metrics hook instead)  
- Full reimplementation of host multi-effort implement memory loop  
