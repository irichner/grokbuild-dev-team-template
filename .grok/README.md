# GrokForge project template (v1.6)

Grok-native paths only. Optimized for **accuracy + coverage + UI design quality** with explicit revise/retry loops.

## What loads automatically

| Path | Loaded by Grok? |
|------|-----------------|
| Root `AGENTS.md` | Yes (project rules) |
| `.grok/rules/*.md` | Yes |
| `.grok/skills/*/SKILL.md` | Yes (skills / slash commands) |
| `.grok/personas/*.toml` | Yes (persona **catalog only**; spawn needs instruction **prepend**) |
| `.grok/roles/*.toml` | Catalog defaults when resolution applies — **skills must still set capability_mode and prepend instructions** |
| `.grok/docs/*`, `.grok/workflows/*` | **No** — reference only (plan-quality + test-accuracy + ui-design standards: **mandatory `read_file`** for reviewers/QA/frontend) |

## Prefer bundled skills

- `/implement` — implement → review → fix loop  
- `/review` — diff review  
- `/check-work` — session verification (includes build/test when relevant)  
- `/code-review` — strict maintainability (optional)  
- `/create-skill` — capture new skills  
- `/plan`, `/view-plan` — Plan Mode  

Project skills add plan-review (hard gates + max 2 passes), targeted/regression testing (max 3 fix cycles), coverage + lint gates, UI design gate + verification (`.grok/docs/ui-design-standards.md`), and the post-change protocol (max 3 full cycles).

## Accuracy loops (v1.6)

| Skill / phase | Loop | Cap |
|---------------|------|-----|
| `/plan-review-loop` or `/cold-review` | revise → re-review | 2 passes |
| `/targeted-unit-test-loop` | fix → re-test (1 full suite run/cycle) | 3 full suite runs |
| `/regression-test-loop` | fix → re-test (1 full phase run/cycle) | 3 full phase runs |
| `/post-change-accuracy-protocol` | full protocol retry | 3 cycles |

## Git required for full protocol

`/review` local mode, worktrees, and git-diff test selection need a git repo. Without git: config may load from CWD `.grok/`, but accuracy protocol is degraded.

## Deprecated

`.grokbuild/` (v1.1) — not discovered.
