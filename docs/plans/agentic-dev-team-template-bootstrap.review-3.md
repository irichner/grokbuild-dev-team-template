# Cold review of agentic-dev-team-template-bootstrap

**Reviewer:** Cold review agent #3 (fresh context)  
**Date:** 2026-07-12  
**Plan version reviewed:** Draft v1  
**Focus:** Fidelity to bootstrap; idempotency; gaming complete; waiver lifecycle

## Top three weakest assumptions

1. **Assumption: V11 Fixture A is a reliable, non-gameable proof that “plan-review works.”**  
   Pass criteria are LLM-judged (`Overall: Request Changes | Major Concerns` **and** free-text that “mentions verification and/or testing gaps”). The same session that just wrote `gf-plan-reviewer` and `plan-review-loop` then judges itself. There is no fixed expected Required Changes list, no deterministic scorer, no rule against Lead authoring the review without a real spawn, and no policy for first-run **Approve** (retry until soft pass vs hard fail). Keyword-matching “verification”/“testing” is trivially satisfied by a one-line concern. Falsifier: run Fixture A three times with temperature/model variance, or have Lead emit a compliant report without spawning—bootstrap still “passes.” If false: V11 is ceremony with a narrative fig leaf, not behavioral proof.

2. **Assumption: Phase 2 “prefer bootstrap v1.4 body text” plus topic checklists yields a faithful install without file-by-file content authority.**  
   The plan never embeds, checksums, or maps each target path to a mandatory extract of bootstrap sections 1–10. It also says “verbatim in spirit” (Exploration findings), which explicitly licenses paraphrase. Falsifier: implementer writes shorter skills/personas that still hit Phase verification bullets (frontmatter keys, “non-empty,” “numbered steps,” “schema references”) while dropping gate language, de-dupe tables, coverage recipes, or QA report fields. If false: tree + V8 can pass while installed policy diverges from v1.4; fidelity is unenforced.

3. **Assumption: “Bootstrap complete” (V8 + V11 + closed commands) implies the Goal’s “enforces measurable gates” on future work.**  
   Plan A11 admits prompt pressure is not a hard OS gate; Phase 3 on this empty workspace expects `NONE` / waived `TODO`; Fixture B/C are explicitly not required. Falsifier: after “complete,” ordinary “implement this” never invokes `/post-change-accuracy-protocol`, and merge proceeds with only a permanent bootstrap-test-commands waiver. If false: success is discovery + one adversarial plan review, not operational accuracy/coverage enforcement—the Goal’s third bullet remains unproven and the fourth is gamed by scaffold completeness.

## Missing failure modes

- **Second install / re-bootstrap:** Phase 0 backs up existing root `AGENTS.md` with a unique timestamp, but there is **no** procedure when `.grok/skills/*`, personas, rules, fixtures, or `docs/waivers/` already exist. Overwrite vs skip vs three-way merge is undefined. Second run can silently clobber local skill customizations, duplicate AGENTS template blocks on naive merge, or leave stale skills that fail V6 “non-stub” while still listing in V8.

- **Partial install recovery:** No resume model after mid-Phase-2 failure (half the skills written), after V8 fail (CLI present but names missing), or after V11 fail. No “safe to re-run from Phase N” matrix; no marker file (e.g. install state); no instruction to delete partial tree vs continue.

- **Rollback path:** Only AGENTS backup is specified. No rollback for `.grok/**`, `docs/waivers/`, or `fixtures/`. Failed bootstrap leaves a polluted tree that the next attempt must invent a merge strategy for—unwritten.

- **Idempotent re-run of V11:** Copying `bad-plan.md` → `docs/plans/acceptance-bad-plan.md` on every verification can overwrite an operator’s prior review notes or a previously edited acceptance plan. No archive of review artifacts; no “if exists, do not clobber” rule.

- **Fixture A flakiness / false Approve:** Intentionally weak plan can still receive Approve from a lenient model or from `/cold-review` with different rubrics. Plan has no second-pass requirement on Approve, no gold-standard issue list, no inter-rater note. Intermittent V11 fail blocks “done” for the wrong reason; intermittent pass ships false confidence.

- **Self-review gaming of V11:** Lead can skip spawn, skip prepend, and write a compliant Review Report into chat. V11 records “verdict + quote” with no requirement that a subagent ran or that `capability_mode` was set. Completeness is self-certified.

- **Waiver lifecycle after create:** Template lists `Expiry`, but nothing defines: expired waiver = gate re-armed; how Lead detects expiry; active vs archived layout; who may write author field; whether agent-authored `docs/waivers/*.md` counts without human sign-off. Permanent `bootstrap-test-commands.md` with expiry “until product stack known” can live forever without re-open. Chat “confirm waivers” in Phase 5 is still non-durable unless written to file—plan mixes “get user fill or confirm” with durable-only doctrine.

