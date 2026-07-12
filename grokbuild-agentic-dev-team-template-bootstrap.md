# Grok Build Agentic Software Development Team Template — Bootstrap

**Version:** 1.4  
**Date:** 2026-07-12  
**Status:** Draft (v1.3 cold-review findings incorporated)  
**Purpose:** Single-file bootstrap for Grok Build CLI. Install a Grok-native agentic team optimized for **code accuracy**, **test accuracy**, and **coverage** — without reinventing or shadowing harness features that already work.

**Prior reviews:**  
- Cold review of v1.1 → findings folded into v1.2/v1.3  
- Cold review of v1.3 → `grokbuild-agentic-dev-team-template-bootstrap.review.md` (this revision addresses those findings)

---

## Goal

Install project config so Grok:

1. **Finds** skills and personas via real discovery paths (`.grok/`).  
2. **Uses** bundled `/review`, `/check-work`, and (when invoked) `/implement`, plus plan-side `/cold-review` / plan-review when available.  
3. **Enforces** measurable gates: tests pass, coverage floor (when tool exists), test-accuracy standards, no open bug/gap review issues without a **durable** user waiver.  
4. **Proves** install via **strict** `grok inspect --json` skill listing **and** mandatory Fixture A (behavioral) — not “files exist.”

Success is operational behavior, not directory ceremony. Static discovery alone does **not** prove accuracy/coverage enforcement.

---

## Non-goals

- Replacing `/implement`, `/review`, `/check-work`, `/code-review`, `/design`, or `/execute-plan`.  
- Shadowing bundled personas (`reviewer`, `implementer`, `test-writer`, `security-auditor`, …).  
- Building product features or CI provider YAML (may mirror gates later).  
- Hardcoding FastAPI/Next.js as mandatory stacks.  
- Nested subagent trees (Grok depth limit is **1**).  
- Assuming `.grok/docs/` auto-loads into context (it does not).  
- Running Fixture B/C during bootstrap on a template-only repo (needs product code; deferred post-install).  
- Installing coverage tools for every language (out of scope; waiver or add tooling is explicit).  
- Relying on undocumented persona/role **resolution** to bind behavior (inject path is the only reliable path).

---

## Assumptions

| # | Assumption | Falsifier | If false |
|---|------------|-----------|----------|
| A1 | Repo skills load from `<repo>/.grok/skills/<name>/SKILL.md` | Missing from `grok inspect --json` | Fix path/frontmatter; **do not claim bootstrap done** |
| A2 | Personas load from `<repo>/.grok/personas/*.toml` into the catalog; they do **not** auto-bind on spawn | Spawn with only `[gf-qa]` tag and no prepended body | Lead/skills **must** read + prepend instructions every spawn; tags never bind behavior |
| A3 | `[tag]` in spawn `description` is **UI label only** (pager); wrong tag only hurts label, not behavior | Label wrong | Keep tags for UX; **missing prepend** is the real failure |
| A4 | Only the **parent** session can `spawn_subagent` (depth 1) | Child spawn errors | All loops orchestrated by Lead; never auto-fire nested skills from a child |
| A5 | `capability_mode: read-only` has **no shell** (no git, no tests) | QA cannot run pytest/npm | Always set `execute` or `all` on spawn for test runners (do not rely on persona TOML defaults) |
| A6 | Plan Mode plan is session `plan.md` under `~/.grok/sessions/<encoded-cwd>/<session-id>/plan.md` | Reviewer finds empty repo plan | Copy durable plan to `docs/plans/<name>.md` after plan mode allows non-plan writes / after exit |
| A7 | Bundled `/review` + `/check-work` remain available; `/implement` is slash-only (`disable-model-invocation`) | Skill missing | Inline minimal equivalent or install bundled skills |
| A8 | Project rules auto-load: root `AGENTS.md` + `.grok/rules/*.md` (not `.grok/docs/`) | Policy ignored | Put short gates in AGENTS + rules; keep AGENTS concise |
| A9 | **Target repo is a git repository** (Grok `projectRoot` = git root). Worktrees, `/review` local mode, git-diff test selection require git | `git rev-parse` fails; `projectRoot: null` | Phase 0: require git or `git init` with user OK; else install config-only and mark worktree/review-dependent skills **degraded** |
| A10 | Project Test Commands are filled from manifests **or** an explicit durable waiver exists | Commands stay silent `TODO` forever | Phase 3 fails closed: user must fill, add tooling, or write `docs/waivers/…` |
| A11 | Prompt pressure (AGENTS/rules) is not a hard gate; Lead can skip protocol | Ordinary “implement this” skips post-change protocol | Prefer explicit slash skills; post-change skill is user/Lead-invoked; Fixture A proves plan-review path works |
| A12 | `/check-work` is **session-adequacy** verification (trace + optional build/test), not a pure coverage meter | Session “bootstrap done” PASSes without product tests | Use check-work as final session check; do **not** treat VERDICT alone as proof of coverage % |

---

## Risks

