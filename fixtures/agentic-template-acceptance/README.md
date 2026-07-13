# Acceptance fixtures (v1.6)

## A — Bad plan (mandatory for bootstrap complete)
1. Copy `bad-plan.md` → `docs/plans/acceptance-bad-plan.md`
2. `/plan-review-loop` or `/cold-review` if available
3. **Pass:** Request Changes / Major Concerns; must cite plan-quality hard gates (acceptance criteria, observable verification, testing strategy / edge cases, blast radius). Weak plans must not Approve.

## B — Seeded bug (post-install; needs product code)
1. Plant bug per `seeded-bug-notes.md` on a throwaway branch
2. Targeted tests + `/review`
3. **Pass:** tests FAIL and/or `/review` files a bug — never both green

## C — Coverage hole (post-install; needs product code + coverage tool)
1. New untested branch in code
2. Targeted loop with coverage
3. **Pass:** NO-GO or gate fail without waiver

## D — Test accuracy (optional harness check)
1. Introduce a circular test (mock call-order only on SUT) or happy-path-only auth path
2. Run `/targeted-unit-test-loop` with gf-qa
3. **Pass:** accuracy NO-GO / gap even if pytest exit 0

## E — Seeded design defect (post-install; needs frontend product code)
1. Seed one defect per `seeded-design-defect-notes.md` on a throwaway branch (e.g. missing disabled/loading state, hardcoded off-token color, removed focus style, missing empty state)
2. `/post-change-accuracy-protocol` — UI changed, so the UI verification step is required; judge must read `.grok/docs/ui-design-standards.md`
3. **Pass:** design blocker filed as **gap** / NO-GO — never “done” with the defect in place and no waiver
