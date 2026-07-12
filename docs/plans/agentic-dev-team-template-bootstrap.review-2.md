# Cold review of agentic-dev-team-template-bootstrap

**Reviewer:** Cold review agent #2 (fresh context)  
**Date:** 2026-07-12  
**Plan version reviewed:** Draft v1  
**Focus:** Implementability; extraction; persona binding; handoff

**Workspace check (2026-07-12):** Repo root has `grokbuild-agentic-dev-team-template-bootstrap.md` (v1.4), `grokbuild-agentic-dev-team-template-bootstrap.review.md` (v1.3 source review), and `docs/plans/agentic-dev-team-template-bootstrap.md` only. No `docs/plans/_archive/`. No `.grok/`, no product app, no fixtures yet. `list_dir` hides dot dirs; plan’s “git may be absent” posture matches prior review (`projectRoot: null`). User environment is **Windows / PowerShell** — plan never mentions that.

---

## Top three weakest assumptions

1. **“Verbatim in spirit” is a safe extraction contract (plan Exploration + Phase 2).**  
   The plan simultaneously says (a) content authority is bootstrap v1.4 sections 1–10, (b) “prefer bootstrap body text,” and (c) create files **“verbatim in spirit”** (same structure, gates, schemas). That phrase is an explicit license to paraphrase. Phase 2 checklists then restate each file as bullet *topics* (e.g. “gf-qa … including QA Test Report schema”), not as copy operations with fence boundaries. A new engineer who implements from the plan alone will invent prose; two installs of the “same” plan will diverge on gates wording, report schemas, de-dupe rules, and skill steps. The fence-corruption mitigation in A13 is useless if the implementer never opens the bootstrap fences.

2. **A new engineer can complete Phase 2 + V8/V11 without a mechanical extract procedure or runtime API recipes.**  
   Plan never specifies: how to locate fence open/close for each path heading; what to do when outer fence is `~~~~` vs ``````; how to parse `grok inspect --json` (field names, source filter, jq/PowerShell); exact `spawn_subagent` shape for Fixture A; or where handoff lives (chat vs durable file). V11 pass criteria depend on model judgment (“mentions verification and/or testing gaps”) with no deterministic scrapable fields. On a greenfield Windows machine, `grok` not on PATH is treated as “CLI unavailable → incomplete,” but the plan gives zero recovery steps beyond “don’t claim done.”

3. **Writing role TOMLs + documenting “roles are not spawn binding” will prevent role/capability confusion.**  
   Phase 2.5 still *installs* `.grok/roles/gf-qa.toml` and `gf-plan-reviewer.toml` with `default_capability_mode`. Persona TOMLs also carry `default_capability_mode`. Canonical rules correctly say: prepend instructions + set `capability_mode` on spawn; tags are UI-only. A new engineer sees three competing signals (role defaults, persona defaults, skill “always set capability”) and will reasonably assume product resolution will apply defaults. Prior cold review already called roles dead weight; this plan keeps them and papers over the failure mode with a one-line “document not spawn binding” checklist item — not a spawn probe, not a negative test.

---

## Missing failure modes

