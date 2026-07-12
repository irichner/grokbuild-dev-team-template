# Cold review of agentic-dev-team-template-bootstrap

**Reviewer:** Cold review agent #1 (fresh context)  
**Date:** 2026-07-12  
**Plan version reviewed:** Draft v1  
**Focus:** Enforcement vs ceremony; V8/V11; Phase 3; orchestration  

**Workspace reality checked:** Root holds only bootstrap v1.4 + prior source review; `docs/plans/` contains this plan only; **no** `docs/plans/_archive/`; **no** `.grok/`, `AGENTS.md`, product manifests, or fixtures yet. Plan’s exploration table is still directionally correct (config scaffold into empty tree). Git posture was not re-executed in this review; plan correctly treats non-git as possible and defers to Phase 0.

---

## Top three weakest assumptions

1. **Assumption (implicit in Goal + “Success looks like”): Completing Phases 0–5 with V8 + V11 pass means accuracy/coverage gates are “enforced” and “operational … ready for the first product change.”**  
   **Falsifier:** Ship bootstrap with all five skills listed in `grok inspect --json`, Fixture A → Request Changes citing testing gaps, Project Test Commands = `NONE` for unit/coverage/regression (with or without waiver text), and never invoke `/targeted-unit-test-loop`, `/regression-test-loop`, `/post-change-accuracy-protocol`, or a seeded failing test. Observe that nothing blocks an ordinary “implement this” session from merging with zero test runs.  
   **What breaks:** The Goal’s third bullet (“Enforces measurable gates”) and success language about operational readiness. V8 proves **discovery**; V11 proves **one plan-critique path** on a cartoon bad plan. Neither runs unit commands, coverage floor, severity→merge map on a real `/review` artifact, durable waiver re-read before GO, or QA accuracy blockers. Out-of-scope already admits hard OS enforcement is impossible (A11 / “prompt + skill discipline only”), but Goal still markets **enforcement**. Completing this plan proves a **discoverable policy scaffold**, not gate enforcement. That is the core ceremony failure mode.

2. **Assumption: Phase 3 “closed” outcomes on this empty / template-only repo produce a truthful command posture that skills can execute against.**  
   **Falsifier:** Scan finds no `package.json` / `pyproject.toml` / etc. Implementer writes `NONE — no tool in repo` for Build, Unit, Coverage, Regression, Lint **or** a single `docs/waivers/bootstrap-test-commands.md` that waives everything. Phase verification (“no bare TODO without waiver”) **passes**. Handoff checklist allows “must not claim accuracy gates operational” **only** when unit+regression are NONE/TODO *without* waiver — so adding a waiver file upgrades silence into **documented permission to have no tests**, while Goal/success still say gates are ready.  
   **What breaks:** Targeted and regression skills become permanent NO-GO or waiver-dependent theater until product tooling lands. Coverage ≥80% is unreachable by design on this workspace. Phase 3 is **closed-form paperwork**, not closed-loop executability. “Expect NONE or waived TODO” (line ~249) is honest; treating that as bootstrap success toward “enforce … coverage floor when a tool exists” is not — the condition never becomes true during install.

3. **Assumption: V11 can be executed as a mandatory Phase 4 step inside the same bootstrap session, with pass criteria that are hard to game.**  
   **Falsifiers:**  
   - Bootstrap implementer is itself a **subagent** (depth 1): `plan-review-loop` requires Lead-only `spawn_subagent` → V11 hard-fails even if files are perfect.  
   - Skills set `disable-model-invocation: true`: “run `/plan-review-loop`” is not auto; the implementer must slash-invoke or manually re-enact steps. Plan does not say whether re-enactment counts or only slash-skill.  
   - Reviewer (or Lead role-playing the report) returns Request Changes and pastes the words “verification” / “testing gaps” without real checklist rigor — pass criteria are **substring-level**, not structured schema checks against Required Changes `bug|gap`.  
   - Review output lives only in chat; no required durable `docs/plans/acceptance-bad-plan.review.md` (or similar) — next session cannot audit V11.  
   **What breaks:** “Bootstrap done” becomes either **blocked by session topology** (false incomplete) or **rubber-stamped by language match** (false complete). V11 is the only behavioral gate; it is both fragile and soft.

