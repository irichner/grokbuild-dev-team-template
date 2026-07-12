# Implementation Plan: GrokForge Agentic Dev Team Template Bootstrap

**Status:** Draft v1  
**Owner:** Lead Engineer (Grok Build)  
**Date:** 2026-07-12  
**Source document:** `grokbuild-agentic-dev-team-template-bootstrap.md` (v1.4)  
**Prior cold reviews of source:** `grokbuild-agentic-dev-team-template-bootstrap.review.md` (v1.3 findings; folded into v1.4)

---

## Goal

Install a complete Grok-native agentic software-development team configuration into the target repository so that Grok:

1. **Discovers** project skills and personas under real paths (`.grok/skills/*/SKILL.md`, `.grok/personas/*.toml`).
2. **Prefers** bundled harness skills (`/review`, `/check-work`, `/implement` when invoked) rather than reinventing them.
3. **Enforces** measurable gates: tests pass, coverage floor when a tool exists, test-accuracy standards, and no open bug/gap without a durable waiver under `docs/waivers/`.
4. **Proves** install with **strict** `grok inspect --json` skill listing (V8) **and** mandatory Fixture A behavioral plan-review (V11) — not file-tree ceremony alone.

**Success looks like:** After bootstrap, the five project skill names appear in `grok inspect --json`, Fixture A yields Request Changes / Major Concerns citing verification or testing gaps, Project Test Commands are closed (REAL / NONE / waived TODO), and handoff states V8–V11 results explicitly. Operational accuracy/coverage enforcement is documented and ready for the first product change; Fixture B/C remain post-install on product code.

---

## Non-goals

- Replacing or reimplementing `/implement`, `/review`, `/check-work`, `/code-review`, `/design`, or `/execute-plan`.
- Shadowing bundled persona names (`reviewer`, `implementer`, `test-writer`, `security-auditor`).
- Building product application features or generating CI provider YAML.
- Hardcoding FastAPI, Next.js, or any specific stack as mandatory.
- Nested subagent trees (Grok depth limit is 1).
- Assuming `.grok/docs/` or `.grok/workflows/` auto-load into context (they do not).
- Running Fixture B (seeded bug) or Fixture C (coverage hole) as bootstrap-complete criteria on a template-only / empty product tree.
- Installing coverage tooling for every language ecosystem.
- Relying on undocumented persona/role resolution to bind spawn behavior (inject/prepend is the only reliable path).
- Claiming bootstrap “done” if V8 or V11 fail.

---

## Assumptions

| # | Assumption | Falsifier | If false |
|---|------------|-----------|----------|
| A1 | Project skills load from `<repo>/.grok/skills/<name>/SKILL.md` with valid frontmatter | Skill names missing from `grok inspect --json` | Fix path/frontmatter; **do not claim bootstrap done** |
| A2 | Personas load into catalog from `.grok/personas/*.toml` but do **not** auto-bind on spawn | Spawn with only `[gf-qa]` tag and no prepended body acts as generic agent | Lead/skills must read + prepend instruction files on every spawn |
| A3 | `[tag]` in spawn `description` is pager UI only | Wrong tag only mislabels | Missing prepend is the real failure; keep tags for UX only |
| A4 | Only the parent session can `spawn_subagent` (depth 1) | Child spawn errors | All loops orchestrated by Lead; no nested skill auto-fire from children |
| A5 | `capability_mode: read-only` has no shell (no git, no tests) | QA cannot run test commands | Always set `execute` or `all` on spawn for test runners |
| A6 | Durable plans live in `docs/plans/` after Plan Mode allows non-plan writes / after exit; session plan is under `~/.grok/sessions/.../plan.md` | Reviewer finds empty or wrong plan path | Copy session plan to `docs/plans/<name>.md` before critique |
| A7 | Bundled `/review` and `/check-work` remain available; `/implement` is slash-only | Skill missing from inspect | Document fallback / install bundled skills; do not invent parallel roots |
| A8 | Auto-loaded rules are root `AGENTS.md` + `.grok/rules/*.md` only | Policy ignored in practice | Put short gates in AGENTS + rules; long prose in `.grok/docs/` with explicit `read_file` in skills |
| A9 | Target is a **git** repository for full protocol (`projectRoot` = git root) | `git rev-parse` fails; `projectRoot: null` | Phase 0: `git init` with user OK, or config-only degraded mode |
| A10 | Project Test Commands are filled from manifests **or** durable waiver exists | Silent `TODO` forever | Phase 3 fails closed |
| A11 | Prompt pressure is not a hard OS gate; Lead can skip protocol | Ordinary “implement this” skips post-change | Prefer explicit slash skills; Fixture A proves plan-review path only |
| A12 | `/check-work` is session-adequacy verification, not a coverage meter | Bootstrap session PASSes without product tests | Do not treat VERDICT alone as coverage proof |
| A13 | Source of truth for file bodies is bootstrap v1.4 sections 1–10; extraction uses section path headings and `~~~~` / indented schemas to avoid fence corruption | Truncated QA/Review report schemas | Re-read bootstrap section; prefer write from bootstrap, not improvised stubs |
| A14 | Plugin `/cold-review` may be missing or `[compat unresolved]` in this workspace | Inspect does not list cold-review | Fallback `/plan-review-loop`; V10 documents status; do not claim cold-review works |

