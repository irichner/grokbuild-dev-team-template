# Test Accuracy Standards

## Good
- Fails when the bug is reintroduced.
- Edge/negative cases for non-trivial branches.
- Contract checks at boundaries.
- Mock I/O boundaries, not SUT internals.
- Deterministic (seed time/network); public interface over private guts.

## Blockers (NO-GO)
- Only mock call-order assertions on the SUT.
- Meaningless snapshot updates.
- Happy-path-only for error/auth code.
- Flaky time/network without control.

High coverage with inaccurate tests is still failure.
