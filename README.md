# specsmith

[![CI](https://github.com/BitConcepts/specsmith/actions/workflows/ci.yml/badge.svg)](https://github.com/BitConcepts/specsmith/actions/workflows/ci.yml)
[![Docs](https://readthedocs.org/projects/specsmith/badge/?version=latest)](https://specsmith.readthedocs.io/en/latest/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Forge governed project scaffolds from the Agentic AI Development Workflow Specification.

> Intelligence proposes. Constraints decide. The ledger remembers.

---

## What is specsmith?

`specsmith` is a CLI tool that generates full project scaffolds with built-in AI agent governance. It creates the file structure, CI/CD pipelines, governance documents, and agent integration files that AI coding assistants need to work within a structured, auditable workflow.

Every scaffolded project follows the closed-loop workflow: **propose → check → execute → verify → record**.

## Install

```bash
pip install specsmith
```

From source:

```bash
git clone https://github.com/BitConcepts/specsmith.git
cd specsmith
pip install -e ".[dev]"
```

## Quick Start

```bash
# Interactive scaffold
specsmith init

# From config file
specsmith init --config scaffold.yml --no-git

# Guided scaffold with architecture definition
specsmith init --guided

# Import an existing project (generate governance overlay)
specsmith import --project-dir ./my-existing-project
specsmith import --project-dir ./my-existing-project --force

# Health checks on an existing governed project
specsmith audit --project-dir ./my-project
specsmith validate --project-dir ./my-project

# Ledger maintenance
specsmith compress --project-dir ./my-project

# Upgrade governance to newer spec version
specsmith upgrade --spec-version 0.2.0 --project-dir ./my-project

# VCS platform status (CI, alerts, PRs)
specsmith status --project-dir ./my-project

# Compare governance files against templates
specsmith diff --project-dir ./my-project
```

## Commands

| Command | Description |
|---------|-------------|
| `specsmith init` | Scaffold a new governed project (interactive or YAML-driven) |
| `specsmith init --guided` | Scaffold with interactive architecture definition (REQ/TEST stub generation) |
| `specsmith import` | Import an existing project and generate governance overlay |
| `specsmith audit [--fix]` | Drift detection and health checks; `--fix` auto-repairs missing files and oversized ledgers |
| `specsmith validate` | Governance consistency (scaffold.yml, AGENTS.md refs, REQ uniqueness, arch↔req linkage) |
| `specsmith compress` | Archive old ledger entries to `docs/ledger-archive.md` |
| `specsmith upgrade` | Re-render governance files for a new spec version |
| `specsmith status` | Show CI status, dependency alerts, and open PRs from VCS platform CLI |
| `specsmith diff` | Compare governance files against what spec templates would generate |

## Project Types (30)

Software: Python (CLI, library, backend+frontend), Rust (CLI, library), Go, C/C++, .NET, JS/TS (web, fullstack, browser extension), mobile, monorepo, microservices, DevOps/IaC, data/ML.

Hardware: FPGA/RTL, Yocto BSP, PCB, embedded.

Document: technical specs, user manuals, research papers, API specifications, requirements management.

Business/Legal: business plans, patent applications, legal/compliance.

Each type gets tool-aware CI, domain-specific directory structure, governance rules, and template starters. See [full project types reference](https://specsmith.readthedocs.io/en/latest/project-types/).

## Agent Integrations

specsmith generates agent-specific governance files so AI assistants understand your project's rules:

| Agent | Generated File |
|-------|---------------|
| **AGENTS.md** (cross-tool standard) | `AGENTS.md` (always) |
| Warp / Oz | `.warp/skills/SKILL.md` |
| Claude Code | `CLAUDE.md` |
| GitHub Copilot | `.github/copilot-instructions.md` |
| Cursor | `.cursor/rules/governance.mdc` |
| Gemini CLI | `GEMINI.md` |
| Windsurf | `.windsurfrules` |
| Aider | `.aider.conf.yml` |

## VCS Platform Support

CI configs are **tool-aware** — generated from the verification tool registry per project type.

| Platform | CLI | CI Config | Dependency Mgmt | Security |
|----------|-----|-----------|-----------------|----------|
| **GitHub** | `gh` | GitHub Actions | Dependabot (pip/cargo/gomod/npm/nuget) | Tool-specific per type |
| **GitLab** | `glab` | `.gitlab-ci.yml` | Renovate | Tool-specific per type |
| **Bitbucket** | `bb` | Bitbucket Pipelines | Renovate | Tool-specific per type |

## Branching Strategy

Configure one of three branching strategies per project:

- **gitflow** (default) — `main` + `develop` + feature/release/hotfix branches
- **trunk-based** — single `main` with short-lived feature branches
- **github-flow** — `main` + feature branches with PR-based workflow

Branch protection (required reviews, CI checks, no force push) is configurable.

## Configuration

Projects are configured via `scaffold.yml`:

```yaml
name: my-project
type: cli-python
platforms: [windows, linux, macos]
language: python
vcs_platform: github
branching_strategy: gitflow
require_pr_reviews: true
required_approvals: 1
require_ci_pass: true
integrations: [agents-md, warp, claude-code]
```

| `specsmith export` | Generate compliance report (REQ coverage, audit summary, tool status) |

## Documentation

Full documentation: [specsmith.readthedocs.io](https://specsmith.readthedocs.io)

## Specification

See [`docs/AGENT-WORKFLOW-SPEC.md`](docs/AGENT-WORKFLOW-SPEC.md) for the complete workflow specification.

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md) for setup and guidelines.

## Security

See [SECURITY.md](SECURITY.md) for vulnerability reporting.

## License

MIT — Copyright (c) 2026 BitConcepts, LLC. See [LICENSE](LICENSE).