---

## Missing failure modes

- **Enforcement vs ceremony (not mitigated by “strict V8”):** Listing skills ≠ running them. No V-check forces post-change protocol, targeted loop, coverage number, or merge block on open gap. A11 + Out-of-scope correctly demote enforcement to prompt pressure; Goal and success text do not. Implementers will report “done” when V8/V11 green while accuracy gates remain unproven.

- **Phase 3 empty-repo vacuity:** Closed REAL/NONE/WAIVED rows with all NONE still satisfy Phase verification. Plan forbids claiming gates operational only in a narrow case (unit+regression NONE/TODO **without** waiver). Path of least resistance: write a waiver, claim Phase 3 closed, claim bootstrap complete. No requirement that handoff use a single machine-checkable flag such as `GATES_OPERATIONAL=false` when unit suite is NONE.

- **V8 rigor gaps:**  
  - No specified JSON pointer / sample shape for skill names (source field names vary; implementer may “see” names in human inspect text and claim JSON pass).  
  - No assertion that skills resolve as **project/local/repo** vs accidental name collision with a plugin.  
  - No persona catalog check (`/personas` or inspect agents); V3 is file-read only — does not prove catalog load.  
  - CLI present but inspect fails (auth, version, CWD ≠ git root / `projectRoot: null`) is partially covered by incomplete handoff, but **installing full tree under non-projectRoot CWD** then claiming V8 against a different root is unaddressed.  
  - Windows: `grok` not on PATH in the agent shell while available in user TUI → systematic false “CLI unavailable / incomplete” or false pass if implementer skips.

- **V11 rigor gaps:**  
  - Pass = overall Request Changes/Major Concerns **and** “mentions verification and/or testing gaps” — trivially satisfied by a one-line report.  
  - No required fields from Review Report schema (Required Changes severities, Test/coverage gaps section non-empty with substance).  
  - No negative control (e.g. that a good plan would not falsely fail) — out of scope maybe, but then V11 only tests “model can dislike a stub,” not skill wiring.  
  - Cold-review vs plan-review-loop: if cold-review is `[compat unresolved]`, fallback path is mandatory for V11; plan allows either. No check that **project** skill was the one that ran when plugin is broken.  
  - Concurrent orchestration: running Fixture A while another orchestration skill or `/implement` is mid-flight is not forbidden in Phase 4 text (ownership rule lives in skill bodies not yet written).

- **Double / stacked orchestration (under-specified operationally):**  
  - De-dupe rule: “zero open bugs” + “tree matches review scope” — **no** definition of implement issue artifact path, how to parse open bugs, or how to prove tree match (`git status` clean? same commit? unstaged noise?). Operators will always-skip or always-rerun.  
  - De-dupe ignores gate-mapped **suggestions** (missing tests → gap). Clean “zero bugs” can still leave blocking gaps; skip `/review` then never re-classify.  
  - `post-change-accuracy-protocol` steps say run `/targeted-unit-test-loop` and `/regression-test-loop` (also `disable-model-invocation: true`). Is post-change a **procedure checklist for Lead** or a skill that must re-invoke slash skills? If Lead “runs” post-change as freeform steps, de-dupe and ownership rules are prose only. If skills nest via tool calls from a child, depth-1 breaks. Plan’s “one orchestrator” rule is correct in spirit and **unenforceable in Phase 4**.  
  - Parallel-fullstack step 5 always runs post-change; step 2 prefers `/implement` — stacking implement’s multi-reviewer loop + post-change de-dupe is only narrative.  
  - User invokes `/review` after clean implement while post-change already SKIPPED — fine; reverse order (post-change mid-implement) still only warned in skill text, not in Phase 4.

