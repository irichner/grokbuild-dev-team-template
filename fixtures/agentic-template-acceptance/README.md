# Acceptance fixtures (v1.4)

## A — Bad plan (mandatory for bootstrap complete)
1. Copy `bad-plan.md` → `docs/plans/acceptance-bad-plan.md`
2. `/plan-review-loop` or `/cold-review` if available
3. **Pass:** Request Changes / Major Concerns; mentions verification or testing gaps

## B — Seeded bug (post-install; needs product code)
1. Plant bug per `seeded-bug-notes.md` on a throwaway branch
2. Targeted tests + `/review`
3. **Pass:** tests FAIL and/or `/review` files a bug — never both green

## C — Coverage hole (post-install; needs product code + coverage tool)
1. New untested branch in code
2. Targeted loop with coverage
3. **Pass:** NO-GO or gate fail without waiver
