# Implementation Plan: GrokForge Agentic Dev Team Template Bootstrap

**Status:** Draft v2  
**Owner:** Lead Engineer (Grok Build)  
**Date:** 2026-07-12  
**Source document:** `grokbuild-agentic-dev-team-template-bootstrap.md` (v1.4) — **sole authority for file bodies**  
**Prior reviews:**  
- Source cold review (v1.3): `grokbuild-agentic-dev-team-template-bootstrap.review.md`  
- Plan Draft v1 cold reviews: `docs/plans/agentic-dev-team-template-bootstrap.review-{1,2,3}.md` (findings folded here)

---

## Goal

Install the GrokForge agentic team **config scaffold** into the target repository so that:

1. **Discovers** — Project skills and personas exist under real Grok paths (`.grok/skills/*/SKILL.md`, `.grok/personas/*.toml`) and the five skill names appear in `grok inspect --json`.
2. **Prefers harness** — Installed policy tells Lead to use bundled `/review`, `/check-work`, and `/implement` (when invoked) rather than reinventing them.
3. **Documents gates** — AGENTS + rules encode measurable gate *policy* (tests, coverage floor when a tool exists, test accuracy, durable waivers).  
   **Explicit:** Prompt pressure is **not** a hard OS gate. Bootstrap does **not** prove that ordinary “implement this” sessions will enforce gates.
4. **Proves install (scaffold only)** via:  
   - **Strict V8** — saved `grok inspect --json` evidence listing the five project skills  
   - **Mandatory V11** — Fixture A plan review with durable artifact and schema-level pass  
   - **V13** — targeted-loop dry-run that **fails closed** when Unit commands are NONE  
   - **Closed Phase 3** — every Project Test Command row is REAL, NONE, or TODO+waiver (never silent TODO)

**Success looks like (honest):**

| Status field | Meaning |
|--------------|---------|
| `bootstrap_status: COMPLETE` | V1–V11 + V13 pass; git full mode; content fidelity checks pass |
| `bootstrap_status: COMPLETE_DEGRADED` | Same proofs, but git degraded and/or worktree-dependent skills non-operational |
| `bootstrap_status: INCOMPLETE` | Any of V8, V11, V13, content fidelity, or Phase 3 open TODO without waiver failed |
| `accuracy_gates: OPERATIONAL` | Unit **and** Regression commands are REAL (Coverage REAL or durable coverage waiver) |
| `accuracy_gates: NOT_OPERATIONAL` | Unit or Regression is NONE/TODO/waived — **required** on empty/template-only repos |

**COMPLETE does not imply `accuracy_gates: OPERATIONAL`.** On this template repo they are expected to stay `NOT_OPERATIONAL` until product tooling lands and Fixture B/C pass.

---

## Non-goals

- Replacing `/implement`, `/review`, `/check-work`, `/code-review`, `/design`, `/execute-plan`.
- Shadowing bundled personas (`reviewer`, `implementer`, `test-writer`, `security-auditor`).
- Building product features or CI YAML.
- Hardcoding FastAPI/Next.js/any stack.
- Nested subagent trees (depth limit **1**).
- Assuming `.grok/docs/` or `.grok/workflows/` auto-load.
- Fixture B/C as bootstrap-complete criteria on empty product trees.
- Installing coverage tools for every language.
- Relying on persona/role **resolution** to bind spawn behavior (prepend only).
- Claiming accuracy/coverage **enforcement is proven** by V8/V11 alone.
- Treating roles as required for bootstrap (optional catalog metadata only).
- Paraphrasing bootstrap file bodies (“verbatim in spirit” is **forbidden**).

---

## Assumptions

