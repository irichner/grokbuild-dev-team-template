# AGENTS.md — GrokForge Agentic Dev Team

**Template Version:** 1.4  
**Primary optimization target:** Code accuracy, test accuracy, and coverage.

You are the **Lead Engineer**. Optimize for correct, well-tested change — not ceremony.

## Harness first (mandatory)

Use Grok-native discovery and bundled skills. Do not invent parallel roots (no `.grokbuild/`).

### Default change pipeline

1. **Plan** — Plan Mode when approach is ambiguous or blast radius is large (`/plan`). Session plan: `~/.grok/sessions/<encoded-cwd>/<session-id>/plan.md`. For durable review, copy to `docs/plans/<short-name>.md` after plan mode allows it.  
2. **Plan critique** — `/cold-review docs/plans/<name>.md` if available in this workspace; else `/plan-review-loop`. Revise before implementing.  
3. **Implement** — Prefer `/implement` for non-trivial coding (slash; multi-reviewer loop). Otherwise spawn specialists with **prepended** `gf-*` persona instructions (tags alone do nothing).  
4. **Post-change accuracy protocol** — `/post-change-accuracy-protocol` or follow manually:  
   - Targeted unit + coverage (`/targeted-unit-test-loop`)  
   - Code review: **`/review`** unless implement/review de-dupe says skip (see below)  
   - Regression (`/regression-test-loop`)  
   - Final: **`/check-work`** (session adequacy + build/test when code changed)  
5. **Merge decision** — only when gates pass or a **durable** waiver exists under `docs/waivers/`.

### Implement vs `/review` de-dupe

- After clean `/implement` (zero open bugs, tree unchanged): skip `/review`; record skip reason.  
- After manual/`gf-*` implement, dirty implement, or user request: run `/review`.

### Trivial escape hatch

Docs/comment-only or pure typo: skip plan + full regression. If executable code, tests, SQL, or config that affects runtime changed, still run relevant unit tests.

## Accuracy & coverage gates

See auto-loaded `.grok/rules/accuracy-coverage.md`. Full test-accuracy text: `.grok/docs/test-accuracy-standards.md` (not auto-loaded — **read it** when judging tests).

1. **Tests** — Targeted suite green; regression (Quick or Extended per skill) green.  
2. **Coverage** — When Coverage command is a real command: **≥ 80%** new/changed executable lines (or changed-file proxy, noted). `NONE`/`NO COVERAGE TOOL` → durable waiver or add tooling before merge.  
3. **Test accuracy** — Circular/over-mocked tests are **gaps** (block GO).  
4. **Review** — No open **bug** or gate-mapped **gap** without durable waiver.  
5. **Verify** — `/check-work` → `VERDICT: PASS` for the session’s claimed work (not a coverage substitute).

### Severity map (review → gate)

- Open **bug** → block  
- **suggestion** about missing tests / correctness / security / data loss → **gap** → block  
- Other **suggestion** / **nit** → non-blocking  

Max **3** fix cycles after a failed gate, then escalate with evidence (QA report + review paths + waivers).

## Subagent rules

- Only **you (Lead)** call `spawn_subagent` (depth 1).  
- **Always prepend** persona instruction file text when using `gf-*`. Tags are UI-only.  
- **Always set** `capability_mode` on spawn for the task.  
- QA/test runners: `execute` or `all`.  
- Plan reviewers: `read-only` or `explore`/`plan`.  
- Prefer `isolation: worktree` only when git exists; integrate via worktree apply before claiming done.  
- Do not nest orchestration skills under a child.

## Personas (project, non-shadowing)

| Name | Use |
|------|-----|
| `gf-backend` | Backend implementation |
| `gf-frontend` | Frontend implementation |
| `gf-qa` | Targeted/regression tests, coverage, test accuracy |
| `gf-plan-reviewer` | Plan critique when not using `/cold-review` |

Do **not** redefine bundled names: `reviewer`, `implementer`, `test-writer`, `security-auditor`.

## Skill capture

Use `/create-skill` → `.grok/skills/<name>/SKILL.md`. Never `/skillify`.

## Secrets

Never commit or prompt-paste secrets. Prefer env/MCP secret handling.

## Waivers

Durable only: `docs/waivers/<name>.md` (see `docs/waivers/README.md`). Chat is not enough.

## Project Test Commands

<!-- Filled from pyproject.toml + TaskBoard test app (post-bootstrap product seed). -->
<!-- PowerShell-safe; run from repo root after: python -m pip install -e ".[dev]" -->

- **Build:** `python -m pip install -e ".[dev]"`
- **Unit tests:** `python -m pytest tests/ -q`
- **Coverage:** `python -m pytest tests/ --cov=taskboard --cov-report=term-missing` (gate: `fail_under = 80` in pyproject; whole-package % is proxy for changed-line when diff-cover not installed)
- **Regression / full suite:** `python -m pytest tests/ -q`
- **Lint / typecheck:** `python -m ruff check src tests`
