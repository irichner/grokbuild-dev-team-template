# GrokForge project template (v1.4)

Grok-native paths only. Optimized for **accuracy + coverage**.

## What loads automatically

| Path | Loaded by Grok? |
|------|-----------------|
| Root `AGENTS.md` | Yes (project rules) |
| `.grok/rules/*.md` | Yes |
| `.grok/skills/*/SKILL.md` | Yes (skills / slash commands) |
| `.grok/personas/*.toml` | Yes (persona **catalog only**; spawn needs instruction **prepend**) |
| `.grok/roles/*.toml` | Catalog defaults when resolution applies — **skills must still set capability_mode and prepend instructions** |
| `.grok/docs/*`, `.grok/workflows/*` | **No** — reference only |

## Prefer bundled skills

- `/implement` — implement → review → fix loop  
- `/review` — diff review  
- `/check-work` — session verification (includes build/test when relevant)  
- `/code-review` — strict maintainability (optional)  
- `/create-skill` — capture new skills  
- `/plan`, `/view-plan` — Plan Mode  

Project skills add plan-review fallback, targeted/regression testing, coverage gates, and the post-change protocol.

## Git required for full protocol

`/review` local mode, worktrees, and git-diff test selection need a git repo. Without git: config may load from CWD `.grok/`, but accuracy protocol is degraded.

## Deprecated

`.grokbuild/` (v1.1) — not discovered.