| # | Assumption | Falsifier | If false |
|---|------------|-----------|----------|
| A1 | Skills load from `<repo>/.grok/skills/<name>/SKILL.md` | Names missing from inspect JSON | Fix path/frontmatter; status = INCOMPLETE |
| A2 | Personas catalog from `.toml` but do **not** auto-bind | Tag-only spawn = generic agent | Always read + prepend instruction md |
| A3 | `[tag]` in description is UI-only | Wrong tag only mislabels | Missing prepend is the real failure |
| A4 | Only parent can `spawn_subagent` (depth 1) | Child spawn errors | Lead orchestrates all loops |
| A5 | `read-only` has no shell | QA cannot run tests | Spawn tests with `execute` or `all` |
| A6 | Durable plans under `docs/plans/`; session plan under `~/.grok/sessions/...` (Windows: `%USERPROFILE%\.grok\sessions\...`) | Wrong path | Copy to `docs/plans/` before critique |
| A7 | Bundled `/review` + `/check-work` available; `/implement` slash-only | Missing from inspect | Document fallback; no parallel roots |
| A8 | Auto-load: root `AGENTS.md` + `.grok/rules/*.md` only | Policy ignored | Short gates in AGENTS/rules; full standards via `read_file` |
| A9 | Full protocol needs **git** (`projectRoot` = git root) | `git rev-parse` fails | Phase 0: init with OK, or COMPLETE_DEGRADED |
| A10 | Test commands filled or waived | Silent TODO | Phase 3 fails closed |
| A11 | Prompt pressure ≠ hard gate | Protocol skipped in normal use | Prefer slash skills; do not claim OS enforcement |
| A12 | `/check-work` = session adequacy, not coverage % | PASS without product tests | Never treat VERDICT as coverage proof |
| A13 | **File bodies = exact extract** from bootstrap v1.4 §1–10 fences | Required phrases missing | Re-extract; no paraphrase |
| A14 | `/cold-review` may be missing/unresolved | Not in inspect | V10 fallback; use `/plan-review-loop` for V11 |
| A15 | V11 must run in a **parent** session with spawn rights | Implementer is a depth-1 child | Mark V11 blocked/INCOMPLETE; do not fake review in Lead-only chat without recording `spawn_used: false` |
| A16 | Same-session skill discovery may require re-open or new session after writing skills | Slash/inspect misses new skills | Re-run inspect; if still missing, INCOMPLETE with recovery steps |

---

## Risks

| Risk | Mitigation |
|------|------------|
| Content divergence from v1.4 | Path↔section extract map + required-phrase checks (Phase 2.9) |
| Fence corruption | Document fence styles per path; schema field checklist |
| Ceremony without gate proof | V13 fail-closed dry-run; `accuracy_gates` status field |
| V11 keyword gaming | Schema pass criteria + durable artifact + gold-standard list |
| Self-review without spawn | Record `spawn_used`; prefer real spawn; flag if false |
| Double orchestration | De-dupe with defined artifacts; one orchestrator rule |
| Non-git / Windows PATH | Phase 0 + COMPLETE_DEGRADED; PowerShell notes |
| Silent TODO / waiver theater | NONE does not become OPERATIONAL via waiver |
| Re-bootstrap clobber | Phase 0 re-run matrix; timestamped backups |
| Partial install | Resume markers; do not claim COMPLETE mid-tree |
| Roles mistaken for binding | Install optional; AGENTS says “not spawn binding” |
| Parallel-fullstack overclaim | Install skill but handoff marks degraded if no git |

---

## Exploration findings

**Workspace / remote (2026-07-12):**

| Finding | Detail |
|---------|--------|
| GitHub | https://github.com/irichner/grokbuild-dev-team-template — `main` has bootstrap + this plan tree |
| Product app | None |
| Stack manifests | None → expect Project Test Commands = NONE |
| Prior plan | Draft v1 + three cold reviews; this is Draft v2 |
| Files to create | Root `AGENTS.md`; entire `.grok/**`; `docs/waivers/`; `fixtures/agentic-template-acceptance/` |
| Content source | **Only** bootstrap v1.4 sections 1–10 — copy, do not invent |
| OS | Author environment is Windows/PowerShell; commands must work or note Unix equivalents |

**Implication:** Config scaffold install. Prove discovery + plan-review path + fail-closed test loop. Do not claim accuracy gates operational until REAL unit/regression commands and (post-install) Fixture B/C.

---

## Content authority (mandatory)

### Rule

