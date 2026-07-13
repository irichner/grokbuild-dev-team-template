# Post-change testing (narrative)

Executable source of truth: `.grok/skills/post-change-accuracy-protocol/SKILL.md`.

1. Targeted unit + coverage (fix→re-test, max 3 cycles)  
2. `/review` (or SKIPPED per implement de-dupe)  
3. Regression (fix→re-test, max 3 cycles)  
4. `/check-work`  
5. Lead merge decision + waivers  

Full protocol may repeat up to **3** times on failure, then escalate.

This file is **not** auto-loaded; AGENTS.md and the skill are.

Cross-links:

- Plan quality: `.grok/docs/plan-quality-standards.md`  
- Test accuracy: `.grok/docs/test-accuracy-standards.md`  
- Coverage: `.grok/docs/coverage-policy.md`  
- Auto-loaded gates: `.grok/rules/accuracy-coverage.md`  