- **Merge conflicts with future product `AGENTS.md`:** Backup-before-write does not define merge algorithm (prepend template section, replace markers, preserve Project Test Commands user filled later). Re-bootstrap after product teams add rules risks deleting product gates or double-inserting pipeline sections. No conflict markers, no “template version” header check, no upgrade path from template 1.4 → later.

- **Chicken-and-egg for V11 in a fresh session:** V11 requires `/plan-review-loop` or `/cold-review` after install. Plan does not state whether slash discovery of newly written skills works in the **same** session without restart, or what to do if inspect lists the skill but invocation fails. “Cannot run → V11 fail” is correct but unrecoverable without session guidance.

- **Degraded git mode “completeness”:** Degraded install can still pass V8/V11 and be called complete while `/review` local mode and worktrees are non-operational. Handoff documents degraded mode but verification criteria “complete only when” does not exclude degraded-from-full-protocol claims beyond a reminder.

- **Phase 3 NONE theater on template-only repo:** Every accuracy skill’s first real use NO-GOs or waives. Plan forbids claiming “accuracy gates operational” yet still allows **bootstrap complete**. Operators will equate complete with ready-to-merge discipline—false.

- **Nested fence corruption still under-specified operationally:** A13 + “use bootstrap `~~~~` sections” is correct but Phase 2 verification only checks non-empty + “schemas present,” not field-level schema completeness (e.g. every QA report bullet). Truncated extract can still “pass.”

- **Concurrent orchestrators / double review:** Encoded in canonical rules but Phase 4 never verifies de-dupe language is in the **installed** post-change skill body (V6 says “has implement de-dupe” as a soft phrase check).

- **Fixture B/C readiness void:** V12 = “document as post-install” only. No readiness criteria (e.g. Unit command REAL, coverage tool present, at least one product module), no mandatory trigger on first product feature branch, no owner, no fail-closed if B/C never run. Goal language about enforcement remains aspirational after “complete.”

## Undocumented prior knowledge

