---
name: implement
description: >
  Implement product changes with gf-* specialists, then run the full accuracy
  protocol (targeted QA, review, regression, UI verify, check-work). Primary
  implement entry point for this template. Owns all implement-phase agents.
  Use after /plan Approve (when planning required), for coding, bugfix,
  parallel fullstack, or /implement. Does not clone host implement memory/effort loop.
disable-model-invocation: true
---

# Skill: Implement (authoritative)

Lead may **re-enact this SKILL.md** when slash UI is unavailable; slash is preferred operator entry.

**This is the only first-class implement skill for GrokForge accuracy-gated work.**

Deprecated aliases (redirect stubs only — do not treat as full procedures):

- `/post-change-accuracy-protocol` → Accuracy protocol below  
- `/targeted-unit-test-loop` → § Targeted unit loop  
- `/regression-test-loop` → § Regression loop  
- `/parallel-fullstack-feature` → Mode `parallel-fullstack`  

## Do not skip accuracy

After any executable code, tests, SQL, or runtime config change, the **Accuracy protocol** is mandatory (unless trivial docs-only or user-approved spike with durable note). Implementer Ready:yes is **not** a substitute for QA accuracy judgment.

## Agents owned (implement phase only)

| Agent | Role | capability_mode | When |
|-------|------|-----------------|------|
| **`gf-backend`** | Backend code + tests | `all` | Mode feature (BE scope) |
| **`gf-frontend`** | Frontend code + tests + UI design bar | `all` | Mode feature (UI scope) |
| **`gf-debugger`** | Root-cause: reproduce → isolate → fix + regression test | `all` | Mode bugfix |
| **`gf-qa`** | Targeted + regression, coverage, test accuracy | `execute` / `all` | Accuracy protocol |
| **`gf-reviewer`** | Thin local code review | `read-only` | Host `/review` missing or Lead requests local pass |
| Host **`/review`** | Diff review | host | Preferred when available |
| Host **`security-auditor`** | Security pass | host | Auth/secrets/payments/untrusted input |
| Host **`/check-work`** | Session VERDICT | host | Final verify |

**Do not spawn** `gf-plan-reviewer` from this skill (that is `/plan` only).  
**Spawn `gf-*` only** as directed by the phases below (Lead-only; depth 1).

## Relationship to host bundled `/implement`

Host may ship a separate implement→review→fix skill (memory, multi-effort reviewers).  
**This project skill is template-authoritative** for accuracy-gated product work: it uses **`gf-*` personas** and the **accuracy protocol**. It does **not** reimplement host memory.py / effort multi-reviewer machinery. If the operator explicitly wants the host-only loop, invoke the host skill by name after probing — default for this template is **this** `/implement`.

---

## Preconditions

1. When planning was required: **`/plan`** left **Ready to implement** (Approve + user OK) **or** durable waiver for residual hard-gate failures.  
2. **Never implement from a chat-only plan.** Durable `docs/plans/<name>.md` required when planning was required.  
3. **Trivial escape:** docs/comment-only or pure typo — may skip plan; if executable code/tests/SQL/runtime config changed → still green targeted tests (at least § Targeted).  
4. **Spike escape:** user-approved time box + durable note listing skips; not merge-ready without re-entering gates.

---

## Mode select

| Mode | When | Primary agents |
|------|------|----------------|
| **`feature`** (default) | Feature, refactor, non-bug change | `gf-backend` and/or `gf-frontend` |
| **`bugfix`** | Wrong behavior / failing test / exception | `gf-debugger` first |
| **`parallel-fullstack`** | Independent BE+FE with frozen contract + git | Both implementers in worktrees |

Prefer sequential `feature` when parallelism is unnecessary.

---

## Phase 1 — Implement

### Spawn rules (every specialist)

