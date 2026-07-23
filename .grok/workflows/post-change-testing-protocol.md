# Post-change testing (narrative)

Executable source of truth: **`.grok/skills/implement/SKILL.md`** (Phase 2 Accuracy protocol).

Deprecated alias path: `.grok/skills/post-change-accuracy-protocol/SKILL.md` (redirect stub only).

1. Targeted unit + coverage + lint (fix→re-test, max 3 cycles) via `gf-qa`  
2. `/review` (or SKIPPED per implement de-dupe — **review only**; never skip QA/security/regression/UI/check-work) + security pass when diff touches auth/secrets/payments/untrusted input; fallback `gf-reviewer` when host missing  
3. Regression (fix→re-test, max 3 cycles) via `gf-qa`  
4. UI verification when UI surfaces changed (design blockers = gaps; observable evidence or `NO UI TOOLING`)  
5. `/check-work`  
6. Lead merge decision + waivers  

Full protocol may repeat up to **3** times on failure, then escalate.

This file is **not** auto-loaded; AGENTS.md and `/implement` are.

Cross-links:

- Plan skill: `.grok/skills/plan/SKILL.md`  
- Plan quality: `.grok/docs/plan-quality-standards.md`  
- Test accuracy: `.grok/docs/test-accuracy-standards.md`  
- UI design: `.grok/docs/ui-design-standards.md`  
- Coverage: `.grok/docs/coverage-policy.md`  
- Auto-loaded gates: `.grok/rules/accuracy-coverage.md`  