| Risk | Mitigation |
|------|------------|
| Shadow bundled `reviewer` / `implementer` | Use **prefixed** persona names only (`gf-*`) |
| Double review loop (`/implement` then `/review`) | **Orchestration rule** (below): skip redundant `/review` when implement left zero open bugs; else re-run `/review` |
| `read-only` QA cannot test | Always set `capability_mode` on spawn; roles/TOML defaults are **not** sufficient |
| Docs under `.grok/docs` never loaded | Mirror critical policy in `.grok/rules/` + AGENTS.md; skills **must** `read_file` full standards |
| Process tax | Trivial-change escape hatch; implement/review de-dupe |
| AGENTS.md merge loss | Timestamped backup; never overwrite existing `.bak-*` |
| Silent `TODO` test commands | Phase 3 closed: fill, or durable waiver |
| Non-git directory | Phase 0 gate |
| Waiver evaporates next session | Durable `docs/waivers/*.md` only |
| Severity taxonomy mismatch (`bug\|suggestion\|nit` vs gap) | Explicit **severity → gate** map in AGENTS + rules |
| Skill auto-invoke mid-`/implement` | `disable-model-invocation: true` on heavy orchestration skills; Lead-only ownership |
| Nested fence corruption when extracting plan content | Report schemas use **indented / tilde** fences in this bootstrap file (see Section 4+) |
| Plugin `/cold-review` missing or `[compat unresolved]` | Probe in Phase 4; fallback to `/plan-review-loop` without claiming cold-review works |
| Roles never resolve | Roles optional; **always** prepend instructions + set capability on spawn |

---

## How would this fail to ship?

- Skills under wrong root or wrong shape → not in `grok inspect --json`.  
- Personas named `reviewer` → shadow bundled catalog.  
- Nested QA spawns Reviewer → depth error.  
- Coverage gate with no tool and silent pass (no durable waiver).  
- Ignoring `/check-work` / `/review` and rubber-stamping.  
- Bootstrap “passes” on file tree only without Fixture A or strict V8.  
- Non-git repo: `/review` and worktrees fail after “successful” install.  
- Lead spawns with `[gf-qa]` tag only → generic agent, no QA schema.

---

## Bootstrap Instructions for Grok Build

You are Grok Build. Implement this **v1.4** Agentic Software Development Team template in the current repository.

### Phase 0 — Safety & prerequisites

1. **Git check:** Run `git rev-parse --show-toplevel`.  
   - If OK: continue.  
   - If fail: tell the user Grok scopes project root via `.git`, and that `/review`, worktrees, and git-diff test selection need git. Offer: (a) `git init` with user approval, or (b) **config-only install** with degraded mode (document in handoff; skip parallel-fullstack operational claims).  
2. If root `AGENTS.md` exists, copy to `AGENTS.md.bak-before-agentic-template-<YYYYMMDD>` (never overwrite an existing backup).  
3. **Do not** create `.grokbuild/` (deprecated). Use **`.grok/`** only.  
4. **Do not** create personas named `reviewer`, `implementer`, `test-writer`, or `security-auditor` (bundled names).  
5. Merge; do not delete project-specific rules. Prefer short AGENTS (actionable gates + commands); put long prose in `.grok/docs/`.

### Phase 1 — Directory structure

Create:

```
.grok/
├── README.md
├── rules/
│   └── accuracy-coverage.md          # AUTO-LOADED project rules
├── personas/
│   ├── gf-backend.toml
│   ├── gf-frontend.toml
│   ├── gf-qa.toml
│   ├── gf-plan-reviewer.toml
│   └── instructions/
│       ├── gf-backend.md
│       ├── gf-frontend.md
│       ├── gf-qa.md
│       └── gf-plan-reviewer.md
├── roles/                            # optional catalog defaults only; NOT spawn binding
│   ├── gf-qa.toml
│   └── gf-plan-reviewer.toml
├── skills/
│   ├── plan-review-loop/
│   │   └── SKILL.md
│   ├── targeted-unit-test-loop/
│   │   └── SKILL.md
│   ├── regression-test-loop/
│   │   └── SKILL.md
│   ├── post-change-accuracy-protocol/
│   │   └── SKILL.md
│   └── parallel-fullstack-feature/
│       └── SKILL.md
├── workflows/
│   └── post-change-testing-protocol.md   # narrative only; not auto-loaded
└── docs/                                 # reference only; not auto-loaded
    ├── privacy-safety.md
    ├── test-accuracy-standards.md
    └── coverage-policy.md
docs/
├── plans/
└── waivers/                              # durable gate waivers (see schema)
    └── README.md
fixtures/
└── agentic-template-acceptance/
    ├── README.md
    ├── bad-plan.md
    └── seeded-bug-notes.md
```

Also create/update root `AGENTS.md` per Section 1.

**Note:** Do **not** add a project skill named `code-review` or `review` (collides with bundled skills). Code review is **`/review`** (and optional `/code-review` for maintainability).

### Phase 2 — Write contents

Write every file from the sections below. For each persona: `.toml` + matching `instructions/*.md`.

**Extraction rule:** When copying embedded file bodies from this bootstrap, use the section under each path heading only. Report schemas use `~~~~` fences inside instruction files so triple-backtick extractors do not truncate.

### Phase 3 — Project Test Commands (closed)

