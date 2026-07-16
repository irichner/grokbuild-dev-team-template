# Plan: GrokForge Template Accuracy Review + Remediation

**Date:** 2026-07-15  
**Mode:** Multi-agent review complete (explore ×3 → adversarial code-reviewer ×1)  
**Template:** v1.7.1 (`VERSION`) / feature train 1.7  
**Primary optimization:** Code accuracy + implementation accuracy of the harness and seed product

---

## Context

This repository is the **GrokForge Agentic Dev Team** template: Lead rules (`AGENTS.md`), auto-loaded `.grok/rules/`, orchestration skills, personas, install/metrics scripts, acceptance fixtures A–E, and a TaskBoard seed app used to exercise the accuracy pipeline.

**Why this review:** The template’s purpose is to spawn specialist loops that maximize correctness. A self-review must therefore stress (1) whether the harness gates are sound and executable, (2) whether the seed product and fixtures actually falsify failures, and (3) whether dual-stack docs undermine the operator/agent path.

**Review method (completed in this session):**

| Loop | Agents | Focus |
|------|--------|--------|
| 1 | explore (harness map) | Architecture, skills inventory, doc dual-identity, consistency |
| 1 | explore (skills deep dive) | Loop GO/NO-GO, de-dupe, coverage/UI, handback, fixtures |
| 1 | explore (product + scripts) | TaskBoard, installer, metrics, test accuracy |
| 2 | code-reviewer (adversarial) | Validate/rank claims; kill theater; prioritize fixes |

---

## Goal + measurable acceptance criteria

### Review deliverable (this session — done when plan approved)

- [x] Multi-agent review with second-pass adversarial validation  
- [ ] Durable plan with severity-ranked findings + work packages  
- [ ] Clear non-goals and “do not change” list  

### Remediation success (when implementation is authorized)

| ID | Criterion | Observable pass |
|----|-----------|-----------------|
| A1 | Fixture B plant fails existing clamp tests | Plant seed bug → `pytest tests/test_util.py` red; unplant → green |
| A2 | QA product-bug path does not burn 3-run budget | Skill + `gf-qa.md` say: handback → stop (`WAITING_ON_PRODUCT`); cycle resumes only after product fix |
| A3 | `/review` de-dupe requires zero bugs **and** zero gate-mapped gaps | Same wording in `AGENTS.md`, `accuracy-coverage.md`, `post-change-accuracy-protocol/SKILL.md` |
| A4 | Operator docs primary path = GrokForge | `docs/USER_GUIDE.md` (and siblings) install `.grok/` + AGENTS pipeline, or Claude content is explicitly secondary/legacy with banner |
| A5 | Host skill dependency is fail-closed or degraded | Installer `--verify` and/or protocol skill documents probe; missing `/review` or `/check-work` → explicit degraded/NO-GO, not silent skip |
| A6 | Plan-review write ownership is coherent | Read-only child returns report; Lead writes `docs/plans/*.review.md` |
| A7 | Targeted/protocol exit tables align with merge coverage waiver rule for `NO COVERAGE TOOL` | Skill GO tables require durable waiver cite when tool absent |
| A8 | Hook install is non-destructive by default | Existing `.git/hooks/pre-commit` backed up or refuse without `--force` |
| A9 | Targeted tests + lint green after code changes | `python -m pytest tests/ -q`; `python -m ruff check src tests scripts` |

---

## Non-goals

- Replacing host-bundled `/implement`, `/review`, `/check-work` with full reimplementations  
- Making tags/persona names auto-bind instructions (platform cannot; prepend stays mandatory)  
- Collapsing `TEMPLATE_VERSION` (feature train) and `VERSION` (patch-per-commit) into one scheme  
- Adding CLI persistence as a product feature (optional later; not accuracy-critical)  
- Deleting the Claude `.claude/` tree unless user chooses single-stack (may re-label docs instead)  
- Running full acceptance fixtures B–E on throwaway branches in this plan phase  

---

## Risk / blast radius