1. Open `grokbuild-agentic-dev-team-template-bootstrap.md` (v1.4).  
2. For each path below, extract the fenced body under that section heading.  
3. **Write the extracted body to disk unchanged in substance** (normalize line endings OK; do not rewrite gates, schemas, or steps).  
4. **Forbidden:** “verbatim in spirit,” paraphrased skills, stub personas.  
5. After write, run **required-phrase checks** (Phase 2.9).

### Fence extraction procedure

| Outer fence style in bootstrap | Paths |
|--------------------------------|--------|
| `~~~~markdown` / `~~~~toml` | Most bodies (AGENTS, README, rules, most personas, skills, workflows, docs, waivers, fixtures) |
| Five backticks `` ``` `` `` `markdown` | `gf-qa.md`, `gf-plan-reviewer.md` only |

**Steps:**

1. Find heading for path (e.g. `### \`.grok/personas/instructions/gf-qa.md\``).  
2. Open fence on next fence line; strip language tag.  
3. Close at matching close fence of same style.  
4. For QA/Review **schemas**: they are **indented plain-text blocks** inside the instruction files — preserve indentation; do not drop them.  
5. Do not leave fence markers inside the written file.

### Path ↔ bootstrap section map

| Write path | Bootstrap section |
|------------|-------------------|
| `AGENTS.md` | §1 |
| `.grok/README.md` | §2 |
| `.grok/rules/accuracy-coverage.md` | §3 |
| `.grok/personas/gf-backend.toml` | §4 |
| `.grok/personas/instructions/gf-backend.md` | §4 |
| `.grok/personas/gf-frontend.toml` | §4 |
| `.grok/personas/instructions/gf-frontend.md` | §4 |
| `.grok/personas/gf-qa.toml` | §4 |
| `.grok/personas/instructions/gf-qa.md` | §4 |
| `.grok/personas/gf-plan-reviewer.toml` | §4 |
| `.grok/personas/instructions/gf-plan-reviewer.md` | §4 |
| `.grok/roles/gf-qa.toml` | §5 (optional; install for catalog parity) |
| `.grok/roles/gf-plan-reviewer.toml` | §5 |
| `.grok/skills/plan-review-loop/SKILL.md` | §6 |
| `.grok/skills/targeted-unit-test-loop/SKILL.md` | §6 |
| `.grok/skills/regression-test-loop/SKILL.md` | §6 |
| `.grok/skills/post-change-accuracy-protocol/SKILL.md` | §6 |
| `.grok/skills/parallel-fullstack-feature/SKILL.md` | §6 |
| `.grok/workflows/post-change-testing-protocol.md` | §7 |
| `.grok/docs/test-accuracy-standards.md` | §8 |
| `.grok/docs/coverage-policy.md` | §8 |
| `.grok/docs/privacy-safety.md` | §8 |
| `docs/waivers/README.md` | §9 |
| `fixtures/agentic-template-acceptance/README.md` | §10 |
| `fixtures/agentic-template-acceptance/bad-plan.md` | §10 |
| `fixtures/agentic-template-acceptance/seeded-bug-notes.md` | §10 |

---

## Phases

### Phase 0 — Safety, prerequisites, re-run rules

**Objective:** Git posture, backups, install-mode decision, re-bootstrap rules.

#### 0.1 Git

- [ ] Run `git rev-parse --show-toplevel` (PowerShell/cmd same).  
- [ ] **OK** → `git_mode: full`.  
- [ ] **Fail** → ask user: (a) `git init` + initial commit with approval, or (b) config-only.  
  - (a) success → `git_mode: full`  
  - (b) → `git_mode: degraded` (max status COMPLETE_DEGRADED)

#### 0.2 Backups (first install or re-run)

- [ ] If root `AGENTS.md` exists: copy to `AGENTS.md.bak-before-agentic-template-<YYYYMMDD-HHMMSS>` (unique; never overwrite existing backups).  
- [ ] If `.grok/` already exists (re-bootstrap):

