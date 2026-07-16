# Token & model usage ledger

**Template version:** 1.7.1  
**Last updated:** 2026-07-16  
**Policy:** update **VERSION** + this ledger on **every git commit** (`scripts/prepare_commit_metrics.py` / pre-commit hook).  
**Source of figures:** session stats (`/context`, `/session-info`, host UI) — never invent.

## Running totals

| Metric | Value |
|--------|------:|
| Total input tokens (measured) | 0 |
| Total output tokens (measured) | 0 |
| Total tokens (measured) | 0 |
| Measured entries | 0 |
| Unmeasured commit stamps | 1 |
| All ledger entries | 1 |

## By model (measured only)

| Model | Input | Output | Total | Entries |
|-------|------:|-------:|------:|--------:|
| *(none yet)* | 0 | 0 | 0 | 0 |

## Entries

| Date (UTC) | Session / label | Model | Input | Output | Total | Notes |
|------------|-----------------|-------|------:|-------:|------:|-------|
| 2026-07-16 | commit-2026-07-16 | unmeasured | 0 | 0 | 0 | commit metrics v1.7.1: auto unmeasured (no metrics in env/pending file) [unmeasured] |

<!-- LEDGER_END -->

## Notes

- **Every commit** must refresh VERSION (patch bump) and append a ledger row via `prepare_commit_metrics.py` (enforced by git pre-commit when hooks installed).
- Model `unmeasured` / notes containing `[unmeasured]` do **not** add to token totals.
- Subagent usage: when the host only reports parent-session totals, note that limitation.
- Entries are append-only; corrections use a follow-up entry (negative only if host confirms).
- Keep this file in version control so the team shares one running total.
