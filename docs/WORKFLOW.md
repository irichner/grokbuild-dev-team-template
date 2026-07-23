# The Accuracy / Verification Loop (GrokForge)

This template is built around one idea: **code is not done when it's written — it's done when it's verified.**  
Primary orchestration is **Grok Lead** via `AGENTS.md` and two skills: **`/plan`** and **`/implement`**.

> **Optional sibling:** Claude Code surfaces (`.claude/`, Stop hooks, `/ship`) may exist in this monorepo for dual-stack development. They are **not** installed by `install_agentic_team.py`. Grok sessions should follow this document and `AGENTS.md`.

```
   ┌──────────┐   ┌────────────────────┐
   │ EXPLORE  │ → │ /plan              │
   └──────────┘   │ author + critique  │
        ▲         │ (max 2 passes)     │
        │         └─────────┬──────────┘
        │                   │
        │                   ▼
   ┌────┴─────┐   ┌────────────────────┐
   │  COMMIT  │ ← │ /implement         │
   │ + metrics│   │ code + accuracy    │
   └──────────┘   │ (max 3 protocol)   │
                  └────────────────────┘
```

All `gf-*` agents spawn **only** under `/plan` or `/implement` (see `.grok/rules/spawn.md`).

---

## The phases

### 1–2. Plan skill (`/plan`)

**Explore** — Map relevant code, contracts, and conventions before changing.  
**Author** — Durable Markdown: `docs/plans/<name>.md`. Session Plan Mode files must be copied there. **Chat-only plans are not valid.** Hard gates: `.grok/docs/plan-quality-standards.md`.  
**Critique** — Spawn `gf-plan-reviewer` (read-only); Lead writes `docs/plans/*.review.md`. Max **2** passes; plan must change between passes. Optional `/cold-review` only if listed in `grok inspect`.  

**Exit:** Approve + user OK, or residual hard-gate failures + durable waiver.  
**Never implement from a chat-only plan.**

Full procedure: `.grok/skills/plan/SKILL.md`.

### 3–4. Implement skill (`/implement`)

**Implement** — Modes: `feature` (`gf-backend` / `gf-frontend`), `bugfix` (`gf-debugger`), or `parallel-fullstack` (worktrees + contract). Ready:yes only after green targeted tests when shell available.

**Accuracy protocol** (same skill, Phase 2) when executable code, tests, SQL, or runtime config changed:

1. **Targeted unit loop** (`gf-qa`) — tests + lint + coverage ladder + test accuracy (max 3 runs; product bugs → `WAITING_ON_PRODUCT`)  
2. **Review** — host `/review` or `gf-reviewer`; skip only if bugs=0 and gaps=0 and tree matches; security pass when auth/secrets/payments/untrusted input  
3. **Regression loop** (`gf-qa`)  
4. **UI verification** when UI changed  
5. **`/check-work`** — session adequacy (`VERDICT: PASS`); not a substitute for QA GO  

Max **3** full protocol cycles. Host skills missing → `HOST_SKILLS=PARTIAL` with explicit fallback (never silent skip).

Full procedure: `.grok/skills/implement/SKILL.md`.

### 5. Merge

Only when gates pass or durable `docs/waivers/` covers residual risk.

### 6. Commit + metrics

Every commit: `prepare_commit_metrics.py` bumps `VERSION` and appends the token ledger. Never invent counts.

---

## How surfaces cooperate

| Surface | Role |
|---------|------|
| `AGENTS.md` | Standing Lead policy + Project Test Commands |
| `.grok/rules/*` | Auto-loaded spawn + accuracy gates |
| `/plan` + `/implement` | Only first-class SDLC skills; agent owners |
| Deprecated skill stubs | Redirects only (muscle memory) |
| Personas | Prepend instruction files; tags are UI-only |
| Host `/review`, `/check-work`, `security-auditor` | Used inside `/implement` when present |
| Pre-commit hook | Enforces VERSION + ledger on commit |

**Key insight:** Policy is advisory unless Lead runs `/plan` → `/implement` and the metrics hook fires. There is no Claude-style Stop hook on the pure Grok path — discipline is intentional.

---

## Loop caps

| Loop | Max |
|------|-----|
| Plan review (`/plan`) | 2 |
| Targeted unit (`/implement`) | 3 full suite runs (after material fixes) |
| Regression (`/implement`) | 3 full phase runs |
| Accuracy protocol (`/implement`) | 3 full cycles |

After max: escalate with evidence. **Do not claim done.**

---

## Trivial escape

Docs/comment-only or pure typo: skip plan + full regression. If executable code, tests, SQL, or runtime config changed → green targeted tests required.

## Spike / prototype mode

User-approved, **time-boxed** exploratory work (explicit approval for this session/task). May skip full `/plan` critique, full `/implement` accuracy protocol, and regression Extended — **must** leave a durable note under `docs/plans/` or `docs/waivers/spike-<name>.md` listing skips and residual risk. Prefer a smoke/targeted test when code changes; never invent secrets. **Not merge-ready** until normal gates re-enter (or durable waiver). Separate from the trivial docs/typo hatch.
