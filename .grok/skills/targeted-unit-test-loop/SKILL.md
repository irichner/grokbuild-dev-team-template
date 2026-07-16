---
name: targeted-unit-test-loop
description: >
  Fast unit tests on changed code with coverage delta, lint/typecheck gate,
  test-accuracy checks, and fix→re-test loop (max 3 full suite runs).
  Use after implementation or /targeted-unit-test-loop.
disable-model-invocation: true
---

# Skill: Targeted Unit Test Loop

Lead may **re-enact this SKILL.md** when slash UI is unavailable; slash is preferred operator entry.

## Spawn rules

- Orchestrated by **Lead** (not nested under another subagent).
- Spawn with `capability_mode: execute` or `all` (shell required) — set explicitly.
- Prepend full `.grok/personas/instructions/gf-qa.md`; `description`: `[gf-qa] targeted tests`.

## Prerequisites

- Prefer git for changed-file list. If no git: require user-supplied path list or fail with NO-GO (cannot define “changed”).
- QA must `read_file` `.grok/docs/test-accuracy-standards.md` before accuracy GO/NO-GO.

## Steps

1. Read AGENTS.md Project Test Commands. If Unit is TODO/NONE without waiver → **NO-GO**. Resolve **Lint** command too (part of GO when real).  
2. List changed files (`git status` / `git diff --name-only` when git exists).  
3. Map to tests (in order): plan Testing Strategy paths → colocated tests → smallest module suite that covers changed packages. Record selection rule used.  
4. Enter **fix → re-test loop** (below).  
5. Emit QA Test Report (`Mode: targeted`) with cycle count and coverage.

## Fix → re-test loop (mandatory)

One full suite run per cycle. Max **3** runs that follow a **material change** (test fix applied or product fix integrated) or an explicit “re-run as-is” (flake isolation). No double-run within a cycle.
Aligned with `gf-qa` and `/regression-test-loop`.

```
cycle = 0
MAX = 3
while True:
  cycle += 1
  run unit command once (selected paths when supported; else full unit suite with scope note)
  run Lint command when real; capture exit code
  if Coverage command is real: measure per the coverage ladder below; never invent numbers
  accuracy pass per test-accuracy-standards.md
  if tests exit 0 AND lint exit 0 (when real) AND accuracy pass
     AND coverage_gate_ok (see Coverage gate):
    Recommendation: GO
    break
  triage failures:
  - product bug → Recommendation: WAITING_ON_PRODUCT | NO-GO; hand back to implementer/Lead
                  with failing command. **Stop this loop** — do not burn remaining cycles
                  re-running unfixed product code. Resume (cycle reset to 0) only after
                  product fix is integrated.
  - inaccurate test → QA may fix the test without weakening assertions; disclose under
                      Self-applied fixes; next iteration is the next full suite run
  - flake → re-run failed subset up to 2 times for isolation only (do not count isolation
            re-runs as full cycles); if still flaky, quarantine with reason
  if cycle >= MAX and still failing (after material fixes, not product-wait):
    Recommendation: NO-GO; escalate with QA report + failing commands
    break   # no 4th run; no further fix commitment
```

### Coverage gate

- **≥ 80%** when tool exists and **changed lines were measured**.  
- Measurement ladder — record which rung was used:  
  1. changed-line % (diff-cover or equivalent) — preferred  
  2. changed-file % proxy  
  3. whole-package % — weakest; only with explicit limitation note  
- **Vacuous diff:** if diff-cover says “No lines with coverage information in this diff” (or 0 relevant lines):  
  - If git shows **product/executable file diffs** in scope → **diagnose first** (path roots, compare branch, XML mismatch) → **NO-GO** until diagnosed or fixed; do **not** free-GO.  
  - If truly no changed executable lines → record **`UNMEASURED / no changed lines`**. Do **not** report 100%. See `.grok/docs/coverage-policy.md`.  
- Compare-branch ladder: `origin/main` → `main` → `master` → UNMEASURED + missing-ref note.  
- **`NO COVERAGE TOOL`:** loop may continue only if a durable waiver path is **cited** (`docs/waivers/…`) **or** the report records `merge-blocker: coverage-waiver-required` (not merge-grade done). Never invent %.

### Accuracy blockers (NO-GO regardless of green exit)

- Circular / SUT mock call-order-only tests  
- Happy-path-only for non-trivial auth/error/data-loss behavior  
- Missing edge/negative for non-trivial new branches  

## Exit criteria

| Result | Condition |
|--------|-----------|
| **GO** | Tests exit 0; lint exit 0 (when command real); accuracy pass; coverage ≥80% **or** durable waiver cited **or** `UNMEASURED/no-changed-lines` (after vacuous diagnose) **or** `NO COVERAGE TOOL` + waiver cited / merge-blocker recorded |
| **WAITING_ON_PRODUCT** | Product bug handback; loop paused; cycles not burned on re-fail without fix |
| **NO-GO** | Failures after 3 full suite runs (post-fix), lint failures, accuracy blockers, undiagnosed vacuous+product-diff, or missing unit command without waiver |

Max **3** full suite runs after material changes (AGENTS.md). Do not claim targeted PASS without a real run this session.

On each new **protocol** cycle that re-enters this skill: reset nested `cycle` to 0.
