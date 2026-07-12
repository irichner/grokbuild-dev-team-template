# Cold review of grokbuild-agentic-dev-team-template-bootstrap

**Reviewer:** Claude Code (fresh-context forked agent)  
**Date:** 2026-07-12  
**Plan version reviewed:** 1.3 (Draft; doc-accurate vs Grok 0.2.x user guide + `grok inspect`)

**Repo reality check:** Workspace contains only this bootstrap file and the prior v1.1 review. No `docs/plans/_archive/`, no `.grok/` tree, **not a git repository** (`projectRoot: null` from `grok inspect --json` on Grok 0.2.99). Claims checked against `~/.grok/docs/user-guide/` (skills, subagents, plan mode, project rules), bundled `/review` + `/implement` + `/check-work`, bundled personas under `~/.grok/bundled/personas/`, and live `grok inspect`.

---

## Top three weakest assumptions

1. **Assumption: installing the file tree + passing Phase 4 (including V8 `grok inspect`) means Grok will enforce accuracy/coverage gates on real work.**  
   **Falsifier:** After install, run a non-trivial change without explicitly invoking `/post-change-accuracy-protocol` / `/review` / `/check-work`. Observe whether Lead still runs the full pipeline under ordinary “implement this” prompts, and whether merge is blocked when coverage tool is absent or QA report is narrative-only.  
   **If false:** Success collapses to discovery ceremony. AGENTS.md and `.grok/rules/` are prompt pressure, not hard gates. Coverage floor, test-accuracy blockers, and “no open bug/gap” become optional style if the model shortcuts. Operational goal (code/test accuracy + coverage) is not proven by V1–V9.

2. **Assumption: Project Test Commands will be filled meaningfully (Phase 3), so the ≥80% coverage gate and targeted/regression loops are executable.**  
   **Falsifier:** Bootstrap lands in a greenfield or multi-stack repo; scan finds nothing; AGENTS.md keeps `TODO` for Build / Unit / Coverage / Regression.  
   **If false:** Targeted and regression skills have nothing concrete to run. Coverage path becomes permanent `NO COVERAGE TOOL` + waiver theater. `/check-work` may still invent commands from README, but project skills diverge from check-work discovery and produce incomparable reports. The accuracy/coverage product claim fails on the first install where tooling is unknown.

3. **Assumption: Lead (and project skills) will reliably prepend `gf-*` instruction files on every specialist spawn, so persona/role TOML defaults matter.**  
   **Falsifier:** Any spawn that only sets `description: [gf-qa] …` without reading/prepending `.grok/personas/instructions/gf-qa.md` (docs + bundled `/review`/`/implement` both state: no `persona=` parameter; tags are UI labels only). Persona catalog presence does not inject behavior. Role files apply only when “resolution” requests them — and the product docs never specify the request mechanism skills actually use.  
   **If false:** `default_capability_mode` / `reasoning_effort` on `gf-*.toml` are inert for the inject path. QA may run as generic general-purpose without report schema or accuracy rules. Optional `.grok/roles/` is dead weight. You get labeled rows in the pager, not specialist behavior.

---

## Missing failure modes

- **No git repository:** Project root discovery walks to `.git` (`projectRoot: null` here). Worktree isolation, `git status`/`diff` test selection, `/review` local mode, and parallel-fullstack apply all require git. Bootstrap does not require `git init` or document “template must land in a git repo.” Partial install in a non-git folder yields discoverable skills that fail operationally.

- **Nested fence corruption when extracting “exact content”:** Sections 4–9 embed file bodies inside markdown fences that themselves contain triple-backtick blocks (QA report schema, Review Report schema, seeded-bug python). A mechanical extract (or a hurried implementer) will truncate those files. Failure mode: malformed instruction/skill files that still pass shallow shape checks (frontmatter exists) but break at runtime.

