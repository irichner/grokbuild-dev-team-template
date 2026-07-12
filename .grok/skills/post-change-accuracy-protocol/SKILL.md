---
name: post-change-accuracy-protocol
description: >
  End-to-end accuracy protocol after non-trivial code changes: targeted tests,
  /review (with implement de-dupe), regression, /check-work.
  Use after implementation or /post-change-accuracy-protocol.
disable-model-invocation: true
---

# Skill: Post-Change Accuracy Protocol

## Order (mandatory)

1. **Targeted Unit Test Loop** (`/targeted-unit-test-loop`)  
2. **Code review** — apply implement/review de-dupe from AGENTS.md:  
   - Clean `/implement` + zero open bugs + tree matches → **SKIP** `/review` and record reason  
   - Else run bundled **`/review`** (optional `/code-review` for maintainability)  
3. **Regression Test Loop** (`/regression-test-loop`)  
4. **Final verify** — bundled **`/check-work`** (spawn description starts with `[checking my work]`; require `VERDICT: PASS`)  
5. **Lead merge decision** per gates + `docs/waivers/`  

## On failure
Resume from failed step; max 3 full cycles; then escalate with QA + review evidence.

## Trivial escape
Docs/comment-only: skip except when executable code, tests, SQL, or runtime config changed.

## Ownership
Do not run this skill concurrently with `/implement` mid-loop. Finish implement (or abort it), then run protocol.

## Summary table

| Step | Result | Evidence |
|------|--------|----------|
| Targeted | PASS/FAIL | commands + coverage |
| /review | PASS/FAIL/SKIPPED | open bugs/gaps or skip reason |
| Regression | PASS/FAIL | phase + commands |
| /check-work | PASS/FAIL | VERDICT |
