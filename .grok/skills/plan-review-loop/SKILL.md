---
name: plan-review-loop
description: >
  Critique a plan before implementation using gf-plan-reviewer (or recommend /cold-review).
  Use before coding, for plan critique, or /plan-review-loop.
disable-model-invocation: true
---

# Skill: Plan Review Loop

## Prefer
If `/cold-review` appears in `grok inspect` for this workspace, prefer it for adversarial plan review. This skill is the fallback when cold-review is missing or unresolved.

## Inputs
- Plan path: prefer `docs/plans/<name>.md`. If only session plan exists, copy session `plan.md` to `docs/plans/` first (after Plan Mode allows non-plan writes, or after exiting plan mode).
- Max passes: 2

## Steps
1. Read the plan. Flag missing Testing Strategy / non-observable verification.
2. Read `.grok/personas/instructions/gf-plan-reviewer.md` and **prepend** full text to the child prompt.
3. Spawn **from Lead only**:
   - `subagent_type`: `general-purpose` with `capability_mode: read-only`, **or** `subagent_type: explore` / `plan`
   - `description`: `[gf-plan-reviewer] plan review` (UI label only)
   - Prompt = persona instructions + plan path + Review Report schema + “Do not edit product code.”
4. Apply Required Changes to the plan.
5. Optional second pass if still Request Changes.
6. Present to user; **do not implement** until user approves.
7. Residual Major Concerns require durable waiver under `docs/waivers/` if user accepts without full fix.

## Exit
Approve, or durable waiver for residual Major Concerns.