| Risk | Impact | Mitigation |
|------|--------|------------|
| Doc rewrite confuses Claude-stack users | Medium | Banner dual-stack; keep `.claude/` usable; AGENTS remains Grok Lead source |
| Tightening de-dupe increases review cost | Low | Still skip only when implement report shows bugs=0 and gaps=0 |
| Coverage waiver strictness blocks empty-tool repos | Medium | `NO COVERAGE TOOL` + durable waiver path already exists; vacuous UNMEASURED stays free |
| Hook backup changes install behavior | Medium | Default safe; `--force` for overwrite |
| Fixture B rewrite breaks handoff narrative | Low | Update fixture README + handoff notes in same WP |

**Blast radius:** Mostly `.grok/**`, `AGENTS.md`, `docs/*`, fixtures, small script/test changes. No production service. Installer consumers of future template versions inherit WP2–WP5 policy text.

---

## Review findings (validated)

### Strengths (keep)

1. **Coherent accuracy pipeline:** plan gates → Ready bar → targeted (accuracy + lint + coverage) → review/security → regression → UI → check-work → metrics.  
2. **Aligned loop caps** (plan 2 / targeted 3 / regression 3 / protocol 3) across AGENTS, rules, skills, personas.  
3. **Honest coverage semantics:** vacuous diff-cover ≠ 100%; ladder + compare-branch.  
4. **Test-accuracy as a first-class gate** + QA independence (tests only).  
5. **UI as gate 8** + protocol step with design blockers → gap.  
6. **Installer quality:** no product leakage, conflict backups, ledger never clobbered.  
7. **Tags subsystem** (product + tests) is a strong accuracy demo.  
8. **Metrics honesty:** unmeasured stamps over invented tokens.

### Critical / high (fix first)

| ID | Finding | Severity | Evidence |
|----|---------|----------|----------|
| **P3** | Fixture B seeded clamp “bug” is **value-noop** — both `< hi` and `<= hi` yield same returns; existing tests stay green | **High** | `fixtures/.../seeded-bug-notes.md`; `tests/test_util.py` |
| **H4** | Product-bug handback still advances full suite cycle — burns 3-run budget without waiting for fix | **High** | `targeted-unit-test-loop`, `gf-qa.md` loops |
| **H2** | `/review` de-dupe keys off **bugs only**, not gate-mapped **gaps** | **High** | `AGENTS.md` de-dupe; merge gate still wants no bug/gap |
| **H7** | Protocol depends on host `/review`, `/check-work`, `/implement` — not vendored; missing host → silent incomplete protocol | **High** | post-change skill; no project wrappers |
| **H1** | Operator `docs/USER_GUIDE|WORKFLOW|FEATURES` teach **Claude Code** (`.claude/`, `/ship`); installer delivers **GrokForge** | **High** | `docs/USER_GUIDE.md` L29–36 vs `README.md` install |

### Medium

| ID | Finding | Severity |
|----|---------|----------|
| **H3** | `NO COVERAGE TOOL` can targeted/protocol GO without requiring durable waiver (merge policy stricter) | Medium |
| **H5** | Plan-review spawn is read-only but skill/persona say write `*.review.md` | Medium |
| **M5** | UI verification lacks structured report schema (rubber-stamp risk) | Medium |
| **P2** | `install_git_hooks.py` overwrites existing pre-commit with no backup | Medium |
| **M6** | `Claude.md` Project Facts still placeholders | Medium (tied to H1) |

### Lower / intentional (do not over-fix)

| ID | Notes |
|----|--------|
| **H6** | Prepend-only personas are **by design**; do not invent fake auto-bind |
| **P1** | Ephemeral CLI is documented smoke-only — low accuracy impact |
| **M2** | `1.7` feature train vs `1.7.1` VERSION is intentional dual scheme |
| **M1** | CI lint includes `scripts`; AGENTS lint does not — minor align |
| **M3** | Bad env ints → uncaught `ValueError` in prepare_commit_metrics |
| **M4** | Board edge test gaps (`set_priority` clamp, `get` miss) — polish |

---

## Recommended approach

Implement remediation in **five work packages** ordered by accuracy ROI. Prefer **smallest viable policy/code diffs**; no harness redesign.

### WP1 — Fixture B + seed product test accuracy (highest ROI)