- Exact extraction procedure from bootstrap v1.4 (`~~~~` / ````` fence discipline, which sections map 1:1 to paths, how to avoid truncating QA/Review schemas).
- That plan text “verbatim in spirit” **conflicts** with bootstrap’s role as single source of file bodies—implementers need a hard rule: **copy section bodies; do not rewrite**.
- `grok inspect --json` schema: where skill `name` and source fields live; how to distinguish project vs bundled; what “CLI unavailable” means on Windows PATH vs not installed.
- Whether project skills written mid-session appear in inspect/slash without process restart.
- Persona catalog is not validated by V8; `/personas` or equivalent is never required (carried over gap from source review).
- Waiver **enforcement** steps inside skills (post-change step 5 says “per gates + docs/waivers/” but not “list waivers, filter unexpired, reject agent-only author if policy requires human”).
- How Plan Mode session path encoding works on Windows for A6 when copying plans—mentioned in bootstrap, not operationalized in Phase 2/4.
- That Fixture A pass strings can be satisfied without reading the bad plan if the model pattern-matches the acceptance README.
- Prior cold-review (v1.3) already demanded strict V8, Fixture A, waivers, git, de-dupe—plan claims these are folded, but **re-run/idempotency/rollback/merge** were never in bootstrap either; treating the plan as “execution ready” inherits those holes as if solved.

## Verification gaps

| Claim | Plan check | Gap |
|-------|------------|-----|
| Faithful content vs v1.4 | “Non-empty,” topic bullets, “matching bootstrap intent” | No hash/diff against bootstrap section bodies; paraphrase allowed |
| Skills discoverable | V8 name list | No same-session invoke test; no persona catalog proof |
| Personas bind | V3 files non-empty | No spawn+prepend probe; tags-only failure mode untested |
| Gates enforce | Text in AGENTS/rules | Explicitly not hard gates (A11); no product change exercise |
| Fixture A behavioral | V11 LLM verdict + keyword | Flaky; gameable; no gold issues; no subagent evidence required |
| Commands closed | REAL/NONE/waived TODO | Waived TODO + complete is permanent green on empty repos |
| Waiver durable | README template fields | No expiry enforcement test; agent can write waiver to “pass” residual concerns |
| “Complete” honest | Handoff bullets | Criteria 3–4 still allow “or handoff incomplete” wording adjacent to “complete only when,” inviting ship-with-asterisk |
| Rollback/re-run | Phase 0 AGENTS backup | No verify of re-run safety; no second-install dry-run |
| Fixture B/C post-install | V12 document only | No readiness criteria, no scheduled gate, no observable “B/C done” artifact |

**Non-observable / soft exits still present:**

- “Get user fill or confirm” for Phase 3 without requiring the confirmation to land in `docs/waivers/` or AGENTS.
- Residual Major Concerns → “durable waiver” with no human-auth step (author field is free text).
- V11 “mentions verification and/or testing gaps” (substring theater).
- Handoff “ask user to fill remaining commands” after already marking complete.
- Degraded mode still eligible for complete if V8/V11 pass.

**Gaming “complete” (concrete paths):**

1. Write minimal skill stubs that list in inspect → V8 pass.  
2. Self-author Fixture A review with Request Changes + “verification gaps” → V11 pass.  
3. Set all Project Test Commands to `NONE` or one perpetual waiver → Phase 3 closed.  
4. Skip any real test/coverage run.  
5. Claim bootstrap done. Goal bullets 3–4 satisfied on paper only.

## Scope concerns

**Under-scoped relative to stated Goal (especially enforce + prove, and operational reuse):**

- Idempotent re-bootstrap / second-install merge strategy for `AGENTS.md` and `.grok/**`.  
- Rollback beyond AGENTS `.bak-*`.  
- File-by-file content authority (path → bootstrap section → copy rule → content verification).  
- Durable waiver **lifecycle** (expiry, re-arm, human author, re-read algorithm in post-change skill).  
- Fixture A anti-flake / anti-game rules.  
- Fixture B/C **readiness criteria** and post-install mandatory window.  
- Partial failure resume markers.

**Over-scoped / distraction relative to install Goal:**

- Parallel fullstack skill remains in the critical path of V8’s five names while product tree is empty and git may be degraded—amplifies false readiness.  
- Privacy-safety + optional roles still ride along without binding proof (inherited from bootstrap; plan does not cut them).

**Scope creep vs bootstrap:** Plan adds useful A13/A14, DAG, and risks table—but does **not** add the operational install semantics (idempotency, rollback, merge) that an *implementation plan* is supposed to add over a content bootstrap. It reorganizes bootstrap into phases without solving install-ops.

## Comparison to prior plans

**vs source bootstrap v1.4:**

| Area | Bootstrap v1.4 | This implementation plan | Fidelity |
|------|----------------|--------------------------|----------|
| Exact file bodies | Sections 1–10 full text | Topic checklists + “prefer body text” | **Loss** — content authority weakened |
| V8 strict / V11 mandatory | Yes | Yes | Preserved |
| Durable waivers schema | Path + fields + re-read | README fields listed; weak lifecycle | Partial loss |
| Severity map / de-dupe | Full tables | Reproduced in plan | Preserved as policy text |
| Harness integration table | Full | Mostly collapsed into Goal/non-goals | Mild loss |
| Extraction / fence rules | Explicit | A13 + risk row | Preserved |
| Re-run / partial / rollback | Absent | Still absent | **Not improved** |
| Fixture B/C readiness | Post-install note only | Same + handoff pointer | **Not improved** |
| “Complete” vs operational gates | A11 + empty-repo honesty | Same tension; gaming paths clearer | Unresolved |

**vs prior cold review of bootstrap v1.3 (`grokbuild-agentic-dev-team-template-bootstrap.review.md`):**

Bootstrap v1.4 and this plan correctly fold: `.grok/` paths, strict V8, Fixture A, durable waivers, git Phase 0, implement/review de-dupe, severity map, `disable-model-invocation`, closed Phase 3. They do **not** fold: enforcement vs prompt pressure, Fixture A determinism, second-merge strategy, content integrity checks, B/C as real post-install gates. The implementation plan **adds vague steps** (“matching bootstrap intent,” “verbatim in spirit,” “user confirm”) where bootstrap already solved content by embedding it—raising the risk that execution invents stubs bootstrap already specified.

**Vague steps bootstrap already solved with concrete bodies:**

- Phase 2.1–2.8 topic lists vs bootstrap §1–10 copy-paste.  
- “Non-stub skills” vs full skill markdown in §6.  
- Waiver “template fields” vs full README body in §9.  
- Fixture bad-plan content already exact in §10—plan only says “intentionally weak.”

## Overall

**Not ready to execute as written if “execute” means a faithful, re-runnable, non-gameable install of bootstrap v1.4.** The plan correctly sequences Phase 0–5 and preserves strict V8/V11 and closed Project Test Commands at the policy level, but it **loses content authority** (no file-by-file mandatory extract/verify), **omits install operations** (idempotent re-run, partial recovery, rollback, second-merge with product AGENTS), **leaves waiver expiry as a field without a lifecycle**, and **treats a flaky/self-gradable LLM Fixture A as the behavioral pillar of “complete.”** On this empty workspace, complete is achievable without any operational test gate—by design of Phase 3 NONE/waive—while still claiming Goal success. **Minimum before execute:** (1) mandate copy-from-bootstrap with a path↔section table and a content-diff or required-phrase checklist per file; (2) define re-bootstrap merge/overwrite/skip rules and a rollback note for `.grok/`; (3) harden V11 (gold-standard concerns, require subagent evidence, fail on Approve, ban keyword-only pass); (4) specify waiver expiry re-arm + human author rule and wire re-read into post-change steps; (5) add Fixture B/C readiness criteria and state explicitly that “bootstrap complete ≠ accuracy gates operational” when Unit/Regression are NONE/waived. Without those, implementers will ship a discoverable scaffold that can be labeled done while diverging from v1.4 and gaming proof.