---

## Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Shadow bundled personas | Catalog collision; wrong specialist behavior | Prefix only `gf-*`; never create `reviewer.toml` etc. |
| Double review loop (`/implement` then `/review`) | Token waste or skipped gates | De-dupe rule: skip `/review` only after clean implement + zero open bugs + tree match |
| `read-only` QA cannot run tests | False NO-GO or invented results | Explicit `capability_mode: execute\|all` on every QA spawn |
| Silent TODO test commands | Gates never operational | Phase 3 closed outcomes only; waiver path required |
| Non-git directory | `/review` local mode, worktrees, diff selection fail | Phase 0 gate; degraded handoff |
| Waiver evaporates | Next session re-blocks or silently GO | Only `docs/waivers/*.md` counts |
| Severity taxonomy mismatch | Inconsistent merge decisions | Severity → gate map in AGENTS + rules |
| Nested fence corruption extracting bootstrap | Malformed skills/personas | Use bootstrap `~~~~` sections; verify non-empty instruction files |
| Skill auto-invoke mid-implement | Concurrent orchestrators; depth errors | `disable-model-invocation: true` on orchestration skills |
| Roles treated as spawn binding | Capability defaults never applied | Roles optional; always prepend + set capability on spawn |
| V8 soft-pass if CLI “unavailable” | Ship without discovery proof | **Strict V8:** CLI unavailable = bootstrap incomplete |
| Fixture A skipped under time pressure | No behavioral proof | V11 mandatory for “bootstrap done” |
| AGENTS.md merge loss | Project-specific rules deleted | Timestamped backup; never overwrite existing `.bak-*` |
| Parallel fullstack on non-git / empty product | Skill claims more than it can deliver | Prerequisites check; sequential `/implement` recommended |

---

## Exploration findings

**Workspace reality (2026-07-12):**

| Finding | Detail |
|---------|--------|
| Repo contents | Only `grokbuild-agentic-dev-team-template-bootstrap.md` and prior `.review.md` at root; no product app |
| `docs/plans/` | Did not exist before this plan; no `_archive/` |
| Git | Bootstrap assumes git may be absent; Phase 0 must check `git rev-parse --show-toplevel` |
| Product stack | None — Project Test Commands expected to resolve to `NONE` or waived `TODO` for unit/coverage/regression |
| Prior art | Source bootstrap v1.4 already incorporates v1.1/v1.3 cold-review fixes (`.grok/` paths, SKILL.md shape, gf-* personas, harness-first, durable waivers, strict V8, Fixture A) |
| Files most likely touched | Root `AGENTS.md`; entire `.grok/**` tree; `docs/waivers/`; `docs/plans/` (fixture copy); `fixtures/agentic-template-acceptance/` |
| Patterns | No existing project skills/personas to match — **create from bootstrap sections 1–10 verbatim in spirit** (same structure, gates, schemas) |
| Tests/fixtures | Acceptance fixtures are part of the deliverable, not pre-existing product tests |
| Collisions to avoid | Do not create skill named `review` / `code-review`; do not create personas shadowing bundled names; do not create `.grokbuild/` |

**Implication:** This implementation is a **config scaffold install**, not a product feature. Verification is discovery + Fixture A, not app test green. First real feature branch must run Fixture B/C when product code exists.

---

## Phases

### Phase 0 — Safety & prerequisites

**Objective:** Establish git posture and protect existing project rules before writing anything under `.grok/`.

