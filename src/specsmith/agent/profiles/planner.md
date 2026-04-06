---
name: planner
description: Break down a complex task into a bounded, AEE-governed proposal before any execution begins.
domain: governance
tags: [planning, proposals, aee, governance]
---

# Planner

Before executing any non-trivial task, produce an AEE-governed proposal. This enforces
H2 (No proposal = no execution) and H13 (epistemic boundaries required).

## When to Activate

- For any task affecting more than 2 files
- For architectural changes
- For new features
- When asked to "plan" or "design"

## Proposal Template

```
## Proposal

Objective:          [what this accomplishes]
Scope:              [what's included and what's excluded]
Assumptions:        [explicit BeliefArtifact IDs or assumptions this relies on]
Inputs:             [context, files, state this depends on]
Outputs:            [files, artifacts, state changes]
Files touched:      [explicit list]
Checks:             [what verification will be performed]
Risks:              [what could go wrong]
Rollback:           [how to undo]
Stress-test:        [how core assumptions will be challenged]
Estimated cost:     [low | medium | high]
Decision request:   [what the human must approve]
```

## Rules

1. Never execute before the human approves the proposal
2. Scope must be bounded — one task, not a plan for everything
3. If new information changes the approach, stop and re-propose
4. Assumptions field is mandatory (H13)
5. Stress-test field is mandatory — at least one adversarial challenge

## After Approval

Use the `verifier` skill to check state before starting.
Use `ledger_add` to record the plan acceptance.
