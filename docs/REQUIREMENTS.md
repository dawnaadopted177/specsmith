# Requirements — specsmith

## CLI

- **REQ-CLI-001**: `specsmith init` scaffolds a governed project from interactive prompts or YAML config
- **REQ-CLI-002**: `specsmith audit` runs health and drift checks against a governed project
- **REQ-CLI-003**: `specsmith validate` checks governance file consistency (req ↔ test ↔ arch)
- **REQ-CLI-004**: `specsmith compress` archives old ledger entries when LEDGER.md exceeds threshold
- **REQ-CLI-005**: `specsmith upgrade` regenerates governance files for a newer spec version
- **REQ-CLI-006**: All commands accept `--project-dir` to target a specific project root
- **REQ-CLI-007**: `specsmith --version` displays the current version

## Scaffolding

- **REQ-SCF-001**: Scaffolder generates all governance files (AGENTS.md, LEDGER.md, modular docs)
- **REQ-SCF-002**: Scaffolder generates project-type-specific files (pyproject.toml for Python, etc.)
- **REQ-SCF-003**: Scaffolder creates .gitkeep files in expected empty directories
- **REQ-SCF-004**: Scaffolder optionally runs `git init` in the target directory
- **REQ-SCF-005**: Scaffolder saves scaffold.yml config for re-runs and upgrades
- **REQ-SCF-006**: Scaffolder generates agent integration files based on config.integrations list

## Configuration

- **REQ-CFG-001**: ProjectConfig validates scaffold.yml input with pydantic
- **REQ-CFG-002**: ProjectConfig supports 8 project types (backend-frontend, cli-python, fpga-rtl, etc.)
- **REQ-CFG-003**: ProjectConfig derives package_name from project name (hyphen → underscore)

## Audit

- **REQ-AUD-001**: Audit checks for required governance files (AGENTS.md, LEDGER.md)
- **REQ-AUD-002**: Audit checks modular governance files when AGENTS.md exceeds 200 lines
- **REQ-AUD-003**: Audit checks REQ ↔ TEST coverage consistency
- **REQ-AUD-004**: Audit checks ledger size against threshold (default 500 lines)
- **REQ-AUD-005**: Audit checks open TODO count in ledger
- **REQ-AUD-006**: Audit checks governance file sizes against bloat thresholds

## Validation

- **REQ-VAL-001**: Validate checks scaffold.yml structure and required fields
- **REQ-VAL-002**: Validate checks AGENTS.md local file references resolve
- **REQ-VAL-003**: Validate checks requirement ID uniqueness
- **REQ-VAL-004**: Validate checks architecture.md references requirements

## Compression

- **REQ-CMP-001**: Compress archives entries older than keep_recent threshold
- **REQ-CMP-002**: Compress writes archived entries to docs/ledger-archive.md
- **REQ-CMP-003**: Compress only runs when ledger exceeds line threshold

## Upgrade

- **REQ-UPG-001**: Upgrade reads scaffold.yml for current config
- **REQ-UPG-002**: Upgrade re-renders governance templates with new spec version
- **REQ-UPG-003**: Upgrade updates scaffold.yml with new spec version

## Integrations

- **REQ-INT-001**: Warp adapter generates .warp/skills/SKILL.md
- **REQ-INT-002**: Claude Code adapter generates CLAUDE.md
- **REQ-INT-003**: Cursor adapter generates .cursor/rules/governance.mdc
- **REQ-INT-004**: Copilot adapter generates .github/copilot-instructions.md
- **REQ-INT-005**: Adapter registry allows listing and instantiating adapters by name

## Cross-Platform

- **REQ-XPL-001**: All CLI commands work on Windows, Linux, and macOS
- **REQ-XPL-002**: Generated scripts include both .ps1 and .sh variants