- [ ] Run `git rev-parse --show-toplevel`
- [ ] If fail: present user choice — (a) `git init` with explicit approval, or (b) config-only **degraded** install; record choice in handoff
- [ ] If degraded: document that `/review` local mode, worktrees, and git-diff test selection are non-operational; do not claim parallel-fullstack fully works
- [ ] If root `AGENTS.md` exists: copy to `AGENTS.md.bak-before-agentic-template-<YYYYMMDD>` (do not overwrite an existing backup with the same or different timestamp if a prior bootstrap backup already exists — use unique timestamp)
- [ ] Confirm working tree will use **`.grok/` only** (never `.grokbuild/`)
- [ ] Confirm persona names will be `gf-*` only (no bundled name collisions)

**Phase verification:** Git status known (full vs degraded); backup policy applied if AGENTS existed; no writes yet that violate naming rules.

---

### Phase 1 — Directory structure

**Objective:** Create the full path tree (empty shells ok if contents land in Phase 2).

Create exactly:

```
.grok/
├── README.md
├── rules/
│   └── accuracy-coverage.md
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
├── roles/
│   ├── gf-qa.toml
│   └── gf-plan-reviewer.toml
├── skills/
│   ├── plan-review-loop/SKILL.md
│   ├── targeted-unit-test-loop/SKILL.md
│   ├── regression-test-loop/SKILL.md
│   ├── post-change-accuracy-protocol/SKILL.md
│   └── parallel-fullstack-feature/SKILL.md
├── workflows/
│   └── post-change-testing-protocol.md
└── docs/
    ├── privacy-safety.md
    ├── test-accuracy-standards.md
    └── coverage-policy.md
docs/
├── plans/                    # may already exist (this plan)
└── waivers/
    └── README.md
fixtures/
└── agentic-template-acceptance/
    ├── README.md
    ├── bad-plan.md
    └── seeded-bug-notes.md
```

- [ ] Create all directories above
- [ ] Do **not** create `.grokbuild/`
- [ ] Do **not** create skill dirs named `review` or `code-review`
- [ ] Do **not** create persona files named `reviewer.toml`, `implementer.toml`, `test-writer.toml`, `security-auditor.toml`

**Phase verification:** Tree walk matches Phase 1 list; forbidden paths absent.

---

### Phase 2 — Write file contents

**Objective:** Populate every file from bootstrap v1.4 sections 1–10. Extraction: content under each path heading; report schemas use plain indented blocks / tilde fences so triple-backtick extractors do not truncate.

#### 2.1 Root AGENTS.md (Section 1)

- [ ] Write/merge root `AGENTS.md` with: harness-first pipeline, implement/review de-dupe, trivial escape hatch, accuracy gates, severity map, subagent rules, `gf-*` personas table, skill capture (`/create-skill`), secrets, waivers path, Project Test Commands placeholders
- [ ] If merging with existing AGENTS: preserve project-specific rules; keep AGENTS short (actionable gates + commands); do not delete unique project content

#### 2.2 `.grok/README.md` (Section 2)

- [ ] What auto-loads vs reference-only table
- [ ] Prefer bundled skills list
- [ ] Git required note
- [ ] Deprecated `.grokbuild/` note

#### 2.3 Auto-loaded rules (Section 3)

- [ ] `.grok/rules/accuracy-coverage.md`: gates, severity map, test-accuracy summary, orchestration rules, waiver pointer, `read_file` mandate for full test-accuracy standards

#### 2.4 Personas (Section 4)

- [ ] `gf-backend.toml` + `instructions/gf-backend.md` (non-empty)
- [ ] `gf-frontend.toml` + `instructions/gf-frontend.md` (non-empty)
- [ ] `gf-qa.toml` + `instructions/gf-qa.md` including QA Test Report schema and coverage measurement notes
- [ ] `gf-plan-reviewer.toml` + `instructions/gf-plan-reviewer.md` including Review Report schema
- [ ] Each toml has `description` and `instructions_file` (or `instructions`); paths resolve

#### 2.5 Optional roles (Section 5)

- [ ] `.grok/roles/gf-qa.toml` and `gf-plan-reviewer.toml`
- [ ] Document in skill text / AGENTS that roles are **not** spawn binding

#### 2.6 Skills (Section 6)

For each skill: YAML frontmatter with `name`, `description`, and `disable-model-invocation: true`.