- Lead-only `spawn_subagent` (depth 1). Children must not nest orchestration.  
- **Prepend** full `.grok/personas/instructions/<persona>.md`. Tags are UI-only.  
- Set **`capability_mode` explicitly** (`all` for implementers/debugger; never rely on TOML defaults).  
- `description` starts with `[gf-backend]`, `[gf-frontend]`, or `[gf-debugger]`.

### Mode: feature

1. Scope: backend-only → `gf-backend`; UI-only → `gf-frontend`; both sequential → backend then frontend (or one agent if single-stack).  
2. `capability_mode: all`.  
3. Instruct: follow approved plan; smallest correct diff; tests that fail if bug returns; edge/negative for non-trivial branches; never commit.  
4. **Done / Ready:yes** only when Done criteria in persona file hold (green targeted tests when shell available).  
5. Green exit is **necessary, not sufficient** — Accuracy protocol still judges test accuracy.

### Mode: bugfix

1. Spawn **`gf-debugger`** with prepended instructions; `capability_mode: all`.  
2. Require protocol: reproduce → observe → hypothesize → isolate → confirm → fix → regression test.  
3. **Fail-then-pass** evidence when shell available (failing repro/test before fix, green after).  
4. Ready:yes only per `gf-debugger.md` Done criteria.

### Mode: parallel-fullstack

**Git required.** If no git: stop and use sequential feature mode.

1. **Contract artifact** (before parallel work) — `docs/plans/<feature>-contract.md` or plan section:  
   - Endpoints / events / shared types  
   - Owner for shared types  
   - Error and auth expectations  
   - **UI contract** when FE in scope (states, tokens, a11y per ui-design-standards)  
   - Freeze stamp  
2. Contract should already be consistent with an approved `/plan` (or freeze after plan Approve).  
3. Spawn `gf-backend` and `gf-frontend` with `isolation: worktree`, prepend instructions, `capability_mode: all`. Capture each **worktree path**.  
4. **Integrate** into main tree before Accuracy protocol:  
   1. ACP / IDE worktree apply when available  
   2. Else CLI: inspect `git worktree list`; merge/checkout/patch into main — **no force-push / reset --hard** on shared branches without user confirmation; resolve conflicts; re-check contract  
   3. If neither path works: **stop** — sequential on main  
5. Divergent contracts → stop and re-freeze. Unintegrated worktrees as only copy of changes → **NO-GO**.

---

## Phase 2 — Accuracy protocol (mandatory after code change)

Max **3** full protocol cycles. Nested targeted/regression cycles reset on each new protocol cycle.

### Host skills probe (before review and check-work)

1. Prefer `grok inspect` (or host skill list) when available.  
2. If host `/review` or `/check-work` is missing: record **`HOST_SKILLS=PARTIAL`**.  
3. **Never silent-skip:**  
   - Missing `/review` → thin local checklist and/or spawn **`gf-reviewer`** (read-only; prepend instructions); open bug/gap blocks; or NO-GO for merge claims.  
   - Missing `/check-work` → Lead self-verify against exit criteria; record `check-work: DEGRADED (host skill missing)`.  
4. Full host present → `HOST_SKILLS=OK`.

### Order (mandatory)

```
protocol_cycle = 0
MAX = 3
while protocol_cycle < MAX:
  1. Targeted unit loop  → must be GO (or waived) before continue
     If WAITING_ON_PRODUCT: stop; do not burn cycles; resume after product fix
  2. Code review (+ conditional security)
  3. Regression loop → must be GO (or waived)
  4. UI verification (conditional)
  5. /check-work (or DEGRADED path)
  if all PASS/SKIPPED(with reason)/DEGRADED(with recorded path) and check-work PASS or DEGRADED-accepted:
    exit protocol success
  protocol_cycle += 1
  fix open bugs/gaps/test failures
  resume from failed step (re-run earlier steps if fix changed code; reset nested cycles)
if still failing after MAX:
  escalate with evidence — do not claim done
```

---

### § Targeted unit loop (`gf-qa`)

