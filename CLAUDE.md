# Engineering Operating Manual

> This file loads into every Claude Code session. Keep it lean and high-signal.
> Stable, universal standards live here. On-demand procedures live in `.claude/skills/`.
> Project-specific facts (stack, commands, layout) go in the **Project Facts** section —
> fill that in for your repo.

## How we work: the verification loop

All non-trivial work follows one loop. Do **not** skip straight to editing.

1. **Explore** — Understand before changing. Map the relevant code, contracts, and
   tests first. Read pointed scope inline; delegate to the `explorer` subagent only
   for wide, unfamiliar territory. Never assume an API; open it and read it.
2. **Plan** — State intent, the change surface, the test strategy, and risks *before*
   writing code. **Always** persist required plans as durable Markdown under
   `docs/plans/<name>.md` for review — never chat-only. For anything spanning more
   than ~2 files or introducing a new pattern, use the `planner` subagent or `/plan`:
   it writes the plan to `docs/plans/` with the implementation grouped into **work
   packages** — few, large, coherent batches, each sized for a single implementer
   dispatch (tests and doc updates included). Session-only plans must be copied to
   `docs/plans/` before critique or implement.
3. **Implement** — Smallest change that satisfies the plan, one implementer per
   work package. Do not implement from a chat-only plan. Prefer obvious code over
   clever code. Match existing conventions over personal preference.
4. **Verify** — Run the real checks: typecheck, lint, tests. Green is not optional.
   Reproduce the bug or exercise the feature; don't trust that it "should" work.
5. **Review** — Get a second pair of eyes. The `code-reviewer` and `security-auditor`
   subagents run in their own context and catch what the implementer's context misses.
6. **Commit** — One logical change per commit, Conventional Commits format. See the
   `commit-conventions` skill.

The full version of this loop is the `verification-loop` skill (`/verification-loop`).

## Non-negotiable principles

- **Correctness is proven, not asserted.** "It should work" is a hypothesis. Run it.
- **Read the code before changing it.** Signatures, types, and call sites over memory.
- **Smallest viable diff.** Touch only what the task needs. No drive-by rewrites.
- **Match the codebase.** Mirror its naming, structure, error handling, and test style.
- **Tests are part of the change.** New behavior ships with tests. Bug fixes ship with
  a regression test that fails before the fix.
- **No secrets in code.** No credentials, tokens, or keys in source, logs, or commits.
- **Deterministic logic stays deterministic.** Don't hide core logic behind nondeterminism.
- **Leave it cleaner.** Boy-scout the immediate area, but keep cleanups out of feature commits.
- **Agents are budget, not free labor.** A full task uses at most ~5 subagents:
  planner, one implementer per work package, one reviewer. Fold tests and docs into
  the implementer's package; do quick reads and small edits inline; review the whole
  diff once, not per package.

## Definition of done

A task is done only when **all** of these hold:

- [ ] The change satisfies the agreed plan (or the deviation was surfaced and accepted).
- [ ] Typecheck passes. Lint passes. The full relevant test suite passes.
- [ ] New/changed behavior has tests. Bug fixes have a regression test.
- [ ] No debug prints, commented-out code, or stray scaffolding left behind.
- [ ] Public surfaces and non-obvious decisions are documented.
- [ ] The diff has been reviewed (self + `code-reviewer` for anything non-trivial).

If a check can't pass, **stop and report** — do not paper over it or weaken the test.

## Tooling map (what to reach for)

- **Subagents** (`.claude/agents/`): role specialists with scoped tools and their own
  context. `explorer`, `planner`, `implementer`, `test-engineer`, `code-reviewer`,
  `security-auditor`, `debugger`, `refactorer`, `docs-writer`.
- **Skills** (`.claude/skills/`): reusable procedures Claude loads on demand —
  `verification-loop`, `tdd`, `debug-protocol`, `adr`, plus always-on conventions
  (`code-review-rubric`, `commit-conventions`).
- **Commands** (`.claude/commands/`): operator-triggered workflows — `/ship`, `/plan`,
  `/review`, `/test`, `/fix`, `/commit`, `/pr`, `/checkpoint`.
- **Hooks** (`.claude/settings.json`): deterministic guardrails that fire regardless of
  what the model decides — protected-path blocking (secrets, `.git/`, the hooks
  themselves), auto-format on edit, and a completion gate that refuses to stop on red
  tests. An opt-in dangerous-command guard ships in `.claude/hooks/guard-bash.sh`.

When uncertain about a Claude Code capability or its current syntax, check the docs
(`https://code.claude.com/docs`) rather than guessing.

## Communication style for this repo

- Lead with the answer or the result, then the supporting detail.
- When you change code, say what changed and why in one or two sentences.
- Surface risks, assumptions, and anything you couldn't verify — explicitly.
- If a request is ambiguous in a way that changes the implementation, ask once, then proceed.

---

## Project Facts

> **Grok primary:** When Lead is Grok, authoritative Project Test Commands live in root **`AGENTS.md`**.  
> This block mirrors those commands for Claude Code hooks / dual-stack sessions.

- **Stack:** Python 3.11+, pytest, ruff, pytest-cov, diff-cover; sample app `taskboard`
- **Package manager:** pip / editable install via `pyproject.toml`
- **Install:** `python -m pip install -e ".[dev]"`
- **Run (dev):** `python -m taskboard` (ephemeral demo CLI) or import `taskboard` library
- **Typecheck:** none configured (no mypy gate)
- **Lint:** `python -m ruff check src tests scripts`
- **Test (all):** `python -m pytest tests/ -q`
- **Test (single file/pattern):** `python -m pytest tests/<file> -q` or `-k <pattern>`
- **Build:** `python -m pip install -e ".[dev]"`
- **Coverage:** `python -m pytest tests/ --cov=taskboard --cov-report=term-missing --cov-report=xml` then `python -m diff_cover.diff_cover_tool coverage.xml --compare-branch=origin/main --fail-under=80`
- **Source layout:** `src/taskboard/` product; `tests/`; `.grok/` harness; `scripts/` installer/metrics
- **Architectural notes:** GrokForge harness is primary (`AGENTS.md` + `.grok/`). Claude `.claude/` is optional sibling. In-memory TaskBoard; tags normalize/dedupe; priority clamp 0–10.

> Keep `.claude/hooks/verify-on-stop.sh` and `format.sh` aligned with Lint/Test above when using Claude Stop hooks.