- [ ] `plan-review-loop`: prefer cold-review when inspect shows it; prepend gf-plan-reviewer; Lead-only spawn; max 2 passes; residual Major Concerns → durable waiver
- [ ] `targeted-unit-test-loop`: git changed files; command from AGENTS; coverage gate; accuracy standards read; QA report; max 3 fix cycles
- [ ] `regression-test-loop`: Quick vs Extended triggers; flake re-run ≤2 + quarantine in report; exit 0 or durable waiver
- [ ] `post-change-accuracy-protocol`: order targeted → review (de-dupe) → regression → check-work → merge decision; ownership rule vs concurrent `/implement`
- [ ] `parallel-fullstack-feature`: git prerequisite; contract artifact path `docs/plans/<feature>-contract.md`; worktree spawn; post-change protocol; re-freeze on drift

#### 2.7 Workflows + reference docs (Sections 7–8)

- [ ] `.grok/workflows/post-change-testing-protocol.md` (narrative pointer to skill)
- [ ] `.grok/docs/test-accuracy-standards.md`
- [ ] `.grok/docs/coverage-policy.md` (80% gate, proxy, recipes, UNMEASURED)
- [ ] `.grok/docs/privacy-safety.md`

#### 2.8 Waivers + fixtures (Sections 9–10)

- [ ] `docs/waivers/README.md` with template fields (date, author, scope, gate, residual risk, follow-up, expiry)
- [ ] `fixtures/agentic-template-acceptance/README.md` (A mandatory; B/C post-install)
- [ ] `fixtures/.../bad-plan.md` (non-observable verification intentionally weak)
- [ ] `fixtures/.../seeded-bug-notes.md` (language-agnostic bug sketch)

**Phase verification:** Every path from Phase 1 has non-empty content matching bootstrap intent; each persona instruction file readable and non-empty; each skill has frontmatter `name` + `description` + `disable-model-invocation: true`; no truncated schema (QA report and Review report blocks present).

---

### Phase 3 — Project Test Commands (closed)

**Objective:** Fill AGENTS.md Project Test Commands from repo reality; no silent permanent TODO.

- [ ] Scan manifests and scripts: `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `Makefile`, CI configs, README
- [ ] For each row (Build, Unit tests, Coverage, Regression/full suite, Lint/typecheck), set **exactly one** outcome:

| Outcome | When | Gate impact |
|---------|------|-------------|
| Real command string | Found in repo | Skills use it |
| `NONE — no tool in repo` | Scanned, absent | Coverage → `NO COVERAGE TOOL`; merge needs waiver or tooling |
| `TODO` + durable waiver | Ambiguous after scan | Write `docs/waivers/bootstrap-test-commands.md` listing incomplete rows + residual risk; get user fill or confirm |

- [ ] If Unit and Regression both NONE/TODO without waiver: install may complete files but handoff **must not** claim accuracy gates operational
- [ ] For this template-only workspace: expect NONE or waived TODO for unit/coverage/regression; document that clearly

**Phase verification:** No Project Test Command row is bare `TODO` without a linked waiver file; AGENTS.md reflects REAL / NONE / waived status.

---

### Phase 4 — Bootstrap verification (mandatory)

**Objective:** Prove discovery and behavioral plan-review; static tree alone is insufficient.

| # | Check | Pass criteria | Status |
|---|--------|---------------|--------|
| V1 | Tree | Phase 1 paths exist; no `.grokbuild/`; no forbidden persona filenames | [ ] |
| V2 | Skill shape | Each project skill is `SKILL.md` with YAML `name` + `description` | [ ] |
| V3 | Persona files | Each `gf-*.toml` has description + instructions path; each instructions file non-empty (read-verified) | [ ] |
| V4 | Auto-load rules | `.grok/rules/accuracy-coverage.md` has gates + severity map + waiver pointer | [ ] |
| V5 | AGENTS.md | Pipeline + de-dupe + severity map + Project Test Commands + waiver path | [ ] |
| V6 | Non-stub skills | Targeted + regression have numbered steps + QA schema references; post-change has implement de-dupe | [ ] |
| V7 | Fixtures | Acceptance fixtures present; `docs/waivers/README.md` present | [ ] |
| V8 | **Discovery (strict)** | `grok inspect --json` lists skill names: `plan-review-loop`, `targeted-unit-test-loop`, `regression-test-loop`, `post-change-accuracy-protocol`, `parallel-fullstack-feature` (project/local/repo source). **Missing → fail.** CLI unavailable → **do not pass**; handoff incomplete | [ ] |
| V9 | Protocol map | Print post-change order including implement/review de-dupe | [ ] |
| V10 | Cold-review probe | Note if `/cold-review` in inspect; if absent, document fallback-only | [ ] |
| V11 | **Fixture A (behavioral)** | Copy `fixtures/.../bad-plan.md` → `docs/plans/acceptance-bad-plan.md`; run `/plan-review-loop` or `/cold-review`. **Pass:** overall Request Changes or Major Concerns **and** mentions verification and/or testing gaps. Cannot run → V11 fail, bootstrap incomplete | [ ] |
| V12 | Fixture B/C | Not required for bootstrap complete; document as post-install | [ ] |

- [ ] Execute V1–V11 in order; record pass/fail with evidence (commands, excerpts)
- [ ] On V8 or V11 fail: stop claiming done; handoff status = incomplete

**Phase verification:** All of V1–V7, V9, V10 done; V8 and V11 pass (or handoff explicitly incomplete). V12 documented only.

---

### Phase 5 — Handoff

**Objective:** Leave the human operator with an actionable completion report.

- [ ] List all created/updated files
- [ ] State V8 result with skill name evidence (or blocked reason)
- [ ] State V11 result with overall verdict + quote of verification/testing gap language
- [ ] State V10 cold-review availability
- [ ] Summarize Project Test Commands status per row: `REAL` / `NONE` / `WAIVED`
- [ ] State git mode: full vs degraded
- [ ] Ask user to fill remaining commands or confirm waivers
- [ ] Point to Fixture B/C for first product feature branch
- [ ] Remind: persona tags are UI-only; always prepend instructions; always set `capability_mode` for tests

**Phase verification:** Handoff message contains every bullet above; no claim of “bootstrap done” if V8 or V11 failed.

---

## Implementation order (recommended DAG)

```text
Phase 0 ──► Phase 1 ──► Phase 2 (can write files in parallel groups)
                              │
                              ├─ 2.1 AGENTS.md
                              ├─ 2.2–2.3 README + rules
                              ├─ 2.4–2.5 personas + roles
                              ├─ 2.6 five skills
                              └─ 2.7–2.8 docs, waivers, fixtures
                         Phase 3 (depends on AGENTS + repo scan)
                         Phase 4 (depends on Phase 2+3 complete)
                         Phase 5 (depends on Phase 4 results)
