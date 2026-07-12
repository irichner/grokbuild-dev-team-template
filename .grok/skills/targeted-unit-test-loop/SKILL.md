---
name: targeted-unit-test-loop
description: >
  Fast unit tests on changed code with coverage delta and test-accuracy checks.
  Use after implementation or /targeted-unit-test-loop.
disable-model-invocation: true
---

# Skill: Targeted Unit Test Loop

## Spawn rules
- Orchestrated by **Lead** (not nested under another subagent).
- Spawn with `capability_mode: execute` or `all` (shell required) — set explicitly.
- Prepend full `.grok/personas/instructions/gf-qa.md`; `description`: `[gf-qa] targeted tests`.

## Prerequisites
- Prefer git for changed-file list. If no git: require user-supplied path list or fail with NO-GO (cannot define “changed”).

## Steps
1. Read AGENTS.md Project Test Commands. If Unit is TODO/NONE without waiver → NO-GO.
2. List changed files (`git status` / `git diff --name-only` when git exists).
3. Map to tests (in order): plan Testing Strategy paths → colocated tests → smallest module suite that covers changed packages. Record selection rule used.
4. Run unit command restricted to selected paths when supported; else full unit suite with scope note.
5. Coverage if Coverage command is real; record changed-line % or changed-file proxy; never invent numbers.
6. **Gate:** ≥ 80% when tool exists and measured; else NO COVERAGE TOOL / UNMEASURED.
7. `read_file` `.grok/docs/test-accuracy-standards.md`; accuracy pass.
8. Emit QA Test Report (`Mode: targeted`).

## Exit
Tests exit 0; coverage gate met or durable waiver; no accuracy blockers. Max 3 fix cycles.