- Spawn: `capability_mode: execute` or `all`; prepend `.grok/personas/instructions/gf-qa.md`; `description`: `[gf-qa] targeted tests`.  
- QA must `read_file` `.grok/docs/test-accuracy-standards.md` before accuracy GO/NO-GO.  
- Prefer git for changed-file list; else user path list or NO-GO.

**Steps:**

1. Read AGENTS.md Project Test Commands. Unit TODO/NONE without waiver → **NO-GO**. Resolve Lint too.  
2. List changed files.  
3. Map tests: plan Testing Strategy → colocated → smallest module suite. Record rule.  
4. Fix → re-test loop (below).  
5. Emit QA Test Report (`Mode: targeted`).

**Fix → re-test (max 3 full suite runs after material change):**

```
cycle = 0
MAX = 3
while True:
  cycle += 1
  run unit once; lint when real; coverage when real (ladder below)
  accuracy pass per test-accuracy-standards.md
  if tests exit 0 AND lint exit 0 (when real) AND accuracy pass AND coverage_gate_ok:
    Recommendation: GO; break
  triage:
  - product bug → WAITING_ON_PRODUCT | NO-GO; hand back; stop loop; resume cycle=0 after fix
  - inaccurate test → QA may fix tests without weakening assertions; disclose Self-applied fixes
  - flake → isolate re-runs (do not count as full cycles); quarantine if still flaky
  if cycle >= MAX and still failing: NO-GO; escalate; break
```

**Coverage gate:** ≥80% when tool exists and changed lines measured. Ladder: changed-line (diff-cover) → changed-file proxy → whole-package %. Vacuous “no lines in this diff”: if product diffs exist → diagnose first (NO-GO until fixed); if truly no executable lines → **UNMEASURED / no changed lines** (not 100%). `NO COVERAGE TOOL` → waiver or `merge-blocker: coverage-waiver-required`. See `.grok/docs/coverage-policy.md`.

**Accuracy blockers (NO-GO regardless of green):** circular/mock-order-only tests; happy-path-only non-trivial auth/error/data-loss; missing edge/negative on non-trivial branches.

| Result | Condition |
|--------|-----------|
| **GO** | Green tests + lint (when real) + accuracy + coverage gate/waiver/UNMEASURED |
| **WAITING_ON_PRODUCT** | Product bug handback |
| **NO-GO** | Failures after max cycles, accuracy blockers, missing unit command without waiver |

---

### § Code review

Apply implement/review de-dupe from AGENTS.md:

- Clean implement with **zero open bugs and zero gate-mapped gaps** + tree matches implement scope → **SKIP review only**; record  
  `Review: SKIPPED (implement clean; bugs=0; gaps=0; tree=<note>)`  
- Missing/unclear implement artifact → **do not de-dupe**; run review.  
- **De-dupe never skips** targeted QA, coverage/lint, security, regression, UI verify, or check-work.  
- Else: host **`/review`** when available; or thin local checklist / spawn **`gf-reviewer`** (`capability_mode: read-only`; prepend instructions; `description`: `[gf-reviewer] …`).  
- **Security pass (conditional):** diff touches auth, secrets, payments, or untrusted input → also run host `security-auditor` when present; map findings via severity.  
- Open **bug** or gate-mapped **gap** → fix → resume protocol from targeted or review as appropriate.

Severity map: open **bug** → block; **suggestion** on missing tests/correctness/security/data-loss → **gap** → block; other suggestion/nit → non-blocking.

---

### § Regression loop (`gf-qa`)

- Spawn: `capability_mode: execute` or `all`; prepend `gf-qa.md`; `description`: `[gf-qa] regression`.  
- **Extended** when: auth, payments, migrations, concurrency, shared libs, public API contracts, unclear prior fix, or user asks. Else **Quick**.

