---
name: epistemic-auditor
description: Run a full AEE epistemic audit pipeline and propose recovery actions for all failure modes.
domain: epistemic
tags: [aee, epistemic, belief-artifacts, stress-test, certainty]
---

# Epistemic Auditor

Run a complete Applied Epistemic Engineering audit. Use this skill when you need to
deeply assess the epistemic quality of the project's requirements and beliefs.

## When to Activate

- After a batch of new requirements are added
- Before a milestone or release
- When the audit reports logic knots or equilibrium failures
- When a P1 requirement has low confidence
- When asked to "run epistemic audit" or "check belief quality"

## Protocol

### Step 1: Load Current State
Use `read_file` to load:
- `docs/REQUIREMENTS.md` (last 300 lines)
- `LEDGER.md` (last 50 lines)

### Step 2: Run Stress-Test
Call `stress_test` to apply 8 adversarial challenge functions:
1. Vagueness — imprecise language
2. Missing Test — no falsification mechanism
3. Missing Boundary — no epistemic boundary
4. Compound Claim — multiple primitives masquerading as one
5. No Propositions — empty requirement
6. P1 Confidence — P1 belief below MEDIUM confidence
7. Circular Links — dangling inferential links
8. Logic Knots — contradictory MUST/MUST NOT claims

### Step 3: Run Full Epistemic Audit
Call `epistemic_audit` for:
- Failure-Mode Graph construction
- Equilibrium check S(G)
- Certainty scoring (C = base × coverage × freshness)
- Weakest-link propagation through dependency chains

### Step 4: Assess Results
Report:
- Equilibrium: YES/NO
- Critical failures: count and IDs
- Logic knots: count and pairs
- Overall certainty: score vs threshold
- Artifacts below threshold: list

### Step 5: Propose Recovery
Call `req_gaps` to find uncovered requirements.
Generate recovery proposals for the top 5 critical/high failures.
Each proposal must be BOUNDED and require human approval.

### Step 6: Seal the Audit
If equilibrium is reached, call `trace_seal` with:
- type: "audit-gate"
- description: "Epistemic audit passed — equilibrium reached, certainty ≥ 0.7"

If not, seal with:
- type: "epistemic"
- description: "Epistemic audit incomplete — [N] critical failures, [N] logic knots"

### Step 7: Record in Ledger
Add a ledger entry with:
- Epistemic status: [high/medium/low/unknown]
- Belief artifacts touched: [list of IDs examined]
- Results and next steps

## Output Format

```
EPISTEMIC AUDIT REPORT
======================
Equilibrium:     [YES/NO]
Failure modes:   N (critical: N)
Logic knots:     N
Overall certainty: 0.XX (threshold: 0.70)
Below threshold: N artifacts

[If failures exist:]
Critical issues:
  1. [ID]: [challenge] — [recovery hint]
  ...

[Recovery proposals:]
  1. [STRATEGY] [ID]: [description]
  ...

[Seal status: sealed/pending]
```