| Existing path | Action |
|---------------|--------|
| `.grok/skills/*`, personas, rules matching template names | **Overwrite** with bootstrap extract (template is source of truth for those paths) |
| Other `.grok/**` files not in map | **Leave** (do not delete unknown project files) |
| `docs/waivers/*.md` except README | **Leave** (never clobber human waivers) |
| `docs/plans/acceptance-bad-plan.md` | If exists, move to `docs/plans/acceptance-bad-plan.bak-<timestamp>.md` before re-copy |
| Custom edits inside mapped template files | Overwritten; operator must re-apply customs after — document in handoff |

#### 0.3 Forbidden names / roots

- [ ] Never create `.grokbuild/`.  
- [ ] Never create personas `reviewer`, `implementer`, `test-writer`, `security-auditor`.  
- [ ] Never create skills named `review` or `code-review`.

#### 0.4 Windows / shell notes

- [ ] Prefer `grok` on PATH; if missing try `where.exe grok` / `Get-Command grok`.  
- [ ] Use PowerShell-friendly commands in AGENTS when filling REAL commands later (avoid bash-only pipes unless repo uses them).  
- [ ] Session plans: `%USERPROFILE%\.grok\sessions\<encoded-cwd>\<session-id>\plan.md`.  
- [ ] CRLF vs LF: OK for markdown; ensure YAML frontmatter of SKILL.md still parses (no BOM).

#### 0.5 Partial-failure / rollback

- [ ] On abort mid-Phase-2: leave tree; write `docs/plans/bootstrap-install-state.md` with `phase: partial`, last file written.  
- [ ] Rollback: restore `AGENTS.md` from latest `.bak-*` if needed; delete `.grok/` only with **explicit user approval** (destructive).  
- [ ] Resume: re-run from Phase 0.2, then Phase 1–2 overwrite mapped paths.

**Phase verification:** `git_mode` known; backups done if needed; install-state file created if partial.

---

### Phase 1 — Directory structure

Create:

```
.grok/
├── README.md
├── rules/accuracy-coverage.md
├── personas/
│   ├── gf-backend.toml, gf-frontend.toml, gf-qa.toml, gf-plan-reviewer.toml
│   └── instructions/{gf-backend,gf-frontend,gf-qa,gf-plan-reviewer}.md
├── roles/                    # optional catalog only — NOT spawn binding
│   ├── gf-qa.toml
│   └── gf-plan-reviewer.toml
├── skills/
│   ├── plan-review-loop/SKILL.md
│   ├── targeted-unit-test-loop/SKILL.md
│   ├── regression-test-loop/SKILL.md
│   ├── post-change-accuracy-protocol/SKILL.md
│   └── parallel-fullstack-feature/SKILL.md
├── workflows/post-change-testing-protocol.md
└── docs/{privacy-safety,test-accuracy-standards,coverage-policy}.md
docs/
├── plans/                    # exists
├── waivers/README.md
└── (later) bootstrap-handoff.md, bootstrap-install-state.md, V8/V11 artifacts
fixtures/agentic-template-acceptance/{README,bad-plan,seeded-bug-notes}.md
```

- [ ] Create dirs; no forbidden paths.

**Phase verification:** Tree walk matches map; no `.grokbuild/`.

---

### Phase 2 — Write file contents (extract only)

- [ ] For each row in **Path ↔ bootstrap section map**, extract and write.  
- [ ] If merging AGENTS into existing project AGENTS: preserve non-template project rules; ensure template sections (pipeline, de-dupe, severity map, subagent rules, personas table, waivers, Project Test Commands) are present. Prefer replacing a prior GrokForge template block if `Template Version:` marker exists; else append template block under a clear heading and backup first.  
- [ ] After all writes: **Phase 2.9 content fidelity checks**.

#### Phase 2.9 — Required phrases (fail = re-extract)