- **Double-loop process tax / contradictory orchestration:** AGENTS prefers `/implement` (already implement → multi-reviewer → fix), then **again** `/review` + targeted/regression + `/check-work` via post-change protocol. No rule for when `/implement`’s internal review supersedes external `/review`, or how open issues transfer. Agents either skip half the pipeline or burn tokens re-reviewing the same diff.

- **Waiver without durable record:** Gates allow “user waives in writing” / residual failures with references, but there is no waiver file path, schema, expiry, or “next session must re-read waivers” step. Waivers evaporate; future sessions re-block or silently assume GO.

- **Severity taxonomy mismatch:** `/review` issues are `bug|suggestion|nit`. Plan-reviewer / AGENTS gates talk about `bug|gap`. Is a review `suggestion` about missing tests a merge-blocking **gap**? Skills do not map taxonomies. Merge decisions become inconsistent across operators.

- **`/check-work` is not a pure build/test gate:** Bundled check-work verdicts session adequacy (trace review + optional code phase). AGENTS treats `VERDICT: PASS` as if it were “build+tests green.” A session that “completed bootstrap scaffolding” can PASS check-work without ever running product tests; conversely, a correct code change can FAIL on checklist items unrelated to coverage.

- **Coverage measurement undefined at the tool boundary:** “≥80% new/changed executable lines” or “changed-file proxy” has no command templates per ecosystem, no baseline storage, no instruction for partial runs, and no handling when coverage tools report whole-project % only. Agents will invent numbers or mark waived.

- **Test-accuracy standards are not auto-loaded:** Full criteria live in `.grok/docs/test-accuracy-standards.md` (explicitly non-auto-load). Only a short summary is in rules. If QA skips the doc read (step exists in skill but is soft), circular tests pass the “tests exit 0” gate.

- **Skill auto-invocation collisions:** Project skills do not set `disable-model-invocation`. Model may auto-fire `/targeted-unit-test-loop` mid-`/implement`, or stack protocols. No ownership rule for concurrent orchestrators. Depth-1 forbids nested spawns, so a skill running *inside* a child fails hard.

- **Parallel fullstack contract freeze is prose-only:** Step “freeze API/contract” has no artifact path, schema, or conflict owner. Divergent worktrees still likely; “stop and re-freeze” has no detection procedure beyond human judgment.

- **Plugin `/cold-review` availability is environment-dependent:** Live inspect lists Lanshore skills as `plugin: … [compat unresolved]`. Plan prefers `/cold-review` when available; fallback is project `plan-review-loop`. No bootstrap check that cold-review is invocable in *this* workspace, and no instruction if compat stays unresolved.

- **Persona `instructions_file` only fails when resolution requests the persona:** Inject path uses `read_file` on the md path. If paths drift, inject fails open (Lead forgets) rather than spawn-fail. Silent generic agent.

- **AGENTS.md overwrite/merge still lossy:** Backup is one-shot (`AGENTS.md.bak-before-agentic-template` not overwritten). Second bootstrap or manual merge has no three-way strategy for project-specific rules vs template pipeline.

- **Fixture B/C cannot run on a template-only repo:** Seeded bug needs product language/layout. Coverage hole needs real code. Acceptance README claims behavioral proof the bootstrap repo cannot host without inventing an app — out of scope of “install config,” yet implied by goal language.

- **Flaky / partial regression:** Regression skill has triage + re-run subset then full phase, but no flaky quarantine, timeout budget, or “known fail list” format. Extended trigger list is good; operational flake handling is not.

---

## Undocumented prior knowledge

