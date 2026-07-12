# Accuracy & coverage (project rules — auto-loaded)

## Gates before “done” / merge

1. Targeted tests for changed code: pass.  
2. Code review: no open **bug** or gate-mapped **gap**, or durable waiver in `docs/waivers/`.  
   - After clean `/implement` (zero open bugs, tree unchanged): `/review` may be skipped with recorded reason.  
3. Regression Quick (or Extended when required): pass.  
4. Coverage ≥ 80% on new/changed executable lines when Coverage command is real in AGENTS.md; else `NO COVERAGE TOOL` + durable waiver.  
5. `/check-work` → `VERDICT: PASS` for claimed session work (session adequacy; not coverage %).

## Severity map

- `/review` bug (open) → block  
- `/review` suggestion on tests/correctness/security/data-loss → gap → block  
- nit / pure style suggestion → non-blocking  
- QA circular or happy-path-only auth/error tests → gap → block  

## Test accuracy (summary — always apply; full doc is mandatory read for QA)

- Prefer tests that fail when the bug returns.  
- Non-trivial behavior needs at least one edge/negative case.  
- Reject tests that only assert mock call order of the SUT.  
- Full text: `.grok/docs/test-accuracy-standards.md` — QA **must** `read_file` this during targeted loop.

## Orchestration

Lead-only `spawn_subagent`. Do not nest subagents. Always set `capability_mode` for shell when running tests (`execute`/`all`). Prepend persona instruction files; tags are UI-only.