**Files:**
- `fixtures/agentic-template-acceptance/seeded-bug-notes.md`
- `fixtures/agentic-template-acceptance/README.md` (Fixture B pass criteria)
- Optionally strengthen `tests/test_util.py` / `tests/test_board.py` for M4 edges

**Change:**
- Replace seeded defect with a **value-breaking** bug that fails current tests when planted, e.g.:

```python
def clamp(n, lo, hi):
    if lo > hi:
        raise ValueError(...)
    if n < lo:
        return lo
    if n > hi:
        return n  # BUG: should return hi
    return n
```

- Document plant → red / unplant → green procedure explicitly.
- Add board negatives if cheap: `set_priority` out of range + unknown id; `get` → `None`.

**Reuse:** existing `clamp` tests as the falsifier (do not invent parallel fixture-only tests that only the seed bug would use unless needed).

**Verify:** plant mutation manually on throwaway branch → targeted suite red on `test_clamp_*`; restore → green.

### WP2 — Harness loop honesty (de-dupe, handback, coverage)

**Files:**
- `AGENTS.md`
- `.grok/rules/accuracy-coverage.md`
- `.grok/skills/targeted-unit-test-loop/SKILL.md`
- `.grok/skills/regression-test-loop/SKILL.md`
- `.grok/skills/post-change-accuracy-protocol/SKILL.md`
- `.grok/personas/instructions/gf-qa.md`

**Change:**
1. **De-dupe predicate:** skip `/review` only when implement left **zero open bugs and zero gate-mapped gaps** + tree match evidence (`git status --porcelain` / scope note). If implement artifact unclear → **run `/review`**.  
2. **Product-bug handback:** after triage = product bug → emit `WAITING_ON_PRODUCT` / NO-GO handback; **do not** consume remaining full-suite cycles until product fix lands; on protocol re-entry reset nested `cycle` to 0.  
3. **`NO COVERAGE TOOL`:** targeted + protocol exit tables require durable waiver path **for merge-grade done**; vacuous `UNMEASURED / no changed lines` remains allowed without waiver; product-diff + empty diff-cover → diagnose/NO-GO first.

**Verify:** text consistency across the six files (grep de-dupe / WAITING_ON_PRODUCT / NO COVERAGE TOOL). Optional: short scenario notes in fixture README (C, D).

### WP3 — Plan-review write ownership + UI verify schema

**Files:**
- `.grok/skills/plan-review-loop/SKILL.md`
- `.grok/personas/instructions/gf-plan-reviewer.md`
- `.grok/skills/post-change-accuracy-protocol/SKILL.md`
- Optionally `.grok/docs/ui-design-standards.md` (pointer only)

**Change:**
- Child (read-only) returns Review Report body in chat; **Lead** writes `docs/plans/<name>.review.md` / `.review-2.md`.  
- Add **UI Verification Report** schema (mode, surfaces, blockers, evidence paths, NO UI TOOLING + waiver/manual checklist, PASS/FAIL).  
- `NO UI TOOLING` alone is not merge PASS without manual blocker checklist or durable ui-design waiver.

**Verify:** no skill step requires read-only child to write files.

### WP4 — Operator docs single identity + host skill probe

**Files:**
- `docs/USER_GUIDE.md`, `docs/WORKFLOW.md`, `docs/FEATURES.md` (rewrite primary path **or** legacy banner + Grok section)
- `Claude.md` Project Facts (fill from AGENTS REAL commands **or** mark non-authoritative for Grok Lead)
- `.grok/skills/install-agentic-team/SKILL.md` and/or `scripts/install_agentic_team.py` verify messages
- `.grok/skills/post-change-accuracy-protocol/SKILL.md` (host skill missing → degraded)
- `README.md` (cross-link if needed)
- `docs/plans/bootstrap-handoff.md` (one-line accuracy notes)

**Change:**
- Primary install/use story = GrokForge (`.grok/`, `AGENTS.md`, `/plan-review-loop`, `/post-change-accuracy-protocol`).  
- Claude stack documented as optional sibling if kept.  
- Protocol/install: if host lacks `/review` or `/check-work`, record `HOST_SKILLS=PARTIAL` and either run thin local review checklist or NO-GO for merge claims — never silent skip.

