---
name: parallel-fullstack-feature
description: >
  Parallel backend/frontend in worktrees with contract-first integration and
  post-change accuracy protocol. Use for full-stack features or /parallel-fullstack-feature.
disable-model-invocation: true
---

# Skill: Parallel Full-Stack Feature

## Prerequisites
- Git repository required. If no git: stop and recommend sequential `/implement` or single-tree work.

## Contract artifact (required before parallel work)
Write `docs/plans/<feature>-contract.md` (or section in the plan) containing:
- Endpoints / events / shared types
- Owner for shared types (backend | frontend | package path)
- Error and auth expectations
- Freeze stamp (date + “no divergent fields without re-freeze”)

## Steps
1. Plan Mode + plan critique (`/cold-review` or `/plan-review-loop`). Freeze contract artifact.
2. Prefer `/implement` for sequential high-rigor work when parallelism is unnecessary.
3. If parallel: spawn `gf-backend` and `gf-frontend` with `isolation: worktree`, **prepend** persona instructions, tags `[gf-backend]` / `[gf-frontend]`, capability_mode `all`.
4. Integrate via Grok **worktree apply** (or explicit merge); resolve conflicts; re-check contract artifact for drift.
5. Run **`/post-change-accuracy-protocol`** on integrated tree.
6. Lead-only spawns throughout (depth 1).

## Failure
Divergent contracts (fields/types not in freeze doc) → stop and re-freeze. Partial integration → NO-GO until protocol passes.
