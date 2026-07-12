# GrokForge Agentic Dev Team Template

Bootstrap config for a Grok-native agentic software team (accuracy, tests, coverage), plus a **TaskBoard** sample app used to exercise the team.

## What's in this repo

| Path | Purpose |
|------|---------|
| `AGENTS.md` | Lead rules, gates, Project Test Commands |
| `.grok/` | Personas, skills, auto-loaded rules, reference docs |
| `docs/plans/` | Plans + bootstrap verification artifacts |
| `docs/waivers/` | Durable gate waivers |
| `fixtures/agentic-template-acceptance/` | Acceptance fixtures A/B/C |
| `src/taskboard/` | **Test application** for agents to extend |
| `tests/` | Pytest suite |

## TaskBoard (test application)

Minimal in-memory task board library:

```bash
# install dev deps
python -m pip install -e ".[dev]"

# unit tests
python -m pytest tests/ -q

# coverage
python -m pytest tests/ --cov=taskboard --cov-report=term-missing

# lint
python -m ruff check src tests
```

### Feature for agents to build

See `docs/plans/taskboard-tags-feature.md` — add **tags** to tasks with normalization, filtering, and tests.

Suggested agent pipeline:

1. `/plan-review-loop` or `/cold-review` on the tags plan  
2. `/implement` (or spawn `gf-backend` with prepended instructions)  
3. `/post-change-accuracy-protocol`  

## Bootstrap status

See `docs/plans/bootstrap-handoff.md`.
