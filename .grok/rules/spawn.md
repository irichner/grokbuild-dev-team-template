# Spawn checklist (auto-loaded)

Lead-only `spawn_subagent` (depth 1). Children cannot spawn.

## Skill ownership (mandatory)

All project `gf-*` agents are **tied to one of two skills**. Spawn them **only** while re-enacting that skill’s `SKILL.md`:

| Skill | Agents |
|-------|--------|
| **`/plan`** (`.grok/skills/plan/SKILL.md`) | `gf-plan-reviewer` (+ Lead inline explore/author) |
| **`/implement`** (`.grok/skills/implement/SKILL.md`) | `gf-backend`, `gf-frontend`, `gf-qa`, `gf-reviewer`, `gf-debugger` |

Do **not** free-spawn `gf-*` outside those procedures. Deprecated skill stubs (`plan-review-loop`, `targeted-unit-test-loop`, etc.) are **not** spawn owners — open `/plan` or `/implement` instead.

User-requested emergency override is allowed only with an explicit record of which skill phase is being short-circuited.

## Every spawn

1. **Prepend** full persona instruction file text when using a `gf-*` specialist  
   (e.g. `.grok/personas/instructions/gf-qa.md`). Tags like `[gf-qa]` are **UI labels only**.  
2. **Set `capability_mode` explicitly** on the tool call — do not rely on persona/role TOML defaults.  
   - QA / test runners: `execute` or `all`  
   - Plan reviewers / code reviewers (`gf-plan-reviewer`, `gf-reviewer`): `read-only` (or `explore` / `plan` agent type)  
   - Implementers (`gf-backend`, `gf-frontend`): `all` (or `read-write` if no shell needed)  
   - Debugger (`gf-debugger`): `all` (shell required to reproduce and confirm)  
3. **Description** starts with a bracketed tag for the pager label: `[gf-qa] …`, `[gf-backend] …`, `[gf-reviewer] …`, `[gf-debugger] …`, `[gf-plan-reviewer] …`.  
4. Prefer `isolation: worktree` only when git exists and edits must not collide (`/implement` parallel-fullstack mode); integrate before claiming done.

## Roles / personas

`.grok/roles/*.toml` and persona `default_capability_mode` are **catalog metadata only** — not spawn binding. Skills and this checklist still require explicit `capability_mode` + instruction prepend.

## Do not

- Nest orchestration skills under a child.  
- Assume a persona name is applied without prepending its instruction file.  
- Claim Ready:yes for implementers/debugger without green targeted tests when shell was available.  
- Redefine bundled names (`reviewer`, `implementer`, `test-writer`, `security-auditor`) — use project `gf-*` names instead.  
- Spawn `gf-plan-reviewer` from `/implement`, or implement/QA personas from `/plan`.  
