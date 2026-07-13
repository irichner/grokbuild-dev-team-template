# Accuracy & coverage (project rules — auto-loaded)

## Gates before “done” / merge

1. Targeted tests for changed code: **pass** (real run; `/targeted-unit-test-loop` or equivalent).  
2. Code review: no open **bug** or gate-mapped **gap**, or durable waiver in `docs/waivers/`.  
   - After clean `/implement` (zero open bugs, tree unchanged): `/review` may be skipped with recorded reason.  
3. Regression Quick (or Extended when required): **pass**.  
4. Coverage ≥ 80% on new/changed executable lines when Coverage command is real in AGENTS.md; else `NO COVERAGE TOOL` + durable waiver.  
5. `/check-work` → `VERDICT: PASS` for claimed session work (session adequacy; not coverage %).  
6. **Plan quality** (when a plan was required): Approve from `/plan-review-loop` or `/cold-review`, or durable waiver for residual hard-gate failures (any Overall other than Approve) — see `.grok/docs/plan-quality-standards.md` (all **7** hard gates).

## Severity map

- `/review` bug (open) → block  
- `/review` suggestion on tests/correctness/security/data-loss → gap → block  
- nit / pure style suggestion → non-blocking  
- QA circular or happy-path-only auth/error tests → gap → block  
- Plan missing **any of the 7 hard gates** in `.grok/docs/plan-quality-standards.md` → do not implement until revised (or durable waiver after max 2 review passes)  

## Fix / revise loops (aligned max cycles)

| Loop | Max cycles | Exit |
|------|------------|------|
| Plan review (`/plan-review-loop` or `/cold-review`) | 2 passes | Approve + user OK, or waiver for residual hard-gate failures |
| Targeted unit | 3 full suite runs | GO (green + accuracy + coverage/waiver) or escalate |
| Regression | 3 full suite runs | Phase green or durable waiver |
| Full post-change protocol | 3 cycles | All protocol gates pass or escalate with evidence |

After max cycles: escalate with QA report + review paths + waiver proposals. **Do not claim done.**

## Test accuracy (summary — always apply; full doc is mandatory read for QA)

- Prefer tests that fail when the bug returns.  
- Non-trivial behavior needs at least one edge/negative case.  
- Reject tests that only assert mock call order of the SUT.  
- Full text: `.grok/docs/test-accuracy-standards.md` — QA **must** `read_file` this during targeted loop.  
- Plan hard gates: `.grok/docs/plan-quality-standards.md` — plan reviewer **must** `read_file` during plan critique.

## Implementer done bar

Specialists (`gf-backend`, `gf-frontend`):

- **With shell** (`execute`/`all`): Ready for `/review`: **yes** only if targeted tests for changed code exited 0 this session.  
- **Without shell**: Ready: **no** + state that Lead must run `/targeted-unit-test-loop` (or re-spawn with `execute`/`all`).  
- **Ready:no solely because tests were not run** → Lead proceeds to `/targeted-unit-test-loop` or protocol; do not block forever waiting for Ready:yes.  
- **Green exit is necessary, not sufficient** — Lead `/targeted-unit-test-loop` still judges test accuracy; Ready:yes does not skip protocol.  
- Lead must not skip post-change protocol when executable code changed.

## Orchestration

Lead-only `spawn_subagent`. Do not nest subagents. Always set `capability_mode` for shell when running tests (`execute`/`all`). Prepend persona instruction files; tags are UI-only.