```
cycle = 0
MAX = 3
while True:
  cycle += 1
  run full chosen phase once
  if exit 0: Recommendation: GO; break
  triage flakes (isolation re-runs do not count as full cycles)
  product bug → WAITING_ON_PRODUCT | NO-GO; stop; resume after fix
  inaccurate test → fix without weakening; disclose
  if cycle >= MAX and still failing: NO-GO; escalate; break
```

| Result | Condition |
|--------|-----------|
| **GO** | Phase exit 0 |
| **WAITING_ON_PRODUCT** | Product handback |
| **NO-GO** | Residual after 3 runs without waiver |
| **Waived** | Durable `docs/waivers/<name>.md` |

---

### § UI verification (conditional)

When diff touches UI surfaces (views, components, styling, user-facing states, including fixture sample UI):

1. `read_file` `.grok/docs/ui-design-standards.md` (Blockers list authoritative).  
2. Verify against plan design criteria (gate 8) with **observable evidence**.  
3. Emit **UI Verification Report**:

```
# UI Verification Report
- Surfaces (paths):
- Standards read: .grok/docs/ui-design-standards.md (yes/no)
- State inventory checked (empty/loading/error/disabled/focus):
- Blockers (list each: pass|fail + evidence):
- NO UI TOOLING: yes/no (if yes: waiver path or manual checklist complete?)
- Result: PASS | FAIL | SKIPPED (no UI changed)
- Risk if overridden:
```

4. No UI tooling → `NO UI TOOLING` + manual checklist; merge claims need durable ui-design waiver **or** all blockers pass with evidence.  
5. Design blocker → **gap** → fix → resume.  
6. No UI changed → **SKIPPED** with reason.

---

### § Final verify (`/check-work`)

- When host present: spawn description starts with `[checking my work]`; require `VERDICT: PASS`.  
- Session-adequacy gate — **not** a substitute for QA GO / coverage.  
- Missing host → DEGRADED path from host probe.

---

## Phase 3 — Merge decision + metrics

1. Lead merge decision per gates + `docs/waivers/`.  
   - `merge-blocker: coverage-waiver-required` is **not** merge-ready until waiver or tooling.  
2. Before any commit: `python scripts/prepare_commit_metrics.py --model … --input N --output M` (or `--unmeasured`). Never invent counts.

---

## Exit criteria (all required for “done”)

| Gate | Pass condition |
|------|----------------|
| Implement | Ready criteria for chosen mode; plan Approve/waiver when planning required |
| Targeted | GO (or waived / UNMEASURED / NO TOOL path recorded) |
| Review | No open bug/gap (incl. security when triggered), or SKIPPED with bugs=0;gaps=0, or durable waiver |
| Regression | GO (or durable waiver) |
| UI verification | No design blockers + report, or SKIPPED (no UI), or NO UI TOOLING + checklist/waiver |
| check-work | `VERDICT: PASS` or DEGRADED with explicit note |
| Host skills | `HOST_SKILLS=OK` or `PARTIAL` with non-silent fallback recorded |

**Do not claim session done** when code changed and targeted tests were not run green (unless trivial escape).

## Summary table (protocol)

| Step | Result | Evidence |
|------|--------|----------|
| Host probe | OK / PARTIAL | skill list or inspect note |
| Targeted | PASS/FAIL/WAITING_ON_PRODUCT | commands + coverage + lint + cycle N |
| Review | PASS/FAIL/SKIPPED | open bugs/gaps or skip reason; security if triggered |
| Regression | PASS/FAIL/WAITING_ON_PRODUCT | phase + commands + cycle N |
| UI verify | PASS/FAIL/SKIPPED | UI Verification Report |
| check-work | PASS/FAIL/DEGRADED | VERDICT or degraded note |
| Protocol cycles | N of 3 | escalate if N==3 and failing |
| Merge blockers | none / list | e.g. coverage-waiver-required |
| Token ledger | updated / skipped | entry or “unknown — not recorded” |