- **Partial install / non-idempotent re-run:**  
  - No rollback if V8/V11 fail after writing `.grok/**` — tree remains; consumers may treat files as success and ignore handoff “incomplete.”  
  - Second bootstrap: AGENTS merge strategy is “preserve project-specific rules” without algorithm; timestamped backup policy does not define merge of v1.4 template into already-customized AGENTS.  
  - Re-copy Fixture A over `docs/plans/acceptance-bad-plan.md` may clobber a human-edited acceptance artifact.  
  - Phase 2 parallel writes: no locking; if implementer parallelizes AGENTS (2.1) with Phase 3 edits, last writer wins.

- **Git degraded mode overclaim:** Phase 0 allows config-only install. Many skills (targeted change list, parallel worktrees, `/review` local) are degraded, but **V8/V11 can still pass** (inspect + plan review need no product tests). Bootstrap “complete” in degraded mode still installs `parallel-fullstack-feature` skill that will fail later — prerequisites are inside skill, not install-time disable/quarantine of that skill’s claims.

- **Fence / extraction corruption:** Plan points at bootstrap `~~~~` / indented schemas (good). Phase 2 verification says “no truncated schema” but gives no mechanical check (e.g. instruction files must contain the strings `QA Test Report` and `Review Report` and `Recommendation:` / `Overall:`). Shallow non-empty file still passes if implementer writes stubs.

- **Waiver misuse:** Durable waiver path exists; no Phase 4 check that Lead re-reads waivers, no expiry enforcement, no ban on waiving Fixture A / V8. Bootstrap-test-commands waiver can become a permanent blanket.

- **Auth / tenant / multi-root:** Not applicable as product multi-tenancy, but multi-checkout and monorepo roots are ignored: skills assume single AGENTS.md at git root.

- **Retries:** Max 3 fix cycles appear in skills content to write; bootstrap Phase 4 itself has no retry budget or flake policy if `grok inspect` flakes.

- **Idempotency of “bootstrap done”:** Success allows handoff marked incomplete when V8/V11 fail — but Acceptance mapping still checks the same boxes. No single required status file (e.g. `docs/waivers/` or `fixtures/.../BOOTSTRAP_STATUS.md`) recording `COMPLETE|INCOMPLETE` with V8/V11 evidence digests. Chat handoff is ephemeral.

---

## Undocumented prior knowledge

- **What `grok inspect --json` actually looks like** (skill name field, source enum, whether personas appear). Plan asserts names and “project/local/repo source” without a sample snippet or jq filter. Implementer who has never run inspect will improvise.

- **That V11 almost certainly requires the bootstrap agent to be the parent session Lead**, not a nested implementer — depth-1 implication is in Canonical rules but not called out as a **Phase 4 session constraint** (“do not run bootstrap verification from a subagent”).

- **Slash vs manual skill execution** when `disable-model-invocation: true`: whether Lead pasting skill steps counts as V11/V9, or only `/plan-review-loop` UI invocation.

- **Implement issue / review artifact locations** for de-dupe (“zero open bugs”) — bundled `/implement` paths are assumed known, never named in the plan.

- **Worktree apply** UX for parallel-fullstack — “integrate via Grok worktree apply” is product-specific; no verification that the operator/session can do it.

- **Session plan path encoding** (`~/.grok/sessions/<encoded-cwd>/...`) — in Canonical rules / bootstrap; plan A6 states it but Phase 2 does not require documenting it in AGENTS beyond bootstrap paste.

- **How coverage “changed-line %” is computed** on each stack — still recipe hints only in source bootstrap; plan forbids inventing thresholds but does not add discovery of concrete Coverage command templates when a tool *will* exist later.

- **Prior cold review of bootstrap v1.3** already concluded enforcement/proof was the remaining gap; this plan folds process fixes but an implementer reading **only** the plan may think V8/V11 closed that gap. They did not.

- **This workspace has no git archive of prior plans** — comparison is to root bootstrap + root `.review.md` only; plan’s “prior art” claim depends on reading those files.

