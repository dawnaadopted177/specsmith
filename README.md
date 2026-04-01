# specsmith

Forge governed project scaffolds from the Agentic AI Development Workflow Specification.

---

## What this is

`specsmith` is a CLI tool and specification system for projects that use AI agents as development assistants. It provides:

- **CLI tool** (`specsmith init`) — generate full governed project scaffolds interactively or from YAML config
- **Agentic Workflow Spec** — closed-loop workflow (propose → check → execute → verify → record)
- **Modular governance** — AGENTS.md hub + delegated docs (rules, roles, verification, drift-metrics, etc.)
- **8 project types** — backend+frontend, CLI, library, embedded, FPGA/RTL, Yocto/BSP, PCB/hardware
- **Health commands** — audit, validate, compress, upgrade for ongoing governance maintenance
- **Agent integrations** — Warp/Oz, Claude Code, GitHub Copilot, Cursor, and more
- **Execution safety** — timeout shims, non-interactive mandates, hung-process protection

## Core principle

> Intelligence proposes. Constraints decide. The ledger remembers.

## Install

```bash
pip install specsmith
```

Or from source:

```bash
git clone https://github.com/BitConcepts/specsmith.git
cd specsmith
pip install -e ".[dev]"
```

## Quick start

```bash
# Interactive scaffold
specsmith init

# From config file
specsmith init --config scaffold.yml

# Health checks
specsmith audit
specsmith validate

# Ledger maintenance
specsmith compress

# Upgrade governance to newer spec version
specsmith upgrade --spec-version 0.2.0
```

## Commands

| Command | Description |
|---------|-------------|
| `specsmith init` | Scaffold a new governed project |
| `specsmith audit` | Run drift and health checks (Sections 23+26) |
| `specsmith validate` | Check governance file consistency (req ↔ test ↔ arch) |
| `specsmith compress` | Archive old ledger entries |
| `specsmith upgrade` | Update governance files to newer spec version |

## Project types

1. Python backend + web frontend
2. Python backend + web frontend + tray app
3. CLI tool (Python)
4. Library / SDK (Python)
5. Embedded / hardware
6. FPGA / RTL
7. Yocto / embedded Linux BSP
8. PCB / hardware design

## Specification

See `AGENT-WORKFLOW-SPEC.md` for the complete workflow specification.

## License

MIT — see [LICENSE](LICENSE).
