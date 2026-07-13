# Fixture E — seeded design defect (post-install; needs frontend product code)

Goal: prove the UI design gate catches a real design defect, the same way Fixture B
proves tests + `/review` catch a seeded bug. Run on a throwaway branch only.

## Seeding (pick ONE, in a real component)

1. Remove the disabled/loading state from a submit button (double-submit possible; no pending feedback).
2. Replace a design-system token with a hardcoded off-palette value (e.g. `#00ff41` where a token exists).
3. Delete the focus-visible style from an interactive element.
4. Remove the empty-state branch from a list view (blank screen on zero data).

## Run

1. `/post-change-accuracy-protocol` on the branch — UI changed, so the UI verification
   step is required (not skippable).
2. Whoever judges design must `read_file` `.grok/docs/ui-design-standards.md` first.

## Pass

- UI verification (or `/review`) files the defect as a **gap** (design blocker) → NO-GO / block.
- **Fail:** the protocol reaches "done" with the defect in place and no durable waiver.