---

## Verification gaps

| Claim | What plan checks | Why not observable / insufficient |
|-------|------------------|-----------------------------------|
| Skills discovered | V8 names in inspect JSON | No required saved excerpt path; no schema; no source=project assertion recipe |
| Personas usable | V3 non-empty files | No spawn+prepend probe; no catalog listing |
| Accuracy gates enforce | Text in AGENTS/rules (V4/V5); deferred B/C | **No bootstrap run of targeted/regression/coverage fail path** |
| Coverage floor | Documented ≥80% | Empty repo → NONE; never measured |
| Test accuracy | Doc + rules summary | No circular-test fixture at install |
| `/review` integration | De-dupe text + V9 print | No seeded bug; skip path untested |
| `/check-work` | Protocol mentions VERDICT | Explicitly session adequacy; can PASS install session without product tests (A12) — correct warning, still listed in gates |
| Phase 3 closed | REAL/NONE/WAIVED rows | Scan evidence not required; all-NONE is a pass |
| V11 behavioral | Verdict + “mentions” testing/verification | Substring gameable; no durable report artifact required |
| One orchestrator | Canonical rule #7 | Not tested; cannot be tested by file tree |
| Bootstrap complete ≠ incomplete | Handoff bullets | No committed status artifact; consumer of repo files cannot see V8/V11 result |

**V8/V11 specifically:** Making them mandatory and removing CLI soft-pass is necessary and still **insufficient** for the Goal’s enforce clause. The plan’s own Verification criteria §3–4 allow “or handoff incomplete” — good honesty, but then “bootstrap complete only when all are true” coexists with success language that overstates readiness after complete install on an empty tree.

**Phase 3 specifically:** Verification is “no bare TODO.” That is a **form** check. Missing: evidence of manifest scan (log of files examined), explicit `GATES_OPERATIONAL` / per-row readiness, and for this template repo a **required** handoff sentence that accuracy/coverage gates are **not** operational until unit command is REAL.

---

## Scope concerns

**Under-scoped relative to Goal (“enforces measurable gates” / operational readiness):**

- Any install-time proof that post-change protocol or targeted loop can run (even as dry-run / NO-GO with NONE commands and a required recorded NO-GO).
- Durable V8/V11 evidence artifacts in-repo.
- Hard handoff flag when commands are all NONE.
- Operational definition of implement/review de-dupe inputs.
- Phase 4 constraint: verification must run as parent Lead with spawn rights.
- Persona discovery check beyond files on disk.

**Over-scoped / ceremony relative to install Goal:**

- **`parallel-fullstack-feature`** required in tree and V8 name list — worktree orchestration does not prove accuracy; fails without git; empty product has nothing to parallelize. Should be optional or explicitly “installed but non-operational until git + dual surfaces.”
- **Optional roles** still mandatory paths in Phase 1 — plan admits not spawn binding; pure surface area.
- **`.grok/workflows/` narrative** — non-loaded duplicate of skill; checklist still requires it.
- **`privacy-safety.md`** — orthogonal to accuracy/coverage gates unless tied to review secrets rule (already in AGENTS).
- **Five cold-review next steps** (three plan reviews) — process meta; fine, but does not fix enforcement gap.

**Goal vs Out-of-scope contradiction:** Goal §3 “Enforces measurable gates” vs Out-of-scope “Hard OS-level enforcement … prompt + skill discipline only.” Plan should reword Goal to **“Specifies and disciplines gates via AGENTS/rules/skills; proves discovery + plan-review; does not hard-enforce.”** Until then, implementers optimize for checklist ceremony that matches marketing language.

**Success looks like** still claims “Operational accuracy/coverage enforcement is documented and ready for the first product change.” On this workspace, after perfect execution, enforcement is **documented and known non-operational** (no unit command). That sentence is false for the intended target (this template repo) and misleading for copy-paste into a product repo until Phase 3 finds REAL commands.

---

## Comparison to prior plans