| File | Must contain (substring checks) |
|------|----------------------------------|
| `AGENTS.md` | `post-change-accuracy-protocol`, `de-dupe` or `De-dupe`, `docs/waivers`, `Project Test Commands`, `gf-backend`, `capability_mode`, `≥ 80%` or `80%` |
| `.grok/rules/accuracy-coverage.md` | `docs/waivers`, `gap`, `capability_mode`, `test-accuracy-standards` |
| `gf-qa.md` | `QA Test Report`, `Recommendation: GO`, `NO COVERAGE TOOL` or `UNMEASURED`, `test-accuracy-standards` |
| `gf-plan-reviewer.md` | `Review Report`, `Request Changes`, `bug|gap` or `bug\|gap` |
| Each skill `SKILL.md` | YAML `name:`, `description:`, `disable-model-invocation: true` |
| `targeted-unit-test-loop/SKILL.md` | `80%`, `gf-qa`, `execute` |
| `post-change-accuracy-protocol/SKILL.md` | `SKIPPED` or `de-dupe` / implement, `check-work` |
| `parallel-fullstack-feature/SKILL.md` | `contract`, `worktree`, `git` |
| `docs/waivers/README.md` | `Expiry`, `Residual risk`, `Gate waived` |
| `fixtures/.../bad-plan.md` | `Works correctly` |

- [ ] Roles files: if installed, AGENTS must still say roles are **not** spawn binding.  
- [ ] Read each of four instruction files; confirm non-empty and schema blocks present for QA + plan-reviewer.

**Phase verification:** All map paths exist; Phase 2.9 all pass; no paraphrase drift.

---

### Phase 3 — Project Test Commands (closed) + accuracy_gates flag

