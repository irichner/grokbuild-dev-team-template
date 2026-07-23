# Plan: Compile all agents into `/plan` and `/implement` skills

**Status:** Implemented (WP1–WP3)  
**Type:** Harness / template architecture (no product TaskBoard code)  
**Date:** 2026-07-22  

## 1. Goal + acceptance criteria

**Goal:** Every GrokForge `gf-*` agent is owned and only spawned through one of two operator skills:

| Skill | Path | Owns |
|-------|------|------|
| **`/plan`** | `.grok/skills/plan/SKILL.md` | Plan authoring + plan critique |
| **`/implement`** | `.grok/skills/implement/SKILL.md` | Code change + accuracy gates through merge readiness |

**Acceptance (falsifiable):**

1. Project skills include **`plan`** and **`implement`** with full orchestrated procedures (not stubs).  
2. Agent ownership is explicit in both skills + `AGENTS.md` + `.grok/README.md` (table: persona → skill → phase).  
3. Spawn policy: Lead spawns `gf-*` **only** when executing `/plan` or `/implement` steps (documented in `spawn.md` + accuracy rules).  
4. Content of deprecated skills is **inlined** into plan/implement; old skill dirs remain as **thin redirect stubs** only (muscle memory + installer backward compat).  
5. Installer `EXPECTED_SKILLS` + verify + unit tests pass with the new set.  
6. Docs (`AGENTS.md`, `WORKFLOW.md`, `FEATURES.md`, `USER_GUIDE.md`, install skill, workflow narrative) reference `/plan` and `/implement` as primary entry points; old slash names marked deprecated.  
7. Persona instruction files stay as **inject modules** (not deleted).  
8. `install-agentic-team` remains a third skill (meta-install; not an SDLC agent owner).

## 2. Non-goals

- Re-implement host bundled `/implement` memory loop, multi-effort parallel reviewers, or `memory.py` inside the project skill.  
- Delete persona TOMLs/instructions or collapse all personas into one blob.  
- Change TaskBoard product code, pytest product tests (except installer/harness tests).  
- Install Claude sibling agents into Grok path.  
- Force Plan Mode host agent to disappear; project `/plan` is the **durable plan + critique** skill (may start after Plan Mode session file exists).  
- Nest subagent orchestration (children still cannot spawn).

## 3. Risk / blast radius

| Area | Impact |
|------|--------|
| Operator muscle memory | Old slash names (`/plan-review-loop`, `/post-change-accuracy-protocol`, etc.) become redirects |
| Host skill name collision | Project `plan` / `implement` may take precedence over host skills in this workspace — intentional; document clearly |
| Installer targets | New skills must ship; old skill paths must still exist as stubs so verify/copy of trees does not break partial upgrades |
| AGENTS.md / rules auto-load | Pipeline text rewrite; high visibility |
| Long SKILL.md files | implement skill will be large; mitigate with clear sections + TOC, not nested skills as first-class agents |

## 4. Agent → skill ownership map (target)

| Agent / role | Skill | Phase | capability_mode |
|--------------|-------|-------|-----------------|
| Lead (inline explore + write durable plan) | `/plan` | Explore + author | n/a (Lead) |
| `gf-plan-reviewer` | `/plan` | Critique (max 2 passes) | `read-only` |
| Optional external `/cold-review` | `/plan` (optional step) | Adversarial critique if host lists it | per host |
| `gf-backend` | `/implement` | Code + tests | `all` |
| `gf-frontend` | `/implement` | UI code + tests | `all` |
| `gf-debugger` | `/implement` | Bug path: reproduce→fix | `all` |
| `gf-qa` | `/implement` | Targeted + regression loops | `execute`/`all` |
| `gf-reviewer` | `/implement` | Code review when host `/review` missing | `read-only` |
| Host `security-auditor` (if present) | `/implement` | Conditional security pass | host |
| Host `/check-work` (if present) | `/implement` | Final session verify | host |

**Forbidden:** Spawn any `gf-*` outside `/plan` or `/implement` procedure steps (except user explicitly overrides for emergency debugging — still record skill context).

## 5. Ordered implementation steps + per-step verification

### Step 1 — Create `/plan` skill (authoritative)

**Write** `.grok/skills/plan/SKILL.md` with:

1. Frontmatter: `name: plan`, description covering durable plan + critique, `disable-model-invocation: true`.  
2. **Phase A — Explore:** map code/contracts; read-only; no product edits.  
3. **Phase B — Author:** write/update `docs/plans/<name>.md` with hard gates 1–8 (point at `.grok/docs/plan-quality-standards.md`). Sync from session Plan Mode file if that is the only source. Reject chat-only as durable.  
4. **Phase C — Critique (inlined plan-review-loop):** spawn `gf-plan-reviewer` with prepended instructions; Lead persists `docs/plans/<name>.review.md` / `.review-2.md`; max 2 passes; plan must change between passes; optional cold-review note.  
5. **Exit criteria table:** Ready to implement | Blocked | Waived residual.  
6. **Agents owned** section listing only Lead + `gf-plan-reviewer`.  
7. Explicit: do **not** implement from this skill.

**Verify:** File exists; hard gates 1–8 listed; spawn checklist matches `spawn.md`; no product-code edit instructions for reviewer.

### Step 2 — Create `/implement` skill (authoritative)

**Write** `.grok/skills/implement/SKILL.md` with TOC sections:

1. **Preconditions** — plan Approve/waiver when planning was required; trivial/spike escapes.  
2. **Mode select**  
   - `feature` (default): sequential `gf-backend` and/or `gf-frontend`  
   - `bugfix`: `gf-debugger` first (fail-then-pass evidence)  
   - `parallel-fullstack`: contract freeze + worktrees (inlined from parallel-fullstack-feature)  
3. **Implement phase** — Lead-only spawn; prepend instructions; `capability_mode`; Ready:yes rules.  
4. **Accuracy protocol (inlined post-change)** — mandatory order:  
   - Targeted unit loop (inlined from targeted-unit-test-loop) → `gf-qa`  
   - Review: host `/review` or `gf-reviewer`; implement de-dupe rules; conditional security  
   - Regression loop (inlined) → `gf-qa`  
   - UI verification when UI changed  
   - `/check-work` (or DEGRADED path)  
   - Max 3 protocol cycles  
5. **Exit / merge / metrics** — gates table; prepare_commit_metrics reminder.  
6. **Agents owned** section: backend, frontend, debugger, qa, reviewer (+ host security/check-work).  
7. **Relationship to host `/implement`:** Project skill is the **template-authoritative** path for accuracy-gated work. Do not reimplement host memory/effort multi-reviewer loop; if host skill is still preferred for a pure implement→review spin, user may invoke host explicitly — default for this template is project `/implement`.

**Verify:** All five protocol steps present; loops cap at 3; de-dupe only skips review not QA; parallel path requires git + contract.

### Step 3 — Deprecate old skills → thin redirect stubs

Replace body of each with short deprecation pointing to `/plan` or `/implement`:

| Old skill | Redirects to | Notes |
|-----------|--------------|-------|
| `plan-review-loop` | `/plan` Phase C | Keep frontmatter name for discoverability; description says deprecated |
| `targeted-unit-test-loop` | `/implement` Accuracy → Targeted | Same |
| `regression-test-loop` | `/implement` Accuracy → Regression | Same |
| `post-change-accuracy-protocol` | `/implement` Accuracy protocol | Same |
| `parallel-fullstack-feature` | `/implement` mode `parallel-fullstack` | Same |
| `install-agentic-team` | **unchanged** (not deprecated) | Meta skill |

Stub content pattern:

```markdown
# Deprecated: use /plan or /implement
This skill is no longer a first-class entry point. Full procedure lives in
`.grok/skills/plan/SKILL.md` or `.grok/skills/implement/SKILL.md`.
Lead: open that skill and re-enact; do not spawn agents from this stub alone.
```

**Verify:** Stubs exist; grep for “Deprecated”; no full loop logic remaining in stubs (avoids dual sources of truth).

### Step 4 — Policy updates (auto-loaded)

Update:

- `AGENTS.md` — Default change pipeline: step 1–2 collapse under **`/plan`**; step 3–4 under **`/implement`** (implement includes post-change protocol). Personas table adds “Owned by skill” column.  
- `.grok/rules/accuracy-coverage.md` — same pipeline + “spawn only via plan/implement skills”.  
- `.grok/rules/spawn.md` — rule: `gf-*` only from plan/implement procedures; description tags unchanged.  
- `.grok/README.md` — skills table: plan + implement primary; old names deprecated.  
- `.grok/workflows/post-change-testing-protocol.md` — point source of truth to implement skill.

**Verify:** No remaining “prefer free-standing `/plan-review-loop` as default primary” without deprecation note.

### Step 5 — Docs surface updates

- `docs/WORKFLOW.md` — phases use `/plan` and `/implement`  
- `docs/FEATURES.md` — skill inventory + agent map  
- `docs/USER_GUIDE.md` — operator entry points  
- `.grok/skills/install-agentic-team/SKILL.md` — expected skills list  
- Any fixtures/acceptance text that names old skills as primary

