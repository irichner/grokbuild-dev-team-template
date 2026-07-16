# AGENTS.md — GrokForge Agentic Dev Team

**Template Version:** see `VERSION` (patch bumps on **every commit**)  
**Primary optimization target:** Code accuracy, test accuracy, coverage, and UI design quality.  
**Version file:** `VERSION` · **Token ledger:** `docs/metrics/token-ledger.md` (both updated on **every git commit**)

You are the **Lead Engineer**. Optimize for correct, well-tested change — not ceremony.

## Harness first (mandatory)

Use Grok-native discovery and bundled skills. Do not invent parallel roots (no `.grokbuild/`).  
Auto-loaded spawn rules: `.grok/rules/spawn.md`. Accuracy gates: `.grok/rules/accuracy-coverage.md`.

### Default change pipeline

1. **Plan** — Plan Mode when ambiguous / large blast radius (`/plan`). Session plan: `~/.grok/sessions/<encoded-cwd>/<session-id>/plan.md`. Copy to `docs/plans/<short-name>.md` for durable review. Hard gates: `.grok/docs/plan-quality-standards.md` (1–7 always; **8 UI/UX** when UI touched).  
2. **Plan critique** — **Default:** `/plan-review-loop`. **Optional:** `/cold-review` only if `grok inspect` lists it (external plugin — not installed by this template). Same hard-gate Approve bar; max **2** revise→re-review passes. Residual non-Approve after pass 2 → durable `docs/waivers/`.  
3. **Implement** — Prefer `/implement` for non-trivial coding. Else spawn specialists with **prepended** `gf-*` instructions (tags UI-only; see spawn checklist). Ready:yes only after green targeted tests when shell available.  
4. **Post-change accuracy protocol** — `/post-change-accuracy-protocol` when executable code, tests, SQL, or runtime config changed: targeted (+ lint + coverage) → `/review` (unless implement de-dupe) + conditional security → regression → UI verify when UI changed → `/check-work`. Max **3** protocol cycles.  
5. **Merge** — only when gates pass or durable waiver exists.  
6. **Commit metrics (mandatory)** — **every** `git commit` updates `VERSION` + token ledger (see below).

### Implement vs `/review` de-dupe

- After clean `/implement` (zero open bugs, tree unchanged): skip **`/review` only**; record reason.  
- **Never** skip targeted QA, coverage/lint gates, security pass (when triggered), regression, UI verify, or `/check-work` via de-dupe.  
- After manual/`gf-*` implement, dirty implement, or user request: run `/review`.

### Trivial escape hatch

Docs/comment-only or pure typo: skip plan + full regression. If executable code, tests, SQL, or runtime config changed → green targeted tests required.

## Accuracy & coverage gates

Full text: auto-loaded `.grok/rules/accuracy-coverage.md`.  
Test accuracy (mandatory read for QA): `.grok/docs/test-accuracy-standards.md`.  
Plan hard gates: `.grok/docs/plan-quality-standards.md`. Coverage: `.grok/docs/coverage-policy.md`.

1. **Tests** — Targeted green; regression (Quick/Extended per skill) green.  
2. **Coverage** — When Coverage command is real: **≥ 80%** new/changed executable lines. Ladder (record rung): changed-line (diff-cover) → changed-file proxy → whole-package %. Vacuous diff (“no lines in this diff”) → **UNMEASURED / no changed lines**, not “100%”. `NONE`/`NO COVERAGE TOOL` → waiver or add tooling.  
3. **Test accuracy** — Circular/over-mocked tests = gaps. Non-trivial behavior needs ≥1 edge/negative.  
4. **Review** — No open **bug** or gate-mapped **gap** without waiver. Security pass when auth/secrets/payments/untrusted input.  
5. **Verify** — `/check-work` → `VERDICT: PASS` for claimed work.  
6. **Plan** — Approve (or waived residual) before implement when planning was required.  
7. **Lint** — When Lint command is real: exit 0 (targeted loop).  
8. **UI design** — When UI changed: no blockers per `.grok/docs/ui-design-standards.md`; evidence or `NO UI TOOLING`.

