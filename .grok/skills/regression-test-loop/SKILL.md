---
name: regression-test-loop
description: >
  Phased regression Quick (default) or Extended with triage.
  Use before merge or /regression-test-loop.
disable-model-invocation: true
---

# Skill: Regression Test Loop

## Spawn
Lead-orchestrated; capability_mode execute/all; prepend gf-qa instructions; `[gf-qa] regression`.

## Quick vs Extended
**Extended required when:** auth, payments, migrations, concurrency, shared libs, public API contracts, unclear prior fix, or user asks.

## Steps
1. Choose phase; run AGENTS.md commands (fail if NONE/TODO without waiver).
2. Capture exit codes; triage failures (product bug vs flake vs env).
3. Flakes: re-run failed subset up to 2 times; if still flaky, quarantine in report with command + reason; do not silently ignore.
4. Re-run full chosen phase after fixes.
5. QA Test Report (`regression-quick` | `regression-extended`).

## Exit
Phase exit 0, or durable waiver for residual failures with references.
