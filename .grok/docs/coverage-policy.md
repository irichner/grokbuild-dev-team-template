# Coverage Policy

- Default gate: **≥ 80%** new/changed executable lines when Coverage command is real in AGENTS.md.
- Measurement ladder — record which rung was used in the QA report:
  1. **changed-line %** via diff-cover or equivalent (preferred; the template repo installs `diff-cover` in dev deps)
  2. **changed-file %** proxy (files touched must meet threshold or be listed as gaps)
  3. **whole-package %** — weakest; only with an explicit limitation note
- No tool: `NO COVERAGE TOOL` → durable waiver in `docs/waivers/` or add tooling before merge.
- Never invent percentages; use UNMEASURED if the tool ran but delta cannot be computed.
- Recipe hints (adapt to repo):
  - Python: pytest --cov + diff-cover against git diff when available
  - JS/TS: vitest/jest --coverage or nyc; prefer changed files if supported
  - Go: go test -coverprofile + go tool cover
- Waivers: scope, residual risk, follow-up, expiry.
- Not a substitute for test accuracy or `/review`.
- Targeted loop must record coverage gate met / waived / NO TOOL each cycle (see `/targeted-unit-test-loop`).