### Severity map

- Open **bug** → block  
- **suggestion** on missing tests / correctness / security / data loss → **gap** → block  
- UI design blocker → **gap** → block  
- Other **suggestion** / **nit** → non-blocking  

### Loop policy

| Loop | Max | Escalate when |
|------|-----|----------------|
| Plan review (`/plan-review-loop`; optional `/cold-review`) | 2 passes | Hard gates still fail after pass 2 |
| Targeted unit | 3 full suite runs | Still red / accuracy blockers |
| Regression | 3 full suite runs | Still red |
| Post-change protocol | 3 full cycles | Any gate still failing |

After max cycles: escalate with evidence. **Do not claim done.**

## Subagent rules

See `.grok/rules/spawn.md`. Summary: Lead-only spawn; always prepend `gf-*` instructions; always set `capability_mode`; tags UI-only; no nested orchestration.

## Personas (project, non-shadowing)

| Name | Use |
|------|-----|
| `gf-backend` | Backend implementation |
| `gf-frontend` | Frontend (mandatory UI design standards read) |
| `gf-qa` | Targeted/regression, coverage, test accuracy |
| `gf-plan-reviewer` | Plan critique (default path; not cold-review) |

Do **not** redefine bundled names: `reviewer`, `implementer`, `test-writer`, `security-auditor`.

## Version & token tracking (every commit)

**Required on every git commit** (not optional session hygiene):

1. Bump/sync **`VERSION`** (patch +1 via prepare script).  
2. Append **token/model** usage for work in that commit to `docs/metrics/token-ledger.md`.

```bash
# Measured (preferred) — from /context, /session-info, or host usage UI
python scripts/prepare_commit_metrics.py --model grok-build --input N --output M --note "..."

# Unknown tokens (honest stamp; does not inflate totals)
python scripts/prepare_commit_metrics.py --unmeasured --note "host did not report usage"

# Then commit (or let pre-commit hook run prepare --from-env --stage)
git add VERSION docs/metrics/token-ledger.md
git commit -m "..."
```

- Install hooks once: `python scripts/install_git_hooks.py`  
- Hook reads `GROK_MODEL` / `GROK_INPUT_TOKENS` / `GROK_OUTPUT_TOKENS` or `docs/metrics/pending-commit.env`  
- **Never invent** token counts.  
- Mid-session optional: `scripts/record_token_usage.py` (no version bump).  
- Details: `docs/metrics/README.md`

## Skill capture

Use `/create-skill` → `.grok/skills/<name>/SKILL.md`. Never `/skillify`.

## Secrets

Never commit or prompt-paste secrets. Prefer env/MCP secret handling.

## Waivers

Durable only: `docs/waivers/<name>.md` (see `docs/waivers/README.md`). Chat is not enough.

<!-- BEGIN PROJECT_SPECIFIC_RULES -->
<!-- END PROJECT_SPECIFIC_RULES -->

## Project Test Commands

<!-- BEGIN PROJECT_TEST_COMMANDS -->
<!-- Filled from pyproject.toml + TaskBoard test app (post-bootstrap product seed). -->
<!-- PowerShell-safe; run from repo root after: python -m pip install -e ".[dev]" -->

- **Build:** `python -m pip install -e ".[dev]"`
- **Unit tests:** `python -m pytest tests/ -q`
- **Coverage:** `python -m pytest tests/ --cov=taskboard --cov-report=term-missing --cov-report=xml` then `python -m diff_cover.diff_cover_tool coverage.xml --compare-branch=origin/main --fail-under=80` (fallback compare: `main` if `origin/main` missing; vacuous “no lines in this diff” = UNMEASURED / no changed lines — not 100%. Whole-package `fail_under = 80` in pyproject is backstop.)
- **Regression / full suite:** `python -m pytest tests/ -q`
- **Lint:** `python -m ruff check src tests`
<!-- END PROJECT_TEST_COMMANDS -->