**Verify:** opening `docs/USER_GUIDE.md` cannot be mistaken for “copy `.claude/` only” as the Grok path.

### WP5 — Scripts hygiene (ship with or after WP4)

**Files:**
- `scripts/install_git_hooks.py` + new `tests/test_install_git_hooks.py`
- `scripts/prepare_commit_metrics.py` + tests for bad ints
- `AGENTS.md` Lint row (optional: include `scripts` to match CI)

**Change:**
- Backup existing pre-commit (`pre-commit.bak.<ts>`) or require `--force`.  
- Catch `ValueError` on token parse → clear `SystemExit` message.  
- Align lint command with CI if desired.

**Verify:** unit tests for hook backup + bad `INPUT=abc`.

---

## Implementation order

```
WP1 (Fixture B) → WP2 (loop honesty) → WP3 (plan/UI schema) → WP4 (docs + host probe) → WP5 (scripts)
```

- After any WP that touches executable code/tests/scripts: run `/post-change-accuracy-protocol` (or targeted + lint + regression + check-work).  
- Docs-only WPs: trivial escape for full regression; still sanity-read links.  
- Prefer single implementer per WP with prepended `gf-backend` / docs edits by Lead for pure markdown.

---

## Ordered steps with verification

1. **WP1** — Fix Fixture B seed; optional board edge tests.  
   - *Verify:* plant/unplant procedure; `pytest tests/test_util.py tests/test_board.py -q`  
2. **WP2** — Align de-dupe, handback, coverage GO tables.  
   - *Verify:* grep consistency; no contradictory max-cycle tables  
3. **WP3** — Plan-review Lead-write + UI report schema.  
   - *Verify:* skill text re-read; Fixture E notes mention UI report  
4. **WP4** — Docs dual-identity fix + host skill degrade path.  
   - *Verify:* USER_GUIDE first screen is GrokForge-primary  
5. **WP5** — Hook backup + metrics parse errors + tests.  
   - *Verify:* new unit tests green; ruff on scripts  
6. **Protocol** — targeted + lint + coverage/UNMEASURED + `/review` + regression + `/check-work`.  
7. **Commit metrics** — `prepare_commit_metrics.py` with measured or `--unmeasured`; bump VERSION + ledger.

---

## Testing strategy

| Layer | What | Edge/negative |
|-------|------|----------------|
| Unit | Fixture B plant fails `test_clamp_*` | Boundary values after plant |
| Unit | Hook install backup / refuse without force | Existing hook present |
| Unit | prepare metrics bad int env | `INPUT=abc` → exit ≠ 0, clear message |
| Unit | Board edges (if WP1 expands) | unknown id, priority clamp |
| Harness text | Grep de-dupe / WAITING_ON_PRODUCT / NO COVERAGE TOOL | No bugs-only de-dupe left |
| Manual acceptance | Fixture B on throwaway branch | Review + tests both catch |
| Regression | Full `pytest tests/ -q` | After script/product edits |
| Coverage | diff-cover when product lines change | ≥80% or UNMEASURED honestly |

**Coverage expectation:** Script/product changes aim ≥80% changed lines when measurable; pure policy markdown → UNMEASURED / no changed lines.

**Lint:** Prefer CI-aligned `python -m ruff check src tests scripts` once AGENTS updated.

---

## Failure modes

| Failure | Response |
|---------|----------|
| Planted Fixture B still green | Wrong mutation; re-design value-breaking bug |
| Stricter de-dupe causes always-run `/review` | Acceptable; cost for accuracy; only skip when implement report lists gaps=0 |
| Docs rewrite incomplete (Claude leftover as primary) | Block WP4 done until first 40 lines of USER_GUIDE are GrokForge |
| Host has no skill probe API | Document manual `grok inspect` check + degraded protocol checklist |
| Hook chain needed (Husky) | Prefer backup + warn; do not auto-merge foreign hooks without user choice |

---

## Observable verification (reject vague “works”)

