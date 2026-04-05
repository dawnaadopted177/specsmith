# Architecture — specsmith

## Overview

specsmith is a CLI tool (Python) targeting Windows, Linux, macOS. It generates governed project scaffolds with AI agent governance files, CI/CD pipelines, and verification tool configurations.

## Components

### CLI (`cli.py`)
Entry point. Click-based command group with 50+ commands including all original scaffold/governance commands plus: `stress-test`, `epistemic-audit`, `belief-graph`, `trace seal/verify/log`, `integrate`, `run`, `agent providers/tools/skills`.

### Config (`config.py`)
Pydantic model validating scaffold.yml. 33 project types enum (added: `epistemic-pipeline`, `knowledge-engineering`, `aee-research`), platform enum, type labels, section refs. New fields: `enable_epistemic`, `epistemic_threshold`, `enable_trace_vault`.

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

## Epistemic Layer (`src/epistemic/` + `src/specsmith/agent/`)

### `epistemic` package (standalone library, zero deps)
Co-installed with specsmith. Canonical location for all AEE machinery.
- **`belief.py`** — `BeliefArtifact` dataclass (propositions, boundary, confidence, status, failure_modes, evidence)
- **`stress_tester.py`** — `StressTester` applies 8 adversarial challenge categories; emits `FailureMode` records; detects Logic Knots
- **`failure_graph.py`** — `FailureModeGraph` directed graph; `equilibrium_check()` and `logic_knot_detect()`; Mermaid rendering
- **`recovery.py`** — `RecoveryOperator` emits bounded `RecoveryProposal` objects; never auto-applies; ranked by severity
- **`certainty.py`** — `CertaintyEngine` scores C = base × coverage × freshness; weakest-link propagation through inferential links
- **`session.py`** — `AEESession` facade: `add_belief`, `accept`, `add_evidence`, `run`, `save`, `load`, `seal`
- **`trace.py`** — `TraceVault` SHA-256 append-only chain; STP-inspired decision sealing

### `specsmith.epistemic` (compatibility shim)
Re-exports all symbols from `epistemic`. Allows `from specsmith.epistemic import BeliefArtifact` for backward compat.

### Crypto Audit Chain (`ledger.py`)
`CryptoAuditChain` stores SHA-256 hashes per ledger entry in `.specsmith/ledger-chain.txt`. Each hash chains to the previous, making the ledger tamper-evident.

### Agentic Client (`src/specsmith/agent/`)
- **`core.py`** — `Message`, `Tool`, `CompletionResponse`, `ModelTier`, `BaseProvider` protocol
- **`providers/`** — Anthropic, OpenAI (+ Ollama via compat), Gemini, Ollama (stdlib-only). All optional extras.
- **`tools.py`** — 20 specsmith commands as native LLM-callable tools with epistemic contracts
- **`hooks.py`** — `HookRegistry` with Pre/PostTool, SessionStart, SessionEnd. Built-in H13 check.
- **`skills.py`** — SKILL.md loader with domain priority order
- **`runner.py`** — REPL loop, tool execution, streaming, session state, model routing
- **`profiles/`** — Built-in skill profiles: planner, verifier, epistemic-auditor

## Verification Tools

**Lint:** ruff check
**Typecheck:** mypy
**Test:** pytest
**Security:** pip-audit
**Format:** ruff format