- That **persona application in practice is prompt-prepend**, matching bundled `/review` and `/implement`, and that catalog TOML does not change spawn unless some undocumented role-resolution path fires.
- How **roles** (`.grok/roles/*.toml`) are selected at spawn time — docs say resolution can apply them; skills never show a role selector. Implementers need an explicit “roles are optional defaults only; always set `capability_mode` on spawn.”
- That **`[tag]` in `description` is pager UI only** (correct in plan) — but also that **misspelling tags only hurts labels**, not behavior; the critical failure is missing prepend, not wrong tag.
- That **project root is the git root**, and non-git CWDs have `projectRoot: null` with CWD-only rule scan behavior — bootstrap should require git or document CWD-local `.grok/` expectations.
- Exact **session plan path** encoding (`~/.grok/sessions/<encoded-cwd>/<session-id>/plan.md`) and when Plan Mode allows writing `docs/plans/` (only after exit / non-plan writes allowed).
- How to compute **changed-line coverage** for pytest-cov / istanbul / go cover / llvm-cov — plan assumes “if tool configured” without discovery recipes.
- Mapping **review severities → merge gate** (bug vs suggestion vs gap).
- That **bundled `test-writer` persona already encodes stronger test strategy** than `gf-qa` (happy/edge/error/concurrency; public interface; deterministic) — template does not point implementers at it when writing tests under `/implement` effort specialists.
- That **`grok inspect` human output lists skills/agents/plugins, not a personas section** (live 0.2.99). V8 does not verify persona catalog; `/personas` UI is a separate check the plan never requires.
- Windows vs Unix assumptions in any future command fill (plan is OS-agnostic; check-work and review skills lean on unixy shell idioms in places).

---

## Verification gaps

Phase 4 is stronger than v1.1 (shape checks + V8 discovery + protocol map print) but still mostly **static**. Observable gaps:

| Claimed outcome | What Phase 4 actually checks | Missing observable check |
|-----------------|------------------------------|---------------------------|
| Skills discoverable | V8: appear in `grok inspect` (or “CLI missing” escape) | Escape hatch allows ship without discovery proof; no required names list asserted against JSON |
| Personas usable | V3: toml shape + file path exists | No probe spawn with prepend; no `/personas` catalog check; `instructions_file` readability not proven via resolution |
| Gates enforce accuracy | V4/V5 text exists | No forced run of Fixture A/B/C as bootstrap acceptance; presence ≠ behavior |
| Coverage gate | Mentioned in rules/docs | No sample Coverage command that produces a numeric changed-line %; no fail demo |
| Test accuracy | Doc + short rules | No fixture where circular mock-only tests are marked NO-GO |
| `/review` integration | Protocol map text | No seeded bug requiring Request Changes / open bug |
| `/check-work` | Protocol mentions VERDICT | No definition of which AGENTS gates check-work must see as FAIL (policy vs session task) |
| Lead-only spawn | Documented | No negative test (child spawn) — hard to automate, but unstated |
| Trivial escape hatch | Documented | No criteria for “docs/comment-only” vs “executable code changed” edge cases (generated files, SQL, config) |

Subjective / non-observable exits still present:

- “User accepts residual Major Concerns in writing”
- “user-accepted residual failures with references”
- “`/check-work` would yield `VERDICT: PASS`” (counterfactual, not a recorded artifact path)

V8 fallback (“if `grok` unavailable, list expected skill names”) is **not** a pass criterion; it is a skip.

---

## Scope concerns

**Relative to Goal (find skills, use harness, enforce measurable gates, prove install):**

Under-scoped / incomplete for the Goal:

- Mandatory **behavioral** acceptance (at least Fixture A on install; B/C deferred only with explicit “needs product code” note)
- Concrete **Project Test Commands** discovery algorithm with failure if still TODO on non-empty repos that have scripts
- Severity mapping + waiver artifact
- Git prerequisite
- Persona catalog verification beyond file existence
- Conflict rules between `/implement` internal review and post-change `/review`

Over-scoped relative to install Goal (candidates for Out-of-scope or Phase 2):

- **`parallel-fullstack-feature`** — worktree orchestration is process scale; does not improve accuracy by itself; depends on git worktree apply expertise
- Full **privacy-safety** essay (Green/Yellow/Red) — orthogonal to gates unless tied to secret-scan in review
- Optional roles directory without resolution story — adds surface without proven binding