- Fixture B: command transcript with failing then passing `pytest` after plant/unplant.  
- Skills: unified de-dupe sentence present in three policy surfaces.  
- Docs: `docs/USER_GUIDE.md` installs `.grok/` not only `.claude/`.  
- Scripts: new tests pass; ruff exit 0.  
- Protocol: QA report GO + check-work `VERDICT: PASS` for the remediation session.

---

## UI/UX design gate

**N/A** — no product UI surface changes in this plan (Fixture E sample-ui untouched unless a later optional polish). Gate 8 does not apply.

---

## Critical files

| Path | Role |
|------|------|
| `AGENTS.md` | Lead policy, de-dupe, Project Test Commands |
| `.grok/rules/accuracy-coverage.md` | Merge gates |
| `.grok/rules/spawn.md` | Spawn discipline (keep) |
| `.grok/skills/*/SKILL.md` | Loop procedures |
| `.grok/personas/instructions/gf-*.md` | Specialist behavior |
| `fixtures/agentic-template-acceptance/*` | Acceptance truth |
| `docs/USER_GUIDE.md` (+ WORKFLOW, FEATURES) | Operator identity |
| `scripts/install_git_hooks.py` | Hook safety |
| `scripts/prepare_commit_metrics.py` | Metrics edge handling |
| `src/taskboard/util.py` / `tests/test_util.py` | Fixture B falsifier |

**Reuse:** existing QA report schema, plan-quality hard gates, coverage-policy vacuous rules, installer’s EXPECTED_* verify lists.

---

## Work package dispatch (implement phase)

| WP | Specialist | capability_mode | Notes |
|----|------------|-----------------|-------|
| WP1 | Lead or `gf-backend` | `all` | Fixture + optional board tests |
| WP2 | Lead | `read-write` | Policy skill alignment |
| WP3 | Lead | `read-write` | Plan-review + UI schema |
| WP4 | Lead / docs | `read-write` | Dual-identity docs |
| WP5 | `gf-backend` | `all` | Scripts + tests |
| QA | `gf-qa` | `execute`/`all` | After WP1/WP5 |

Max plan-review for this plan: 2 passes via `/plan-review-loop` before implement.

---

## Residual risks after remediation

- Soft enforcement remains: Grok path has no Stop-hook equivalent; accuracy still depends on Lead running protocol.  
- Host skill completeness varies by Grok install; degrade path reduces but does not eliminate dependency.  
- Claude dual-tree may still load in mixed sessions — WP4 docs help; session precedence may need ongoing discipline.

---

## Summary verdict of current template

| Dimension | Grade | Notes |
|-----------|-------|-------|
| Harness loop design | **Strong** | Caps, accuracy blockers, UI gate, metrics integrity |
| Spec executable detail | **Good with holes** | Handback, de-dupe gaps, read-only write, UI report |
| Operator docs | **Weak for Grok** | Claude primary in `docs/*` |
| Acceptance fixtures | **Mixed** | A good; B broken; C–E manual |
| Seed product tests | **Good tags / weak CLI** | Tags exemplary; Fixture B story fails |
| Installer/scripts | **Strong + edge gaps** | Hook clobber; metrics parse |

**Bottom line:** The GrokForge core is a mature accuracy harness with aligned policies. Highest-impact accuracy holes are **Fixture B’s non-catching seed bug**, **QA handback budget burn**, **bugs-only review de-dupe**, **Claude-primary operator docs**, and **host skill soft dependency**. Remediation is mostly policy + fixture + small script fixes—not a redesign.

---

## Decision needed from user

Approve this plan to implement WP1→WP5 (or a subset). Recommended default: **all five WPs** for highest template accuracy; minimum viable accuracy pack is **WP1 + WP2**.

---

## Plan critique (pass 1)

- **Overall:** Approve (`gf-plan-reviewer`, hard gates 1–8 PASS; gate 8 N/A)
- **Required changes:** none
- **Soft nits for implement:** (1) make A5 fail-closed with explicit `HOST_SKILLS=PARTIAL` never silent skip; (2) do not claim M4 closed if board edges skipped; (3) optional Assumptions section if WP4 host probe needs `grok inspect`