**Verify:** Grep for primary references to old slash names; remaining hits are deprecation aliases only.

### Step 6 — Installer + tests

- `scripts/install_agentic_team.py`  
  - `EXPECTED_SKILLS` = `("plan", "implement", "install-agentic-team")` **plus** deprecated stub names if we still ship them for compatibility: include stubs in `EXPECTED_SKILLS` so `--verify` still checks tree integrity.  
  - Recommended set:  
    `plan`, `implement`, `install-agentic-team`,  
    and deprecated: `plan-review-loop`, `targeted-unit-test-loop`, `regression-test-loop`, `post-change-accuracy-protocol`, `parallel-fullstack-feature`  
  - Handoff text: prefer `/plan` then `/implement`  
- `tests/test_install_agentic_team.py` — assert new skills exist; stubs exist; verify list updated  

**Verify:** `python -m pytest tests/test_install_agentic_team.py -q` green; `python -m ruff check scripts tests` if touched.

## 6. Testing strategy

| Layer | What |
|-------|------|
| Unit | Installer tests: skills present, verify paths, persona instructions still required |
| Contract | Grep-style sanity: plan skill mentions `gf-plan-reviewer`; implement skill mentions all five remaining personas |
| Negative | Stubs do not contain full “while pass <= 2” / “MAX = 3” loop bodies (prevent dual maintenance) |
| Edge | `install-agentic-team` still installs and verifies; no TaskBoard regression expected |
| Coverage | N/A product lines; harness/docs change — record `UNMEASURED / no changed product lines` if only template docs/skills change. If installer Python changes, cover with existing tests (≥80% changed lines via diff-cover when measured) |

## 7. Failure modes

| Failure | Mitigation |
|---------|------------|
| Host and project both named `implement` confuse Lead | Document project skill as authoritative for this template; stub notes |
| Implement SKILL.md too large → model skips sections | Numbered mandatory order; TOC; “do not skip accuracy” banner at top |
| Someone spawns `gf-qa` ad-hoc | spawn.md + accuracy rules forbid outside implement skill |
| Install targets mid-upgrade | Keep deprecated dirs so old docs/links soft-fail to redirect |
| Plan skill vs Plan Mode | Clarify: Plan Mode may draft session plan; project `/plan` owns durable MD + critique |

## 8. Observable verification

- Files exist at paths above.  
- `pytest tests/test_install_agentic_team.py` exit 0.  
- Manual: open `/plan` and `/implement` skill descriptions and confirm agent ownership tables.  
- Reject “should work” — use grep counts: zero primary “Default path: `/plan-review-loop`” without Deprecated.

## 9. UI/UX design

**N/A** — no product UI surfaces. (Harness docs only.)

## 10. Assumptions

1. User chose skill names **`plan`** + **`implement`**.  
2. User chose **inline + deprecate** old standalone skills.  
3. Personas remain separate files for prepend injection.  
4. Project implement skill intentionally does **not** clone host implement memory/effort machinery.

## 11. Ship-failure thinking

If Lead still treats old skills as full procedures after this change, dual sources of truth return. **Prevention:** stubs must not contain runnable loop bodies; AGENTS.md pipeline must only name `/plan` and `/implement` as first-class.

If implement skill omits a protocol step during inline, accuracy gates weaken silently. **Prevention:** copy exit-criteria tables verbatim from current post-change + targeted + regression skills; checklist review in plan-review pass.

## 12. Work packages (for implement)

### WP1 — Skills (create plan + implement; stub deprecations)

- Create `.grok/skills/plan/SKILL.md`  
- Create `.grok/skills/implement/SKILL.md`  
- Replace bodies of 5 deprecated skills with redirects  
- Update `.grok/workflows/post-change-testing-protocol.md`  

### WP2 — Policy + docs

- `AGENTS.md`, `.grok/rules/*`, `.grok/README.md`  
- `docs/WORKFLOW.md`, `docs/FEATURES.md`, `docs/USER_GUIDE.md`  
- install-agentic-team skill text  

### WP3 — Installer + tests

- `scripts/install_agentic_team.py` EXPECTED_SKILLS + handoff strings  
- `tests/test_install_agentic_team.py`  
- Run targeted pytest + ruff on touched scripts/tests  

**Suggested implement order:** WP1 → WP2 → WP3 (single sequential implementer; no parallel needed).

## 13. Out-of-scope follow-ups (optional later)

- Version bump of TEMPLATE_VERSION string in installer when shipping as release.  
- Workflow Rhai automation wrapping `/plan` then `/implement`.  
- Thin host-implement adapter mode inside project implement (effort/memory).
