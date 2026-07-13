# Coverage Policy

- Default gate: **≥ 80%** new/changed executable lines when Coverage command is real in AGENTS.md.
- Proxy: changed-file % if line-level unavailable (note limitation in QA report).
- No tool: `NO COVERAGE TOOL` → durable waiver in `docs/waivers/` or add tooling before merge.
- Never invent percentages; use UNMEASURED if the tool ran but delta cannot be computed.
- Recipe hints (adapt to repo):
  - Python: pytest --cov + diff-cover against git diff when available
  - JS/TS: vitest/jest --coverage or nyc; prefer changed files if supported
  - Go: go test -coverprofile + go tool cover
- Waivers: scope, residual risk, follow-up, expiry.
- Not a substitute for test accuracy or `/review`.
- Targeted loop must record coverage gate met / waived / NO TOOL each cycle (see `/targeted-unit-test-loop`).
