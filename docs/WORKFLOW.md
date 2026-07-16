# The Accuracy / Verification Loop (GrokForge)

This template is built around one idea: **code is not done when it's written — it's done when it's verified.**  
Primary orchestration is **Grok Lead** via `AGENTS.md` and `.grok/` skills.

> **Optional sibling:** Claude Code surfaces (`.claude/`, Stop hooks, `/ship`) may exist in this monorepo for dual-stack development. They are **not** installed by `install_agentic_team.py`. Grok sessions should follow this document and `AGENTS.md`.

```
   ┌──────────┐   ┌────────┐   ┌────────────────┐
   │ EXPLORE  │ → │  PLAN  │ → │ PLAN-REVIEW    │
   └──────────┘   └────────┘   │ (max 2 passes) │
        ▲                      └───────┬────────┘
        │                              │
        │                              ▼
   ┌────┴─────┐   ┌──────────┐   ┌───────────┐
   │  COMMIT  │ ← │ PROTOCOL │ ← │ IMPLEMENT  │
   │ + metrics│   │ (max 3)  │   └───────────┘
   └──────────┘   └──────────┘
```

---

## The phases

### 1. Explore

Map relevant code, contracts, and conventions **before** changing. Use read tools or an explore-style subagent.  
**Exit:** you can name files you'll touch and contracts you must not break.

### 2. Plan

Concrete, testable plan with hard gates (see `.grok/docs/plan-quality-standards.md`): goal, non-goals, risks, ordered steps + verification, testing strategy with edge/negative cases, failure modes, observable verification, UI design when UI touched.  
Prefer durable `docs/plans/<name>.md`.

### 3. Plan critique (`/plan-review-loop`)

Default path: spawn `gf-plan-reviewer` (read-only); **Lead** writes `docs/plans/*.review.md`. Max **2** passes; plan must change between passes. Optional `/cold-review` only if listed in `grok inspect` (external; not shipped).  
**Exit:** Approve + user OK, or residual hard-gate failures + durable waiver.

### 4. Implement

Smallest correct diff via `/implement` or `gf-backend` / `gf-frontend` with **prepended** instructions. Ready:yes only after green targeted tests when shell available. Green exit is necessary, not sufficient — Lead still runs accuracy-aware QA.

### 5. Post-change accuracy protocol

`/post-change-accuracy-protocol` when executable code, tests, SQL, or runtime config changed:

1. **Targeted unit loop** — tests + lint + coverage ladder + test accuracy (max 3 runs; product bugs → `WAITING_ON_PRODUCT`, do not burn budget)  
2. **`/review`** — skip only if implement left **bugs=0 and gaps=0** and tree matches; security pass when auth/secrets/payments/untrusted input  
3. **Regression loop**  
4. **UI verification** when UI changed (UI Verification Report)  
5. **`/check-work`** — session adequacy (`VERDICT: PASS`); not a substitute for QA GO  

Max **3** full protocol cycles. Host skills missing → `HOST_SKILLS=PARTIAL` with explicit fallback (never silent skip).

### 6. Merge

Only when gates pass or durable `docs/waivers/` covers residual risk.

### 7. Commit + metrics

Every commit: `prepare_commit_metrics.py` bumps `VERSION` and appends the token ledger. Never invent counts.

---

## How surfaces cooperate

| Surface | Role |
|---------|------|
| `AGENTS.md` | Standing Lead policy + Project Test Commands |
| `.grok/rules/*` | Auto-loaded spawn + accuracy gates |
| `.grok/skills/*` | Operator/Lead procedures (slash or re-enact) |
| Personas | Prepend instruction files; tags are UI-only |
| Host `/implement`, `/review`, `/check-work` | Bundled Grok skills (probe; degrade if missing) |
| Pre-commit hook | Enforces VERSION + ledger on commit |

**Key insight:** Policy is advisory unless Lead runs the protocol and the metrics hook fires. There is no Claude-style Stop hook on the pure Grok path — discipline is intentional.

---

## Loop caps

| Loop | Max |
|------|-----|
| Plan review | 2 |
| Targeted unit | 3 full suite runs (after material fixes) |
| Regression | 3 full phase runs |
| Post-change protocol | 3 full cycles |

After max: escalate with evidence. **Do not claim done.**

---

## Trivial escape

Docs/comment-only or pure typo: skip plan + full regression. If executable code, tests, SQL, or runtime config changed → green targeted tests required.
