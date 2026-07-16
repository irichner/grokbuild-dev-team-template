---
name: regression-test-loop
description: >
  Phased regression Quick (default) or Extended with triage and fix→re-test loop
  (max 3 full suite runs). Use before merge or /regression-test-loop.
disable-model-invocation: true
---

# Skill: Regression Test Loop

Lead may **re-enact this SKILL.md** when slash UI is unavailable; slash is preferred operator entry.

## Spawn

Lead-orchestrated; `capability_mode: execute` or `all`; prepend full `.grok/personas/instructions/gf-qa.md`;
`description`: `[gf-qa] regression`.

QA must `read_file` `.grok/docs/test-accuracy-standards.md` when judging new tests added in-session.

## Quick vs Extended

**Extended required when:** auth, payments, migrations, concurrency, shared libs, public API contracts, unclear prior fix, or user asks.  
Otherwise **Quick** (full unit / project regression command from AGENTS.md).

## Steps

1. Choose phase; resolve AGENTS.md commands (fail if NONE/TODO without waiver).  
2. Enter **fix → re-test loop** (below).  
3. QA Test Report (`regression-quick` | `regression-extended`) with cycle count.

## Fix → re-test loop (mandatory)

One full phase run per cycle. Max **3** runs after a **material change** or explicit re-run-as-is. No double-run within a cycle.
Aligned with `gf-qa` and `/targeted-unit-test-loop`.

```
cycle = 0
MAX = 3
while True:
  cycle += 1
  run full chosen phase commands once; capture exit codes
  if phase exit 0:
    Recommendation: GO
    break
  triage failures
  flakes: re-run failed subset up to 2 times for isolation only;
          isolation re-runs do not count as full cycles
  Non-blocking flake = intermittent under isolation re-runs on the same deterministic
  input path; assertion failures on deterministic input are **not** flakes → treat as fail.
  If still flaky → quarantine in report with command + reason (do not silently ignore)
  if product bug: Recommendation: WAITING_ON_PRODUCT | NO-GO; hand back to implementer/Lead
                  with failing command. **Stop this loop** — do not burn remaining cycles
                  re-running unfixed product. Resume (cycle reset to 0) only after product fix.
  if inaccurate test: QA may fix tests without weakening assertions; disclose Self-applied fixes
  if cycle >= MAX and still failing (after material fixes, not product-wait):
    Recommendation: NO-GO; escalate with QA report + evidence
    break   # no 4th run; no further fix commitment
```

## Exit criteria

| Result | Condition |
|--------|-----------|
| **GO** | Chosen phase exit 0 (flakes quarantined with reason only if non-blocking and reported) |
| **WAITING_ON_PRODUCT** | Product bug handback; loop paused |
| **NO-GO** | Residual failures after 3 full phase runs without durable waiver |
| **Waived** | Durable `docs/waivers/<name>.md` for residual failures with references |

Max **3** full phase runs then escalate. Do not claim regression PASS without a real run this session.

On each new **protocol** cycle that re-enters this skill: reset nested `cycle` to 0.
