# Architecture — specsmith

## Overview

specsmith is a CLI tool (Python) targeting Windows, Linux, macOS. It generates governed project scaffolds with AI agent governance files, CI/CD pipelines, and verification tool configurations.

## Components

### CLI (`cli.py`)
Entry point. Click-based command group with 10 commands: init, import, audit, validate, compress, upgrade, status, diff, export.

### Config (`config.py`)
Pydantic model validating scaffold.yml. 30 project types enum, platform enum, type labels, section refs.

### Scaffolder (`scaffolder.py`)
Jinja2 template renderer. Generates governance files, project structure, scripts. Delegates to VCS platforms and agent integrations.

### Tool Registry (`tools.py`)
Data structure mapping project types to verification tools (lint, typecheck, test, security, build, format, compliance). CI metadata per language.

### Importer (`importer.py`)
Detection engine: walks directories, detects language/build/test/CI/governance. Infers ProjectType. Generates overlay files.

### Exporter (`exporter.py`)
Generates compliance reports: REQ coverage matrix, audit summary, tool status, governance inventory.

### Auditor (`auditor.py`)
Health checks: file existence, REQ↔TEST coverage, ledger health, governance size, tool configuration.

### VCS Platforms (`vcs/`)
GitHub, GitLab, Bitbucket integrations. Tool-aware CI config generation, dependency management, status checks.

### Agent Integrations (`integrations/`)
7 adapters: Warp, Claude Code, Cursor, Copilot, Gemini, Windsurf, Aider.

## Verification Tools

**Lint:** ruff check
**Typecheck:** mypy
**Test:** pytest
**Security:** pip-audit
**Format:** ruff format