Scan package manifests / README / existing scripts (`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `Makefile`, CI configs, etc.). Fill **Project Test Commands** in root `AGENTS.md`:

- Build  
- Unit tests  
- Coverage (if any) — include **how** to read changed-line or changed-file % when known  
- Regression / full suite  
- Lint / typecheck  

**Closed outcomes (pick exactly one per command row):**

| Outcome | When | Gate impact |
|---------|------|-------------|
| Real command | Found in repo | Use in skills |
| `NONE — no tool in repo` | Scanned, absent | Coverage: treat as `NO COVERAGE TOOL`; merge needs durable waiver or add tooling |
| `TODO — user must fill` | Ambiguous after scan | **Not allowed as silent final state.** Either get user to fill in handoff **or** write `docs/waivers/bootstrap-test-commands.md` listing which rows are incomplete and residual risk |

If Unit tests and Regression are both `NONE`/`TODO` without waiver → bootstrap may install files but **must not** claim accuracy gates are operational.

### Phase 4 — Bootstrap verification (mandatory)

| # | Check | Pass criteria |
|---|--------|----------------|
| V1 | Tree | Phase 1 paths exist; **no** `.grokbuild/`; **no** persona files named `reviewer.toml` / `implementer.toml` / `test-writer.toml` |
| V2 | Skill shape | Each project skill is `SKILL.md` with YAML `name` + `description` |
| V3 | Persona files | Each `gf-*.toml` has `description` and `instructions` or `instructions_file`; **read** each instructions file (non-empty); path exists |
| V4 | Auto-load rules | `.grok/rules/accuracy-coverage.md` exists; includes gates + severity map + waiver pointer |
| V5 | AGENTS.md | Pipeline + implement/review de-dupe + severity map + Project Test Commands + waiver path |
| V6 | Non-stub skills | Targeted + regression have numbered steps + QA report schema; post-change has implement de-dupe |
| V7 | Fixtures | Acceptance fixtures present; `docs/waivers/README.md` present |
| V8 | **Discovery (strict)** | Run `grok inspect --json`. Assert these skill **names** appear with project/local (or repo) source: `plan-review-loop`, `targeted-unit-test-loop`, `regression-test-loop`, `post-change-accuracy-protocol`, `parallel-fullstack-feature`. **Fail bootstrap if missing.** If `grok` CLI truly unavailable: **do not pass V8** — report blocked and list exact names for user to verify after install; handoff status = incomplete |
| V9 | Protocol map | Print post-change order including implement/review de-dupe rule |
| V10 | Cold-review probe | Note whether `/cold-review` appears in inspect skills (any source). If absent/unresolved, document fallback-only |
| V11 | **Fixture A (behavioral, mandatory)** | Copy `fixtures/.../bad-plan.md` → `docs/plans/acceptance-bad-plan.md`; run `/plan-review-loop` or `/cold-review` if available. **Pass:** overall Request Changes or Major Concerns **and** mentions verification and/or testing gaps. If plan-review cannot run in this session, mark V11 failed and handoff incomplete — do not claim bootstrap done |
| V12 | Fixture B/C | **Not required for bootstrap complete.** Document as post-install on first product code |

### Phase 5 — Handoff

List files; state V8–V11 results explicitly; summarize gates and Project Test Commands status (`REAL` / `NONE` / `WAIVED`); ask user to fill remaining commands or confirm waivers; point to Fixture B/C for first real feature branch.

---

## Canonical harness integration (do not reinvent)

| Step | Prefer | Project skill role |
|------|--------|--------------------|
| Plan (ambiguous / large) | Plan Mode (`/plan`) | — |
| Adversarial plan critique | Plugin `/cold-review` if inspect shows it; else `/plan-review-loop` | `plan-review-loop` |
| Implement + multi-reviewer fix loop | **`/implement`** (slash; not auto-invoked) | Specialists via `gf-*` only when not using `/implement` |
| Code review of diff | **`/review`** (see de-dupe rule) | Do not reimplement |
| Maintainability deep audit | **`/code-review`** (optional) | — |
| Targeted unit + coverage | — | `targeted-unit-test-loop` |
| Regression | — | `regression-test-loop` |
| Final session verify | **`/check-work`** (`[checking my work]` + `VERDICT`) | Session adequacy — not a substitute for QA report coverage % |
| End-to-end after change | — | `post-change-accuracy-protocol` |
| Plan vs diff audit | Plugin `/plan-audit` if available | — |
| Pre-PR bundle | Plugin `/pre-pr` if available | — |

### Implement vs post-change `/review` (de-dupe rule)

| Situation | Code-review step in post-change protocol |
|-----------|------------------------------------------|
| Change landed via **`/implement`**, final implement round reported **zero open bugs**, and working tree matches that review scope | **Skip** re-running `/review`. Record: `Review: SKIPPED (implement clean; <summary path or round note>)`. Still run targeted tests, regression, check-work |
| `/implement` left open bugs/suggestions that map to **gate-blocking** severities, or tree changed after implement | Run **`/review`** on current local/branch diff |
| Change landed **without** `/implement` (manual / `gf-*` specialists) | Always run **`/review`** |
| User explicitly requests `/review` | Always run |

### Severity → merge gate map

`/review` severities are `bug | suggestion | nit`. Template gates use `bug | gap`.

| Source | Gate effect |
|--------|-------------|
| `/review` **bug** (Status open) | **Block merge** unless durable waiver |
| `/review` **suggestion** that is missing tests, wrong behavior risk, security, or data loss | Treat as **gap** → **block** unless fixed or waived |
| `/review` **suggestion** (style/refactor only) | Do not block merge; may track |
| `/review` **nit** | Do not block |
| QA test-accuracy finding (circular tests, happy-path-only on auth/errors) | **gap** → block |
| Plan-reviewer Required Changes `bug\|gap` | Block implement until plan revised or user accepts residual Major Concerns **in a durable waiver** |

### Durable waivers

Path: `docs/waivers/<short-name>.md`

Required fields:

- Date, author (user), scope (paths / gate name)  
- Gate waived (coverage / test-commands / review-bug / regression residual / …)  
- Residual risk  
- Follow-up (issue link or “none”)  
- Expiry (date or “until <event>”)

Chat-only “LGTM” is **not** a waiver. Lead must re-read open waivers under `docs/waivers/` before merge decision.

### Hard runtime rules (Grok product)

1. **Lead orchestrates all spawns** — subagents cannot spawn subagents.  
2. **Persona binding** — read `.grok/personas/instructions/<name>.md` (or bundled persona paths used by `/implement`/`/review`) and **prepend** to the child prompt. No `persona=` parameter. Catalog TOML does not inject by itself.  
3. **`description` tags** — e.g. `[gf-qa] targeted tests` — for TUI labels only. Misspelled tag ≠ missing persona; missing **prepend** is.  
4. **Always set `capability_mode` on spawn** for the task (do not rely on persona/role defaults for the inject path):  
   - Plan review / read-only critique: `read-only` **or** `subagent_type: explore`/`plan`  
   - Code review that needs `git`: parent collects diff **or** child uses `execute`/`all`  
   - Run tests: **`execute` or `all`** (never `read-only`)  
5. **Worktrees** — require git; `isolation: worktree` for parallel implementers; apply via Grok worktree apply.  
6. **`/check-work`** — use skill as written; look for `VERDICT: PASS` or `VERDICT: FAIL`. Interpret as session verification, not coverage certification.  
7. **Orchestration ownership** — only one of: Lead running post-change protocol, `/implement`, or a single project orchestration skill. Do not stack concurrent orchestrators.  
8. **Bundled test-writer** — when `/implement` effort includes a Tests specialist, prefer harness behavior; for project QA, `gf-qa` owns execution + accuracy critique. When writing new tests outside `/implement`, Lead may prepend bundled `test-writer` instructions if available under bundled personas (do not shadow the name with a project persona file).

---

## 1. AGENTS.md (project root)

~~~~markdown
# AGENTS.md — GrokForge Agentic Dev Team

**Template Version:** 1.4  
**Primary optimization target:** Code accuracy, test accuracy, and coverage.

You are the **Lead Engineer**. Optimize for correct, well-tested change — not ceremony.

## Harness first (mandatory)

Use Grok-native discovery and bundled skills. Do not invent parallel roots (no `.grokbuild/`).

### Default change pipeline

1. **Plan** — Plan Mode when approach is ambiguous or blast radius is large (`/plan`). Session plan: `~/.grok/sessions/<encoded-cwd>/<session-id>/plan.md`. For durable review, copy to `docs/plans/<short-name>.md` after plan mode allows it.  
2. **Plan critique** — `/cold-review docs/plans/<name>.md` if available in this workspace; else `/plan-review-loop`. Revise before implementing.  
3. **Implement** — Prefer `/implement` for non-trivial coding (slash; multi-reviewer loop). Otherwise spawn specialists with **prepended** `gf-*` persona instructions (tags alone do nothing).  
4. **Post-change accuracy protocol** — `/post-change-accuracy-protocol` or follow manually:  
   - Targeted unit + coverage (`/targeted-unit-test-loop`)  
   - Code review: **`/review`** unless implement/review de-dupe says skip (see below)  
   - Regression (`/regression-test-loop`)  
   - Final: **`/check-work`** (session adequacy + build/test when code changed)  
5. **Merge decision** — only when gates pass or a **durable** waiver exists under `docs/waivers/`.

### Implement vs `/review` de-dupe

- After clean `/implement` (zero open bugs, tree unchanged): skip `/review`; record skip reason.  
- After manual/`gf-*` implement, dirty implement, or user request: run `/review`.

### Trivial escape hatch

Docs/comment-only or pure typo: skip plan + full regression. If executable code, tests, SQL, or config that affects runtime changed, still run relevant unit tests.

## Accuracy & coverage gates

See auto-loaded `.grok/rules/accuracy-coverage.md`. Full test-accuracy text: `.grok/docs/test-accuracy-standards.md` (not auto-loaded — **read it** when judging tests).

1. **Tests** — Targeted suite green; regression (Quick or Extended per skill) green.  
2. **Coverage** — When Coverage command is a real command: **≥ 80%** new/changed executable lines (or changed-file proxy, noted). `NONE`/`NO COVERAGE TOOL` → durable waiver or add tooling before merge.  
3. **Test accuracy** — Circular/over-mocked tests are **gaps** (block GO).  
4. **Review** — No open **bug** or gate-mapped **gap** without durable waiver.  
5. **Verify** — `/check-work` → `VERDICT: PASS` for the session’s claimed work (not a coverage substitute).

### Severity map (review → gate)

- Open **bug** → block  
- **suggestion** about missing tests / correctness / security / data loss → **gap** → block  
- Other **suggestion** / **nit** → non-blocking  

Max **3** fix cycles after a failed gate, then escalate with evidence (QA report + review paths + waivers).

## Subagent rules

- Only **you (Lead)** call `spawn_subagent` (depth 1).  
- **Always prepend** persona instruction file text when using `gf-*`. Tags are UI-only.  
- **Always set** `capability_mode` on spawn for the task.  
- QA/test runners: `execute` or `all`.  
- Plan reviewers: `read-only` or `explore`/`plan`.  
- Prefer `isolation: worktree` only when git exists; integrate via worktree apply before claiming done.  
- Do not nest orchestration skills under a child.

## Personas (project, non-shadowing)

| Name | Use |
|------|-----|
| `gf-backend` | Backend implementation |
| `gf-frontend` | Frontend implementation |
| `gf-qa` | Targeted/regression tests, coverage, test accuracy |
| `gf-plan-reviewer` | Plan critique when not using `/cold-review` |

Do **not** redefine bundled names: `reviewer`, `implementer`, `test-writer`, `security-auditor`.

## Skill capture

Use `/create-skill` → `.grok/skills/<name>/SKILL.md`. Never `/skillify`.

## Secrets

Never commit or prompt-paste secrets. Prefer env/MCP secret handling.

## Waivers

Durable only: `docs/waivers/<name>.md` (see `docs/waivers/README.md`). Chat is not enough.

## Project Test Commands

<!-- Bootstrap fills from repo scan — each row REAL command | NONE | TODO+waiver -->

- **Build:** `TODO`
- **Unit tests:** `TODO`
- **Coverage:** `TODO`
- **Regression / full suite:** `TODO`
- **Lint / typecheck:** `TODO`
~~~~

---

## 2. `.grok/README.md`

~~~~markdown
# GrokForge project template (v1.4)

Grok-native paths only. Optimized for **accuracy + coverage**.

## What loads automatically

| Path | Loaded by Grok? |
|------|-----------------|
| Root `AGENTS.md` | Yes (project rules) |
| `.grok/rules/*.md` | Yes |
| `.grok/skills/*/SKILL.md` | Yes (skills / slash commands) |
| `.grok/personas/*.toml` | Yes (persona **catalog only**; spawn needs instruction **prepend**) |
| `.grok/roles/*.toml` | Catalog defaults when resolution applies — **skills must still set capability_mode and prepend instructions** |
| `.grok/docs/*`, `.grok/workflows/*` | **No** — reference only |

## Prefer bundled skills

- `/implement` — implement → review → fix loop  
- `/review` — diff review  
- `/check-work` — session verification (includes build/test when relevant)  
- `/code-review` — strict maintainability (optional)  
- `/create-skill` — capture new skills  
- `/plan`, `/view-plan` — Plan Mode  

Project skills add plan-review fallback, targeted/regression testing, coverage gates, and the post-change protocol.

## Git required for full protocol

`/review` local mode, worktrees, and git-diff test selection need a git repo. Without git: config may load from CWD `.grok/`, but accuracy protocol is degraded.

## Deprecated

`.grokbuild/` (v1.1) — not discovered.
~~~~

---

## 3. Auto-loaded rules

### `.grok/rules/accuracy-coverage.md`

~~~~markdown
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
~~~~

---

## 4. Personas (non-shadowing names)

### `.grok/personas/gf-backend.toml`

~~~~toml
description = "GrokForge backend specialist. Stack-adaptive. Correctness and tests first."
instructions_file = ".grok/personas/instructions/gf-backend.md"
reasoning_effort = "high"
default_capability_mode = "all"
~~~~

### `.grok/personas/instructions/gf-backend.md`

~~~~markdown
# gf-backend

Senior backend engineer. Infer stack from the repo; do not assume a framework.

## Constraints
- Follow the approved plan and existing patterns.
- Every behavior change includes tests.
- Never commit; deliver diffs + structured summary.
- Surface ambiguities; do not invent product requirements.

## Output
1. Summary  2. Files + rationale  3. Correctness decisions  
4. Tests (what behavior each locks)  5. Coverage notes  
6. Risks  7. Ready for `/review`: yes/no
~~~~

### `.grok/personas/gf-frontend.toml`

~~~~toml
description = "GrokForge frontend specialist. Stack-adaptive. UX states and tests."
instructions_file = ".grok/personas/instructions/gf-frontend.md"
reasoning_effort = "high"
default_capability_mode = "all"
~~~~

### `.grok/personas/instructions/gf-frontend.md`

~~~~markdown
# gf-frontend

Senior frontend engineer. Infer stack from the repo (do not assume Next.js).

## Constraints
- Follow plan and existing UI patterns/design system.
- Strong typing when the project uses TypeScript.
- Include tests for interactive behavior when a runner exists.
- Never commit; structured summary only.

## Output
Same structure as gf-backend.
~~~~

### `.grok/personas/gf-qa.toml`

~~~~toml
description = "GrokForge QA: targeted/regression tests, coverage measurement, test accuracy."
instructions_file = ".grok/personas/instructions/gf-qa.md"
reasoning_effort = "high"
default_capability_mode = "all"
~~~~

### `.grok/personas/instructions/gf-qa.md`

`````markdown
# gf-qa

You own test execution, coverage numbers, and test-accuracy critique.

## Rules
- Discover commands from AGENTS.md → Project Test Commands, then README.
- If commands are TODO/NONE without a durable waiver path cited by Lead, report NO-GO for operational gates.
- Parent must spawn you with capability_mode execute or all (not read-only). Do not assume TOML defaults applied.
- Prefer real test runs over claims.
- Always read_file `.grok/docs/test-accuracy-standards.md` before accuracy judgment.
- Emit QA Test Report every run (schema below).
- Circular tests = accuracy failure (blocks GO).

## Coverage measurement notes
- Prefer line-level changed coverage when the tool supports it (e.g. pytest-cov + diff-cover, nyc/istanbul changed files, go cover profiles, llvm-cov).
- If only whole-project % is available, record that limitation and use changed-file proxy (files touched must meet threshold or be listed as gaps).
- Never invent a percentage. If unmeasured: NO COVERAGE TOOL or UNMEASURED.

## QA Test Report schema

Use this plain-text block (no nested code fence required when writing the file):

    # QA Test Report
    - Mode: targeted | regression-quick | regression-extended
    - Scope (files / git range):
    - Commands (exact):
    - Results (pass/fail counts; critical failures):
    - Coverage (tool; changed % or UNMEASURED; gate met? yes/no/waived/NO TOOL):
    - Test accuracy findings:
    - Gaps (untested behaviors in diff):
    - Flakes (quarantined? command?):
    - Recommendation: GO | NO-GO
    - Risk if overridden:
`````

### `.grok/personas/gf-plan-reviewer.toml`

~~~~toml
description = "GrokForge plan reviewer. Adversarial. No implementation."
instructions_file = ".grok/personas/instructions/gf-plan-reviewer.md"
reasoning_effort = "high"
default_capability_mode = "read-only"
~~~~

### `.grok/personas/instructions/gf-plan-reviewer.md`

`````markdown
# gf-plan-reviewer

Critique plans before coding. Do not implement.

## Checklist
- Measurable goal / success criteria
- Weak assumptions and falsifiers
- Missing failure modes
- Observable verification (reject “works correctly”)
- Testing strategy: commands, edge cases, coverage expectation
- Scope vs non-goals
- Ship-failure thinking

## Review Report schema

Use this plain-text block when writing the file:

    # Review Report
    - Target: plan
    - Paths:
    - Overall: Approve | Request Changes | Major Concerns
    - Required Changes: (severity bug|gap|risk)
    - Test/coverage gaps:
    - Questions:
    - Risk if implemented as-is:
`````

---

## 5. Roles (optional defaults — not spawn binding)

### `.grok/roles/gf-qa.toml`

~~~~toml
description = "QA runner defaults: full tools for tests"
default_capability_mode = "all"
reasoning_effort = "high"
~~~~

### `.grok/roles/gf-plan-reviewer.toml`

~~~~toml
description = "Plan review defaults: no edits"
default_capability_mode = "read-only"
reasoning_effort = "high"
~~~~

**Important:** Product docs do not specify a skill-facing role selector. Treat roles as optional catalog metadata. **Every skill spawn must:** (1) prepend instruction markdown, (2) set `capability_mode` explicitly, (3) use `[gf-*]` only as pager label.

---

## 6. Skills

### `.grok/skills/plan-review-loop/SKILL.md`

~~~~markdown
---
name: plan-review-loop
description: >
  Critique a plan before implementation using gf-plan-reviewer (or recommend /cold-review).
  Use before coding, for plan critique, or /plan-review-loop.
disable-model-invocation: true
---

# Skill: Plan Review Loop

## Prefer
If `/cold-review` appears in `grok inspect` for this workspace, prefer it for adversarial plan review. This skill is the fallback when cold-review is missing or unresolved.

## Inputs
- Plan path: prefer `docs/plans/<name>.md`. If only session plan exists, copy session `plan.md` to `docs/plans/` first (after Plan Mode allows non-plan writes, or after exiting plan mode).
- Max passes: 2

## Steps
1. Read the plan. Flag missing Testing Strategy / non-observable verification.
2. Read `.grok/personas/instructions/gf-plan-reviewer.md` and **prepend** full text to the child prompt.
3. Spawn **from Lead only**:
   - `subagent_type`: `general-purpose` with `capability_mode: read-only`, **or** `subagent_type: explore` / `plan`
   - `description`: `[gf-plan-reviewer] plan review` (UI label only)
   - Prompt = persona instructions + plan path + Review Report schema + “Do not edit product code.”
4. Apply Required Changes to the plan.
5. Optional second pass if still Request Changes.
6. Present to user; **do not implement** until user approves.
7. Residual Major Concerns require durable waiver under `docs/waivers/` if user accepts without full fix.

## Exit
Approve, or durable waiver for residual Major Concerns.
~~~~

### `.grok/skills/targeted-unit-test-loop/SKILL.md`

~~~~markdown
---
name: targeted-unit-test-loop
description: >
  Fast unit tests on changed code with coverage delta and test-accuracy checks.
  Use after implementation or /targeted-unit-test-loop.
disable-model-invocation: true
---

# Skill: Targeted Unit Test Loop

## Spawn rules
- Orchestrated by **Lead** (not nested under another subagent).
- Spawn with `capability_mode: execute` or `all` (shell required) — set explicitly.
- Prepend full `.grok/personas/instructions/gf-qa.md`; `description`: `[gf-qa] targeted tests`.

## Prerequisites
- Prefer git for changed-file list. If no git: require user-supplied path list or fail with NO-GO (cannot define “changed”).

## Steps
1. Read AGENTS.md Project Test Commands. If Unit is TODO/NONE without waiver → NO-GO.
2. List changed files (`git status` / `git diff --name-only` when git exists).
3. Map to tests (in order): plan Testing Strategy paths → colocated tests → smallest module suite that covers changed packages. Record selection rule used.
4. Run unit command restricted to selected paths when supported; else full unit suite with scope note.
5. Coverage if Coverage command is real; record changed-line % or changed-file proxy; never invent numbers.
6. **Gate:** ≥ 80% when tool exists and measured; else NO COVERAGE TOOL / UNMEASURED.
7. `read_file` `.grok/docs/test-accuracy-standards.md`; accuracy pass.
8. Emit QA Test Report (`Mode: targeted`).

## Exit
Tests exit 0; coverage gate met or durable waiver; no accuracy blockers. Max 3 fix cycles.
~~~~

### `.grok/skills/regression-test-loop/SKILL.md`

~~~~markdown
---
name: regression-test-loop
description: >
  Phased regression Quick (default) or Extended with triage.
  Use before merge or /regression-test-loop.
disable-model-invocation: true
---

# Skill: Regression Test Loop

## Spawn
Lead-orchestrated; capability_mode execute/all; prepend gf-qa instructions; `[gf-qa] regression`.

## Quick vs Extended
**Extended required when:** auth, payments, migrations, concurrency, shared libs, public API contracts, unclear prior fix, or user asks.

## Steps
1. Choose phase; run AGENTS.md commands (fail if NONE/TODO without waiver).
2. Capture exit codes; triage failures (product bug vs flake vs env).
3. Flakes: re-run failed subset up to 2 times; if still flaky, quarantine in report with command + reason; do not silently ignore.
4. Re-run full chosen phase after fixes.
5. QA Test Report (`regression-quick` | `regression-extended`).

## Exit
Phase exit 0, or durable waiver for residual failures with references.
~~~~

### `.grok/skills/post-change-accuracy-protocol/SKILL.md`

~~~~markdown
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
~~~~

### `.grok/skills/parallel-fullstack-feature/SKILL.md`

~~~~markdown
---
name: parallel-fullstack-feature
description: >
  Parallel backend/frontend in worktrees with contract-first integration and
  post-change accuracy protocol. Use for full-stack features or /parallel-fullstack-feature.
disable-model-invocation: true
---

# Skill: Parallel Full-Stack Feature

## Prerequisites
- Git repository required. If no git: stop and recommend sequential `/implement` or single-tree work.

## Contract artifact (required before parallel work)
Write `docs/plans/<feature>-contract.md` (or section in the plan) containing:
- Endpoints / events / shared types
- Owner for shared types (backend | frontend | package path)
- Error and auth expectations
- Freeze stamp (date + “no divergent fields without re-freeze”)

## Steps
1. Plan Mode + plan critique (`/cold-review` or `/plan-review-loop`). Freeze contract artifact.
2. Prefer `/implement` for sequential high-rigor work when parallelism is unnecessary.
3. If parallel: spawn `gf-backend` and `gf-frontend` with `isolation: worktree`, **prepend** persona instructions, tags `[gf-backend]` / `[gf-frontend]`, capability_mode `all`.
4. Integrate via Grok **worktree apply** (or explicit merge); resolve conflicts; re-check contract artifact for drift.
5. Run **`/post-change-accuracy-protocol`** on integrated tree.
6. Lead-only spawns throughout (depth 1).

## Failure
Divergent contracts (fields/types not in freeze doc) → stop and re-freeze. Partial integration → NO-GO until protocol passes.
~~~~

---

## 7. Workflows (narrative only)

### `.grok/workflows/post-change-testing-protocol.md`

~~~~markdown
# Post-change testing (narrative)

Executable source of truth: `.grok/skills/post-change-accuracy-protocol/SKILL.md`.

1. Targeted unit + coverage  
2. `/review` (or SKIPPED per implement de-dupe)  
3. Regression  
4. `/check-work`  
5. Lead merge decision + waivers  

This file is **not** auto-loaded; AGENTS.md and the skill are.
~~~~

---

## 8. Reference docs (not auto-loaded)

### `.grok/docs/test-accuracy-standards.md`

~~~~markdown
# Test Accuracy Standards

## Good
- Fails when the bug is reintroduced.
- Edge/negative cases for non-trivial branches.
- Contract checks at boundaries.
- Mock I/O boundaries, not SUT internals.
- Deterministic (seed time/network); public interface over private guts.

## Blockers (NO-GO)
- Only mock call-order assertions on the SUT.
- Meaningless snapshot updates.
- Happy-path-only for error/auth code.
- Flaky time/network without control.

High coverage with inaccurate tests is still failure.
~~~~

### `.grok/docs/coverage-policy.md`

~~~~markdown
# Coverage Policy

- Default gate: **≥ 80%** new/changed executable lines when Coverage command is real in AGENTS.md.
- Proxy: changed-file % if line-level unavailable (note limitation in QA report).
- No tool: `NO COVERAGE TOOL` → durable waiver in `docs/waivers/` or add tooling before merge.
- Never invent percentages; use UNMEASURED if the tool ran but delta cannot be computed.
- Recipe hints (adapt to repo):
  - Python: pytest --cov + diff-cover against git diff when available
  - JS/TS: vitest/jest --coverage or nyc; prefer changed files if supported
  - Go: go test -coverprofile + go tool cover
- Waivers: scope, residual risk, follow-up, expiry.
- Not a substitute for test accuracy or `/review`.
~~~~

### `.grok/docs/privacy-safety.md`

~~~~markdown
# Privacy & safety

- Never commit or prompt-paste secrets.
- Prefer env / MCP for privileged ops.
- Classify Green / Yellow / Red sensitivity as a team (optional process).
- Verify current Grok cloud/remote data handling in official docs; do not assume upload semantics.
~~~~

---

## 9. Waivers

### `docs/waivers/README.md`

~~~~markdown
# Gate waivers

Durable record only. Chat LGTM is not a waiver.

## File name
`docs/waivers/<short-name>.md`

## Template

- **Date:**
- **Author:** (human user)
- **Scope:** paths / feature
- **Gate waived:** coverage | test-commands | review-bug | review-gap | regression-residual | other
- **Reason:**
- **Residual risk:**
- **Follow-up:**
- **Expiry:** date or event

Lead re-reads this directory before merge decisions.
~~~~

---

## 10. Acceptance fixtures

### `fixtures/agentic-template-acceptance/README.md`

~~~~markdown
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
~~~~

### `fixtures/agentic-template-acceptance/bad-plan.md`

~~~~markdown
# Bad plan (acceptance)

**Goal:** Make the app better.

## Steps
- Change some files
- Deploy

## Testing Strategy
Works correctly.

## Verification
It should work.
~~~~

### `fixtures/agentic-template-acceptance/seeded-bug-notes.md`

~~~~markdown
# Seeded bug

Example pure-function bug (Python illustration — use language-equivalent in-repo):

    def clamp(n, lo, hi):
        if n < lo:
            return lo
        if n < hi:  # BUG: should be <=
            return n
        return hi

Delete after verification.
~~~~

---

## 11. Implementation checklist

- [ ] Phase 0 git check (or degraded mode documented); timestamped AGENTS backup; no `.grokbuild/`; no shadowed persona names  
- [ ] `.grok/rules/accuracy-coverage.md` (gates + severity map + waiver pointer)  
- [ ] Four `gf-*` personas + non-empty instructions (read-verified)  
- [ ] Optional roles with “not spawn binding” note  
- [ ] Five skills with frontmatter + `disable-model-invocation: true` on orchestration skills  
- [ ] Workflows + docs + coverage recipe hints  
- [ ] Fixtures + `docs/waivers/README.md`  
- [ ] AGENTS.md: pipeline, de-dupe, severity map, Project Test Commands (closed Phase 3)  
- [ ] Phase 4 **V8 strict** (`grok inspect --json` skill names)  
- [ ] Phase 4 **V11 Fixture A** pass  
- [ ] Handoff with incomplete flags if V8/V11 failed  

---

## 12. Out of scope

- CI YAML generation  
- Mutation testing automation  
- Installing coverage tools for every language  
- Graphite automation (use `/pr-babysit` / `/execute-plan` when relevant)  
- Redefining bundled `/implement` behavior  
- Fixture B/C as bootstrap-complete criteria on empty product trees  
- Making persona/role resolution bind without prompt prepend (product limitation)

---

## How to use

In the target project:

> Read `grokbuild-agentic-dev-team-template-bootstrap.md` (v1.4). Implement the full template per Bootstrap Instructions. Optimize for code accuracy, test accuracy, and coverage. Prefer bundled `/review`, `/check-work`, and `/implement`. Complete Phase 4 including **strict** `grok inspect --json` and **Fixture A** before claiming done. Do not treat file presence alone as success.

---

## Changelog

### v1.4 (2026-07-12)
- Incorporated cold review of v1.3 (`*.review.md`).  
- **Git prerequisite** (Phase 0) + degraded mode when absent.  
- **Phase 3 closed:** no silent TODO; durable `docs/waivers/` for incomplete commands / gates.  
- **Strict V8:** `grok inspect --json` must list five project skills; CLI-missing ≠ pass.  
- **V11 Fixture A mandatory** for bootstrap complete; B/C deferred post-install.  
- **Implement vs `/review` de-dupe** rule; severity → gate map.  
- **`/check-work` semantics** clarified (session adequacy ≠ coverage %).  
- Persona/role: inject-only reliability; always set `capability_mode` on spawn.  
- `disable-model-invocation: true` on orchestration skills.  
- Parallel fullstack: required contract artifact path; git required.  
- Nested-fence fix: bootstrap embeds use `~~~~` / indent for schemas.  
- Coverage: no invented %; UNMEASURED; recipe hints; flake quarantine in regression.  
- Assumptions A9–A12; expanded risks / fail-to-ship / checklist.

### v1.3 (2026-07-12)
- Doc-accurate vs Grok 0.2.x: depth-1 spawning, capability matrix, persona inject pattern, session plan path.  
- Non-shadowing personas; harness-first pipeline; rules auto-load; V8 inspect (soft).  

### v1.2
- Moved to `.grok/`; SKILL.md packages; procedural testing; 80% gate; acceptance fixtures.

### v1.1
- Superseded: non-discoverable `.grokbuild/`, stub skills, `/skillify`.