- [ ] Scan: `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `Makefile`, CI configs, README, `*.sln` / `*.csproj` if present.  
- [ ] Record scan evidence in handoff (`scanned_paths: [...]`, `found: [...]`).  
- [ ] Fill each AGENTS row with **exactly one**:

| Outcome | When | Gate impact |
|---------|------|-------------|
| Real command | Found | Skills use it |
| `NONE — no tool in repo` | Scanned, absent | Not OPERATIONAL for that capability |
| `TODO` + `docs/waivers/bootstrap-test-commands.md` | Ambiguous | Must list rows, residual risk, expiry; **still NOT_OPERATIONAL** if Unit/Regression incomplete |

**accuracy_gates rules:**

- [ ] If Unit is REAL **and** Regression is REAL **and** (Coverage REAL **or** coverage waiver exists) → may set `accuracy_gates: OPERATIONAL` only after first successful targeted+regression run (usually post-product).  
- [ ] If Unit or Regression is NONE/TODO/waived → **must** set `accuracy_gates: NOT_OPERATIONAL`.  
- [ ] A waiver **never** upgrades `accuracy_gates` to OPERATIONAL.

**This template repo expectation:** all NONE (or waived TODO) → `accuracy_gates: NOT_OPERATIONAL`.

**Phase verification:** No bare TODO; `accuracy_gates` set correctly; waiver file present if any TODO.

---

### Phase 4 — Bootstrap verification

| # | Check | Pass criteria |
|---|--------|----------------|
| V1 | Tree | Map paths exist; no `.grokbuild/`; no forbidden persona names |
| V2 | Skill shape | Each skill has `name` + `description` + `disable-model-invocation: true` |
| V3 | Personas | Four toml + four non-empty instructions; 2.9 phrases for QA/plan-reviewer |
| V4 | Rules | accuracy-coverage has gates + severity + waiver pointer |
| V5 | AGENTS | Pipeline, de-dupe, severity, commands, waivers |
| V6 | Non-stub skills | Numbered steps; post-change has implement skip path |
| V7 | Fixtures + waivers README | Present |
| V8 | **Discovery (strict)** | See below |
| V9 | Protocol map | Print order + de-dupe rule to handoff |
| V10 | Cold-review probe | Note present/absent/unresolved in handoff |
| V11 | **Fixture A** | See below |
| V12 | Fixture B/C | Not required; document readiness (below) |
| V13 | **Fail-closed targeted dry-run** | See below |

#### V8 — Discovery (strict)

- [ ] Run `grok inspect --json` from repo root (git root if full mode).  
- [ ] Save raw output to `docs/plans/bootstrap-v8-inspect.json` (or `.txt` if not valid JSON).  
- [ ] Assert these **names** appear as project/local/repo skills (not only as unrelated plugins):  
  `plan-review-loop`, `targeted-unit-test-loop`, `regression-test-loop`, `post-change-accuracy-protocol`, `parallel-fullstack-feature`  
- [ ] **Fail** if any missing.  
- [ ] If CLI unavailable: **do not pass V8**; `bootstrap_status: INCOMPLETE`; list names for user verification.  
- [ ] Optional: note whether personas appear in UI/`/personas` — not required for V8 pass, record as V8b if checked.

#### V11 — Fixture A (behavioral)

**Gold-standard concerns** (review must cover at least 2 of these concretely, not one keyword):

1. Goal is non-measurable (“make the app better”).  
2. Steps lack concrete files/behaviors.  
3. Testing Strategy is non-observable (“Works correctly”).  
4. Verification is non-observable (“It should work”).  

**Procedure:**

1. Copy `fixtures/agentic-template-acceptance/bad-plan.md` → `docs/plans/acceptance-bad-plan.md` (backup first if exists).  
2. Prefer `/cold-review` if V10 says available; else `/plan-review-loop` or Lead re-enacts skill steps with spawn.  
3. **Spawn recipe (Lead parent only):**  
   - `read_file` `.grok/personas/instructions/gf-plan-reviewer.md`  
   - Prepend full text to child prompt  
   - `subagent_type`: `explore` or `general-purpose` with `capability_mode: read-only`  
   - `description`: `[gf-plan-reviewer] Fixture A plan review`  
   - Prompt includes plan path + Review Report schema + “Do not edit product code”  
4. Write durable artifact: `docs/plans/acceptance-bad-plan.review.md` containing Review Report fields.  
5. Record in handoff: `spawn_used: true|false` (false → note limitation; still require schema-quality report).

**Pass (all required):**

- Overall is `Request Changes` or `Major Concerns` (**Approve = fail V11**; one retry allowed, then fail).  
- Non-empty section on test/coverage or verification gaps.  
- At least one Required Change with severity `bug` or `gap` tied to verification/testing.  
- At least **2** gold-standard concerns addressed in substance.  
- Durable review file exists.

#### V13 — Targeted loop fail-closed dry-run

When Unit command is NONE or TODO without REAL command:

- [ ] Lead runs targeted-loop **steps** (or slash skill if available): read AGENTS commands → conclude NO-GO.  
- [ ] Write `docs/plans/bootstrap-v13-targeted-dry-run.md` with: commands seen, result `NO-GO`, reason `Unit tests command not REAL`.  
- [ ] **Pass:** explicit NO-GO (proves gate fails closed).  
- [ ] If Unit is REAL: run real targeted selection on a trivial path or document skip with reason; still record artifact.

#### De-dupe definitions (install into skills/AGENTS; operational for later)

| Term | Definition |
|------|------------|
| Open bugs | `/review` or implement issue list with severity `bug` and status open |
| Gate-mapped gaps | Open `suggestion` about missing tests / correctness / security / data loss → treat as gap; **blocks** skip |
| Tree match | `git status --porcelain` empty for paths in review scope, or same HEAD as implement review + no unstaged changes to those paths |
| Skip `/review` allowed only if | Clean `/implement` + zero open bugs + zero gate-mapped gaps + tree match; record skip reason in protocol summary |

#### Fixture B/C readiness (V12 — post-install, not bootstrap complete)

Ready when **all** true:

1. `accuracy_gates` can become OPERATIONAL (Unit + Regression REAL).  
2. At least one product module/source tree exists.  
3. For C: Coverage command REAL.  
4. On throwaway branch: run B then C per `fixtures/agentic-template-acceptance/README.md`.  
5. Record results under `docs/plans/fixture-b-result.md` / `fixture-c-result.md`.

**Phase verification:** V1–V11, V13 done with artifacts; V12 readiness text in handoff.

---

### Phase 5 — Handoff

Write durable handoff: **`docs/plans/bootstrap-handoff.md`**.

Required fields:

```markdown
# Bootstrap handoff

