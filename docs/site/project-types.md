# Project Types

specsmith supports 30 project types across six categories. Each type determines:

- **Directory structure** — what directories and .gitkeep files are created
- **Verification tools** — what lint/test/security/build tools are configured in CI
- **Governance rules** — what type-specific rules appear in AGENTS.md
- **Template starters** — what domain-specific requirements and tests are pre-populated
- **CI config** — what GitHub Actions setup steps, Docker images, and cache keys are used
- **.gitignore** — what type-specific ignore patterns are included

## Software — Python

| Type | Key | Lint | Test | Security |
|------|-----|------|------|----------|
| Python backend + web frontend | `backend-frontend` | ruff, eslint | pytest, vitest | pip-audit, npm audit |
| Python backend + frontend + tray | `backend-frontend-tray` | ruff, eslint | pytest, vitest | pip-audit, npm audit |
| CLI tool (Python) | `cli-python` | ruff | pytest | pip-audit |
| Library / SDK (Python) | `library-python` | ruff | pytest | pip-audit |

**Directory structure (cli-python):** `src/{package}/`, `src/{package}/commands/`, `src/{package}/utils/`, `tests/`

**Governance rules:** CLI must have `--help` for all commands. Exit codes must be documented and tested. Cross-platform rules apply.

## Software — Systems Languages

| Type | Key | Lint | Test | Security |
|------|-----|------|------|----------|
| CLI tool (Rust) | `cli-rust` | cargo clippy | cargo test | cargo audit |
| Library / crate (Rust) | `library-rust` | cargo clippy | cargo test | cargo audit |
| CLI tool (Go) | `cli-go` | golangci-lint | go test | govulncheck |
| CLI tool (C/C++) | `cli-c` | clang-tidy | ctest | flawfinder |
| Library (C/C++) | `library-c` | clang-tidy | ctest | flawfinder |
| .NET / C# application | `dotnet-app` | dotnet format | dotnet test | dotnet audit |

**Rust governance rules:** `cargo clippy` must pass with no warnings. All public APIs must have doc comments. `cargo audit` must pass in CI.

**C/C++ governance rules:** MISRA-C compliance rules apply where annotated. `clang-tidy` and `cppcheck` must pass. Memory safety must be verified.

## Software — Web / Mobile / Infra

| Type | Key | Lint | Test | Build |
|------|-----|------|------|-------|
| Web frontend (SPA) | `web-frontend` | eslint | vitest | — |
| Fullstack JS/TS | `fullstack-js` | eslint | vitest, jest | — |
| Mobile app | `mobile-app` | flutter analyze | flutter test | flutter build |
| Browser extension | `browser-extension` | eslint, web-ext lint | vitest | web-ext build |
| Monorepo | `monorepo` | eslint, ruff | nx/turbo test | nx/turbo build |
| Microservices | `microservices` | ruff, eslint | pytest, jest | docker compose |
| DevOps / IaC | `devops-iac` | tflint, ansible-lint | terratest | — |
| Data / ML pipeline | `data-ml` | ruff | pytest | — |

**DevOps governance rules:** Security scanning (tfsec/checkov) is mandatory. State files must never be committed. Infrastructure changes require proposals.

## Hardware / Embedded

| Type | Key | Lint | Test | Build |
|------|-----|------|------|-------|
| Embedded / hardware | `embedded-hardware` | clang-tidy | ctest, unity | cmake |
| FPGA / RTL | `fpga-rtl` | vsg, verilator | ghdl, cocotb | vivado, quartus |
| Yocto / embedded Linux BSP | `yocto-bsp` | oelint-adv | bitbake | kas build |
| PCB / hardware design | `pcb-hardware` | — | DRC, ERC | kicad-cli |

**FPGA governance rules:** Tool invocations MUST use batch/non-interactive modes only. Constraint files (.xdc, .sdc) are governance artifacts. Timing closure is a formal milestone.

**PCB governance rules:** BOM files are governance artifacts. Schematic review is a formal gate before layout. ECAD-MCAD sync points must be documented.

## Document / Knowledge

| Type | Key | Lint | Test | Build |
|------|-----|------|------|-------|
| Technical specification | `spec-document` | vale, markdownlint, cspell | markdown-link-check | pandoc, mkdocs |
| User manual | `user-manual` | vale, markdownlint, cspell | markdown-link-check | sphinx, mkdocs |
| Research paper | `research-paper` | vale, cspell, chktex | — | pdflatex, bibtex |
| API specification | `api-specification` | spectral, buf lint | schemathesis, dredd | openapi-generator |
| Requirements management | `requirements-mgmt` | vale, markdownlint | req-trace | — |

**Research paper governance rules:** Citation integrity must be maintained — all `\cite{}` must resolve. Data and figures must be reproducible. LaTeX must compile clean.

**API specification governance rules:** API specs are governance artifacts. Breaking changes require proposals and version bumps. Generated code must not be manually edited.

**Template starters for spec-document/user-manual:** Pre-populated with REQ-DOC-001 (precise language) and REQ-REF-001 (cross-reference validation).

## Business / Legal

| Type | Key | Lint | Build | Compliance |
|------|-----|------|-------|------------|
| Business plan | `business-plan` | vale, cspell | pandoc | — |
| Patent application | `patent-application` | vale, cspell | pandoc | claim-ref-check |
| Legal / compliance | `legal-compliance` | vale, cspell | pandoc | regulation-ref-check |

**Patent governance rules:** Claims are governance artifacts — ALL changes require proposals. Independent claims must be self-contained. Prior art references must include publication dates. Figures must be numbered and referenced. Claim dependency chains must be validated.

**Template starters for patent-application:** Pre-populated with REQ-CLM-001 (self-contained claims), REQ-SPEC-001 (enablement), REQ-FIG-001 (figure references), and corresponding test stubs.

**Legal governance rules:** All document changes must be tracked with version history. Regulatory references must include jurisdiction and effective date. Approval workflows are mandatory before publication.

**Directory structure (patent-application):** `claims/`, `specification/`, `figures/`, `prior-art/`, `correspondence/`

**Directory structure (legal-compliance):** `contracts/`, `policies/`, `templates/`, `evidence/`, `audit-trail/`