Checklist items that do not fully trace to Goal:

- “Optional roles” — not required for find/use/enforce/prove
- Narrative workflow file under `.grok/workflows/` — explicitly non-loaded; pure duplication of skill

Goal says success is “operational behavior, not directory ceremony,” but checklist + Phase 4 still overweight ceremony (files, shapes, inspect listing).

---

## Comparison to prior plans

No `docs/plans/_archive/` in this repo.

**vs prior cold review of this same bootstrap (v1.1 → stored in this `.review.md`):**

| v1.1 gap | v1.3 status |
|----------|-------------|
| Wrong root `.grokbuild/` | Fixed → `.grok/` |
| Flat md skills / md personas | Fixed → `SKILL.md` + `gf-*.toml` |
| Stub testing loops | Partially fixed — numbered steps + report schemas; still weak on coverage tooling recipes and selection determinism |
| No `/review` / `/check-work` integration | Fixed at policy level (harness-first table) |
| `/skillify` | Fixed → `/create-skill` |
| Session plan path | Fixed (documented) |
| Shadow bundled persona names | Fixed (`gf-*`) |
| No `grok inspect` verification | Partially fixed (V8 with soft escape) |
| Acceptance fixtures | Added as files; **not** mandatory behavioral gates |
| Persona spawn mechanics | Documented inject pattern; roles still hand-wavy |

**vs bundled harness skills (higher bar than this template’s loops):**

| Artifact | Still stricter / missing in template |
|----------|--------------------------------------|
| `/review` | Diff collection, size gates, severity parsing, artifact paths — template only “call it” |
| `/implement` | Multi-reviewer effort model, issue file protocol, memory flush — template does not define handoff from implement artifacts into post-change protocol |
| `/check-work` | Full verifier prompt + 3 retries — template reduces to VERDICT string |
| Bundled `test-writer` | Richer test strategy than `gf-qa` execution focus |
| Lanshore `feature` plan template | Per-phase verification; this bootstrap’s Phase 4 is install-centric only |
| Lanshore `plan-audit` | Plan-vs-diff — mentioned as optional plugin, not wired into post-change order |

**Gap type:** Many v1.1 oversights were intentionally fixed in v1.3. Remaining gaps are **enforcement and proof**, not path discovery — i.e. the hard part of the stated Goal.

---

## Overall

**Not ready to execute if “done” means measurable accuracy/coverage behavior.** It **is** ready to execute as a **config scaffold** that is largely path- and format-correct for Grok 0.2.x (`.grok/skills`, `.grok/rules`, non-shadowing personas, harness-first policy, inject-not-parameter spawn pattern). That is a real upgrade from v1.1.

**Minimum before treating install as proof of the Goal:**

1. **Require git** (or document non-git limitations) before Phase 1; fail bootstrap if worktree/review-dependent skills are claimed without git.  
2. **Close the TODO hole:** Phase 3 must either fill real commands from manifests **or** set an explicit project-level `GATES=WAIVED` / `NO COVERAGE TOOL` record with user confirmation — not silent TODO forever.  
3. **Make V8 strict:** `grok inspect --json` must list the five project skill names; remove “CLI unavailable → pass.” Add persona path checks (`/personas` or file read of all four instruction files).  
4. **Run Fixture A as mandatory Phase 4** (bad plan → Request Changes). Mark B/C as post-install on first product code, not bootstrap-complete.  
5. **Resolve double orchestration:** either “if `/implement` used, post-change skips duplicate `/review` unless open bugs remain” or “always external `/review` and ignore implement’s review artifacts” — pick one.  
6. **Fix extractable content:** de-nest report schemas (indent fences, use `~~~~`, or point to files without embedding inner ```).  
7. **Map severities + waivers** to a single merge rule and a durable waiver path under `docs/` or `.grok/`.

Without those, implementing v1.3 will produce a discoverable template that *describes* accuracy and coverage well, but still cannot *prove* either after install.