- Date:
- Template version: 1.4
- bootstrap_status: COMPLETE | COMPLETE_DEGRADED | INCOMPLETE
- accuracy_gates: OPERATIONAL | NOT_OPERATIONAL
- git_mode: full | degraded
- V8: PASS|FAIL (path to inspect artifact)
- V10 cold-review: available | absent | unresolved
- V11: PASS|FAIL (path to review artifact; spawn_used)
- V13: PASS|FAIL (path to dry-run artifact)
- Project Test Commands: (each row REAL|NONE|TODO+waiver)
- Files created/updated: (list)
- Waivers present:
- Next steps: fill commands / Fixture B/C when ready
- Reminders: prepend personas; tags UI-only; set capability_mode; roles not binding
```

- [ ] Do **not** set COMPLETE if V8, V11, V13, or 2.9 failed.  
- [ ] Ask user to confirm waivers / fill commands if needed.  
- [ ] Point to Fixture B/C readiness.

**Phase verification:** Handoff file exists with all fields; status consistent with evidence.

---

## Implementation order (DAG)

```text
Phase 0 ──► Phase 1 ──► Phase 2 (sequential writes OK; parallel only if no partial handoff risk)
                    └──► Phase 2.9 fidelity
                         Phase 3 (scan + AGENTS commands + accuracy_gates)
                         Phase 4 (V1–V13; parent session for V11)
                         Phase 5 (bootstrap-handoff.md)
```

---

## Spawn cookbook (copy into operator muscle memory)

### Plan reviewer

```
read_file .grok/personas/instructions/gf-plan-reviewer.md
spawn_subagent:
  subagent_type: explore   # or general-purpose + capability_mode: read-only
  capability_mode: read-only
  description: [gf-plan-reviewer] plan review
  prompt: <full instruction md> + plan path + Review Report schema + no product edits
```

### QA / tests

```
read_file .grok/personas/instructions/gf-qa.md
spawn_subagent:
  subagent_type: general-purpose
  capability_mode: execute   # or all — never read-only
  description: [gf-qa] targeted tests
  prompt: <full instruction md> + scope + AGENTS commands + QA Test Report schema
```

### Backend / frontend implementer

```
read_file .grok/personas/instructions/gf-backend.md  # or gf-frontend
spawn:
  capability_mode: all
  description: [gf-backend] implement …
  prompt: <full instruction md> + plan + constraints
  isolation: worktree  # only if git_mode full
