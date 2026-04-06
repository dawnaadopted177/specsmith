---
name: verifier
description: Run the full verification loop — governance audit, validate, doctor — and report pass/fail per gate.
domain: verification
tags: [audit, validate, governance, ci]
---

# Verifier

Run the complete specsmith verification loop before any commit or PR.

## When to Activate

- Before creating a commit
- Before creating a PR
- After completing a feature
- When asked to "verify", "check", or "run all checks"

## Verification Gates

### Gate 1: Governance Audit
Call `audit` — checks file existence, REQ↔TEST coverage, ledger health.
If fails: call `audit` with fix=true to auto-repair.

### Gate 2: Consistency Validation
Call `validate` — checks governance consistency, H11 loop detection, AGENTS.md refs.

### Gate 3: Tool Check
Call `doctor` — verifies lint/typecheck/test tools are installed.

### Gate 4: Coverage Check
Call `req_gaps` — lists requirements without test coverage.

### Gate 5: Epistemic Health (optional, run if epistemic layer is active)
Call `epistemic_audit` — checks belief artifact certainty.

## Output Format

```
VERIFICATION REPORT
===================
Gate 1 — Audit:       [PASS/FAIL]
Gate 2 — Validate:    [PASS/FAIL]
Gate 3 — Doctor:      [PASS/FAIL]
Gate 4 — Coverage:    [PASS/FAIL] (N uncovered)
Gate 5 — Epistemic:   [PASS/FAIL/SKIPPED]

Overall: [READY/NOT READY] for commit/PR
```

If all gates pass and work is ready: suggest `commit` command.
