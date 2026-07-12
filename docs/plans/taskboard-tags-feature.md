# Feature plan: Task tags

**Status:** Ready for plan critique / implementation  
**Product:** TaskBoard (`src/taskboard/`)  
**Date:** 2026-07-12

## Goal (measurable)

A task can carry zero or more **tags** (normalized lowercase strings). Callers can:

1. Add a task with optional tags.
2. Add / remove tags on an existing task.
3. List tasks filtered by a single tag (must have that tag).
4. Unit tests cover happy path + empty tag rejection + case normalization; coverage on new/changed lines ≥ 80%.

**Done when:** `pytest` green; `pytest --cov=taskboard` meets project fail_under; public API documented in module docstring or README snippet.

## Non-goals

- Persistence / database
- Multi-user auth
- Tag hierarchy or colors
- Full-text search beyond exact tag match

## Assumptions

| Assumption | Falsifier |
|------------|-----------|
| Tags are free-form short strings (no registry) | Product later requires controlled vocabulary |
| Case-insensitive: store lowercase | Callers need original case preserved |
| Empty / whitespace-only tags are invalid | Product wants blank tags |

## Steps / files

1. Extend `Task` in `src/taskboard/models.py` with `tags: set[str]` (or frozenset at rest).
2. Normalize tags via a helper `normalize_tag(s: str) -> str` in `util.py` or `models.py` (strip, lower; reject empty).
3. Update `TaskBoard.add(..., tags: Iterable[str] | None = None)`.
4. Add `TaskBoard.add_tag(task_id, tag)`, `remove_tag(task_id, tag)`, `list(tag=...)` filter (compose with existing status filter).
5. Tests in `tests/test_tags.py` (and extend board tests as needed).
6. Optional: CLI `--tag` on `add` / `list` (nice-to-have; not required for GO).

## Testing Strategy

| Case | Observable |
|------|------------|
| Add with tags `["Bug", "bug", "  api  "]` | Stored as `{"bug", "api"}` (dedupe + normalize) |
| `add_tag` / `remove_tag` | Membership updates; remove missing is no-op or documented |
| Empty tag `""` or `"  "` | `ValueError` |
| `list(tag="bug")` | Only tasks with that tag |
| Combined `list(status=..., tag=...)` | Intersection |
| Regression | Existing board tests still pass |

Commands:

```text
python -m pytest tests/ -q
python -m pytest tests/ --cov=taskboard --cov-report=term-missing
```

Coverage expectation: ≥ 80% on new/changed executable lines (or changed files under `taskboard` per project policy).

## Verification

- [ ] `pytest` exit 0
- [ ] Coverage gate met (or durable waiver)
- [ ] No open review **bug** / gate-mapped **gap**
- [ ] `/check-work` VERDICT: PASS for the session claim

## Failure modes

- Mutating shared tag set across tasks → use per-task copies
- Case drift (`Bug` vs `bug`) → always normalize on write
- Breaking existing `list(status=)` signature → keep `status` kw-only/optional; add `tag` optional
