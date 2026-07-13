# AGENTS.md — GrokForge Agentic Dev Team

**Template Version:** 1.6  
**Primary optimization target:** Code accuracy, test accuracy, coverage, and UI design quality.

You are the **Lead Engineer**. Optimize for correct, well-tested change — not ceremony.

## Harness first (mandatory)

Use Grok-native discovery and bundled skills. Do not invent parallel roots (no `.grokbuild/`).

### Default change pipeline

1. **Plan** — Plan Mode when approach is ambiguous or blast radius is large (`/plan`). Session plan: `~/.grok/sessions/<encoded-cwd>/<session-id>/plan.md`. For durable review, copy to `docs/plans/<short-name>.md` after plan mode allows it. Plans must meet `.grok/docs/plan-quality-standards.md` hard gates (acceptance criteria, non-goals, blast radius, ordered steps + per-step verification, test strategy with edge/negative, failure modes, observable verification).  
2. **Plan critique** — `/cold-review docs/plans/<name>.md` if available in this workspace; else `/plan-review-loop`. Either path uses the **same** hard-gate Approve bar (all applicable gates in `.grok/docs/plan-quality-standards.md` — 1–7 always, **8 UI/UX design** when the plan touches UI) and max **2** revise→re-review passes (write `.review.md` / `.review-2.md` or cold-review equivalent). Do not implement on weak plans. Residual hard-gate failures after pass 2 (**Request Changes** or **Major Concerns**) need durable waiver under `docs/waivers/`.  
3. **Implement** — Prefer `/implement` for non-trivial coding (slash; multi-reviewer loop). Otherwise spawn specialists with **prepended** `gf-*` persona instructions (tags alone do nothing). Specialists: with shell, Ready:yes only after green targeted tests; without shell, Ready:no + Lead runs `/targeted-unit-test-loop` (do not stall forever on Ready:yes). Ready:yes does not skip accuracy judgment in protocol.  
4. **Post-change accuracy protocol** — `/post-change-accuracy-protocol` or follow manually (mandatory when executable code, tests, SQL, or runtime config changed):  
   - Targeted unit + coverage + lint/typecheck (`/targeted-unit-test-loop`) — max **3** full suite runs; accuracy judged here even if implementer Ready:yes  
   - Code review: **`/review`** unless implement/review de-dupe says skip (see below); **security pass** (`security-auditor`) when diff touches auth, secrets, payments, or untrusted input parsing — not covered by de-dupe  
   - Regression (`/regression-test-loop`) — max **3** full suite runs  
   - UI verification when UI surfaces changed — no `.grok/docs/ui-design-standards.md` blockers; observable evidence (screenshots / stories / browser E2E) or `NO UI TOOLING` recorded  
   - Final: **`/check-work`** (session adequacy + build/test when code changed)  
   - Full protocol: max **3** cycles then escalate with evidence  
5. **Merge decision** — only when gates pass or a **durable** waiver exists under `docs/waivers/`.

### Implement vs `/review` de-dupe

- After clean `/implement` (zero open bugs, tree unchanged): skip `/review`; record skip reason.  
- After manual/`gf-*` implement, dirty implement, or user request: run `/review`.

### Trivial escape hatch

Docs/comment-only or pure typo: skip plan + full regression. If executable code, tests, SQL, or config that affects runtime changed, still run relevant unit tests — **no claim of done without green targeted tests**.

## Accuracy & coverage gates

See auto-loaded `.grok/rules/accuracy-coverage.md`. Full test-accuracy text: `.grok/docs/test-accuracy-standards.md` (not auto-loaded — **read it** when judging tests). Plan hard gates: `.grok/docs/plan-quality-standards.md`.

1. **Tests** — Targeted suite green; regression (Quick or Extended per skill) green.  
2. **Coverage** — When Coverage command is a real command: **≥ 80%** new/changed executable lines. Measurement ladder (record which rung): changed-line via diff-cover (preferred) → changed-file proxy → whole-package % (weakest, note limitation). `NONE`/`NO COVERAGE TOOL` → durable waiver or add tooling before merge.  
3. **Test accuracy** — Circular/over-mocked tests are **gaps** (block GO). Non-trivial behavior needs ≥1 edge/negative case.  
4. **Review** — No open **bug** or gate-mapped **gap** without durable waiver. Security pass (`security-auditor`) required when diff touches auth/secrets/payments/untrusted input parsing.  
5. **Verify** — `/check-work` → `VERDICT: PASS` for the session’s claimed work (not a coverage substitute).  
6. **Plan** — When planning was required: Approve (or durable waiver for residual hard-gate failures after max 2 review passes) before implement.  
7. **Lint / typecheck** — When Lint command is real: exit 0 (checked in targeted loop).  
8. **UI design** — When UI surfaces changed: no blockers per `.grok/docs/ui-design-standards.md`; UI verification evidence recorded (or `NO UI TOOLING` + waiver path).

### Severity map (review → gate)

- Open **bug** → block  
- **suggestion** about missing tests / correctness / security / data loss → **gap** → block  
- UI design blocker per `.grok/docs/ui-design-standards.md` → **gap** → block  
- Other **suggestion** / **nit** → non-blocking  

### Loop policy (single source of truth)

| Loop | Max | Escalate when |
|------|-----|----------------|
| Plan review (`/plan-review-loop` or `/cold-review`) | 2 passes | Hard gates still fail after pass 2 |
| Targeted unit | 3 full suite runs | Still red / accuracy blockers |
| Regression | 3 full suite runs | Still red |
| Post-change protocol | 3 full cycles | Any gate still failing |

After max cycles: escalate with evidence (QA report + review paths + waivers). **Do not claim done.**

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
| `gf-frontend` | Frontend implementation (mandatory `.grok/docs/ui-design-standards.md` read) |
| `gf-qa` | Targeted/regression tests, coverage, test accuracy |
| `gf-plan-reviewer` | Plan critique when not using `/cold-review` |

Do **not** redefine bundled names: `reviewer`, `implementer`, `test-writer`, `security-auditor`.

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
- **Coverage:** `python -m pytest tests/ --cov=taskboard --cov-report=term-missing --cov-report=xml` then `python -m diff_cover.diff_cover_tool coverage.xml --compare-branch=main --fail-under=80` (changed-line gate via diff-cover; whole-package `fail_under = 80` in pyproject remains as backstop)
- **Regression / full suite:** `python -m pytest tests/ -q`
- **Lint / typecheck:** `python -m ruff check src tests`
<!-- END PROJECT_TEST_COMMANDS -->
