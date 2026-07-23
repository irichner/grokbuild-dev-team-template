---
name: plan
description: >
  Author a durable plan under docs/plans/ and critique it with gf-plan-reviewer
  (hard gates 1–8, max 2 revise→re-review passes). Primary plan entry point for
  this template. Owns all plan-phase agents. Use before coding, for plan work,
  or /plan. Do not implement product code from this skill.
disable-model-invocation: true
---

# Skill: Plan (authoritative)

Lead may **re-enact this SKILL.md** when slash UI is unavailable; slash is preferred operator entry.

**This is the only first-class plan skill.** Deprecated alias: `/plan-review-loop` (redirect stub only).

## Agents owned (plan phase only)

| Agent | Role | capability_mode | When |
|-------|------|-----------------|------|
| **Lead** (inline) | Explore + write durable plan | n/a | Always |
| **`gf-plan-reviewer`** | Hard-gate plan critique | `read-only` | Phase C |
| Optional host **`/cold-review`** | Adversarial critique | per host | Only if `grok inspect` lists it |

**Do not spawn** implement/QA/reviewer/debugger personas from this skill.  
**Do not implement** product code. Hand off to **`/implement`** only after exit criteria.

## Relation to Plan Mode

Host Plan Mode may draft a session plan under `~/.grok/sessions/.../plan.md`.  
This skill still **owns**:

1. Durable artifact at `docs/plans/<name>.md`  
2. Hard-gate content  
3. Critique loop with `gf-plan-reviewer`  

Session-only or chat-only text is **not** a review artifact.

---

## Phase A — Explore

1. Map relevant code, contracts, tests, and conventions.  
2. Use read tools; optional explore-style read-only subagent for wide unfamiliar territory.  
3. Do **not** edit product code.  
4. **Exit when:** you can name files/contracts in scope and what must not break.

---

## Phase B — Author durable plan

1. Write or update **`docs/plans/<name>.md`**.  
2. If only a session plan exists: **copy/sync** it to `docs/plans/` first (after Plan Mode allows non-plan writes, or after exiting plan mode).  
3. **Stop** if the only plan is chat text — durable `.md` is required.  
4. Plan content must satisfy hard gates (Lead self-check before critique). Standards: `.grok/docs/plan-quality-standards.md`.

### Hard gates (reject weak plans)

1. Goal + measurable acceptance criteria  
2. Non-goals  
3. Risk / blast radius  
4. Ordered implementation steps with **verification per step**  
5. Testing strategy (unit + edge/negative + coverage expectation or NO COVERAGE TOOL + waiver path)  
6. Failure modes  
7. Observable verification (reject “works correctly” / “should work”)  
8. UI/UX design when the plan touches UI — state inventory, design reference, a11y, falsifiable design criteria per `.grok/docs/ui-design-standards.md` (N/A counts as pass when no UI)

---

## Phase C — Critique (max 2 passes)

Optional: if `/cold-review` appears in `grok inspect`, you may use it for adversarial review — still apply the **same hard gates** and **same** loop policy (max **2** passes). Cold-review is **not** required and is **not** installed by `install_agentic_team.py`.

### Loop (mandatory)

```
pass = 1
while pass <= 2:
  1. Read plan + .grok/docs/plan-quality-standards.md
     (UI plans: also .grok/docs/ui-design-standards.md)
  2. Prepend full .grok/personas/instructions/gf-plan-reviewer.md to child prompt
  3. Spawn from Lead only:
       - subagent_type: general-purpose + capability_mode: read-only
         OR subagent_type: explore | plan
       - description: [gf-plan-reviewer] plan review pass N  (UI label only)
       - Prompt = persona + plan path + standards path + Review Report schema
         + “Return the full Review Report in your message. Do not edit product code.
            Do not write files (read-only). Lead will persist the report.”
  4. Lead writes report → docs/plans/<name>.review.md  (pass 2 → .review-2.md)
     from the child’s returned report body
  5. If Overall == Approve: break
  6. If pass == 2:
       escalate — max reviews used; optional plan edits may continue outside this loop
       break
  7. Else (pass 1 and Request Changes | Major Concerns):
       - Lead/author applies Required Changes (material edits required)
       - Do not re-run review on an unchanged plan
       - pass += 1
if still not Approve:
  do not implement unless user accepts residual hard-gate failures
  with durable waiver under docs/waivers/
```

**Material plan edits after the last review pass** require a **new review pass** or a durable waiver — do not implement on an unreviewed material delta.

### Steps (detail)

1. Confirm durable plan path under `docs/plans/`.  
2. Run loop above (max 2 passes).  
3. Present final Review Report + revised plan to user.  
4. **Do not call `/implement`** until user approves **or** durable waiver covers residual hard-gate failures.  
5. Record residual risks / waiver paths in the handoff to `/implement`.

---

## Exit criteria

| Outcome | Condition |
|---------|-----------|
| **Ready to implement** | Overall Approve (pass 1 or 2) **and** user approval → proceed to `/implement` |
| **Blocked** | Hard gates still failing after pass 2; no implement |
| **Waived residual** | User accepts residual hard-gate failures **and** durable `docs/waivers/<name>.md` exists |

Max **2** review passes; between pass 1 and pass 2 the plan **must** change. After pass 2 failure, escalate (no automatic third review). No silent Approve of weak plans.

## Trivial / spike escapes

- **Trivial** (docs/comment-only or pure typo): may skip this skill entirely.  
- **Spike** (user-approved, time-boxed): may skip full critique — durable note under `docs/plans/` or `docs/waivers/spike-<name>.md` required. Not production merge-ready.