**vs bootstrap source v1.4:** Plan is a faithful operationalization of Phases 0–5, V1–V12, de-dupe, severity map, waivers, `disable-model-invocation`, strict V8, mandatory Fixture A. Content authority correctly defers bodies to bootstrap sections 1–10. Little new technical content; main value is checklist DAG + exploration findings.

**vs prior cold review of bootstrap v1.3 (`grokbuild-agentic-dev-team-template-bootstrap.review.md`):**

| v1.3 finding | Plan Draft v1 status |
|--------------|----------------------|
| Soft V8 CLI escape | **Addressed** — unavailable = incomplete |
| Fixture A not mandatory | **Addressed** — V11 mandatory |
| Silent TODO commands | **Partially addressed** — closed REAL/NONE/WAIVED; empty-repo vacuity + waiver theater remain |
| No git prerequisite | **Addressed** as Phase 0 + degraded mode; degraded still allows “complete” discovery proof |
| Double orchestration | **Partially addressed** — de-dupe table + ownership prose; operational inputs undefined; Phase 4 does not exercise |
| Severity map / durable waivers | **Addressed** in plan text and required file content |
| Fence corruption | **Addressed** via extract rules; Phase verification still weak mechanically |
| Enforcement ≠ file tree | **Named** in Goal/non-goals/A11; **not solved** — V8+V11 still do not prove accuracy/coverage gates |
| Persona prepend reliability | Documented; still no probe |
| Fixture B/C need product code | Correctly deferred; Goal success language still implies readiness |

**Gap type:** Same residual as v1.3 review’s “Overall”: path/format scaffold ready; **enforcement and proof of accuracy/coverage still ceremony**. Plan improved process rigor around V8/V11/Phase 3 form without adding a single install-time observation that a test gate can fire.

**vs workspace:** No `_archive/` plans. Exploration claim “`docs/plans/` did not exist before this plan” is historical; **now** the plan file exists and is the only inhabitant — fine.

---

## Overall

**Not ready to execute if “done” means the Goal’s enforce + operational-readiness claims.** **Ready to execute as a config-scaffold install plan** that will likely produce correct `.grok/` paths, gf-* personas, five discoverable skills, closed command rows (almost all NONE here), and—if run as parent Lead with a working CLI—strict V8 plus a soft Fixture A critique. That is still **discovery + plan-review ceremony**, not proof that accuracy/coverage gates work.

**Minimum before execution without lying about the Goal:**

1. **Rewrite Goal/success** to match A11/Out-of-scope: prove discovery + Fixture A + closed commands; state explicitly that accuracy/coverage enforcement is **unproven at bootstrap** and remains prompt discipline until Fixture B/C and REAL unit/coverage commands exist.  
2. **Phase 3:** Require recorded scan evidence; if Unit is NONE, handoff **must** set a clear non-optional `accuracy_gates: NOT_OPERATIONAL` (or equivalent) even when a waiver exists; ban waivers from upgrading NONE into “ready.”  
3. **V8:** Mandate saved JSON excerpt path + exact five names + source class; fail if source is not project/repo.  
4. **V11:** Require durable review artifact under `docs/plans/`; pass criteria = schema fields (Overall + non-empty Test/coverage gaps + at least one Required Change severity `gap` or `bug` tied to verification/testing)—not mere word mention; Phase 4 must run as parent session with spawn rights.  
5. **Add V13 (or extend Phase 4):** Dry-run `/targeted-unit-test-loop` (or Lead steps) and **expect NO-GO** with NONE unit commands — proves the closed gate fails closed, not only that a bad plan gets scolded.  
6. **De-dupe:** Define artifacts for “open bugs” and “tree match”; map open gate-suggestions; forbid skip when gap-class suggestions remain.  
7. **Optionalize or quarantine** parallel-fullstack (and roles/workflow narrative) so V8 does not force non-accuracy surface area into “bootstrap complete.”

Without those, executing Draft v1 will install a polished template and still fail the adversarial test: **gates described, not shown to fire.**
