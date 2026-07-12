# Bootstrap handoff

- **Date:** 2026-07-12
- **Template version:** 1.4
- **bootstrap_status:** COMPLETE
- **accuracy_gates:** OPERATIONAL (updated after TaskBoard seed + green targeted/regression; see Post-bootstrap section)
- **git_mode:** full
- **V8:** PASS (`docs/plans/bootstrap-v8-inspect.json`) — five project skills present with `source.type: project`
- **V10 cold-review:** available (plugin `lanshore-claude-workflow`)
- **V11:** PASS (`docs/plans/acceptance-bad-plan.review.md`; `spawn_used: true`) — Overall: Major Concerns; gold standards covered
- **V13:** PASS (`docs/plans/bootstrap-v13-targeted-dry-run.md`) — NO-GO at bootstrap time when Unit was NONE (fail-closed proven)
- **Project Test Commands (current):**
  - Build: REAL — `python -m pip install -e ".[dev]"`
  - Unit tests: REAL — `python -m pytest tests/ -q`
  - Coverage: REAL — `python -m pytest tests/ --cov=taskboard --cov-report=term-missing`
  - Regression / full suite: REAL — `python -m pytest tests/ -q`
  - Lint / typecheck: REAL — `python -m ruff check src tests`
- **Scan evidence (bootstrap time):** no product manifests → commands were NONE; V13 NO-GO  
- **Scan evidence (post-seed):** `pyproject.toml`, `src/taskboard/`, `tests/`
- **Files created/updated:**
  - `AGENTS.md`
  - `.grok/README.md`
  - `.grok/rules/accuracy-coverage.md`
  - `.grok/personas/gf-*.toml` + `instructions/gf-*.md` (4 personas)
  - `.grok/roles/gf-qa.toml`, `.grok/roles/gf-plan-reviewer.toml` (catalog only — not spawn binding)
  - `.grok/skills/{plan-review-loop,targeted-unit-test-loop,regression-test-loop,post-change-accuracy-protocol,parallel-fullstack-feature}/SKILL.md`
  - `.grok/workflows/post-change-testing-protocol.md`
  - `.grok/docs/{test-accuracy-standards,coverage-policy,privacy-safety}.md`
  - `docs/waivers/README.md`
  - `fixtures/agentic-template-acceptance/{README,bad-plan,seeded-bug-notes}.md`
  - Artifacts: `docs/plans/bootstrap-v8-inspect.json`, `acceptance-bad-plan.md`, `acceptance-bad-plan.review.md`, `bootstrap-v13-targeted-dry-run.md`, this handoff
- **Waivers present:** none (NONE is correct; no TODO+waiver needed)
- **Phase 2.9 content fidelity:** PASS
- **Next steps:**
  1. Optional: Fixture B (seeded bug) / Fixture C (coverage hole) on a throwaway branch.
  2. Prefer bundled `/review`, `/check-work`, `/implement` for future features.
  3. Continue agent work via plans under `docs/plans/` (example: tags feature already exercised).
- **Reminders:**
  - Prepend persona instruction files on every spawn; tags are UI-only
  - Always set `capability_mode` on spawn (QA: execute/all; plan review: read-only)
  - Roles are optional catalog metadata — not spawn binding
  - Lead-only spawn (depth 1)
  - COMPLETE does **not** imply accuracy_gates OPERATIONAL
  - Prompt pressure is not a hard OS gate

## Protocol map (V9)

Post-change order:

1. Targeted unit test loop (`/targeted-unit-test-loop`)
2. Code review: `/review` unless implement/review de-dupe says skip
3. Regression (`/regression-test-loop`)
4. `/check-work` → VERDICT: PASS (session adequacy only)
5. Lead merge decision + `docs/waivers/`

**De-dupe rule:** After clean `/implement` (zero open bugs, tree unchanged / tree match): skip `/review` and record reason. Else run `/review`. Gate-mapped gaps (missing tests / correctness / security / data loss) block skip.

---

## Post-bootstrap: TaskBoard test application + agent exercise

To prove the scaffold is useful beyond ceremony, a **TaskBoard** sample product was added and agents were run against it.

| Item | Detail |
|------|--------|
| Product | `src/taskboard/` — in-memory task board (Python 3.11+) |
| Tooling | `pyproject.toml` with pytest, pytest-cov, ruff |
| Feature plan | `docs/plans/taskboard-tags-feature.md` |
| Agent implement | `[gf-backend]` spawned with prepended instructions → tags feature |
| Agent QA | `[gf-qa]` targeted loop → **GO** (`docs/plans/taskboard-tags-qa-report.md`) |
| Evidence | 32 tests passed; package coverage ~97%; ruff clean |
| Impl summary | `docs/plans/taskboard-tags-impl-summary.md` |

**accuracy_gates: OPERATIONAL** because Unit + Regression are REAL, Coverage is REAL, and a successful targeted+regression run completed (QA GO).

### Fixture B/C readiness (V12)

| Criterion | Status |
|-----------|--------|
| Unit + Regression REAL | yes |
| Product source tree | yes (`src/taskboard/`) |
| Coverage command REAL | yes |
| Fixture B/C executed | not required for bootstrap; ready to run per `fixtures/agentic-template-acceptance/README.md` |
