# agentic-scaffold

Specification-first, constraint-governed workflow for AI-assisted software development.

---

## What this is

A portable reference specification and scaffolding system for projects that use AI agents as development assistants. It defines:

- a closed-loop workflow (propose → check → execute → verify → record)
- governance file schemas (AGENTS.md, LEDGER.md, REQUIREMENTS.md, TEST_SPEC.md)
- session lifecycle rules (start, resume, save, commit, sync)
- agent role boundaries (proposal generators, not decision-makers)
- context window management strategies
- project type templates (backend+frontend, CLI, library, embedded/hardware)
- requirement and test specification formats
- cross-platform rules and bootstrap contracts

## Core principle

> Intelligence proposes. Constraints decide. The ledger remembers.

## Who this is for

- Developers using AI agents (Claude, GPT, Copilot, etc.) for software development
- Teams that want auditable, specification-first agentic workflows
- Anyone bootstrapping a new project with built-in governance from day one

## Quick start

1. Read `AGENTIC-WORKFLOW-SPEC.md` — the complete workflow specification
2. Choose a project type from Section 17
3. Follow the scaffold bootstrap procedure in Section 18
4. Hand the spec to your AI agent alongside your project goals

## Files

- `AGENTIC-WORKFLOW-SPEC.md` — full workflow specification (start here)
- `LICENSE` — MIT

## License

MIT — see [LICENSE](LICENSE).
