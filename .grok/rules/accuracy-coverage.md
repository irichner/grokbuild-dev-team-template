# Accuracy & coverage (project rules — auto-loaded)

## Skill ownership

- **Plan phase agents** → `/plan` only (`.grok/skills/plan/SKILL.md`)  
- **Implement + accuracy agents** → `/implement` only (`.grok/skills/implement/SKILL.md`)  
- Deprecated skill stubs are not alternate procedures — see redirect files under `.grok/skills/*/SKILL.md`.

## Gates before “done” / merge

1. Targeted tests for changed code: **pass** (real run; `/implement` Accuracy → targeted unit loop).  
2. Code review: no open **bug** or gate-mapped **gap**, or durable waiver in `docs/waivers/`.  
   - After clean `/implement` (**zero open bugs and zero gate-mapped gaps**, tree matches implement scope): **review only** may be skipped with recorded reason — never skip targeted QA, security (when triggered), regression, UI verify, or `/check-work`. If implement artifact is missing/unclear → run `/review` or `gf-reviewer`.  
3. Regression Quick (or Extended when required): **pass** (`/implement` Accuracy → regression).  
4. Coverage ≥ 80% on new/changed executable lines when Coverage command is real in AGENTS.md; else `NO COVERAGE TOOL` + durable waiver. Vacuous diff-cover (“no lines in this diff”) → **UNMEASURED / no changed lines**, not 100%.  
5. `/check-work` → `VERDICT: PASS` for claimed session work (session adequacy; not coverage %). Not a substitute for QA GO.  
6. **Plan quality** (when a plan was required): durable plan file at **`docs/plans/<name>.md`**; Approve from **`/plan`** Phase C (optional `/cold-review` only if present in `grok inspect`), or durable waiver for residual hard-gate failures — see `.grok/docs/plan-quality-standards.md` (hard gates 1–7 always; gate **8 UI/UX design** when the plan touches UI). **Never implement from a chat-only plan.**  
7. **Lint**: exit 0 when the Lint command is real in AGENTS.md (checked inside the targeted loop).  
8. **UI design**: when UI surfaces changed — no blockers per `.grok/docs/ui-design-standards.md`; UI verification evidence recorded in `/implement` protocol (or `NO UI TOOLING` + durable waiver / completed manual blocker checklist).

## Severity map

- `/review` (or `gf-reviewer`) bug (open) → block  
- suggestion on tests/correctness/security/data-loss → gap → block  
- nit / pure style suggestion → non-blocking  
- QA circular or happy-path-only auth/error tests → gap → block  
- UI design blocker per `.grok/docs/ui-design-standards.md` → gap → block  
- Plan missing **any applicable hard gate** (1–7 always; 8 when UI touched) in `.grok/docs/plan-quality-standards.md` → do not implement until revised (or durable waiver after max 2 review passes)  
- Plan required but only chat/session text exists (no `docs/plans/<name>.md`) → gap → do not critique-as-approved and **do not implement** until durable `.md` exists

## Fix / revise loops (aligned max cycles)

| Loop | Max cycles | Exit |
|------|------------|------|
| Plan review (`/plan` Phase C; optional `/cold-review`) | 2 passes | Approve + user OK, or waiver for residual hard-gate failures |
| Targeted unit (`/implement`) | 3 full suite runs | GO (green + accuracy + coverage/waiver) or escalate |
| Regression (`/implement`) | 3 full suite runs | Phase green or durable waiver |
| Full accuracy protocol (`/implement` Phase 2) | 3 cycles | All protocol gates pass or escalate with evidence |

After max cycles: escalate with QA report + review paths + waiver proposals. **Do not claim done.**

## Test accuracy (summary — always apply; full doc is mandatory read for QA)

- Prefer tests that fail when the bug returns.  
- Non-trivial behavior needs at least one edge/negative case.  
- Reject tests that only assert mock call order of the SUT.  
- **QA independence:** QA fixes tests only (never weakening assertions) and discloses self-applied fixes in the QA report; product-code fixes hand back to the implementer/Lead.  
- Full text: `.grok/docs/test-accuracy-standards.md` — QA **must** `read_file` this during targeted loop.  
- Plan hard gates: `.grok/docs/plan-quality-standards.md` — plan reviewer **must** `read_file` during plan critique.  
- UI design standards: `.grok/docs/ui-design-standards.md` — `gf-frontend` and UI verification **must** `read_file` when UI is in scope.

## Security pass

Diff touches auth, secrets handling, payments, or untrusted input parsing → run bundled
security review (`security-auditor`) before merge; findings map via the severity map above.

## Implementer done bar

Specialists (`gf-backend`, `gf-frontend`, `gf-debugger`) — spawned only via `/implement`:

- **With shell** (`execute`/`all`): Ready for review: **yes** only if targeted tests for changed code exited 0 this session.  
- **`gf-debugger` extra:** when shell is available, also requires **fail-then-pass** evidence (failing repro or failing test before the fix, then green after) — see `.grok/personas/instructions/gf-debugger.md` done criteria. Post-fix green alone is not enough.  
- **Without shell**: Ready: **no** + state that Lead must run `/implement` accuracy targeted loop (or re-spawn with `execute`/`all`).  
- **Ready:no solely because tests were not run** → Lead proceeds to `/implement` accuracy; do not block forever waiting for Ready:yes.  
- **Green exit is necessary, not sufficient** — Lead `/implement` still judges test accuracy; Ready:yes does not skip protocol.  
- Lead must not skip accuracy protocol when executable code changed.

## Orchestration

Lead-only `spawn_subagent`. Do not nest subagents. Always set `capability_mode` for shell when running tests (`execute`/`all`). Prepend persona instruction files; tags are UI-only. Full checklist: `.grok/rules/spawn.md`.

## Escape hatches (not silent skip)

- **Trivial** (docs/comment-only or pure typo): skip plan + full regression; executable/SQL/runtime-config changes still need green targeted tests.  
- **Spike / prototype mode:** only with **explicit user approval** and a **time box** for the session/task. May skip full `/plan` critique, full `/implement` accuracy protocol, and regression Extended — but **must** leave a durable note under `docs/plans/` or `docs/waivers/spike-<name>.md` listing what was skipped and residual risk. Prefer at least a smoke/targeted test for executable code when feasible. **Not merge-ready** without re-entering normal gates or a durable waiver. Never invent secrets. Silent gate-skip is not spike mode.

## Version + token ledger (every commit)

**Every git commit** must update `VERSION` (patch bump) and append to `docs/metrics/token-ledger.md` via `python scripts/prepare_commit_metrics.py` (or the pre-commit hook). Never invent token counts; use `--unmeasured` when stats are unavailable. See `docs/metrics/README.md`.