- **Fence / extract corruption (still live in source, underspecified in plan):** Bootstrap v1.4 mixes `~~~~markdown` / `~~~~toml` for most bodies with **five-backtick** outer fences for `gf-qa.md` and `gf-plan-reviewer.md` (``````markdown` … ``````). Extraction note claims schemas use `~~~~` *inside* instruction files; actual schemas are **indented plain-text blocks**, not tilde fences. A hurried implementer who “copies the fence” can: (1) drop the schema indent block, (2) leave outer fence markers in the written file, (3) truncate at the first nested `` ``` `` if any remain, (4) write QA/Review schemas as markdown code fences that then break *downstream* extractors. Plan Phase verification only requires “non-empty” + “QA/Review report blocks present” — not field-complete schema equality to bootstrap.

- **Implement-from-plan-only divergence:** Suggested execution prompt says read plan *and* bootstrap, but Phase 2 is fully executable as a topic checklist. Failure mode: install that passes V1–V7 shape checks with rewritten skills missing de-dupe tables, ownership rules, or coverage “never invent %” language.

- **Persona prepend not exercised:** V3 = files non-empty. No failure mode for “catalog loads, prepend never happens.” Handoff *reminds* about prepend; nothing verifies a child received instruction text. Tag-only spawn remains the silent production failure (plan lists it under “How would this fail to ship?” but does not test it).

- **Role vs persona vs capability confusion at spawn time:** Engineer sets only `description: [gf-qa]` and relies on role TOML → read-only or generic agent → invented test results or false NO-GO. Plan mitigates in prose; skills must restate every time — no single “spawn checklist” artifact in the installed tree that is auto-loaded (roles/docs are not).

- **Windows / PowerShell command assumptions:** Plan and bootstrap use `git rev-parse`, `git status`, `git diff --name-only`, Unix home path `~/.grok/sessions/...`, Makefile/CI as scan targets, and coverage recipes written for shell one-liners. Missing failure modes: git not installed; `grok` only available as `grok.cmd` / different PATH in agent shell vs user terminal; PowerShell quoting of `grok inspect --json`; line-ending (CRLF) corruption of YAML frontmatter; path separator mistakes when writing `instructions_file = ".grok/personas/instructions/..."` vs backslashes; agents inventing bash-only pipes in AGENTS Project Test Commands on a Windows-only repo.

- **V11 non-determinism / false pass / false fail:** Model may Approve a deliberately bad plan; or Request Changes for off-topic reasons without citing verification/testing — both break the binary V11 criterion. Plan has no second-judge rule, no required Required Changes severity, no golden phrases checklist beyond “mentions verification and/or testing gaps.”

- **V8 JSON schema unknown:** “Lists skill names … (project/local/repo source)” — no sample JSON path. Engineer greps human `grok inspect` output or wrong key → false fail/pass. Source filter may not match actual inspect enums on this CLI version.

- **Dual completion status underspecified:** “Bootstrap complete” (V8+V11+tree) vs “accuracy gates operational” (commands REAL enough) vs “degraded git.” Handoff bullets list pieces but no mandatory status enum (e.g. `COMPLETE | COMPLETE_DEGRADED | INCOMPLETE`) and no rule for V1–V7 fail (only V8/V11 called out as incomplete). Engineer can claim complete with broken tree if they skip honesty.

- **AGENTS merge loss:** Backup policy improved (unique timestamp). Still no merge algorithm when existing AGENTS has conflicting pipelines, different severity maps, or existing Project Test Commands. Second bootstrap / re-run not defined.

- **Phase 2 parallel writes:** DAG allows concurrent groups with no partial-state verification until end of phase — interrupted agent leaves half a persona set; Phase 4 may start after “Phase 2 done” claim without full tree.

- **Fixture A path collision:** Copy to `docs/plans/acceptance-bad-plan.md` with no instruction if file already exists from prior bootstrap attempt.

- **Degraded install still installs parallel-fullstack skill:** Skill claims worktree behavior; handoff says don’t claim it fully works — consumers still discover `/parallel-fullstack-feature` and invoke it on non-git CWD.

- **instructions_file path resolution:** Plan allows `instructions_file` or `instructions` without stating which key Grok 0.2.x actually resolves, or whether path is repo-relative. Wrong key → catalog entry without loadable body; inject path still works only if Lead hardcodes the md path.

---

## Undocumented prior knowledge

- Bootstrap is the **only** full file-body source; the plan is an orchestration shell. New engineers who treat the plan as self-contained will under-deliver. That dependency is implied, not labeled “BLOCKING: do not invent bodies.”

- How to **mechanically extract** `~~~~` / `` ````` `` sections (strip language tag line; stop at matching close fence; do not include section headings; preserve indented schema blocks as-is).

- Why **two fence styles** exist in v1.4 (4-tilde vs 5-backtick) and that the extraction note’s claim about “`~~~~` schemas” does not match the indented-block implementation for QA/Review reports.

- Exact **spawn inject recipe** matching bundled `/review`/`/implement` (read md → prepend full text → set capability_mode → description tag for UI only). Plan states rules but never shows a concrete tool-call example.

- **Role resolution is unspecified in product docs** — installing roles teaches a fiction unless consumer docs explain they are optional catalog metadata only. Prior review already required this; plan still assumes implementer internalizes it.

- **`grok inspect --json` document shape** and how to filter project skills vs bundled/plugin (including `[compat unresolved]` cold-review).

- Session plan path encoding and when Plan Mode allows writing `docs/plans/` (copied from bootstrap assumptions; not re-verified in this plan against live CLI on Windows).

- That **this workspace is likely non-git and empty of product code** — Phase 3 will be all NONE/waived; V11 is the only behavioral proof; “ready for first product change” is aspirational documentation, not a green gate.

- Windows-specific agent shell quirks (PATH, CRLF, PowerShell vs cmd for test commands later filled into AGENTS).

- Severity map and de-dupe tables must be **byte-copied into both AGENTS and rules**, not summarized — plan Phase 2.1 lists topics; bootstrap has the authoritative tables.

---

## Verification gaps

| Claim | Plan check | Gap |
|-------|------------|-----|
| File bodies match bootstrap | “matching bootstrap intent”; non-empty; schemas “present” | No hash/diff against bootstrap sections; “intent” is subjective |
| Extraction integrity | A13 + risk row | No required checklist of schema field names (QA Mode/Coverage/Recommendation; Review Overall/Required Changes) |
| Persona usable | V3 non-empty files | No prepend probe spawn; no `/personas` catalog check |
| Roles understood | “Document not spawn binding” | No negative test; roles still installed |
| Skills discoverable | Strict V8 | No JSON example; no Windows PATH recovery; no assert on `disable-model-invocation` via inspect |
| Behavioral plan-review | V11 | Non-deterministic model verdict; no artifact path required for review output (chat OR `*.review.md`) |
| Commands closed | Phase 3 outcomes | No required waiver **user confirmation** artifact if TODO remains; engineer can self-write waiver and proceed |
| Gates operational vs bootstrap done | Handoff must not claim operational if unit+regression NONE | Not a hard Phase 4 fail; easy to bury in prose |
| Git mode | Phase 0 + handoff bullet | No V-number for git full vs degraded; degraded can still be “complete” |
| Handoff completeness | Bullet list in Phase 5 | No durable handoff file template; no mandatory status enum; V1–V7 failures not tied to incomplete |
| Windows implementability | None | Zero verification that commands/docs work under PowerShell |
| Forbidden collisions | V1 | Does not re-check skill names `review`/`code-review` explicitly in V1 table (only Phase 1 checklist) |

Phase verification language for Phase 2 (“matching bootstrap intent”) is the single largest verification hole: it reintroduces the ceremony problem Phase 4 was meant to fix, one layer earlier (wrong content, right paths).

---

## Scope concerns

**Still over-scoped for a scaffold install (carried from source, not cut by the plan):**

- `parallel-fullstack-feature` + worktree/contract machinery — high process complexity, zero accuracy proof at bootstrap; degrades on non-git template repo.
- Optional `.grok/roles/` — prior review: dead weight; plan keeps them “with a note.”
- `.grok/workflows/` narrative duplicate of a skill.
- Privacy-safety Green/Yellow/Red process — orthogonal to V8/V11.

**Under-scoped for the plan’s own focus (implementability / extraction / binding):**

- No extraction runbook (fence map, strip rules, validation diff).
- No spawn cookbook (capability_mode matrix + prepend + tag).
- No handoff status machine.
- No Windows/PowerShell notes despite owner environment.
- No definition of “verbatim” that forbids paraphrase (contradicted by “in spirit”).
- No required durable handoff path under `docs/plans/` or `docs/waivers/`.

**Scope creep relative to “implementation plan for bootstrap”:** Plan mostly restates bootstrap phases rather than adding implementer-critical procedure. Where it diverges (“verbatim in spirit,” parallel Phase 2 writes, softer Phase 2 verification), it **weakens** the source’s extract-from-bootstrap discipline without adding compensating tests.

---

## Comparison to prior plans

**vs source bootstrap v1.4:** Plan is a faithful phase DAG and acceptance map of §11, with useful operator packaging (risks table, DAG, suggested prompt, severity/de-dupe restate). It does **not** embed bodies; it depends on the bootstrap file. Source extraction rule is clearer (“use the section under each path heading only”) than the plan’s “verbatim in spirit.” Source still has the 4-tilde / 5-backtick inconsistency the plan assumes is solved.

**vs prior cold review of bootstrap v1.3 (`grokbuild-agentic-dev-team-template-bootstrap.review.md`):**

| Prior finding | Plan Draft v1 status |
|---------------|----------------------|
| Strict V8 (no CLI soft-pass) | Addressed in plan |
| Fixture A mandatory | Addressed (V11) |
| Durable waivers + severity map | Addressed |
| Implement/review de-dupe | Addressed |
| Git prerequisite / degraded | Addressed at Phase 0 |
| Nested fence corruption | Partially addressed in source; plan verification still too soft |
| Persona prepend reliability | Documented; **still not verified** |
| Roles hand-wavy / dead weight | **Still installed**; one-line disclaimer only |
| Windows vs Unix | **Still absent** (prior review noted it) |
| TODO commands forever | Phase 3 closed outcomes — good |
| Goal vs ceremony | Better (V8+V11) but Phase 2 “intent” reopens ceremony |
| Acceptance fixtures as files only | Fixed for A; B/C deferred correctly |

**No `docs/plans/_archive/`** — no other historical implementation plans to compare; only this plan + bootstrap + one source review.

**Regression introduced by the plan itself:** phrase **“verbatim in spirit”** and Phase 2 topic-only checklists are worse implementability contracts than “Write every file from the sections below” in bootstrap Phase 2. That is the plan’s distinctive failure mode.

---

## Overall

**Not ready to execute as written if the implementer is a new engineer following the plan as the primary artifact.** The plan is adequate as a phase checklist *for someone who already knows* to copy bootstrap §1–10 bodies through the correct fences, always prepend personas, ignore role defaults, parse `grok inspect --json` on their OS, and refuse “done” without V8+V11 — i.e. for the author, not a cold implementer. Minimum fixes before execution: (1) **delete “verbatim in spirit”** and require byte-faithful extraction from bootstrap fences with an explicit per-path extract map and schema field checklist; (2) **define COMPLETE / COMPLETE_DEGRADED / INCOMPLETE** handoff status with V1–V11 wiring and a durable handoff file path; (3) **add a spawn cookbook + one prepend probe** (or accept in writing that persona binding is unproven); (4) **document Windows/PowerShell** assumptions for git, `grok` PATH, and command fill; (5) **either remove roles from the install tree or mark them non-goals** so capability binding cannot be misread; (6) tighten Phase 2 verification from “intent” to “diff against bootstrap section bodies.” Without those, divergent installs and tag-only specialists remain the default failure modes the prior review already predicted.
