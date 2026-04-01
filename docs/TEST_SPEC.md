# Test Specification — specsmith

## Unit Tests

### Config

- **TEST-CFG-001**: ProjectConfig creates with minimal input (name + type)
  Covers: REQ-CFG-001
- **TEST-CFG-002**: ProjectConfig rejects invalid project type
  Covers: REQ-CFG-001
- **TEST-CFG-003**: package_name converts hyphens to underscores
  Covers: REQ-CFG-003
- **TEST-CFG-004**: All 8 project types have valid type_label and section_ref
  Covers: REQ-CFG-002

### Auditor

- **TEST-AUD-001**: Audit passes for a fully scaffolded project
  Covers: REQ-AUD-001
- **TEST-AUD-002**: Audit detects missing AGENTS.md
  Covers: REQ-AUD-001
- **TEST-AUD-003**: Audit detects oversized ledger
  Covers: REQ-AUD-004
- **TEST-AUD-004**: Audit checks governance bloat thresholds
  Covers: REQ-AUD-006

### Validator

- **TEST-VAL-001**: Validate passes for valid scaffold.yml
  Covers: REQ-VAL-001
- **TEST-VAL-002**: Validate detects broken AGENTS.md references
  Covers: REQ-VAL-002
- **TEST-VAL-003**: Validate detects duplicate requirement IDs
  Covers: REQ-VAL-003

### Compressor

- **TEST-CMP-001**: Compress skips when ledger is below threshold
  Covers: REQ-CMP-003
- **TEST-CMP-002**: Compress archives old entries and creates ledger-archive.md
  Covers: REQ-CMP-001, REQ-CMP-002
- **TEST-CMP-003**: Compress preserves recent entries
  Covers: REQ-CMP-001

### Upgrader

- **TEST-UPG-001**: Upgrade skips when already at target version
  Covers: REQ-UPG-001
- **TEST-UPG-002**: Upgrade re-renders governance files and updates scaffold.yml
  Covers: REQ-UPG-002, REQ-UPG-003

## Integration Tests

### Scaffolder

- **TEST-SCF-001**: CLI Python scaffold creates expected file set
  Covers: REQ-SCF-001, REQ-SCF-002
- **TEST-SCF-002**: FPGA scaffold omits pyproject.toml
  Covers: REQ-SCF-002
- **TEST-SCF-003**: Library scaffold includes pyproject.toml without cli.py
  Covers: REQ-SCF-002
- **TEST-SCF-004**: .gitkeep files created in empty directories
  Covers: REQ-SCF-003
- **TEST-SCF-005**: scaffold.yml written after init
  Covers: REQ-SCF-005
- **TEST-SCF-006**: Warp integration files created when configured
  Covers: REQ-SCF-006, REQ-INT-001

### CLI

- **TEST-CLI-001**: `specsmith --version` outputs version string
  Covers: REQ-CLI-007
- **TEST-CLI-002**: `specsmith init --config` creates project from YAML
  Covers: REQ-CLI-001
- **TEST-CLI-003**: `specsmith audit` exits 0 on healthy project
  Covers: REQ-CLI-002
- **TEST-CLI-004**: `specsmith validate` exits 0 on valid project
  Covers: REQ-CLI-003

### Integrations

- **TEST-INT-001**: Warp adapter generates SKILL.md with project metadata
  Covers: REQ-INT-001
- **TEST-INT-002**: Claude Code adapter generates CLAUDE.md
  Covers: REQ-INT-002
- **TEST-INT-003**: Cursor adapter generates governance.mdc
  Covers: REQ-INT-003
- **TEST-INT-004**: Copilot adapter generates copilot-instructions.md
  Covers: REQ-INT-004
- **TEST-INT-005**: Adapter registry lists all available adapters
  Covers: REQ-INT-005
