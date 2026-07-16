# Bootstrap handoff

- **Date:** 2026-07-15  
- **Template feature train:** 1.7  
- **VERSION file:** patch-bumps on **every commit** (`prepare_commit_metrics.py` + pre-commit hook)  
- **bootstrap_status:** COMPLETE (historical scaffold + post-seed product)  
- **accuracy_gates:** OPERATIONAL  
- **git_mode:** full  

## Current Project Test Commands (v1.7)

- **Build:** REAL — `python -m pip install -e ".[dev]"`
- **Unit tests:** REAL — `python -m pytest tests/ -q`
- **Coverage:** REAL — pytest `--cov=taskboard` + XML, then  
  `python -m diff_cover.diff_cover_tool coverage.xml --compare-branch=origin/main --fail-under=80`  
  (fallback: `main`; vacuous diff = UNMEASURED / no changed lines)
- **Regression / full suite:** REAL — `python -m pytest tests/ -q`
- **Lint:** REAL — `python -m ruff check src tests`

## Metrics (every commit)

- **Version file:** `VERSION` (e.g. `1.7.0` → `1.7.1` on each commit metrics run)
- **Token ledger:** `docs/metrics/token-ledger.md`
- **Helpers:** `scripts/prepare_commit_metrics.py` (required every commit), `scripts/install_git_hooks.py`, optional mid-session `record_token_usage.py`
- **Never invent** token counts; use `--unmeasured` when host stats unavailable

## Harness surfaces (v1.7)

- `.grok/rules/accuracy-coverage.md`, `.grok/rules/spawn.md` (auto-loaded)
- Personas + instructions: `gf-backend`, `gf-frontend`, `gf-qa`, `gf-plan-reviewer`
- Roles (catalog only, all four): `gf-backend`, `gf-frontend`, `gf-qa`, `gf-plan-reviewer`
- Skills: plan-review-loop (**default** plan critique), targeted/regression loops, post-change protocol, parallel-fullstack, install-agentic-team
- Docs: plan-quality, test-accuracy, coverage-policy (incl. vacuous-diff), ui-design, privacy-safety
- Sample UI for Fixture E: `fixtures/agentic-template-acceptance/sample-ui/`
- CI: `.github/workflows/ci.yml`

## Plan critique

- **Default:** `/plan-review-loop`  
- **Optional:** `/cold-review` only if present in `grok inspect` (external plugin; not installed by this template)

## Historical notes (pre-1.7)

Earlier bootstrap passes (V8 inspect, Fixture A Major Concerns, V13 fail-closed when Unit was NONE, TaskBoard seed + tags exercise) remain under `docs/plans/` as artifacts. Coverage command and handoff version were updated for 1.7; do not use older “1.4 / coverage without diff-cover” snapshots as current truth.

## Reminders

- Prepend persona instruction files on every spawn; tags are UI-only  
- Always set `capability_mode` on spawn (see `.grok/rules/spawn.md`)  
- Roles are optional catalog metadata — not spawn binding  
- Lead-only spawn (depth 1)  
- Implement de-dupe skips **`/review` only**, never targeted QA / security / regression / UI / check-work  
- Record tokens/models in the ledger when known  

## Next steps

1. Optional: Fixture B / C / E on a throwaway branch  
2. Prefer bundled `/review`, `/check-work`, `/implement` for product work  
3. Keep `VERSION` and ledger header aligned on template bumps  