```

**Never** rely on role TOML or persona `default_capability_mode` alone for the inject path.

---

## Waiver lifecycle

| Rule | Detail |
|------|--------|
| Path | `docs/waivers/<short-name>.md` only |
| Author | Human user name required; agent may draft but human must confirm (record confirmer) |
| Required fields | Date, Author, Scope, Gate waived, Reason, Residual risk, Follow-up, Expiry |
| Expiry | If past expiry (or event reached) → gate **re-armed**; ignore waiver |
| Lead before merge | List `docs/waivers/`, filter unexpired, apply only matching scope |
| Chat LGTM | Not a waiver |
| bootstrap-test-commands | Allowed for incomplete rows; does **not** set accuracy_gates OPERATIONAL |

---

## Canonical policy (must be in extracted AGENTS/skills)

### Severity → gate

| Source | Effect |
|--------|--------|
| `/review` bug open | Block |
| suggestion: tests/correctness/security/data-loss | gap → block |
| other suggestion / nit | non-blocking |
| QA circular / happy-path-only auth-error | gap → block |
| Plan Required Changes bug\|gap | Block implement until fixed or durable waiver |

### Implement vs `/review` de-dupe

| Situation | Action |
|-----------|--------|
| Clean implement + zero bugs + zero gate-gaps + tree match | Skip `/review`; record reason |
| Else / manual implement / user request | Run `/review` |

### Runtime hard rules

1. Lead-only spawn (depth 1).  
2. Prepend instruction files.  
3. Tags = UI only.  
4. Always set `capability_mode` on spawn.  
5. Worktrees need git.  
6. `/check-work` → `VERDICT` = session adequacy only.  
7. One orchestrator at a time.  
8. Do not shadow bundled `test-writer` name.

---

## Verification criteria (whole feature)

Bootstrap is **COMPLETE** or **COMPLETE_DEGRADED** only if:

1. Content fidelity (2.9) pass for all mapped files.  
2. Phase 3 closed; `accuracy_gates` set correctly (expected NOT_OPERATIONAL on empty repo).  
3. V8 pass with saved inspect artifact listing five skills.  
4. V11 pass with durable review artifact meeting schema + gold-standard bar.  
5. V13 pass with dry-run NO-GO (when unit not REAL) or documented real run.  
6. Handoff file written with consistent status.

**COMPLETE_DEGRADED** if above hold but `git_mode: degraded`.

**INCOMPLETE** otherwise — tree may exist; do not market as done.

---

## Out-of-scope

- CI YAML, mutation testing, installing all coverage tools  
- Graphite automation  
- Redefining `/implement` internals  
- Fixture B/C as bootstrap-complete on empty trees  
- Hard OS enforcement of gates  
- Byte-identical round-trip of bootstrap fences (line endings / fence markers stripped is OK)  
- Making role resolution bind without prepend  

---

## How would this fail to ship?

1. Paraphrased skills pass shape checks but drop de-dupe/coverage rules.  
2. Skills not in inspect → V8 fail ignored → false done.  
3. V11 Approve or keyword-only report → false behavioral proof.  
4. V11 faked without spawn in child session topology.  
5. Unit NONE + waiver → claim accuracy_gates OPERATIONAL.  
6. Tag-only QA spawn → no schema, invented coverage %.  
7. Non-git COMPLETE without DEGRADED label.  
8. Re-bootstrap clobbers human waivers or customs without backup.  
9. Fence extract drops QA schema indent block.  
10. V13 skipped → never prove fail-closed.  
11. Chat-only waiver / expired waiver still used.  
12. Roles treated as binding → wrong capability_mode.

---

## Acceptance checklist

- [ ] Phase 0 git mode + backups + re-run rules  
- [ ] Phase 1 tree  
- [ ] Phase 2 exact extracts for all map paths  
- [ ] Phase 2.9 phrase checks  
- [ ] Phase 3 commands closed + accuracy_gates  
- [ ] V8 inspect artifact + five names  
- [ ] V10 cold-review note  
- [ ] V11 durable review + gold standards  
- [ ] V13 dry-run artifact  
- [ ] Phase 5 `docs/plans/bootstrap-handoff.md` with honest status  

---

## Suggested execution prompt

> Read `docs/plans/agentic-dev-team-template-bootstrap.md` (Draft v2) and extract all file bodies from `grokbuild-agentic-dev-team-template-bootstrap.md` (v1.4) using the path↔section map. Do not paraphrase. Execute Phases 0–5. Save V8/V11/V13 artifacts and `docs/plans/bootstrap-handoff.md`. Set `accuracy_gates: NOT_OPERATIONAL` if Unit/Regression are not REAL. Claim COMPLETE only if V8, V11, V13, and content fidelity pass. Prefer bundled `/review`, `/check-work`, `/implement`. On Windows, use PowerShell-safe commands.

---

## Changelog (v1 → v2)

| Change | Why (cold review) |
|--------|-------------------|
| Goal no longer claims bootstrap proves enforcement | R1 |
| `bootstrap_status` + `accuracy_gates` enums | R1, R2, R3 |
| Forbidden “verbatim in spirit”; extract map + 2.9 phrases | R2, R3 |
| V8 saved artifact + strict fail | R1, R2 |
| V11 gold standards, durable file, Approve=fail, spawn_used | R1, R3 |
| V13 fail-closed targeted dry-run | R1 |
| De-dupe operational definitions | R1 |
| Re-run / backup / partial / rollback | R3 |
| Waiver lifecycle + expiry re-arm | R3 |
| Fixture B/C readiness criteria | R3 |
| Spawn cookbook; roles not binding | R2 |
| Windows/PowerShell notes | R2 |
| COMPLETE ≠ OPERATIONAL explicit | All three |