```

**Parallelism note:** Within Phase 2, persona files, skill files, and docs can be written concurrently. Phase 3 must wait for AGENTS skeleton. Phase 4 must wait for all files + commands closure.

**Content authority:** Prefer bootstrap v1.4 body text for each path. Do not invent alternate gate thresholds (keep ≥80% changed-line / proxy). Do not weaken V8/V11.

---

## Canonical runtime rules (encode in AGENTS + skills; do not re-derive)

1. Lead orchestrates all spawns — depth 1.
2. Persona binding = read instruction md + **prepend** to child prompt. No `persona=` parameter.
3. Description tags = TUI labels only.
4. Always set `capability_mode` on spawn: plan review `read-only`/`explore`/`plan`; tests `execute`/`all`.
5. Worktrees require git; integrate via worktree apply before claiming done.
6. `/check-work` → look for `VERDICT: PASS|FAIL`; session adequacy only.
7. One orchestrator at a time (Lead post-change **or** `/implement` **or** one project orchestration skill).
8. Bundled `test-writer` may be prepended when writing tests outside `/implement`; never shadow the name with a project persona file.

### Severity → merge gate map (must appear in AGENTS + rules)

| Source | Gate effect |
|--------|-------------|
| `/review` **bug** (open) | Block unless durable waiver |
| `/review` **suggestion** (missing tests / wrong behavior / security / data loss) | Treat as **gap** → block |
| Other **suggestion** / **nit** | Non-blocking |
| QA test-accuracy finding (circular, happy-path-only auth/errors) | **gap** → block |
| Plan-reviewer Required Changes `bug\|gap` | Block implement until revised or durable waiver for residual Major Concerns |

### Implement vs `/review` de-dupe (must appear in AGENTS + post-change skill)

| Situation | Action |
|-----------|--------|
| Clean `/implement`, zero open bugs, tree matches review scope | Skip `/review`; record reason |
| Open gate-blocking issues or tree changed after implement | Run `/review` |
| Manual / `gf-*` implement | Always `/review` |
| User requests `/review` | Always run |

---

## Verification criteria (whole feature)

Bootstrap is **complete** only when all are true:

1. **Tree & policy:** All Phase 1 paths exist with Phase 2 content; no `.grokbuild/`; no shadowed persona/skill names; AGENTS + rules contain pipeline, de-dupe, severity map, waiver path.
2. **Commands closed:** Every Project Test Command row is REAL, NONE, or TODO with `docs/waivers/…` — never silent TODO.
3. **V8 strict:** `grok inspect --json` lists all five project skill names (or handoff marked incomplete if CLI blocked — incomplete ≠ done).
4. **V11 behavioral:** Fixture A plan review returns Request Changes / Major Concerns citing verification and/or testing gaps (or handoff incomplete).
5. **Handoff honesty:** Git full vs degraded, V8–V11 results, command status, and B/C post-install next steps are explicit.

**Observable artifacts:**

- File tree under `.grok/`, `docs/waivers/`, `fixtures/agentic-template-acceptance/`
- `docs/plans/acceptance-bad-plan.md` (copy for V11)
- Plan review output (chat or `*.review.md`) with overall verdict
- `grok inspect --json` excerpt listing the five skills
- Optional: `docs/waivers/bootstrap-test-commands.md` if commands incomplete

---

## Out-of-scope

- CI YAML generation
- Mutation testing automation
- Installing coverage tools for every language
- Graphite automation (`/pr-babysit`, `/execute-plan` when relevant later)
- Redefining bundled `/implement` internal behavior
- Fixture B/C as bootstrap-complete on empty product trees
- Making persona/role product resolution bind without prompt prepend
- Product feature implementation inside this template repo
- Hard OS-level enforcement of gates (template is prompt + skill discipline only — A11)

---

## How would this fail to ship?

1. Skills under wrong root (`.grokbuild/`) or wrong shape → absent from `grok inspect --json` → V8 fail.
2. Personas named `reviewer` etc. → shadow bundled catalog → wrong specialist selection.
3. Nested QA spawns Reviewer → depth-1 error → loops broken.
4. Coverage gate with no tool and silent pass (no durable waiver) → false GO on real features.
5. Claiming done on file tree only without Fixture A or strict V8.
6. Non-git repo: install “succeeds,” then `/review`/worktrees fail on first real change.
7. Lead spawns with `[gf-qa]` tag only → generic agent, no QA schema, gates theater.
8. Nested markdown fence corruption → truncated skill/persona files that pass shallow “file exists” checks but break runtime.
9. Project Test Commands left as bare TODO → targeted/regression skills have nothing to run.
10. Double orchestration (`/implement` + post-change `/review` always, or concurrent skills) → token burn or contradictory skip rules.
11. Chat-only waiver → next session loses merge authority.
12. Phase 3 on this empty repo claims “accuracy gates operational” despite NONE unit/regression commands.

---

## Acceptance mapping (bootstrap §11 checklist)

- [ ] Phase 0 git check (or degraded mode documented); timestamped AGENTS backup; no `.grokbuild/`; no shadowed personas
- [ ] `.grok/rules/accuracy-coverage.md` (gates + severity map + waiver pointer)
- [ ] Four `gf-*` personas + non-empty instructions (read-verified)
- [ ] Optional roles with “not spawn binding” note
- [ ] Five skills with frontmatter + `disable-model-invocation: true`
- [ ] Workflows + docs + coverage recipe hints
- [ ] Fixtures + `docs/waivers/README.md`
- [ ] AGENTS.md: pipeline, de-dupe, severity map, Project Test Commands (closed Phase 3)
- [ ] Phase 4 V8 strict
- [ ] Phase 4 V11 Fixture A pass
- [ ] Handoff with incomplete flags if V8/V11 failed

---

## Suggested execution prompt (for implementer)

> Read `docs/plans/agentic-dev-team-template-bootstrap.md` and the source `grokbuild-agentic-dev-team-template-bootstrap.md` (v1.4). Implement Phases 0–5 in order. Prefer bootstrap section bodies for file content. Optimize for code accuracy, test accuracy, and coverage policy as written. Prefer bundled `/review`, `/check-work`, and `/implement`. Complete Phase 4 including **strict** `grok inspect --json` and **Fixture A** before claiming done. Do not treat file presence alone as success.

---

## Next steps after this plan

1. Run **three cold reviews** of this plan (adversarial, fresh context).
2. Revise plan if cold reviews find blocking gaps (especially V8/V11, Phase 3, extraction, git).
3. Execute plan in the target repo (this workspace or a consumer product repo).
4. After first product code lands, run Fixture B and C.
